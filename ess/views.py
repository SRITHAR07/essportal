from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from .models import MasEmpOfficial,Users,EntLoanappl,EntLoanmas,EntLoanschedule, MasLoan,MasExpenses,MasEmpSalsettings,MasEmpLeave,EntEmpLeaveappl, EntEmpExpenses,MasDept,MasDesignation,MasSubdept,EntAddress,MasEmpDocuments, MasDocuments,MasPlantleave,AttnDaily,MasChklist,GennhrAudit,MasSmonth,EntMsalary
from django.http import JsonResponse,HttpResponse,FileResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.views.decorators.cache import cache_control
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.shortcuts import render
from django.db.models import Sum, Count,Q
from datetime import datetime,timedelta
from django.utils import timezone
from django.views.decorators.cache import cache_control
from django.utils.cache import add_never_cache_headers
from django.core.paginator import Paginator
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_control
from django.core.exceptions import ValidationError
import logging
import uuid
from datetime import datetime as dt
from django.contrib.messages import get_messages
from django.conf import settings
from django.shortcuts import render, get_object_or_404
import subprocess
import pdfkit 
import logging
from django.views.decorators.http import require_POST


def log_audit(request, empid, table_name, action, description):
    """Function to log audit actions in GennhrAudit table."""
    ip_address = get_client_ip(request)  # Get user IP

    GennhrAudit.objects.create(
        datetime=timezone.now(),  
        ip=ip_address,
        user=empid,
        table=table_name,
        action=action,
        description=description
    )
print(timezone.now()) 
import socket

def get_client_ip(request):
    """Retrieve the client's IP address, prioritizing real IPs over local addresses."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    # If running locally, replace 127.0.0.1 with the actual machine's IP
    if ip == "127.0.0.1" or ip == "::1":
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

    return ip

def login_required_view(view_func):
    def wrapper(request, *args, **kwargs):
        if "empid" not in request.session:  # ✅ Now checking empid instead of user_id
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper


@never_cache
def login_view(request):
    if "empid" in request.session:  # 🔥 If already logged in, go to home
        return redirect("ehome")

    plantcodes = Users.objects.values_list("plantcode", flat=True).distinct()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        plantcode = request.POST.get("plantcode")

        try:
            user = Users.objects.get(username=username, plantcode=plantcode)
            user.lastactivitydate = timezone.now()

            if user.islockedout:
                messages.error(request, "Your account is locked! Contact HR.")
                log_audit(request, user.id, "Users", "Login Failed", "Attempt to login with locked account")
                return redirect("login")  # 🔹 Redirect to prevent re-posting on refresh

            if check_password(password, user.password):
                user.failedpasswordattemptcount = 0
                user.islockedout = 0
                user.lastlogindate = timezone.now()
                user.save()

                request.session["empid"] = user.empid
                request.session["username"] = user.username
                request.session["fullname"] = user.fullname  
                request.session["plantcode"] = user.plantcode  
                request.session.set_expiry(900)

                # 🔹 Clear messages before redirect
                storage = messages.get_messages(request)
                storage.used = True  

                log_audit(request, user.id, "Users", "Login Successful", "User logged in successfully")
                return redirect("ehome")

            else:
                user.failedpasswordattemptcount = (user.failedpasswordattemptcount or 0) + 1

                if user.failedpasswordattemptcount >= 5:
                    user.islockedout = 1
                    user.lastlockedoutdate = timezone.now()
                    messages.error(request, "Too many failed attempts! Account locked.")
                    log_audit(request, user.id, "Users", "Account Locked", "User locked out due to failed logins")
                else:
                    messages.error(request, f"Invalid Password. {5 - user.failedpasswordattemptcount} attempts left.")
                    log_audit(request, user.id, "Users", "Login Failed", "Incorrect password attempt")

                user.save()

                return redirect("login")  # 🔹 Redirect after failure to prevent resubmission on refresh

        except Users.DoesNotExist:
            messages.error(request, "Invalid Plant and Username.")
            log_audit(request, None, "Users", "Login Failed", f"Attempt to login with invalid user {username}")
            return redirect("login")  # 🔹 Redirect to prevent form resubmission

    response = render(request, "esslogin.html", {"plantcodes": plantcodes})
    add_never_cache_headers(response)  # 🔥 Prevent browser from caching login page
    return response

@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
@login_required_view
def logout_view(request):
    empid = request.session.get("empid")  # Get the logged-in user's empid

    if empid:
        try:
            user = Users.objects.get(empid=empid)  # Fetch the user object
            log_audit(request, user.id, "Users", "Logout", "User logged out")  # ✅ Store user ID
        except Users.DoesNotExist:
            log_audit(request, None, "Users", "Logout", "Logout attempted for non-existent user")

    logout(request)  # Perform logout
    return redirect("login")

@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
@login_required_view
def ehome(request):
    
    empid = request.session.get("empid")
    desig_name = "N/A"  # Default designation
    profile_photo = "/static/default_profile.jpg"
    attendance_summary = {}

    selected_month = request.GET.get("month", str(datetime.today().month))
    selected_year = request.GET.get("year", str(datetime.today().year))

    if empid:
        try:
            employee = MasEmpOfficial.objects.get(id=empid)
             # Construct the correct profile photo URL
            if employee.empphoto:
                profile_photo = f"{settings.PROFILE_PHOTOS_URL}{employee.empphoto}"
            else:
                profile_photo = "/static/user.webp"
            # Fetch attendance records
            attendance_records = AttnDaily.objects.filter(
                empid=empid,
                attndt__year=int(selected_year),
                attndt__month=int(selected_month)
            )
            calender_data = AttnDaily.objects.filter(
                empid=empid,
            )
            calendersheet = sorted([
                {
                    "date": attn.attndt.strftime("%d/%b/%Y"),  # Format: 12/Mar/2025
                    "checkin": attn.checkin.strftime("%I:%M %p") if attn.checkin else "-",  # Format: 08:30 AM
                    "checkout": attn.checkout.strftime("%I:%M %p") if attn.checkout else "-",  # Format: 05:30 PM
                    "perhrs": attn.perhrs,
                    "regot": attn.regot,
                    "la": attn.la,
                    "mustattn": attn.mustattn,
                }
                for attn in calender_data
            ], key=lambda x: datetime.strptime(x["date"], "%d/%b/%Y"), reverse=True)  # Sort by date descending

            timesheet_data = sorted([
                {
                    "date": attn.attndt.strftime("%d/%b/%Y"),  # Format: 12/Mar/2025
                    "checkin": attn.checkin.strftime("%I:%M %p") if attn.checkin else "-",  # Format: 08:30 AM
                    "checkout": attn.checkout.strftime("%I:%M %p") if attn.checkout else "-",  # Format: 05:30 PM
                    "perhrs": attn.perhrs,
                    "regot": attn.regot,
                    "la": attn.la,
                    "mustattn": attn.mustattn,
                }
                for attn in attendance_records
            ], key=lambda x: datetime.strptime(x["date"], "%d/%b/%Y"), reverse=True)  # Sort by date descending

            # Aggregate total present days
            total_present = attendance_records.aggregate(total_present=Sum('regshift'))["total_present"] or 0

            # Get Present Days with additional details
            present_dates = attendance_records.values_list(
                'attndt', 'regshift', 'checkin', 'checkout', 'perhrs', 'regot', 'mustattn'
            )

            # Get WO, NH, FH Dates with additional details
            wo_dates = attendance_records.filter(Q(anlcode="WO") | Q(fnlcode="WO")).values_list(
                'attndt', 'anlcode', 'fnlcode', 'checkin', 'checkout', 'perhrs', 'regot', 'mustattn'
            )
            nh_dates = attendance_records.filter(Q(anlcode="NH") | Q(fnlcode="NH")).values_list(
                'attndt', 'anlcode', 'fnlcode', 'checkin', 'checkout', 'perhrs', 'regot', 'mustattn'
            )
            fh_dates = attendance_records.filter(Q(anlcode="FH") | Q(fnlcode="FH")).values_list(
                'attndt', 'anlcode', 'fnlcode', 'checkin', 'checkout', 'perhrs', 'regot', 'mustattn'
            )

            # Count WO, NH, FH
            wo_count = sum(0.5 for _, anl, fnl, *_ in wo_dates if anl == "WO") + sum(0.5 for _, anl, fnl, *_ in wo_dates if fnl == "WO")
            nh_count = sum(0.5 for _, anl, fnl, *_ in nh_dates if anl == "NH") + sum(0.5 for _, anl, fnl, *_ in nh_dates if fnl == "NH")
            fh_count = sum(0.5 for _, anl, fnl, *_ in fh_dates if anl == "FH") + sum(0.5 for _, anl, fnl, *_ in fh_dates if fnl == "FH")

            # Calculate Absences Only When anlcode or fnlcode is 'AB'
            absent_dates = [
                (date.strftime("%d/%b/%Y"), float(regshift), round(1.00 - float(regshift), 3),checkin.strftime("%I:%M %p") if checkin else "-",
                            checkout.strftime("%I:%M %p") if checkout else "-", perhrs, regot, mustattn)  
                for date, regshift, checkin, checkout, perhrs, regot, mustattn, anl, fnl in attendance_records.values_list(
                    "attndt", "regshift", "checkin", "checkout", "perhrs", "regot", "mustattn", "anlcode", "fnlcode"
                ) if float(regshift) < 1.00 and (anl == "AB" or fnl == "AB")
            ]
            total_absent = sum(absent for _, _, absent, *_ in absent_dates)
            total_holidays = nh_count + fh_count  # Total holidays

            # Fetch CL/EL records (dates & codes) with additional details
            cl_el_records = list(attendance_records.filter(
                Q(anlcode__in=["CL", "EL"]) | Q(fnlcode__in=["CL", "EL"])
            ).values_list("attndt", "anlcode", "fnlcode", "checkin", "checkout", "perhrs", "regot", "mustattn"))

            # Calculate CL and EL count using raw SQL query
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 
                        SUM(CASE WHEN A.ANLcode = M.Lcode AND M.isPH = 1 THEN 0.5 ELSE 0 END) +
                        SUM(CASE WHEN A.FNLcode = M.Lcode AND M.isPH = 1 THEN 0.5 ELSE 0 END) AS cl_el_count
                    FROM Attn_Daily A
                    JOIN Mas_Plantleave M 
                        ON A.Plantcode = M.Plantcode 
                        AND A.EmpID = %s
                        AND YEAR(A.Attndt) = %s
                        AND MONTH(A.Attndt) = %s
                        AND M.Lcode IN ('CL', 'EL')
                    """,
                    [empid, selected_year, selected_month]
                )
                cl_el_count = cursor.fetchone()[0] or 0

            # Store Payable Leave Details in attendance_summary
            attendance_summary = {
                "total_present": total_present,
                "selected_month": selected_month,
                "selected_year": selected_year,
                "present_dates": [
                    (
                        date.strftime("%d/%b/%Y"),
                        regshift,
                        checkin.strftime("%I:%M %p") if checkin else "-",  # Show time only
                        checkout.strftime("%I:%M %p") if checkout else "-",  # Show time only
                        perhrs, regot, mustattn
                    )
                    for date, regshift, checkin, checkout, perhrs, regot, mustattn in present_dates
                ],
                "wo_dates": [
                                (
                                    date.strftime("%d/%b/%Y"),
                                    anl, fnl,
                                    checkin.strftime("%I:%M %p") if checkin else "-",
                                    checkout.strftime("%I:%M %p") if checkout else "-",
                                    perhrs, regot, mustattn
                                )
                                for date, anl, fnl, checkin, checkout, perhrs, regot, mustattn in wo_dates
                            ],
                "wo_count": wo_count,
                "nh_dates": [
                        (
                            date.strftime("%d/%b/%Y"),
                            anl, fnl,
                            checkin.strftime("%I:%M %p") if checkin else "-",
                            checkout.strftime("%I:%M %p") if checkout else "-",
                            perhrs, regot, mustattn
                        )
                        for date, anl, fnl, checkin, checkout, perhrs, regot, mustattn in nh_dates
                    ],                
                "nh_count": nh_count,
                "fh_dates": [
                        (
                            date.strftime("%d/%b/%Y"),
                            anl, fnl,
                            checkin.strftime("%I:%M %p") if checkin else "-",
                            checkout.strftime("%I:%M %p") if checkout else "-",
                            perhrs, regot, mustattn
                        )
                        for date, anl, fnl, checkin, checkout, perhrs, regot, mustattn in fh_dates
                    ],
                 "fh_count": fh_count,
                "total_holidays": total_holidays,
                "absent_dates": absent_dates,
                "total_absent": total_absent,
                "cl_el_records": [
                        (
                            date.date().strftime("%d/%b/%Y"),
                            anl, fnl,
                            checkin.strftime("%I:%M %p") if checkin else "-",
                            checkout.strftime("%I:%M %p") if checkout else "-",
                            perhrs, regot, mustattn
                        )
                        for date, anl, fnl, checkin, checkout, perhrs, regot, mustattn in cl_el_records
                    ],
                 "payable_leaves": cl_el_count,
            }

        except MasEmpOfficial.DoesNotExist:
            profile_photo = "/static/default_profile.jpg"

    months = [(str(i), str(i)) for i in range(1, 13)]
    current_year = datetime.now().year
    years = [(str(y), str(y)) for y in range(current_year - 5, current_year + 6)]

    return render(request, "ehome.html", {
        "fullname": request.session.get("fullname"),
        "username": request.session.get("username"),
        "profile_photo": profile_photo,
        "desig_name": desig_name,
        "calendersheet":calendersheet,
        "timesheet_data": timesheet_data,
        "attendance_summary": attendance_summary,
        "months": months,
        "years": years,
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
@login_required_view
def profile(request):
    """ View to fetch employee profile with logging. """
    empid = request.session.get("empid")  # Get logged-in user's EmpID from session
    print(f"Session EmpID: {empid}")  # Debugging step

    profile_photo = "/static/default_profile.jpg"
    address_data = {
        "communication": None,
        "permanent": None
    }

    if empid:
        try:
            # Fetch employee details
            employee = MasEmpOfficial.objects.get(id=empid)
            if employee.empphoto:
                profile_photo = f"{settings.PROFILE_PHOTOS_URL}{employee.empphoto}"
            else:
                profile_photo = "/static/user.webp"

            # Fetch related details (Department, Sub-Department, Designation)
            dept_name = MasDept.objects.get(id=employee.deptid).deptname if employee.deptid else "N/A"
            subdept_name = MasSubdept.objects.get(id=employee.subdeptid).subdeptname if employee.subdeptid else "N/A"
            desig_name = MasDesignation.objects.get(id=employee.desigid).designame if employee.desigid else "N/A"
            uanno =MasEmpSalsettings.objects.get(empid=employee.id).uanno if employee.id else "N/A"
            pfno = MasEmpSalsettings.objects.get(empid=employee.id).pfno if employee.id else "N/A"
            supervisor_name = "N/A"
            if employee.reportsto:
                try:
                    supervisor = MasEmpOfficial.objects.get(id=employee.reportsto)
                    supervisor_name = supervisor.empname  # Fetch empname of supervisor
                except MasEmpOfficial.DoesNotExist:
                    supervisor_name = "N/A"

            # Fetch Addresses (Communication & Permanent)
            addresses = EntAddress.objects.filter(empid=empid)
            
            for addr in addresses:
                addr_data = {
                    "platno": addr.platno or "",
                    "streetname": addr.streetname or "",
                    "townname": addr.townname or "",
                    "locid": addr.locid or "",
                    "locname": addr.locname or "",
                    "talukname": addr.talukname or "",
                    "districtname": addr.districtname or "",
                    "statename": addr.statename or "",
                    "countryname": addr.countryname or "",
                    "nationality": addr.nationality or "",
                    "pincode": addr.pincode or ""
                }

                if addr.atype == "C":  # Communication Address
                    address_data["communication"] = addr_data
                elif addr.atype == "P":  # Permanent Address
                    address_data["permanent"] = addr_data

            # Ensure at least one address is returned
            if not address_data["communication"] and not address_data["permanent"]:
                address_data = None

            # Prepare profile data
            profile_data = {
                "fullname": employee.empname,
                "profile_photo": profile_photo,
                "biorefno": employee.biorefno,
                "fhflag": employee.fhflag,
                "aadhaarno": employee.aadhaarno,
                "omobile": employee.omobile,
                "fhname": employee.fhname,
                "plantcode": employee.plantcode,
                "dob": employee.dob.strftime("%d-%m-%Y") if employee.dob else "N/A",
                "doj": employee.doj.strftime("%d-%m-%Y") if employee.doj else "N/A",
                "gender": employee.gender,
                "dept_name": dept_name,
                "subdept_name": subdept_name,
                "uanno": uanno,
                "pfno": pfno,
                "desig_name": desig_name,
                "supervisor": supervisor_name,
                "addresses": address_data
            }

            try:
                # Fetch the Users object where empid matches
                user = Users.objects.get(empid=empid)  

                # Ensure we're getting the correct primary key (id)
                user_id = user.pk  # OR user.id (pk is safer if id is overridden)
                
                # ✅ Log Profile View with correct User ID
                log_audit(
                    request, user_id, "MasEmpOfficial", "View",  
                    f"Employee profile viewed for '{employee.empname}' (ID: {empid})."
                )

            except Users.DoesNotExist:
                user_id = None  # Ensure it's handled properly

        except MasEmpOfficial.DoesNotExist:
            print("No employee found with this EmpID")  # Debugging step
            profile_data = None
        except MasDept.DoesNotExist:
            dept_name = "N/A"
        except MasSubdept.DoesNotExist:
            subdept_name = "N/A"
        except MasDesignation.DoesNotExist:
            desig_name = "N/A"

    return render(request, "profile.html", {
        "username": request.session.get("username"),
        "profile_data": profile_data
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
@login_required_view
def documents(request):
    """ View to list documents of the logged-in user and log the activity. """
    empid = request.session.get("empid")  # Get logged-in user's EmpID
    document_data = []

    if empid:
        try:
            # Fetch documents related to the logged-in employee
            emp_documents = MasEmpDocuments.objects.filter(empid=empid)

            for emp_doc in emp_documents:
                try:
                    # Fetch corresponding document details
                    document = MasDocuments.objects.get(id=emp_doc.docid)
                    document_data.append({
                        "id": emp_doc.id,  # Unique ID for edit/delete actions
                        "document_name": document.docname,  # Document name from MasDocuments
                        "docno": emp_doc.docno,
                        "expiry_date": emp_doc.expirydt.strftime("%d-%m-%Y") if emp_doc.expirydt else "N/A",
                        "created_date": emp_doc.createddate.strftime("%d-%m-%Y") if emp_doc.createddate else "N/A",
                        "docname": emp_doc.docname,  # File name
                    })
                except MasDocuments.DoesNotExist:
                    print(f"Document with ID {emp_doc.docid} not found")
                    continue

            try:
                user = Users.objects.get(empid=empid)  
                user_id = user.pk  # OR user.id to ensure the correct ID is used
            except Users.DoesNotExist:
                user_id = None  # Handle case where user is not found

            # Log audit with the correct user ID
            log_audit(
                request, user_id, "MasEmpDocuments", "View",
                f"User viewed document list (Total: {len(document_data)})"
            )
        except Exception as e:
            print(f"Error fetching documents: {e}")
            document_data = None

    return render(request, "documents.html", {
        "username": request.session.get("username"),
        "documents": document_data
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
@login_required_view
def upload_document(request):
    """ View to upload documents and log the activity. """
    empid = request.session.get("empid", "")  # Fetch empid from session
    documents = MasDocuments.objects.filter(isactive=True).values("id", "docname")  # Fetch active documents
    checklist = MasChklist.objects.filter(isactive=True).values("id", "chklistname")

    # Get the logged-in user
    user = request.user  # Django's built-in authentication user

    try:
        user_obj = Users.objects.get(empid=empid)  
        user_id = user_obj.id  # Get user ID from the Users model
    except Users.DoesNotExist:
        user_id = None  # Handle if user is not found

    if request.method == "POST":
        docid = request.POST.get("docid")  # Get document ID
        chkid = request.POST.get("chkid")  # Get checklist ID
        docno = request.POST.get("docno")  # Get Document Number
        expirydt = request.POST.get("expirydt")  # Get Expiry Date
        uploaded_file = request.FILES.get("document_file")  # Get uploaded file

        if uploaded_file:
            fs = FileSystemStorage(location="documents")  # Save in project folder
            filename = fs.save(uploaded_file.name, uploaded_file)  # Save file and get filename

            # Save document with logged-in user's ID in createdby
            MasEmpDocuments.objects.create(
                empid=empid,
                docid=int(docid),  # Store only the ID as an integer
                docname=filename,  # Store the file name in docname field
                docno=docno,  # Save document number
                expirydt=expirydt,  # Save expiry date
                chkid=int(chkid),  # Store only the ID as an integer
                createdby=user_id,  # 🔹 Store the logged-in user's ID instead of empid
                createddate=timezone.now()
            )

            # ✅ Log the user activity in `GennhrAudit`
            log_audit(
                request, user_id, "MasEmpDocuments", "Upload",
                f"User uploaded document: {filename}, DocNo: {docno}, Expiry Date: {expirydt}"
            )

            return redirect("documents")  # Redirect after success

    context = {
        "empid": empid,
        "createddate": timezone.now().strftime("%Y-%m-%dT%H:%M"),
        "documents": documents,
        "checklist": checklist,
    }
    return render(request, "upload_document.html", context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required_view
def edit_document(request, doc_id):
    """ View to edit documents and log the activity. """
    document = get_object_or_404(MasEmpDocuments, id=doc_id)
    documents = MasDocuments.objects.filter(isactive=True).values("id", "docname")
    checklist = MasChklist.objects.filter(isactive=True).values("id", "chklistname")

    if request.method == "POST":
        docid = request.POST.get("docid")
        chkid = request.POST.get("chkid")
        docno = request.POST.get("docno")
        expirydt = request.POST.get("expirydt")  # Get expiry date input
        uploaded_file = request.FILES.get("document_file")  # Get new uploaded file

        # Get logged-in employee ID
        empid = request.session.get("empid", "")

        # Store original values for logging changes
        old_docname = document.docname
        old_docno = document.docno
        old_expirydt = document.expirydt
        try:
            user_obj = Users.objects.get(empid=empid)  
            user_id = user_obj.id  # Get user ID from the Users model
        except Users.DoesNotExist:
            user_id = None 

        # If a new file is uploaded, save it, otherwise retain the existing file
        if uploaded_file:
            fs = FileSystemStorage(location="documents")
            filename = fs.save(uploaded_file.name, uploaded_file)
        else:
            filename = document.docname  # Keep the old file if no new file is uploaded

        # ✅ Fix: Convert empty string to `None` for expiry date
        expirydt = expirydt if expirydt else None  

        # Update the document record
        document.docid = int(docid)
        document.chkid = int(chkid)
        document.docno = docno
        document.expirydt = expirydt  # Save as None if empty
        document.docname = filename  # Update file only if changed
        document.updatedby = user_id  # Store the logged-in user's empid
        document.updateddate = timezone.now()  # Store the current timestamp
        document.save()

        # ✅ Log the edit action in `GennhrAudit`
        changes = []
        if old_docname != filename:
            changes.append(f"Document changed from '{old_docname}' to '{filename}'")
        if old_docno != docno:
            changes.append(f"DocNo changed from '{old_docno}' to '{docno}'")
        if old_expirydt != expirydt:
            changes.append(f"Expiry Date changed from '{old_expirydt}' to '{expirydt}'")
        
        try:
                user = Users.objects.get(empid=empid)  
                user_id = user.pk  # OR user.id to ensure the correct ID is used
        except Users.DoesNotExist:
                user_id = None
        log_audit(
            request, user_id, "MasEmpDocuments", "Edit",
            f"User edited document ID {doc_id}. " + "; ".join(changes)
        )

        return redirect("documents")  # Redirect back to documents list

    context = {
        "document": document,
        "documents": documents,
        "checklist": checklist,
    }
    return render(request, "edit.html", context)

    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required_view
@csrf_exempt
def delete_document(request, doc_id):
    """ View to delete a document with logging. """
    print(f"Attempting to delete document ID: {doc_id}")  # Debugging line

    if request.method == "POST":
        document = get_object_or_404(MasEmpDocuments, id=doc_id)
        print(f"Found document: {document.docname}")  # Debugging line

        # Store document details before deletion for logging
        deleted_docname = document.docname
        deleted_empid = document.empid  # Assuming the document has an empid field

        # Fetch the correct user ID from Users table
        try:
            user = Users.objects.get(empid=deleted_empid)
            user_id = user.pk  # Get the primary key
        except Users.DoesNotExist:
            user_id = None  # Fallback if user not found

        # Delete the associated file from storage
        file_path = os.path.join(settings.MEDIA_ROOT, "documents", document.docname)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")  # Debugging line

        document.delete()

        # ✅ Log the document deletion with correct user ID
        log_audit(
            request, user_id, "MasEmpDocuments", "Delete",
            f"Document '{deleted_docname}' (ID: {doc_id}) was deleted."
        )

        return JsonResponse({"message": "Document deleted successfully."})

    return JsonResponse({"error": "Invalid request."}, status=400)

@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
@login_required_view
def attendance(request):
    """ View to display employee attendance with logging. """
    empid = request.session.get("empid")
    attendance_summary = {}

    selected_month = request.GET.get("month", str(datetime.today().month))
    selected_year = request.GET.get("year", str(datetime.today().year))

    if empid:
        try:
            # Fetch attendance records
            attendance_records = AttnDaily.objects.filter(
                empid=empid,
                attndt__year=int(selected_year),
                attndt__month=int(selected_month)
            )

            # Timesheet Data
            timesheet_data = sorted([
                {
                    "date": attn.attndt.strftime("%d/%b/%Y"),  # Format: 12/Mar/2025
                    "regshift": attn.regshift,
                    "checkin": attn.checkin.strftime("%I:%M %p") if attn.checkin else "-",  # Format: 08:30 AM
                    "checkout": attn.checkout.strftime("%I:%M %p") if attn.checkout else "-",  # Format: 05:30 PM
                    "perhrs": attn.perhrs,
                    "regot": attn.regot,
                    "la": attn.la,
                    "ed": attn.ed,
                    "mustattn": attn.mustattn,
                }
                for attn in attendance_records
            ], key=lambda x: datetime.strptime(x["date"], "%d/%b/%Y"), reverse=True)  # Sort by date descending

            # Calculate Total Present
            total_present = attendance_records.aggregate(total_present=Sum('regshift'))["total_present"] or 0

            # Fetch WO, NH, FH, AB details
            wo_dates = attendance_records.filter(Q(anlcode="WO") | Q(fnlcode="WO")).values_list("anlcode", "fnlcode")
            nh_dates = attendance_records.filter(Q(anlcode="NH") | Q(fnlcode="NH")).values_list("anlcode", "fnlcode")
            fh_dates = attendance_records.filter(Q(anlcode="FH") | Q(fnlcode="FH")).values_list("anlcode", "fnlcode")
            absent_dates = attendance_records.filter(Q(anlcode="AB") | Q(fnlcode="AB")).values_list("attndt", "regshift")

            # Count WO, NH, FH, AB
            wo_count = sum(0.5 for anl, fnl in wo_dates if anl == "WO") + sum(0.5 for anl, fnl in wo_dates if fnl == "WO")
            nh_count = sum(0.5 for anl, fnl in nh_dates if anl == "NH") + sum(0.5 for anl, fnl in nh_dates if fnl == "NH")
            fh_count = sum(0.5 for anl, fnl in fh_dates if anl == "FH") + sum(0.5 for anl, fnl in fh_dates if fnl == "FH")
            total_holidays = nh_count + fh_count  # Total holidays

            # Calculate Absences (When regshift < 1.00 and anlcode/fnlcode is 'AB')
            total_absent = sum(1 - float(regshift) for _, regshift in absent_dates if float(regshift) < 1.00)

            # Calculate Payable Leave (CL + EL)
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 
                        SUM(CASE WHEN A.ANLcode = M.Lcode AND M.isPH = 1 THEN 0.5 ELSE 0 END) +
                        SUM(CASE WHEN A.FNLcode = M.Lcode AND M.isPH = 1 THEN 0.5 ELSE 0 END) AS cl_el_count
                    FROM Attn_Daily A
                    JOIN Mas_Plantleave M 
                        ON A.Plantcode = M.Plantcode 
                        AND A.EmpID = %s
                        AND YEAR(A.Attndt) = %s
                        AND MONTH(A.Attndt) = %s
                        AND M.Lcode IN ('CL', 'EL')
                    """,
                    [empid, selected_year, selected_month]
                )
                cl_el_count = cursor.fetchone()[0] or 0

            # Calculate Overtime (OT)
            total_ot_minutes = attendance_records.aggregate(total_ot=Sum("regot"))["total_ot"] or 0

            # Convert minutes to days (assuming 8-hour workdays)
            total_ot = total_ot_minutes / 60  # Convert to hours, then to days

            # Store Attendance Summary
            attendance_summary = {
                "total_present": total_present,
                "payable_leaves": cl_el_count,
                "loss_of_pay": total_absent,
                "total_holidays": total_holidays,
                "wo_count": wo_count,
                "nh_count": nh_count,
                "fh_count": fh_count,
                "ot_hours": total_ot,  # Total Overtime Hours
                "selected_month": selected_month,
                "selected_year": selected_year,
            }
            try:
                user = Users.objects.get(empid=empid)  
                user_id = user.pk  # OR user.id to ensure the correct ID is used
            except Users.DoesNotExist:
                user_id = None
            # ✅ Log the attendance query
            log_audit(
                request, user_id, "AttnDaily", "View",
                f"User viewed attendance for {selected_month}/{selected_year}. "
                f"Present: {total_present}, Absent: {total_absent}, "
                f"Payable Leave: {cl_el_count}, OT: {total_ot} hours"
            )

        except MasEmpOfficial.DoesNotExist:
            pass

    months = [(str(i), str(i)) for i in range(1, 13)]
    years = [(str(y), str(y)) for y in range(2023, 2027)]

    return render(request, "attendance.html", {
        "attendance_summary": attendance_summary,
        "timesheet_data": timesheet_data,
        "months": months,
        "years": years,
    })

def get_specific_years_months():
    """
    Fetch distinct Smonth values and format them as 'MMM yyyy' (e.g., 'Aug 2023').
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT FORMAT(Smonth, 'MMM yyyy') AS MonthYear
            FROM Mas_smonth
            ORDER BY Smonth DESC
        """)
        months = [row[0] for row in cursor.fetchall()]  # Convert SQL results to list
    return months


from django.utils.dateparse import parse_date
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
@login_required_view  
def payroll(request):
    user_empid = request.session.get("empid")
    print("Logged-in empid:", user_empid)

    # Get filter values
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    page_number = request.GET.get("page")
    sort_by = request.GET.get("sort_by", "smonth")  # Default sorting column
    order = request.GET.get("order", "desc")  # Default order

    print(f"Received from_date: {from_date}, to_date: {to_date}, page: {page_number}, sort_by: {sort_by}, order: {order}")

    # Convert input to date format
    if from_date:
        from_date = parse_date(from_date + "-01")
    if to_date:
        to_date = parse_date(to_date + "-01")

    # Fetch and filter months
    smonths = MasSmonth.objects.filter(smonth__isnull=False)

    if from_date and to_date:
        smonths = smonths.filter(smonth__range=(from_date, to_date))

    # Apply sorting
    if order == "asc":
        smonths = smonths.order_by(sort_by)
    else:
        smonths = smonths.order_by(f"-{sort_by}")

    # Convert queryset to list
    smonth_list = [{"id": month.id, "smonth": month.smonth.date()} for month in smonths]

    # Fetch salary details
    for month in smonth_list:
        ent_salary = EntMsalary.objects.filter(smonthid=month["id"], empid=user_empid).first()
        month["ntot"] = ent_salary.ntot if ent_salary else 0
        month["gramt"] = ent_salary.gramt if ent_salary else 0
        month["dtot"] = ent_salary.dtot if ent_salary else 0
        month["wdays"] = ent_salary.wdays if ent_salary else 0
        month["lopdays"] = ent_salary.lopdays if ent_salary else 0
        month["oth"] = (ent_salary.oth / 60) if ent_salary and ent_salary.oth else 0

    # Pagination (5 records per page)
    paginator = Paginator(smonth_list, 5)
    page_obj = paginator.get_page(page_number)

    return render(request, "payroll.html", {
        "page_obj": page_obj,
        "from_date": request.GET.get("from_date", ""),
        "to_date": request.GET.get("to_date", ""),
        "sort_by": sort_by,
        "order": "desc" if order == "asc" else "asc",  # Toggle order
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
@login_required_view
def testdown(request):
    payslip_pdf = None  # Initialize PDF variable

    if request.method == "POST":
        empID = str(request.session.get("empid"))  # Get logged-in user's EmpID
        sMonth = request.POST.get("month_year")  # Get selected month (YYYY-MM)

        # ✅ Convert "YYYY-MM" to "MMM YYYY"
        sMonth_obj = datetime.strptime(sMonth, "%Y-%m")
        sMonth = sMonth_obj.strftime("%b %Y")  # Example: "2023-11" → "Nov 2023"

        java_program = "java"
        java_class = "EssPayslip"
        java_directory = "D:/gtn/reports/"
        output_folder = os.path.join(java_directory, "output")
        output_file = os.path.join(output_folder, "generated_payslip.html")

        # ✅ Correct Java command with proper classpath
        java_command = [
            java_program,
            "-cp", f"{java_directory};{java_directory}*",
            java_class, empID, sMonth
        ]

        try:
            # Run the Java program to generate the HTML report
            result = subprocess.run(
                java_command,
                check=True,
                capture_output=True,
                text=True
            )

            print("Java Output:", result.stdout)
            print("Java Error:", result.stderr)

            # Check if the generated HTML file exists
            if os.path.exists(output_file):
                # Configure pdfkit to use the wkhtmltopdf binary
                config = pdfkit.configuration(wkhtmltopdf=r'D:\gtn\tools\wkhtmltopdf\bin\wkhtmltopdf.exe')

                # Read the HTML content
                with open(output_file, "r", encoding="utf-8") as file:
                    html_content = file.read()
                options = {
                    "page-size": "A4",  # Set exact A4 size
                    "dpi": 200,  # High resolution for clarity
                    "margin-top": "0mm",
                    "margin-bottom":"0mm",
                    "margin-left":"0mm",
                    "margin-right": "0mm",
                    "zoom": 1.3,  # Adjust zoom level to scale properly
                    "disable-smart-shrinking": "",
                }

                pdf = pdfkit.from_string(html_content, False, configuration=config, options=options)

                # Return the PDF as a downloadable response
                response = HttpResponse(pdf, content_type="application/pdf")
                response["Content-Disposition"] = f'attachment; filename="Payslip_{empID}_{sMonth}.pdf"'
                return response

            else:
                return HttpResponse("Error: Payslip file not found.", status=404)

        except subprocess.CalledProcessError as e:
            return HttpResponse(f"Java Execution Failed:<br>{e.stderr}", status=500)

    # Fetch months for the dropdown
    smonth_list = MasSmonth.objects.filter(smonth__isnull=False).order_by("-smonth").values_list("smonth", flat=True)

    return render(request, "payroll.html", {"smonth_list": smonth_list})

@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
@login_required_view
def testpreview(request):
    if request.method == "POST":
        empID = str(request.session.get("empid"))
        sMonth = request.POST.get("month_year")

        # Convert "YYYY-MM" to "MMM YYYY"
        sMonth_obj = datetime.strptime(sMonth, "%Y-%m")
        sMonth = sMonth_obj.strftime("%b %Y")

        java_program = "java"
        java_class = "EssPayslip"
        java_directory = "D:/gtn/reports/"
        output_folder = os.path.join(java_directory, "output")
        output_file = os.path.join(output_folder, "generated_payslip.html")

        java_command = [
            java_program,
            "-cp", f"{java_directory};{java_directory}*",
            java_class, empID, sMonth
        ]

        try:
            subprocess.run(java_command, check=True, capture_output=True, text=True)

            if os.path.exists(output_file):
                with open(output_file, "r", encoding="utf-8") as file:
                    html_content = file.read()

                return JsonResponse({"html_content": html_content})
            else:
                return JsonResponse({"error": "Payslip file not found."}, status=404)

        except subprocess.CalledProcessError as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request."}, status=400)

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        plantcode = request.POST.get("plantcode")
        fullname = request.POST.get("fullname")
        password = request.POST.get("password")

        # Check if the employee exists in MasEmpOfficial
        try:
            employee = MasEmpOfficial.objects.get(empno=username, plantcode=plantcode, empname=fullname)
        except MasEmpOfficial.DoesNotExist:
            return render(request, "signup.html", {"error": "Employee details not found in records!"})

        if Users.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "User already exists! Please log in."})

        # Create and save new user
        user = Users(
            empid=employee.id,  # Store employee ID
            username=username,
            plantcode=plantcode,
            fullname=fullname,
            password=make_password(password),  # Hash the password
            active=1,  # Set active flag
            usercatg="E",  # Assuming default user type
            creationdate=timezone.now()
        )
        user.save()

        return render(request, "esslogin.html")  # Redirect to login page after successful signup

    return render(request, "signup.html")
# viewsimport
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_control
from django.core.exceptions import ValidationError
import logging
import uuid
from datetime import datetime as dt
from django.contrib.messages import get_messages

from .models import Users, MasEmpLeave, EntEmpLeaveappl, MasEmpOfficial

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required_view
def leave_management(request):
    empid = request.session.get("empid")  
    print(f"Session EmpID: {empid}") 

    leave_data = {
        "Casual_Leave": {"utilized": 0, "total_entitlement": 0},
        "Earned_Leave": {"utilized": 0, "total_entitlement": 0},
        "Maternity_Leave": {"utilized": 0, "total_entitlement": 0},
        "Sick_Leave": {"utilized": 0, "total_entitlement": 0},
    }
    
    leave_records = []  

    if empid:
        try:
            employee = MasEmpOfficial.objects.get(id=empid)
            leave_balances = MasEmpLeave.objects.filter(empid=empid)
            for leave in leave_balances:
                leave_type = leave.lcode  
                leave_balance = leave.lopen + (leave.lcredit or 0)  
                leave_utilized = leave.lutil  

                leave_type_map = {
                    "CL": "Casual_Leave",
                    "EL": "Earned_Leave",
                    "ML": "Maternity_Leave",
                    "SL": "Sick_Leave",
                }

                if leave_type in leave_type_map:
                    mapped_type = leave_type_map[leave_type]
                    leave_data[mapped_type] = {
                        "utilized": leave_utilized,
                        "total_entitlement": leave_balance
                    }

            leave_records_queryset = EntEmpLeaveappl.objects.filter(empid=empid).order_by('-lfrom')

            leave_records = []
            for record in leave_records_queryset:
                # Combine leave types for display
                if record.fromfn and record.froman:
                    # Full day leave - both sessions
                    if record.fnlcode == record.anlcode:
                        lcode = record.fnlcode
                    else:
                        lcode = f"{record.fnlcode}(FN)/{record.anlcode}(AN)"
                elif record.fromfn:
                    # Only forenoon
                    lcode = f"{record.fnlcode}(FN)"
                elif record.froman:
                    # Only afternoon
                    lcode = f"{record.anlcode}(AN)"
                else:
                    lcode = "N/A"

                leave_records.append({
                    "id": record.id,
                    "empid": record.empid,
                    "plantcode": record.plantcode,
                    "lcode": lcode,  # Combined leave code
                    "lfrom": record.lfrom.strftime("%B %d, %Y") if record.lfrom else "",
                    "lto": record.lto.strftime("%B %d, %Y") if record.lto else "",
                    "totldays": record.totldays,
                    "description": record.description,
                    "appstatus": record.appstatus,
                    "fromfn": record.fromfn,
                    "froman": record.froman,
                    "tofn": record.tofn,
                    "toan": record.toan,
                })

            context = {
                "fullname": employee.empname,
                "username": request.session.get("username"),
                "leave_data": leave_data,
                "leave_records": leave_records, 
            }

            return render(request, 'leavemanagement.html', context)

        except MasEmpOfficial.DoesNotExist:
            print("No employee found with this EmpID")  
            messages.error(request, "Employee record not found")

    return render(request, "leavemanagement.html", {
        "username": request.session.get("username"),
        "leave_data": leave_data,
        "leave_records": leave_records  
    })
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from datetime import datetime as dt
from .models import EntEmpLeaveappl, MasEmpLeave, Users
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)

@login_required_view
def apply_newleave(request):
    # Clear existing messages
    storage = messages.get_messages(request)
    for _ in storage:
        pass

    # Get employee details from session
    empid = request.session.get("empid")
    if not empid:
        messages.error(request, "Employee not logged in.")
        return redirect("leavemanagement")

    plantcode = request.session.get("plantcode")
    if not plantcode:
        try:
            user = Users.objects.get(empid=empid)
            plantcode = user.plantcode
            request.session["plantcode"] = plantcode
        except Users.DoesNotExist:
            messages.error(request, "Employee record not found.")
            return redirect("leavemanagement")
        except Exception as e:
            logger.error(f"Error fetching user: {str(e)}")
            messages.error(request, "System error. Please try again.")
            return redirect("leavemanagement")

    # Get available leave types and balance
    try:
        leave_types = MasEmpLeave.objects.filter(empid=empid, isactive=True).values("lcode", "lbal").distinct()
        # Calculate total leave balance (sum of all leave types)
        total_leave_balance = sum(leave['lbal'] for leave in leave_types) if leave_types else 0
    except Exception as e:
        logger.error(f"Error fetching leave types: {str(e)}")
        leave_types = []
        total_leave_balance = 0

    if request.method == "POST":
        try:
            with transaction.atomic():
                # Basic form validation
                required_fields = ['lfrom', 'lto', 'leavebal', 'totldays']
                if not all(k in request.POST for k in required_fields):
                    messages.error(request, "Missing required fields.")
                    return render(request, "apply_newleave.html", {
                        "empid": empid, 
                        "plantcode": plantcode, 
                        "leave_types": leave_types,
                        "leave_balance": total_leave_balance
                    })

                # Validate numerical values first
                try:
                    leavebal = float(request.POST.get("leavebal", 0))
                    totldays = float(request.POST.get("totldays", 0))
                    if leavebal < 0 or totldays <= 0:
                        raise ValueError("Invalid values")
                except (ValueError, TypeError) as e:
                    logger.error(f"Invalid numerical values: {str(e)}")
                    messages.error(request, "Invalid leave balance or total days. Please enter valid numbers.")
                    return render(request, "apply_newleave.html", {
                        "empid": empid, 
                        "plantcode": plantcode, 
                        "leave_types": leave_types,
                        "leave_balance": total_leave_balance
                    })

                # Check if leave days exceed balance
                if totldays > leavebal:
                    messages.error(request, "Leave days requested exceed your available balance.")
                    return render(request, "apply_newleave.html", {
                        "empid": empid, 
                        "plantcode": plantcode, 
                        "leave_types": leave_types,
                        "leave_balance": total_leave_balance
                    })

                # Get form data
                action = request.POST.get("action", "submit")
                appstatus = "Open" if action == "draft" else "Pending"
                description = request.POST.get("description", "")
                attachment = request.FILES.get('attachment')
                
                # Get session selections
                fromfn = request.POST.get("fromfn") == "on"
                froman = request.POST.get("froman") == "on"
                tofn = request.POST.get("tofn") == "on"
                toan = request.POST.get("toan") == "on"

                # Validate at least one session is selected
                if not (fromfn or froman) or not (tofn or toan):
                    messages.error(request, "Select at least one session (Forenoon or Afternoon) for both dates.")
                    return render(request, "apply_newleave.html", {
                        "empid": empid, 
                        "plantcode": plantcode, 
                        "leave_types": leave_types,
                        "leave_balance": total_leave_balance
                    })

                # Get leave types with defaults
                fnlcode = request.POST.get("fnlcode", "AB").strip()
                anlcode = request.POST.get("anlcode", "AB").strip()

                # Validate date format
                try:
                    lfrom_date = dt.strptime(request.POST.get("lfrom"), "%Y-%m-%d").date()
                    lto_date = dt.strptime(request.POST.get("lto"), "%Y-%m-%d").date()
                except (ValueError, TypeError):
                    messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
                    return render(request, "apply_newleave.html", {
                        "empid": empid, 
                        "plantcode": plantcode, 
                        "leave_types": leave_types,
                        "leave_balance": total_leave_balance
                    })

                if lfrom_date > lto_date:
                    messages.error(request, "Leave To date must be after Leave From date.")
                    return render(request, "apply_newleave.html", {
                        "empid": empid, 
                        "plantcode": plantcode, 
                        "leave_types": leave_types,
                        "leave_balance": total_leave_balance
                    })

                # Validate leave type selection based on sessions
                if fromfn and not froman:
                    if not fnlcode or fnlcode == "AB":
                        messages.error(request, "Select a valid Forenoon leave type.")
                        return render(request, "apply_newleave.html", {
                            "empid": empid, 
                            "plantcode": plantcode, 
                            "leave_types": leave_types,
                            "leave_balance": total_leave_balance
                        })
                    anlcode = "AB"
                elif froman and not fromfn:
                    if not anlcode or anlcode == "AB":
                        messages.error(request, "Select a valid Afternoon leave type.")
                        return render(request, "apply_newleave.html", {
                            "empid": empid, 
                            "plantcode": plantcode, 
                            "leave_types": leave_types,
                            "leave_balance": total_leave_balance
                        })
                    fnlcode = "AB"
                else:
                    if (not fnlcode or fnlcode == "AB") or (not anlcode or anlcode == "AB"):
                        messages.error(request, "Select valid leave types for both sessions.")
                        return render(request, "apply_newleave.html", {
                            "empid": empid, 
                            "plantcode": plantcode, 
                            "leave_types": leave_types,
                            "leave_balance": total_leave_balance
                        })
                    if lfrom_date != lto_date and fnlcode != anlcode:
                        messages.error(request, "For multiple days leave, Forenoon and Afternoon leave types must be the same.")
                        return render(request, "apply_newleave.html", {
                            "empid": empid, 
                            "plantcode": plantcode, 
                            "leave_types": leave_types,
                            "leave_balance": total_leave_balance
                        })

                # Special leave types validation
                special_leaves = ['SL', 'ML']
                if (fnlcode in special_leaves or anlcode in special_leaves) and fnlcode != anlcode:
                    messages.error(request, "SL and ML cannot be combined with other leave types.")
                    return render(request, "apply_newleave.html", {
                        "empid": empid, 
                        "plantcode": plantcode, 
                        "leave_types": leave_types,
                        "leave_balance": total_leave_balance
                    })

                # Create leave application entry
                leave_entry = EntEmpLeaveappl(
                    empid=empid,
                    plantcode=plantcode,
                    fnlcode=fnlcode,
                    anlcode=anlcode,
                    leavebal=leavebal,
                    lfrom=lfrom_date,
                    lto=lto_date,
                    totldays=totldays,
                    description=description,
                    fromfn=1 if fromfn else 0,
                    froman=1 if froman else 0,
                    tofn=1 if tofn else 0,
                    toan=1 if toan else 0,
                    appstatus=appstatus,
                    createdby=empid,
                    createddate=timezone.now(),
                )

                leave_entry.save()
                logger.info(f"Leave application saved: {leave_entry.pk}")

                # Handle attachment
                if attachment:
                    try:
                        leave_entry.attachment = attachment.read()
                        leave_entry.attachment_name = attachment.name[:255]
                        leave_entry.save(update_fields=['attachment', 'attachment_name'])
                    except Exception as e:
                        logger.error(f"Attachment error: {str(e)}")
                        messages.warning(request, "Attachment could not be processed.")

                messages.success(request, "Leave application submitted successfully!" if action == "submit" 
                               else "Leave application saved as draft!")
                return redirect("leavemanagement")

        except Exception as e:
            logger.error(f"Leave application error: {str(e)}", exc_info=True)
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, "apply_newleave.html", {
                "empid": empid, 
                "plantcode": plantcode, 
                "leave_types": leave_types,
                "leave_balance": total_leave_balance
            })

    return render(request, "apply_newleave.html", {
        "empid": empid,
        "plantcode": plantcode,
        "leave_types": leave_types,
        "leave_balance": total_leave_balance
    })



def get_leave_details(request, leave_id):
    try:
        leave = get_object_or_404(EntEmpLeaveappl, id=leave_id)

        leave_types = MasEmpLeave.objects.filter(
            empid=leave.empid, 
            isactive=True
        ).values("lcode", "lbal").distinct()

        current_leave_balance = MasEmpLeave.objects.filter(
            empid=leave.empid,
            lcode=leave.lcode
        ).first()

        response_data = {
            "success": True,
            "plantcode": leave.plantcode,
            "leaveFrom": leave.lfrom.strftime("%Y-%m-%d") if leave.lfrom else "",
            "leaveTo": leave.lto.strftime("%Y-%m-%d") if leave.lto else "",
            "totalDays": leave.totldays,
            "leaveCode": leave.lcode,
            "leaveBalance": current_leave_balance.lbal if current_leave_balance else 0,
            "fromFN": leave.fromfn,
            "fromAN": leave.froman,
            "toFN": leave.tofn,
            "toAN": leave.toan,
            "description": leave.description,
            "approvalStatus": leave.appstatus,
            "attachment": leave.attachment.name if leave.attachment else None,
            "leaveTypes": list(leave_types) 
        }

        return JsonResponse(response_data)

    except Exception as e:
        logger.error(f"Error fetching leave details: {str(e)}", exc_info=True)
        return JsonResponse({
            "success": False, 
            "message": f"Error fetching leave details: {str(e)}"
        }, status=500)



@csrf_exempt
def update_leave(request, leave_id):
    logger.info(f"Received request to update leave with ID: {leave_id}")
    empid = request.session.get("empid")
    if not empid:
        return JsonResponse(
            {"success": False, "message": "Session expired!"}, 
            status=401
        )

    try:
        leave = EntEmpLeaveappl.objects.get(id=leave_id, empid=empid)
    except EntEmpLeaveappl.DoesNotExist:
        return JsonResponse(
            {"success": False, "message": "Leave application not found or not owned by user"}, 
            status=404
        )

    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Invalid request method. Only POST allowed."}, 
            status=405
        )

    try:
        required_fields = ['lcode', 'lfrom', 'lto']
        missing_fields = [field for field in required_fields if field not in request.POST]
        if missing_fields:
            return JsonResponse({
                "success": False,
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }, status=400)
        try:
            lfrom = dt.strptime(request.POST['lfrom'], "%Y-%m-%d").date()
            lto = dt.strptime(request.POST['lto'], "%Y-%m-%d").date()
            
            if lto < lfrom:
                return JsonResponse({
                    "success": False,
                    "message": "End date cannot be before start date"
                }, status=400)
                
            if lfrom < timezone.now().date():
                return JsonResponse({
                    "success": False,
                    "message": "Cannot apply for leave in the past"
                }, status=400)
                
        except ValueError as e:
            return JsonResponse({
                "success": False,
                "message": f"Invalid date format: {str(e)}. Use YYYY-MM-DD."
            }, status=400) 
        leave.lcode = request.POST['lcode']
        leave.lfrom = lfrom
        leave.lto = lto
        leave.description = request.POST.get('description', '')
        
        leave.fromfn = request.POST.get('fromfn', 'false').lower() == 'true'
        leave.froman = request.POST.get('froman', 'false').lower() == 'true'
        leave.tofn = request.POST.get('tofn', 'false').lower() == 'true'
        leave.toan = request.POST.get('toan', 'false').lower() == 'true'
        
        if 'attachment' in request.FILES:
            attachment = request.FILES['attachment']
            if attachment.size > 5 * 1024 * 1024:
                return JsonResponse({
                    "success": False,
                    "message": "File size exceeds 5MB limit"
                }, status=400)
            leave.attachment = attachment
        
        # Calculate total days
        delta = (lto - lfrom).days + 1  # Inclusive count
        
        # Adjust for half days
        if leave.fromfn ^ leave.froman:  # XOR operation
            delta -= 0.5
        if leave.tofn ^ leave.toan:
            delta -= 0.5
            
        leave.totldays = max(delta, 0.5)  # Minimum 0.5 day
        
        # Update metadata and reset status
        leave.updated_by = empid
        leave.updated_date = timezone.now()
        leave.appstatus = 'Pending'  # Reset to Pending on edit
        
        # Validate model before saving
        try:
            leave.full_clean()
        except ValidationError as e:
            return JsonResponse({
                "success": False,
                "message": f"Validation error: {str(e)}"
            }, status=400)
        
        # Save changes
        leave.save()
        
        return JsonResponse({
            "success": True,
            "message": "Leave updated successfully! Status reset to Pending.",
            "data": {
                "id": leave.id,
                "lcode": leave.lcode,
                "lfrom": leave.lfrom.strftime('%Y-%m-%d'),
                "lto": leave.lto.strftime('%Y-%m-%d'),
                "totldays": leave.totldays,
                "appstatus": leave.appstatus,
                "description": leave.description,
                "updated_date": leave.updated_date.strftime('%Y-%m-%d %H:%M:%S')
            }
        })

    except Exception as e:
        logger.error(f"Error updating leave {leave_id}: {str(e)}", exc_info=True)
        return JsonResponse({
            "success": False,
            "message": "An error occurred while processing your request."
        }, status=500)

@require_POST
def delete_leave(request, leave_id):
    try:
        leave = get_object_or_404(EntEmpLeaveappl, id=leave_id)
        if leave.appstatus != "Open":
            return JsonResponse({
                "success": False,
                "error": "Only leaves with 'Open' status can be deleted"
            }, status=400)
            
        leave.delete()
        return JsonResponse({
            "success": True,
            "message": "Leave successfully deleted"
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)
# ---------------------------------------------------------------


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required_view
def claims(request):
    empid = request.session.get("empid") 
    
    if not empid:
        return HttpResponse("Unauthorized", status=401)

    try:
        employee = MasEmpOfficial.objects.get(id=empid)

        if request.method == "POST":
            expid = request.POST.get("expenseType")
            claim_date = request.POST.get("claimDate")
            claim_amount = request.POST.get("amount")
            documents = request.FILES.get("Receipt")  # File upload handling
            description = request.POST.get("description")

            if not (expid and claim_date and claim_amount):
                return HttpResponse("Missing required fields", status=400)

            # Validate file type (Allow only PDF, JPEG, JPG)
            if documents:
                allowed_extensions = ["pdf", "jpeg", "jpg"]
                file_extension = documents.name.split('.')[-1].lower()
                
                if file_extension not in allowed_extensions:
                    return HttpResponse("Invalid file type. Only PDF and JPEG/JPG are allowed.", status=400)

            # Save new claim
            claim = EntEmpExpenses(
                empid=empid,
                expid=MasExpenses.objects.get(expid=expid),
                claimdt=claim_date,
                claimamount=claim_amount,
                documents=documents,
                description=description,
                appstatus="Pending",  
                createdby=request.session.get("fullname"),
                createddate=datetime.now()  
            )
            claim.save()
            return redirect("claims") 

        expenses = MasExpenses.objects.all()
        claims = EntEmpExpenses.objects.filter(empid=empid).select_related("expid")

        context = {
            "fullname": employee.empname,
            "username": request.session.get("username"),
            "expenses": expenses,
            "claims": claims,
        }
        return render(request, "claims.html", context)

    except MasEmpOfficial.DoesNotExist:
        return HttpResponse("Employee not found", status=404)

# -------------------------------------------------------------------


@login_required_view
def loans(request): 
    empid = request.session.get("empid")
    plantcode = request.session.get("plantcode")

    if not empid:
        messages.error(request, "Session expired! Please log in again.")
        return redirect("login")

    if not plantcode:
        user = Users.objects.filter(empid=empid).first()
        if user:
            plantcode = user.plantcode
            request.session["plantcode"] = plantcode  

    loan_types = MasLoan.objects.filter(isactive=True)
    loan_applications = EntLoanappl.objects.filter(empid=empid)

    if request.method == "POST":
        try:
            action = request.POST.get("action")  # 'draft' or 'submit'
            if not action:
                messages.error(request, "Action is required. Please try again.")
                return redirect("loans")

            loan_id = request.POST.get("loanId")
            loan_application = None
            if loan_id:
                loan_application = EntLoanappl.objects.filter(id=loan_id, empid=empid).first()
            
            try:
                loan_type_id = int(request.POST.get("loanType"))
                loan_amount = float(request.POST.get("loanAmount", 0))
                no_of_dues = int(request.POST.get("noOfDues", 1))
                interest_rate = float(request.POST.get("interestRate", 0))
                interest_amount = float(request.POST.get("interestAmount", 0))
                deduction_start = datetime.strptime(request.POST.get("dedStart"), "%Y-%m-%d")
                loan_req_date = datetime.strptime(request.POST.get("loanReqDate"), "%Y-%m-%d")
            except ValueError:
                messages.error(request, "Invalid input. Please check your values.")
                return redirect("loans")

            remarks = request.POST.get("remarks", "").strip()
            ded_mode = request.POST.get("dedMode")
            approval_status = "Open" if action == "draft" else "Pending"

            # Calculate EMI more accurately
            if interest_rate > 0:
                monthly_rate = (interest_rate / 12) / 100
                first_emi = (loan_amount * monthly_rate * ((1 + monthly_rate) ** no_of_dues)) / (((1 + monthly_rate) ** no_of_dues) - 1)
                first_emi = round(first_emi, 2)
            else:
                base_emi = loan_amount // no_of_dues  
                remainder = loan_amount % no_of_dues  
                first_emi = base_emi + remainder  

            logger.info(f"Processing Loan: Type ID {loan_type_id}, Amount {loan_amount}, Dues {no_of_dues}")

            if loan_application:
                if loan_application.appstatus == "Approved":
                    messages.error(request, "Cannot edit an approved loan application.")
                    return redirect("loans")

                loan_application.loanreqdt = loan_req_date
                loan_application.loanamt = loan_amount
                loan_application.noofdues = no_of_dues
                loan_application.loanemi = first_emi
                loan_application.dedmode = ded_mode
                loan_application.dedstartfrom = deduction_start
                loan_application.sanctionamt = loan_amount
                loan_application.sanctionemi = first_emi
                loan_application.sanctiondues = no_of_dues
                loan_application.intrate = interest_rate
                loan_application.intamt = interest_amount
                loan_application.sanctionnetamt = loan_amount
                loan_application.appstatus = approval_status
                loan_application.remarks = remarks
                loan_application.save()
                logger.info(f"Loan Application updated: {loan_application}")
            else:
                new_loan = EntLoanappl.objects.create(
                    empid=empid,
                    plantcode=plantcode,
                    lnameid_id=loan_type_id,
                    loanreqdt=loan_req_date,
                    loanamt=loan_amount,
                    noofdues=no_of_dues,
                    loanemi=first_emi,
                    dedmode=ded_mode,
                    dedstartfrom=deduction_start,
                    sanctionamt=loan_amount,
                    sanctionemi=first_emi,
                    sanctiondues=no_of_dues,
                    intrate=interest_rate,
                    intamt=interest_amount,
                    sanctionnetamt=loan_amount,
                    appstatus=approval_status,
                    createdby=str(empid),
                    createddate=datetime.now(),
                    remarks=remarks
                )
                logger.info(f"New Loan Application created: {new_loan}")

            messages.success(request, "Loan application saved successfully!")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            logger.error(f"Error while saving loan: {e}")

        return redirect("loans")  # Corrected route name

    return render(request, "loan.html", {
        "loan_types": loan_types,
        "plantcode": plantcode,
        "empid": empid,
        "loan_applications": loan_applications
    })

def loan_details(request, loan_id):
    empid = request.session.get("empid")

    if not empid:
        messages.error(request, "Session expired! Please log in again.")
        return redirect("login")

    # Fetch loan details from EntLoanappl
    loan_application = EntLoanappl.objects.filter(id=loan_id, empid=empid).first()
    if not loan_application:
        messages.error(request, "Loan not found!")
        return redirect("loans")

    # Fetch Loan Name correctly
    loan_obj = MasLoan.objects.filter(id=loan_application.lnameid.id).first() if loan_application.lnameid else None
    loan_name = loan_obj.loanname if loan_obj else "N/A"

    # Check approval status
    if loan_application.appstatus == "Pending":
        return render(request, "loan_details.html", {
            "loan_application": loan_application,
            "loan_name": loan_name,
            "error_message": "Loan is still pending approval.",
        })

    elif loan_application.appstatus == "Rejected":
        return render(request, "loan_details.html", {
            "loan_application": loan_application,
            "loan_name": loan_name,
            "error_message": "Loan has been rejected.",
        })

    # Fetch loan details from EntLoanmas (Approved Loans Only)
    loan_details = EntLoanmas.objects.filter(appid=loan_application.id).first()

    if not loan_details:
        return render(request, "loan_details.html", {
            "loan_application": loan_application,
            "loan_name": loan_name,
            "error_message": "Loan details not found.",
        })

    # Fetch loan schedule based on loan id in EntLoanmas
    loan_schedule = EntLoanschedule.objects.filter(loanid=loan_details.id).order_by("deddt")

    return render(request, "loan_details.html", {
        "loan_application": loan_application,
        "loan_details": loan_details,
        "loan_schedule": loan_schedule,
        "loan_name": loan_name,  # Pass loan name to template
    })

@login_required_view
def loanapplication(request):
    empid = request.session.get("empid")
    if not empid:
        messages.error(request, "Session expired! Please log in again.")
        return redirect("login")
    loan_applications = EntLoanappl.objects.filter(empid=empid)
    return render(request, "loan.html", {"loan_applications": loan_applications})



@login_required_view
def applynewloan(request):
    empid = request.session.get("empid")
    
    if not empid:
        messages.error(request, "Session expired! Please log in again.")
        return redirect("login")
    
    try:
        user = Users.objects.get(empid=empid)
        plantcode = user.plantcode  
    except Users.DoesNotExist:
        messages.error(request, "Employee record not found.")
        return redirect("esslogin") 

    loan_types = MasLoan.objects.filter(isactive=True)

    if request.method == "POST":
        action = request.POST.get("action")
        
        appstatus = "Open" if action == "draft" else "Pending"

        EntLoanappl.objects.create(
            loanreqdt=request.POST.get("loanReqDate"),
            plantcode=plantcode,
            empid=empid,
            loanamt=request.POST.get("loanAmount"),
            noofdues=request.POST.get("noOfDues"),
            loanemi=request.POST.get("loanEmi"),
            dedmode=request.POST.get("dedMode"),
            dedstartfrom=request.POST.get("dedStart"),
            lnameid=MasLoan.objects.get(id=request.POST.get("loanType")),
            remarks=request.POST.get("remarks"),
            sanctionamt = request.POST.get("sanctionedAmount", 0),
            sanctionemi = request.POST.get("sanctionedEmi", 0),
            sanctiondues = request.POST.get("sanctionedDues", 0),
            intrate=request.POST.get("interestRate"),
            intamt=request.POST.get("interestAmount"),
            sanctionnetamt = request.POST.get("sanctionedNet", 0),
            appstatus=appstatus,
            createdby=empid,
            createddate=now(),
        )

        messages.success(request, f"Loan application {'saved to draft' if action == 'draft' else 'submitted'} successfully!")
        return redirect("loanapplications")

    return render(
        request,
        "apply_newloan.html",
        {
            "loan_types": loan_types,
            "empid": empid,
            "plantcode": plantcode,
        },
    )



@require_POST
def delete_loan(request, loan_id):
    try:
        loan = get_object_or_404(EntLoanappl, id=loan_id)
        if loan.appstatus != "Open":
            return JsonResponse({
                "success": False,
                "error": "Only loans with 'Open' status can be deleted"
            }, status=400)
            
        loan.delete()
        return JsonResponse({
            "success": True,
            "message": "Loan successfully deleted"
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)
    
    


def get_loan_details(request, loan_id):
    loan = get_object_or_404(EntLoanappl, id=loan_id)
    loan_types = MasLoan.objects.all()
    loan_data = {
        "success": True,
        "loanreqdt": loan.loanreqdt.strftime("%Y-%m-%d"),
        "plantcode": loan.plantcode,
        "empid": loan.empid,
        "loanamt": str(loan.loanamt),
        "noofdues": loan.noofdues,
        "loanemi": str(loan.loanemi),
        "dedmode": loan.dedmode,
        "dedstartfrom": loan.dedstartfrom.strftime("%Y-%m-%d"),
        "lnameid": loan.lnameid.id if loan.lnameid else "",  
        "loanTypeName": loan.lnameid.loanname if loan.lnameid else "",  
        "remarks": loan.remarks or "",
        "sanctionamt": str(loan.sanctionamt),
        "sanctionemi": str(loan.sanctionemi),
        "sanctiondues": loan.sanctiondues,
        "intrate": str(loan.intrate),
        "intamt": str(loan.intamt),
        "sanctionnetamt": str(loan.sanctionnetamt),
        "appstatus": loan.appstatus,
        "loanTypes": [{"id": loan_type.id, "name": loan_type.loanname} for loan_type in loan_types] 
    }
    return JsonResponse(loan_data)




logger = logging.getLogger(__name__)

@csrf_exempt
@login_required_view
def update_loan(request, loan_id):
    logger.info(f"Received request to update loan with ID: {loan_id}")
    empid = request.session.get("empid")

    if not empid:
        return JsonResponse({"success": False, "message": "Session expired!"})

    try:
        loan = EntLoanappl.objects.get(id=loan_id)
    except EntLoanappl.DoesNotExist:
        logger.error(f"Loan with ID {loan_id} does not exist.")
        return JsonResponse({"success": False, "message": "Loan not found."})

    if request.method == "POST":
        try:
            loan.loanreqdt = datetime.datetime.strptime(request.POST.get("loanReqDate"), "%Y-%m-%d").date()
            loan.dedstartfrom = datetime.datetime.strptime(request.POST.get("dedStart"), "%Y-%m-%d").date()

            loan_type_id = request.POST.get("loanType")
            if loan_type_id:
                loan.lnameid = get_object_or_404(MasLoan, id=loan_type_id)

            loan.loanamt = float(request.POST.get("loanAmount"))
            loan.noofdues = int(request.POST.get("noOfDues"))
            loan.loanemi = float(request.POST.get("loanEmi"))
            loan.dedmode = request.POST.get("dedMode")
            loan.sanctionamt = float(request.POST.get("sanctionedAmount"))
            loan.sanctiondues = int(request.POST.get("sanctionedDues"))
            loan.sanctionemi = float(request.POST.get("sanctionedEmi"))
            loan.sanctionnetamt = float(request.POST.get("sanctionedNet"))
            loan.remarks = request.POST.get("remarks")
            loan.appstatus = request.POST.get("approvalStatus")

            loan.updatedby = empid
            loan.updateddate = now()

            loan.save()

            return JsonResponse({
                "success": True,
                "message": "Loan updated successfully!",
                "updatedData": {
                    "loanId": loan.id,
                    "loanReqDate": str(loan.loanreqdt),
                    "dedStart": str(loan.dedstartfrom),
                    "loanType": loan.lnameid.id if loan.lnameid else None,
                    "loanAmount": loan.loanamt,
                    "noOfDues": loan.noofdues,
                    "loanEmi": loan.loanemi,
                    "dedMode": loan.dedmode,
                    "sanctionedAmount": loan.sanctionamt,
                    "sanctionedDues": loan.sanctiondues,
                    "sanctionedEmi": loan.sanctionemi,
                    "sanctionedNet": loan.sanctionnetamt,
                    "remarks": loan.remarks,
                    "approvalStatus": loan.appstatus,
                    "updatedBy": loan.updatedby,
                    "updatedDate": str(loan.updateddate),
                }
            })

        except Exception as e:
            logger.error(f"Error updating loan: {str(e)}")
            return JsonResponse({"success": False, "message": f"Error updating loan: {str(e)}"})

    return JsonResponse({"success": False, "message": "Invalid request method."})



# ..........................................Loan application(End).......................................
@login_required_view
def requeststatus(request):
    return render(request, "requeststatus.html")