from django.urls import path
from . import views

urlpatterns = [
    path('',views.ehome,name="ehome"),
    path('esslogin/', views.login_view, name='login'),
    path("signup/", views.signup, name="signup"),
    path('logout/', views.logout_view, name='logout'),
    path('profile/',views.profile,name="profile"),
    path('attendance/',views.attendance,name="attendance"),
    path('documents/',views.documents,name="documents"),
    path("edit_document/<int:doc_id>/", views.edit_document, name="edit_document"),
    path('upload_document/',views.upload_document,name ="upload_document"),
    path('delete_document/<int:doc_id>/', views.delete_document, name='delete_document'),
    path('payroll/',views.payroll,name="payroll"),
    path('testdown/', views.testdown, name='testdown'),
    path('testpreview/',views.testpreview,name='testpreview'),
   # ___
    path('claims/',views.claims,name="claims"),
    path('loans/',views.loans,name="loans"),
    path('requeststatus/',views.requeststatus,name="requeststatus"),

    path('leave-management/', views.leave_management, name='leavemanagement'),
    path('apply-newleave/', views.apply_newleave, name='apply_newleave'),
    path('get-leave-details/<int:leave_id>/', views.get_leave_details, name='get_leave_details'), 
    path('api/update-leave/<int:leave_id>/', views.update_leave, name='update_leave'),
    path('delete-leave/<int:leave_id>/', views.delete_leave, name='delete_leave'),
    
    # ------------------------------------------------------------------------
    path('loan/',views.loanapplication,name="loanapplications"),
     path("loan-details/<int:loan_id>/", views.loan_details, name="loan_details"),
    path('apply-newloan/', views.applynewloan, name='apply_newloan'),
    path("delete-loan/<int:loan_id>/", views.delete_loan, name="delete_loan"),
    path('get-loan-details/<int:loan_id>/', views.get_loan_details, name='get-loan-details'),
    path('api/update-loan/<int:loan_id>/', views.update_loan, name='update_loan'),
  
]
