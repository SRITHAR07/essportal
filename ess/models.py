from django.db import models
import os
from django.core.validators import FileExtensionValidator


class GennhrAudit(models.Model):
    datetime = models.DateTimeField()
    ip = models.CharField(max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS')
    user = models.CharField(max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    table = models.CharField(max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    action = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS')
    description = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'GennHR_audit'

class Users(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    empid = models.IntegerField(db_column='EmpID')  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    fullname = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    plantcode = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    password = models.CharField(db_column='Password', max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    active = models.IntegerField()
    usercatg = models.CharField(db_column='Usercatg', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    passwordquestion = models.CharField(db_column='PasswordQuestion', max_length=256, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    passwordanswer = models.CharField(db_column='PasswordAnswer', max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    isapproved = models.BooleanField(db_column='IsApproved', blank=True, null=True)  # Field name made lowercase.
    lastactivitydate = models.DateTimeField(db_column='LastActivityDate', blank=True, null=True)  # Field name made lowercase.
    lastlogindate = models.DateTimeField(db_column='LastLoginDate', blank=True, null=True)  # Field name made lowercase.
    lastpasswordchangeddate = models.DateTimeField(db_column='LastPasswordChangedDate', blank=True, null=True)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='CreationDate')  # Field name made lowercase.
    islockedout = models.BooleanField(db_column='IsLockedOut', blank=True, null=True)  # Field name made lowercase.
    lastlockedoutdate = models.DateTimeField(db_column='LastLockedOutDate', blank=True, null=True)  # Field name made lowercase.
    failedpasswordattemptcount = models.IntegerField(db_column='FailedPasswordAttemptCount', blank=True, null=True)  # Field name made lowercase.
    failedpasswordattemptwindowstart = models.DateTimeField(db_column='FailedPasswordAttemptWindowStart', blank=True, null=True)  # Field name made lowercase.
    failedpasswordanswerattemptcount = models.IntegerField(db_column='FailedPasswordAnswerAttemptCount', blank=True, null=True)  # Field name made lowercase.
    failedpasswordanswerattemptwindowstart = models.DateTimeField(db_column='FailedPasswordAnswerAttemptWindowStart', blank=True, null=True)  # Field name made lowercase.
    usertype = models.CharField(db_column='Usertype', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    orglevel = models.IntegerField(db_column='Orglevel', blank=True, null=True)  # Field name made lowercase.
    parentlevel = models.IntegerField(db_column='Parentlevel', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Users'

class MasPlantleave(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    plantcode = models.CharField(db_column='Plantcode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    lcode = models.CharField(db_column='Lcode', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    lname = models.CharField(db_column='Lname', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    isnh = models.BooleanField(db_column='IsNH')  # Field name made lowercase.
    isph = models.BooleanField(db_column='IsPH')  # Field name made lowercase.
    maxleave = models.IntegerField(db_column='Maxleave')  # Field name made lowercase.
    isencash = models.BooleanField(db_column='IsEncash')  # Field name made lowercase.
    validdays = models.DecimalField(db_column='Validdays', max_digits=18, decimal_places=2)  # Field name made lowercase.
    isactive = models.BooleanField(db_column='Isactive')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Plantleave'

class AttnDaily(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    plantcode = models.CharField(db_column='Plantcode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    empid = models.IntegerField(db_column='EmpID')  # Field name made lowercase.
    attndt = models.DateTimeField(db_column='Attndt')  # Field name made lowercase.
    wrkdivid = models.IntegerField(db_column='WrkdivID')  # Field name made lowercase.
    shiftcode = models.CharField(db_column='Shiftcode', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    checkin = models.DateTimeField(db_column='Checkin', blank=True, null=True)  # Field name made lowercase.
    checkout = models.DateTimeField(db_column='Checkout', blank=True, null=True)  # Field name made lowercase.
    perhrs = models.IntegerField(db_column='Perhrs')  # Field name made lowercase.
    tothrs = models.IntegerField(db_column='Tothrs', blank=True, null=True)  # Field name made lowercase.
    lshift = models.DecimalField(db_column='Lshift', max_digits=18, decimal_places=3)  # Field name made lowercase.
    regshift = models.DecimalField(db_column='Regshift', max_digits=18, decimal_places=3)  # Field name made lowercase.
    tallow = models.DecimalField(db_column='Tallow', max_digits=18, decimal_places=2)  # Field name made lowercase.
    regot = models.IntegerField(db_column='RegOT')  # Field name made lowercase.
    la = models.IntegerField(db_column='LA')  # Field name made lowercase.
    ed = models.IntegerField(db_column='ED')  # Field name made lowercase.
    laded = models.IntegerField(db_column='Laded')  # Field name made lowercase.
    edded = models.IntegerField(db_column='Edded')  # Field name made lowercase.
    mustattn = models.CharField(db_column='Mustattn', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    isintimatedleave = models.BooleanField(db_column='IsIntimatedLeave')  # Field name made lowercase.
    islock = models.BooleanField(db_column='Islock')  # Field name made lowercase.
    wgen = models.BooleanField(db_column='Wgen')  # Field name made lowercase.
    mgen = models.BooleanField(db_column='Mgen')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.
    break1 = models.DateTimeField(db_column='Break1', blank=True, null=True)  # Field name made lowercase.
    break2 = models.DateTimeField(db_column='Break2', blank=True, null=True)  # Field name made lowercase.
    fnshift = models.DecimalField(db_column='FNshift', max_digits=18, decimal_places=3)  # Field name made lowercase.
    anshift = models.DecimalField(db_column='ANshift', max_digits=18, decimal_places=3)  # Field name made lowercase.
    fnlcode = models.CharField(db_column='FNLcode', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    anlcode = models.CharField(db_column='ANLcode', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Attn_Daily'


class EntAddress(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    empid = models.IntegerField(db_column='EmpID')  # Field name made lowercase.
    atype = models.CharField(db_column='Atype', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    platno = models.CharField(db_column='Platno', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    streetname = models.CharField(db_column='Streetname', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    townname = models.CharField(db_column='Townname', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    locid = models.IntegerField(db_column='LocID', blank=True, null=True)  # Field name made lowercase.
    locname = models.CharField(db_column='Locname', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    talukname = models.CharField(db_column='Talukname', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    districtname = models.CharField(db_column='Districtname', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    statename = models.CharField(db_column='Statename', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    countryname = models.CharField(db_column='Countryname', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    nationality = models.CharField(db_column='Nationality', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    pincode = models.CharField(db_column='Pincode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    nativeps = models.CharField(db_column='NativePS', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    docname = models.TextField(db_column='Docname', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    appstatus = models.CharField(db_column='Appstatus', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ent_Address'

class MasChklist(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    chklistname = models.CharField(db_column='Chklistname', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    chktype = models.CharField(db_column='Chktype', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    isreq = models.BooleanField(db_column='Isreq')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='Isactive')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=18, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Chklist'


class MasDocuments(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    docname = models.CharField(db_column='Docname', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    doccatg = models.CharField(db_column='Doccatg', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    ispf = models.BooleanField(db_column='Ispf')  # Field name made lowercase.
    pfcode = models.CharField(db_column='Pfcode', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    isexpiry = models.BooleanField(db_column='Isexpiry')  # Field name made lowercase.
    alertbefore = models.IntegerField(db_column='Alertbefore')  # Field name made lowercase.
    chkid = models.IntegerField(db_column='ChkID', blank=True, null=True)  # Field name made lowercase.
    isactive = models.BooleanField(db_column='Isactive')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Documents'


class MasEmpDocuments(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) 
    empid = models.IntegerField(db_column='EmpID')  
    docid = models.IntegerField(db_column='DocID')  
    docno = models.CharField(db_column='Docno', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    docname = models.TextField(db_column='Docname', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    chkid = models.IntegerField(db_column='ChkID', blank=True, null=True)  # Field name made lowercase.
    expirydt = models.DateField(db_column='Expirydt', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Emp_Documents'

def document_upload_path(instance, filename):
    """Stores files in the 'uploaded_documents/' folder inside the project."""
    return os.path.join("documents", filename)

class EntMsalary(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    smonthid = models.IntegerField(db_column='SmonthID')  # Field name made lowercase.
    mstart = models.DateTimeField(db_column='Mstart')  # Field name made lowercase.
    mend = models.DateTimeField(db_column='Mend')  # Field name made lowercase.
    plantcode = models.CharField(db_column='Plantcode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    empid = models.IntegerField(db_column='EmpID')  # Field name made lowercase.
    a01 = models.DecimalField(db_column='A01', max_digits=18, decimal_places=2)  # Field name made lowercase.
    a02 = models.DecimalField(db_column='A02', max_digits=18, decimal_places=2)  # Field name made lowercase.
    a03 = models.DecimalField(db_column='A03', max_digits=18, decimal_places=2)  # Field name made lowercase.
    a04 = models.DecimalField(db_column='A04', max_digits=18, decimal_places=2)  # Field name made lowercase.
    a05 = models.DecimalField(db_column='A05', max_digits=18, decimal_places=2)  # Field name made lowercase.
    a06 = models.DecimalField(db_column='A06', max_digits=18, decimal_places=2)  # Field name made lowercase.
    a07 = models.DecimalField(db_column='A07', max_digits=18, decimal_places=2)  # Field name made lowercase.
    a08 = models.DecimalField(db_column='A08', max_digits=18, decimal_places=2)  # Field name made lowercase.
    a09 = models.DecimalField(db_column='A09', max_digits=18, decimal_places=2)  # Field name made lowercase.
    a10 = models.DecimalField(db_column='A10', max_digits=18, decimal_places=2)  # Field name made lowercase.
    a11 = models.DecimalField(db_column='A11', max_digits=18, decimal_places=2)  # Field name made lowercase.
    a12 = models.DecimalField(db_column='A12', max_digits=18, decimal_places=2)  # Field name made lowercase.
    a13 = models.DecimalField(db_column='A13', max_digits=18, decimal_places=2)  # Field name made lowercase.
    a14 = models.DecimalField(db_column='A14', max_digits=18, decimal_places=2)  # Field name made lowercase.
    a15 = models.DecimalField(db_column='A15', max_digits=18, decimal_places=2)  # Field name made lowercase.
    atot = models.DecimalField(db_column='Atot', max_digits=18, decimal_places=2)  # Field name made lowercase.
    e01 = models.DecimalField(db_column='E01', max_digits=18, decimal_places=2)  # Field name made lowercase.
    e02 = models.DecimalField(db_column='E02', max_digits=18, decimal_places=2)  # Field name made lowercase.
    e03 = models.DecimalField(db_column='E03', max_digits=18, decimal_places=2)  # Field name made lowercase.
    e04 = models.DecimalField(db_column='E04', max_digits=18, decimal_places=2)  # Field name made lowercase.
    e05 = models.DecimalField(db_column='E05', max_digits=18, decimal_places=2)  # Field name made lowercase.
    e06 = models.DecimalField(db_column='E06', max_digits=18, decimal_places=2)  # Field name made lowercase.
    e07 = models.DecimalField(db_column='E07', max_digits=18, decimal_places=2)  # Field name made lowercase.
    e08 = models.DecimalField(db_column='E08', max_digits=18, decimal_places=2)  # Field name made lowercase.
    e09 = models.DecimalField(db_column='E09', max_digits=18, decimal_places=2)  # Field name made lowercase.
    e10 = models.DecimalField(db_column='E10', max_digits=18, decimal_places=2)  # Field name made lowercase.
    e11 = models.DecimalField(db_column='E11', max_digits=18, decimal_places=2)  # Field name made lowercase.
    e12 = models.DecimalField(db_column='E12', max_digits=18, decimal_places=2)  # Field name made lowercase.
    e13 = models.DecimalField(db_column='E13', max_digits=18, decimal_places=2)  # Field name made lowercase.
    e14 = models.DecimalField(db_column='E14', max_digits=18, decimal_places=2)  # Field name made lowercase.
    e15 = models.DecimalField(db_column='E15', max_digits=18, decimal_places=2)  # Field name made lowercase.
    etot = models.DecimalField(db_column='Etot', max_digits=18, decimal_places=2)  # Field name made lowercase.
    wdays = models.DecimalField(db_column='Wdays', max_digits=18, decimal_places=2)  # Field name made lowercase.
    aldays = models.DecimalField(db_column='ALdays', max_digits=18, decimal_places=2)  # Field name made lowercase.
    fldays = models.DecimalField(db_column='FLdays', max_digits=18, decimal_places=2)  # Field name made lowercase.
    wodays = models.DecimalField(db_column='WOdays', max_digits=18, decimal_places=2)  # Field name made lowercase.
    wwodays = models.DecimalField(db_column='Wwodays', max_digits=18, decimal_places=2)  # Field name made lowercase.
    wfldays = models.DecimalField(db_column='Wfldays', max_digits=18, decimal_places=2)  # Field name made lowercase.
    oth = models.DecimalField(db_column='Oth', max_digits=18, decimal_places=2)  # Field name made lowercase.
    wamt = models.DecimalField(db_column='Wamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    alamt = models.DecimalField(db_column='Alamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    flamt = models.DecimalField(db_column='Flamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    woamt = models.DecimalField(db_column='WOamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    wwoamt = models.DecimalField(db_column='Wwoamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    wflamt = models.DecimalField(db_column='Wflamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    othamt = models.DecimalField(db_column='Othamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    gramt = models.DecimalField(db_column='Gramt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    d01 = models.DecimalField(db_column='D01', max_digits=18, decimal_places=2)  # Field name made lowercase.
    d02 = models.DecimalField(db_column='D02', max_digits=18, decimal_places=2)  # Field name made lowercase.
    d03 = models.DecimalField(db_column='D03', max_digits=18, decimal_places=2)  # Field name made lowercase.
    d04 = models.DecimalField(db_column='D04', max_digits=18, decimal_places=2)  # Field name made lowercase.
    d05 = models.DecimalField(db_column='D05', max_digits=18, decimal_places=2)  # Field name made lowercase.
    d06 = models.DecimalField(db_column='D06', max_digits=18, decimal_places=2)  # Field name made lowercase.
    d07 = models.DecimalField(db_column='D07', max_digits=18, decimal_places=2)  # Field name made lowercase.
    d08 = models.DecimalField(db_column='D08', max_digits=18, decimal_places=2)  # Field name made lowercase.
    d09 = models.DecimalField(db_column='D09', max_digits=18, decimal_places=2)  # Field name made lowercase.
    d10 = models.DecimalField(db_column='D10', max_digits=18, decimal_places=2)  # Field name made lowercase.
    d11 = models.DecimalField(db_column='D11', max_digits=18, decimal_places=2)  # Field name made lowercase.
    d12 = models.DecimalField(db_column='D12', max_digits=18, decimal_places=2)  # Field name made lowercase.
    d13 = models.DecimalField(db_column='D13', max_digits=18, decimal_places=2)  # Field name made lowercase.
    d14 = models.DecimalField(db_column='D14', max_digits=18, decimal_places=2)  # Field name made lowercase.
    d15 = models.DecimalField(db_column='D15', max_digits=18, decimal_places=2)  # Field name made lowercase.
    dtot = models.DecimalField(db_column='Dtot', max_digits=18, decimal_places=2)  # Field name made lowercase.
    ntot = models.DecimalField(db_column='Ntot', max_digits=18, decimal_places=2)  # Field name made lowercase.
    pftot = models.DecimalField(db_column='Pftot', max_digits=18, decimal_places=2)  # Field name made lowercase.
    pstot = models.DecimalField(db_column='Pstot', max_digits=18, decimal_places=2)  # Field name made lowercase.
    esitot = models.DecimalField(db_column='Esitot', max_digits=18, decimal_places=2)  # Field name made lowercase.
    erpf = models.DecimalField(db_column='Erpf', max_digits=18, decimal_places=2)  # Field name made lowercase.
    erps = models.DecimalField(db_column='Erps', max_digits=18, decimal_places=2)  # Field name made lowercase.
    eresi = models.DecimalField(db_column='ErEsi', max_digits=18, decimal_places=2)  # Field name made lowercase.
    totdays = models.DecimalField(db_column='Totdays', max_digits=18, decimal_places=2)  # Field name made lowercase.
    totwdays = models.DecimalField(db_column='Totwdays', max_digits=18, decimal_places=2)  # Field name made lowercase.
    lopdays = models.DecimalField(db_column='Lopdays', max_digits=18, decimal_places=2)  # Field name made lowercase.
    workdays = models.DecimalField(db_column='Workdays', max_digits=18, decimal_places=2)  # Field name made lowercase.
    erpftot = models.DecimalField(db_column='Erpftot', max_digits=18, decimal_places=2)  # Field name made lowercase.
    pfstatus = models.BooleanField(db_column='PFstatus')  # Field name made lowercase.
    psstatus = models.BooleanField(db_column='PSstatus')  # Field name made lowercase.
    esistatus = models.BooleanField(db_column='ESIstatus')  # Field name made lowercase.
    vpf = models.DecimalField(db_column='Vpf', max_digits=18, decimal_places=2)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    approvalstatus = models.CharField(db_column='Approvalstatus', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    releasestatus = models.CharField(db_column='Releasestatus', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    paystat = models.BooleanField(db_column='Paystat')  # Field name made lowercase.
    paydt = models.DateTimeField(db_column='Paydt', blank=True, null=True)  # Field name made lowercase.
    lopamt = models.DecimalField(db_column='Lopamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    busscode = models.CharField(db_column='Busscode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    deptid = models.IntegerField(db_column='DeptID', blank=True, null=True)  # Field name made lowercase.
    sdeptid = models.IntegerField(db_column='SDeptID', blank=True, null=True)  # Field name made lowercase.
    desigid = models.IntegerField(db_column='DesigID', blank=True, null=True)  # Field name made lowercase.
    catgid = models.IntegerField(db_column='CatgID', blank=True, null=True)  # Field name made lowercase.
    scatgid = models.IntegerField(db_column='SCatgID', blank=True, null=True)  # Field name made lowercase.
    secid = models.IntegerField(db_column='SecID', blank=True, null=True)  # Field name made lowercase.
    gradeid = models.IntegerField(db_column='GradeID', blank=True, null=True)  # Field name made lowercase.
    f11grpid = models.IntegerField(db_column='F11grpID', blank=True, null=True)  # Field name made lowercase.
    payid = models.IntegerField(db_column='PayID', blank=True, null=True)  # Field name made lowercase.
    bankid = models.IntegerField(db_column='BankID', blank=True, null=True)  # Field name made lowercase.
    bankcode = models.CharField(db_column='Bankcode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    branchcode = models.CharField(db_column='Branchcode', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ifscode = models.CharField(db_column='IFScode', max_length=11, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    bankacno = models.CharField(db_column='Bankacno', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    curcode = models.CharField(db_column='Curcode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    curvalue = models.DecimalField(db_column='Curvalue', max_digits=18, decimal_places=2)  # Field name made lowercase.
    fcuramt = models.DecimalField(db_column='Fcuramt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    bnsopshift = models.DecimalField(db_column='Bnsopshift', max_digits=18, decimal_places=2)  # Field name made lowercase.
    bnsopamt = models.DecimalField(db_column='Bnsopamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    bnsclshift = models.DecimalField(db_column='Bnsclshift', max_digits=18, decimal_places=2)  # Field name made lowercase.
    bnsclamt = models.DecimalField(db_column='Bnsclamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    amtinwords = models.TextField(db_column='Amtinwords', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ent_Msalary'

class MasBank(models.Model):
    bankcode = models.CharField(db_column='Bankcode', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    bankname = models.CharField(db_column='Bankname', max_length=75, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='Isactive')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Bank'

class MasDedheads(models.Model):
    dedcode = models.CharField(db_column='Dedcode', primary_key=True, max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    deddesc = models.CharField(db_column='Deddesc', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='Isactive')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Dedheads'

class MasEmpSalsettings(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    empid = models.IntegerField(db_column='EmpID')  # Field name made lowercase.
    saltempid = models.IntegerField(db_column='SaltempID')  # Field name made lowercase.
    salbasis = models.CharField(db_column='Salbasis', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    payid = models.IntegerField(db_column='PayID')  # Field name made lowercase.
    curcode = models.CharField(db_column='Curcode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    pfstatus = models.BooleanField(db_column='PFstatus')  # Field name made lowercase.
    psstatus = models.BooleanField(db_column='PSstatus')  # Field name made lowercase.
    uanno = models.CharField(db_column='UANno', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    pfno = models.CharField(db_column='PFno', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    pfdt = models.DateField(db_column='PFdt', blank=True, null=True)  # Field name made lowercase.
    isheepf = models.BooleanField(db_column='IsHeepf')  # Field name made lowercase.
    isherpf = models.BooleanField(db_column='IsHerpf')  # Field name made lowercase.
    esistatus = models.BooleanField(db_column='ESIstatus')  # Field name made lowercase.
    esino = models.CharField(db_column='ESIno', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    esidt = models.DateField(db_column='Esidt', blank=True, null=True)  # Field name made lowercase.
    dispid = models.IntegerField(db_column='DispID', blank=True, null=True)  # Field name made lowercase.
    bankid = models.IntegerField(db_column='BankID', blank=True, null=True)  # Field name made lowercase.
    bankcode = models.CharField(db_column='Bankcode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    branchname = models.CharField(db_column='Branchname', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ifscode = models.CharField(db_column='IFScode', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    bankacno = models.CharField(db_column='Bankacno', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ltamt = models.DecimalField(db_column='LTamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    salamt = models.DecimalField(db_column='Salamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    vpf = models.DecimalField(db_column='VPF', max_digits=18, decimal_places=2)  # Field name made lowercase.
    asalamt = models.DecimalField(db_column='Asalamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    isot = models.BooleanField(db_column='IsOT')  # Field name made lowercase.
    isabry = models.BooleanField(db_column='Isabry')  # Field name made lowercase.
    sallock = models.BooleanField(db_column='Sallock')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.
    eepfcutoff = models.DecimalField(db_column='EEPFcutoff', max_digits=18, decimal_places=2)  # Field name made lowercase.
    erpfcutoff = models.DecimalField(db_column='ERPFcutoff', max_digits=18, decimal_places=2)  # Field name made lowercase.
    erpscutoff = models.DecimalField(db_column='ERPScutoff', max_digits=18, decimal_places=2)  # Field name made lowercase.
    eeesicutoff = models.DecimalField(db_column='EEESIcutoff', max_digits=18, decimal_places=2)  # Field name made lowercase.
    eresicutoff = models.DecimalField(db_column='ERESIcutoff', max_digits=18, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Emp_Salsettings'

class MasPlant(models.Model):
    plantcode = models.CharField(db_column='Plantcode', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    busscode = models.CharField(db_column='Busscode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    plantname = models.CharField(db_column='Plantname', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    plotno = models.CharField(db_column='Plotno', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    streetname = models.CharField(db_column='Streetname', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    townname = models.CharField(db_column='Townname', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    locid = models.IntegerField(db_column='LocID', blank=True, null=True)  # Field name made lowercase.
    locname = models.CharField(db_column='Locname', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    talukname = models.CharField(db_column='Talukname', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    districtname = models.CharField(db_column='Districtname', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    statename = models.CharField(db_column='Statename', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    countryname = models.CharField(db_column='Countryname', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    pincode = models.CharField(db_column='Pincode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    telno = models.CharField(db_column='Telno', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    faxno = models.CharField(db_column='Faxno', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    website = models.CharField(db_column='Website', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    licenseno = models.CharField(db_column='Licenseno', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    licensedt = models.DateField(db_column='Licensedt', blank=True, null=True)  # Field name made lowercase.
    lbtno = models.CharField(db_column='Lbtno', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    lbtdt = models.DateField(db_column='Lbtdt', blank=True, null=True)  # Field name made lowercase.
    cinno = models.CharField(db_column='Cinno', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    gstno = models.CharField(db_column='Gstno', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    texcommno = models.CharField(db_column='Texcommno', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    texcommdt = models.DateField(db_column='Texcommdt', blank=True, null=True)  # Field name made lowercase.
    aepcregno = models.CharField(db_column='Aepcregno', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    aepcregdt = models.DateField(db_column='Aepcregdt', blank=True, null=True)  # Field name made lowercase.
    pfcode = models.CharField(db_column='PFcode', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    esicode = models.CharField(db_column='ESIcode', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    rbicode = models.CharField(db_column='RBIcode', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    adcode = models.CharField(db_column='ADcode', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    iecode = models.CharField(db_column='IEcode', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    iecodedt = models.DateField(db_column='IEcodedt', blank=True, null=True)  # Field name made lowercase.
    panno = models.CharField(db_column='Panno', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    staxno = models.CharField(db_column='Staxno', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    staxdt = models.DateField(db_column='Staxdt', blank=True, null=True)  # Field name made lowercase.
    dcurcode = models.CharField(db_column='Dcurcode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='Isactive')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.
    logo = models.TextField(db_column='Logo', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    idcardtemplate = models.TextField(db_column='IDCardTemplate', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    signature = models.TextField(db_column='Signature', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    natureofbusiness = models.CharField(db_column='Natureofbusiness', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    bussinesslocation = models.CharField(db_column='Bussinesslocation', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    emppath = models.CharField(db_column='Emppath', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Plant'

class MasSaltempdetail(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    saltempid = models.IntegerField(db_column='SaltempID')  # Field name made lowercase.
    salcode = models.CharField(db_column='Salcode', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    saldesc = models.CharField(db_column='Saldesc', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    calcby = models.CharField(db_column='Calcby', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    saltype = models.CharField(db_column='Saltype', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    salper = models.DecimalField(db_column='Salper', max_digits=18, decimal_places=2)  # Field name made lowercase.
    iswo = models.BooleanField(db_column='IsWO')  # Field name made lowercase.
    isbonus = models.BooleanField(db_column='Isbonus')  # Field name made lowercase.
    isnf = models.BooleanField(db_column='IsNF')  # Field name made lowercase.
    isph = models.BooleanField(db_column='IsPH')  # Field name made lowercase.
    isencash = models.BooleanField(db_column='IsEncash')  # Field name made lowercase.
    isgratuity = models.BooleanField(db_column='IsGratuity')  # Field name made lowercase.
    islayoff = models.BooleanField(db_column='IsLayoff')  # Field name made lowercase.
    layoffper = models.DecimalField(db_column='Layoffper', max_digits=18, decimal_places=2)  # Field name made lowercase.
    isot = models.BooleanField(db_column='IsOT')  # Field name made lowercase.
    pfded = models.BooleanField(db_column='PFded')  # Field name made lowercase.
    esided = models.BooleanField(db_column='ESIded')  # Field name made lowercase.
    isproftax = models.BooleanField(db_column='Isproftax')  # Field name made lowercase.
    roff = models.CharField(db_column='Roff', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='Isactive')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.
    isit = models.BooleanField(db_column='IsIT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Saltempdetail'        

class MasDedheads(models.Model):
    dedcode = models.CharField(db_column='Dedcode', primary_key=True, max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    deddesc = models.CharField(db_column='Deddesc', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='Isactive')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Dedheads'

class MasBank(models.Model):
    bankcode = models.CharField(db_column='Bankcode', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    bankname = models.CharField(db_column='Bankname', max_length=75, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='Isactive')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Bank'
        
class MasSmonth(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    mstart = models.DateTimeField(db_column='Mstart')  # Field name made lowercase.
    mend = models.DateTimeField(db_column='Mend')  # Field name made lowercase.
    smonth = models.DateTimeField(db_column='Smonth', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Smonth'

class MasLoan(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    loanname = models.CharField(db_column='Loanname', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='Isactive')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mas_loan'

class EntLoanappl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    loanreqdt = models.DateTimeField(db_column='Loanreqdt')  # Field name made lowercase.
    plantcode = models.CharField(db_column='Plantcode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    empid = models.IntegerField(db_column='EmpID')  # Field name made lowercase.
    loanamt = models.DecimalField(db_column='Loanamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    noofdues = models.IntegerField(db_column='Noofdues')  # Field name made lowercase.
    loanemi = models.DecimalField(db_column='Loanemi', max_digits=18, decimal_places=2)  # Field name made lowercase.
    dedmode = models.CharField(db_column='Dedmode', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    dedstartfrom = models.DateTimeField(db_column='Dedstartfrom')  # Field name made lowercase.
    lnameid = models.ForeignKey(MasLoan,db_column='LnameID',on_delete=models.CASCADE, blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sanctionamt = models.DecimalField(db_column='Sanctionamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    sanctionemi = models.DecimalField(db_column='Sanctionemi', max_digits=18, decimal_places=2)  # Field name made lowercase.
    sanctiondues = models.IntegerField(db_column='Sanctiondues')  # Field name made lowercase.
    intrate = models.DecimalField(db_column='Intrate', max_digits=18, decimal_places=2)  # Field name made lowercase.
    intamt = models.DecimalField(db_column='Intamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    sanctionnetamt = models.DecimalField(db_column='Sanctionnetamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    appstatus = models.CharField(db_column='Appstatus', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ent_Loanappl'


# Create your models here.
class EntMleave(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    smonthid = models.IntegerField(db_column='SmonthID', blank=True, null=True)  # Field name made lowercase.
    smonth = models.DateTimeField(db_column='Smonth', blank=True, null=True)  # Field name made lowercase.
    mstart = models.DateTimeField(db_column='Mstart', blank=True, null=True)  # Field name made lowercase.
    mend = models.DateTimeField(db_column='Mend', blank=True, null=True)  # Field name made lowercase.
    plantcode = models.CharField(db_column='Plantcode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    empid = models.IntegerField(db_column='EmpID', blank=True, null=True)  # Field name made lowercase.
    clop = models.DecimalField(db_column='CLop', max_digits=18, decimal_places=2)  # Field name made lowercase.
    clcr = models.DecimalField(db_column='CLcr', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    clutil = models.DecimalField(db_column='CLutil', max_digits=18, decimal_places=2)  # Field name made lowercase.
    clbal = models.DecimalField(db_column='CLbal', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    elop = models.DecimalField(db_column='ELop', max_digits=18, decimal_places=2)  # Field name made lowercase.
    elcr = models.DecimalField(db_column='ELcr', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    elutil = models.DecimalField(db_column='ELutil', max_digits=18, decimal_places=0)  # Field name made lowercase.
    elbal = models.DecimalField(db_column='ELbal', max_digits=21, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mlop = models.DecimalField(db_column='MLop', max_digits=18, decimal_places=2)  # Field name made lowercase.
    mlcr = models.DecimalField(db_column='MLcr', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mlutil = models.DecimalField(db_column='MLutil', max_digits=18, decimal_places=2)  # Field name made lowercase.
    mlbal = models.DecimalField(db_column='MLbal', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    slop = models.DecimalField(db_column='SLop', max_digits=18, decimal_places=2)  # Field name made lowercase.
    slcr = models.DecimalField(db_column='SLcr', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    slutil = models.DecimalField(db_column='SLutil', max_digits=18, decimal_places=2)  # Field name made lowercase.
    slbal = models.DecimalField(db_column='SLbal', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ent_Mleave'

class MasEmpLeave(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    empid = models.IntegerField(db_column='EmpID')  # Field name made lowercase.
    lyear = models.IntegerField(db_column='Lyear')  # Field name made lowercase.
    lcode = models.CharField(db_column='Lcode', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    lopen = models.DecimalField(db_column='Lopen', max_digits=18, decimal_places=2)  # Field name made lowercase.
    lcredit = models.DecimalField(db_column='Lcredit', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    lutil = models.DecimalField(db_column='Lutil', max_digits=18, decimal_places=2)  # Field name made lowercase.
    lncash = models.DecimalField(db_column='Lncash', max_digits=18, decimal_places=2)  # Field name made lowercase.
    lbal = models.DecimalField(db_column='Lbal', max_digits=21, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    isactive = models.BooleanField(db_column='Isactive')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Emp_Leave'




from django.db import models

class MasExpenses(models.Model):
    expid = models.AutoField(db_column='ExpID', primary_key=True)  # Field name made lowercase.
    expname = models.CharField(db_column='Expname', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='Isactive', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate')  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Expenses'

class EntEmpExpenses(models.Model):
    claimid = models.AutoField(db_column='ClaimID', primary_key=True)  # Field name made lowercase.
    claimdt = models.DateField(db_column='Claimdt')  # Field name made lowercase.
    empid = models.CharField(db_column='EmpID', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    expid = models.ForeignKey(MasExpenses, on_delete=models.CASCADE, db_column='ExpID')
    claimamount = models.DecimalField(db_column='Claimamount', max_digits=10, decimal_places=2)  # Field name made lowercase.       
    documents = models.FileField(upload_to='documents/', blank=True, null=True,validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpeg', 'jpg'])])  # Field name made lowercase.
    description = models.TextField(db_column='Description', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    appstatus = models.CharField(db_column='Appstatus', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    appamount = models.DecimalField(db_column='Appamount', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    remarks = models.TextField(db_column='Remarks', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    paidamount = models.DecimalField(db_column='Paidamount', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updateby = models.CharField(db_column='Updateby', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='Updatedate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ent_Emp_Expenses'


class MasLoan(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    loanname = models.CharField(db_column='Loanname', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='Isactive')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mas_loan'

class EntLoanappl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    loanreqdt = models.DateTimeField(db_column='Loanreqdt')  # Field name made lowercase.
    plantcode = models.CharField(db_column='Plantcode', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    empid = models.IntegerField(db_column='EmpID')  # Field name made lowercase.
    loanamt = models.DecimalField(db_column='Loanamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    noofdues = models.IntegerField(db_column='Noofdues')  # Field name made lowercase.
    loanemi = models.DecimalField(db_column='Loanemi', max_digits=18, decimal_places=2)  # Field name made lowercase.
    dedmode = models.CharField(db_column='Dedmode', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    dedstartfrom = models.DateTimeField(db_column='Dedstartfrom')  # Field name made lowercase.
    lnameid = models.ForeignKey(MasLoan,db_column='LnameID',on_delete=models.CASCADE, blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sanctionamt = models.DecimalField(db_column='Sanctionamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    sanctionemi = models.DecimalField(db_column='Sanctionemi', max_digits=18, decimal_places=2)  # Field name made lowercase.
    sanctiondues = models.IntegerField(db_column='Sanctiondues')  # Field name made lowercase.
    intrate = models.DecimalField(db_column='Intrate', max_digits=18, decimal_places=2)  # Field name made lowercase.
    intamt = models.DecimalField(db_column='Intamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    sanctionnetamt = models.DecimalField(db_column='Sanctionnetamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    appstatus = models.CharField(db_column='Appstatus', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ent_Loanappl'

class EntLoanschedule(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    loanid = models.IntegerField(db_column='LoanID')  # Field name made lowercase.
    plantcode = models.CharField(db_column='Plantcode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    empid = models.IntegerField(db_column='EmpID')  # Field name made lowercase.
    deddt = models.DateField(db_column='Deddt')  # Field name made lowercase.
    dedmode = models.CharField(db_column='Dedmode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    dueamt = models.DecimalField(db_column='Dueamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    rded = models.DecimalField(db_column='Rded', max_digits=18, decimal_places=2)  # Field name made lowercase.
    cash1 = models.DecimalField(db_column='Cash1', max_digits=18, decimal_places=2)  # Field name made lowercase.
    cash2 = models.DecimalField(db_column='Cash2', max_digits=18, decimal_places=2)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ent_Loanschedule'


class EntLoanmas(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    appid = models.IntegerField(db_column='AppID')  # Field name made lowercase.
    plantcode = models.CharField(db_column='Plantcode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    empid = models.IntegerField(db_column='EmpID')  # Field name made lowercase.
    loanno = models.CharField(db_column='Loanno', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    loandt = models.CharField(db_column='Loandt', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    lnameid = models.IntegerField(db_column='LnameID')  # Field name made lowercase.
    loanamt = models.DecimalField(db_column='Loanamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    intrate = models.DecimalField(db_column='Intrate', max_digits=18, decimal_places=2)  # Field name made lowercase.
    loantenure = models.IntegerField(db_column='Loantenure')  # Field name made lowercase.
    loanemi = models.DecimalField(db_column='LoanEMI', max_digits=18, decimal_places=2)  # Field name made lowercase.
    intamt = models.DecimalField(db_column='Intamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    totalamt = models.DecimalField(db_column='Totalamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    dedby = models.CharField(db_column='Dedby', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    recstarton = models.DateField(db_column='Recstarton')  # Field name made lowercase.
    recendon = models.DateField(db_column='Recendon')  # Field name made lowercase.
    recdamt = models.DecimalField(db_column='Recdamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    foreclosureamt = models.DecimalField(db_column='Foreclosureamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    baddebit = models.DecimalField(db_column='Baddebit', max_digits=18, decimal_places=2)  # Field name made lowercase.
    completedon = models.DateField(db_column='Completedon', blank=True, null=True)  # Field name made lowercase.
    balamt = models.DecimalField(db_column='Balamt', max_digits=18, decimal_places=2)  # Field name made lowercase.
    remarks = models.TextField(db_column='Remarks', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    noofdues = models.DecimalField(db_column='Noofdues', max_digits=18, decimal_places=2)  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ent_Loanmas'

class EntEmpLeaveappl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    plantcode = models.CharField(db_column='Plantcode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    empid = models.IntegerField(db_column='EmpID')  # Field name made lowercase.
    lfrom = models.DateTimeField(db_column='LFrom')  # Field name made lowercase.
    lto = models.DateTimeField(db_column='Lto')  # Field name made lowercase.
    fnlcode = models.CharField(db_column='FNLcode', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    anlcode = models.CharField(db_column='ANLcode', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    leavebal = models.DecimalField(db_column='Leavebal', max_digits=18, decimal_places=2)  # Field name made lowercase.
    fromfn = models.BooleanField(db_column='FromFN')  # Field name made lowercase.
    froman = models.BooleanField(db_column='FromAN')  # Field name made lowercase.
    tofn = models.BooleanField(db_column='ToFN')  # Field name made lowercase.
    toan = models.BooleanField(db_column='ToAN')  # Field name made lowercase.
    totldays = models.DecimalField(db_column='Totldays', max_digits=18, decimal_places=2)  # Field name made lowercase.
    appstatus = models.CharField(db_column='Appstatus', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.
    attachment = models.TextField(blank=True, null=True)  # This field type is a guess.
    description = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Ent_Emp_Leaveappl'

class EntEmpLeavedetails(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    laid = models.IntegerField(db_column='LAID')  # Field name made lowercase.
    empid = models.IntegerField(db_column='EmpID')  # Field name made lowercase.
    plantcode = models.CharField(db_column='Plantcode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    ldate = models.DateTimeField(db_column='Ldate')  # Field name made lowercase.
    fnlcode = models.CharField(db_column='FNLcode', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    anlcode = models.CharField(db_column='ANLcode', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    fn = models.BooleanField(db_column='FN')  # Field name made lowercase.
    an = models.BooleanField(db_column='AN')  # Field name made lowercase.
    appstatus = models.TextField(db_column='Appstatus', db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ent_Emp_Leavedetails'

class CustomDateTimeField(models.DateTimeField):
    def db_type(self, connection):
        return 'DATETIME'    
    
class MasEmpOfficial(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    empno = models.CharField(db_column='Empno', max_length=12, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    emptitle = models.CharField(db_column='Emptitle', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    empname = models.CharField(db_column='Empname', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    empphoto = models.TextField(db_column='Empphoto', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    biorefno = models.CharField(db_column='Biorefno', max_length=12, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    punchstatus = models.CharField(db_column='Punchstatus', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fhflag = models.CharField(db_column='FHflag', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    fhname = models.CharField(db_column='FHname', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    busscode = models.CharField(db_column='Busscode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    plantcode = models.CharField(db_column='Plantcode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    applno = models.CharField(db_column='ApplNo', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    appldt = models.DateTimeField(db_column='Appldt', blank=True, null=True)  # Field name made lowercase.
    dob = models.DateTimeField(db_column='Dob')  # Field name made lowercase.
    ageondoj = models.CharField(db_column='Ageondoj', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    capacityid = models.IntegerField(db_column='CapacityID', blank=True, null=True)  # Field name made lowercase.
    deptid = models.IntegerField(db_column='DeptID')  # Field name made lowercase.
    subdeptid = models.IntegerField(db_column='SubdeptID')  # Field name made lowercase.
    desigid = models.IntegerField(db_column='DesigID')  # Field name made lowercase.
    reportsto = models.IntegerField(db_column='Reportsto', blank=True, null=True)  # Field name made lowercase.
    gradeid = models.IntegerField(db_column='GradeID')  # Field name made lowercase.
    sectionid = models.IntegerField(db_column='SectionID')  # Field name made lowercase.
    wrkdivid = models.IntegerField(db_column='WrkdivID')  # Field name made lowercase.
    isoperator = models.BooleanField(db_column='Isoperator')  # Field name made lowercase.
    empcatgid = models.IntegerField(db_column='EmpcatgID')  # Field name made lowercase.
    empsubcatgid = models.IntegerField(db_column='EmpsubcatgID')  # Field name made lowercase.
    f11grpid = models.IntegerField(db_column='F11grpID')  # Field name made lowercase.
    skillid = models.IntegerField(db_column='SkillID')  # Field name made lowercase.
    doj = models.DateTimeField(db_column='Doj')  # Field name made lowercase.
    dol = models.DateTimeField(db_column='Dol', blank=True, null=True)  # Field name made lowercase.
    empstatus = models.CharField(db_column='Empstatus', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    dop = models.DateTimeField(db_column='Dop', blank=True, null=True)  # Field name made lowercase.
    doc = models.DateTimeField(db_column='Doc', blank=True, null=True)  # Field name made lowercase.
    d480 = models.DateTimeField(db_column='D480', blank=True, null=True)  # Field name made lowercase.
    delayconfirm = models.CharField(db_column='Delayconfirm', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    aadhaarno = models.CharField(db_column='Aadhaarno', max_length=16, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    omail = models.CharField(db_column='Omail', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    omobile = models.CharField(db_column='Omobile', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    weekoff = models.CharField(db_column='Weekoff', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    shiftcode = models.CharField(db_column='Shiftcode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    srgrpid = models.IntegerField(db_column='SRgrpID')  # Field name made lowercase.
    asrgrpid = models.IntegerField(db_column='ASRgrpID', blank=True, null=True)  # Field name made lowercase.
    auditstatus = models.BooleanField(db_column='Auditstatus')  # Field name made lowercase.
    isphychalange = models.BooleanField(db_column='Isphychalange')  # Field name made lowercase.
    isadolescent = models.BooleanField(db_column='Isadolescent')  # Field name made lowercase.
    isiw = models.BooleanField(db_column='IsIW')  # Field name made lowercase.
    ismigrant = models.BooleanField(db_column='Ismigrant')  # Field name made lowercase.
    lstatus = models.BooleanField(db_column='Lstatus')  # Field name made lowercase.
    lreasonactid = models.IntegerField(db_column='LreasonactID', blank=True, null=True)  # Field name made lowercase.
    lreasonstatid = models.IntegerField(db_column='LreasonstatID', blank=True, null=True)  # Field name made lowercase.
    approvalstatus = models.CharField(db_column='Approvalstatus', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    salaryfix = models.BooleanField(db_column='Salaryfix')  # Field name made lowercase.
    asalaryfix = models.BooleanField(db_column='Asalaryfix')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.
    orefno = models.CharField(db_column='Orefno', max_length=12, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    adoj = models.DateTimeField(db_column='Adoj', blank=True, null=True)  # Field name made lowercase.
    paddrid = models.IntegerField(db_column='PaddrID', blank=True, null=True)  # Field name made lowercase.
    caddrid = models.IntegerField(db_column='CaddrID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Emp_Official'


class Temp_Attn(models.Model):
    EmpID = models.ForeignKey(MasEmpOfficial, on_delete=models.CASCADE, related_name="attendances",db_column="EmpID" )  
    Biorefno = models.CharField(max_length=12, null=True, blank=True)
    Plantcode = models.CharField(max_length=10, null=True, blank=True)
    Attndt = models.DateTimeField()
    Shiftcode = models.CharField(max_length=5)
    Earlystart = models.DateTimeField(null=True, blank=True)
    Shiftstart = models.DateTimeField(null=True, blank=True)
    Chkin = models.DateTimeField(null=True, blank=True)
    Attn = models.CharField(max_length=5, default='AB')
    La = models.IntegerField(default=0)
    Lastout = models.DateTimeField(null=True, blank=True)
    Logcount = models.IntegerField(default=0)
    Logstime = models.CharField(max_length=100, null=True)
    Status = models.CharField(max_length=3, default='AB')
    Shiftend = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.EmpID.Empname} ({self.EmpID.Empno})"
    
    
class MasEmprange(models.Model):
    id = models.ForeignKey(MasEmpOfficial, on_delete=models.CASCADE,db_column='ID', primary_key=True)  # Field name made lowercase.
    age = models.IntegerField(db_column='Age')  # Field name made lowercase.
    slength = models.IntegerField(db_column='Slength')  # Field name made lowercase.
    salary = models.DecimalField(db_column='Salary', max_digits=18, decimal_places=2)  # Field name made lowercase.
    agerange = models.CharField(db_column='Agerange', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    servicerange = models.CharField(db_column='Servicerange', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    salrange = models.CharField(db_column='Salrange', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    lastpresent = models.DateTimeField(db_column='Lastpresent', blank=True, null=True)  # Field name made lowercase.
    leavedays = models.IntegerField(db_column='Leavedays')  # Field name made lowercase.
    leaverange = models.CharField(db_column='Leaverange', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Emprange'
  
class MasDept(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='Deptname', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='Isactive')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Dept'

class MasDesignation(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    designame = models.CharField(db_column='Designame', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='Isactive')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Designation'

class MasSubdept(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    subdeptname = models.CharField(db_column='Subdeptname', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='Isactive')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Subdept'

class MasPlantcapacity(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    plantcode = models.CharField(db_column='Plantcode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    deptid = models.IntegerField(db_column='DeptID')  # Field name made lowercase.
    sdeptid = models.IntegerField(db_column='SdeptID')  # Field name made lowercase.
    desigid = models.IntegerField(db_column='DesigID')  # Field name made lowercase.
    isoperator = models.BooleanField(db_column='Isoperator')  # Field name made lowercase.
    manreq = models.IntegerField(db_column='Manreq')  # Field name made lowercase.
    allowper = models.DecimalField(db_column='Allowper', max_digits=18, decimal_places=2)  # Field name made lowercase.
    abreq = models.IntegerField(db_column='Abreq')  # Field name made lowercase.
    totreq = models.IntegerField(db_column='Totreq')  # Field name made lowercase.
    minwage = models.DecimalField(db_column='Minwage', max_digits=18, decimal_places=2)  # Field name made lowercase.
    maxwage = models.DecimalField(db_column='Maxwage', max_digits=18, decimal_places=2)  # Field name made lowercase.
    tallow = models.DecimalField(db_column='Tallow', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    attnincid = models.IntegerField(db_column='AttnincID', blank=True, null=True)  # Field name made lowercase.
    islaed = models.BooleanField(db_column='IsLaed', blank=True, null=True)  # Field name made lowercase.
    isactive = models.BooleanField(db_column='Isactive')  # Field name made lowercase.
    createdby = models.CharField(db_column='Createdby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='Createddate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='Updatedby', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='Updateddate', blank=True, null=True)  # Field name made lowercase.
    empcatgid = models.IntegerField(db_column='EmpcatgID', blank=True, null=True)  # Field name made lowercase.
    saltempid = models.IntegerField(db_column='SaltempID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mas_Plantcapacity'        