from django.urls import path 
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('booking', views.booking, name='booking'),
    path('login-provider', views.login_view, name='login-provider'),


    path('booking-submit', views.bookingSubmit, name='bookingSubmit'),
    path('', views.userPanel, name='userPanel'),
    path('appointment-delete/<int:id>', views.appointmentDelete, name='appointmentDelete'),
    path('appointment-delete-booking/<int:id>', views.appointmentDeleteBooking, name='appointmentDeleteBooking'),

    path('appointment-finished/<int:id>', views.appointmentFinished, name='appointmentFinished'),
    path('inquiry-delete/<int:id>', views.inquiryDelete, name='inquiryDelete'),

    path('inquiry-submit', views.inquirySubmit, name='inquirySubmit'),
    


    path('user-update/<int:id>', views.userUpdate, name='userUpdate'),
    path('user-update-submit/<int:id>', views.userUpdateSubmit, name='userUpdateSubmit'),
    # path('staff-panel', views.staffPanel, name='staffPanel'),
    path('become-vendor', views.become_vendor, name='become-vendor'),
    path('submit-staff-data/', views.submit_staff_data, name='submit_staff_data'),
    path('dashboard-panel', views.vendor_dashboard, name='dashboard-panel'),



    #logout
    path('logout-view', views.logout_view, name='logout-view'),









]