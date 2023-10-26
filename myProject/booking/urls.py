from django.urls import path 
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.booking, name='booking'),
    path('booking-submit', views.bookingSubmit, name='bookingSubmit'),
    path('user-panel', views.userPanel, name='userPanel'),
    path('user-update/<int:id>', views.userUpdate, name='userUpdate'),
    path('user-update-submit/<int:id>', views.userUpdateSubmit, name='userUpdateSubmit'),
    # path('staff-panel', views.staffPanel, name='staffPanel'),
    path('become-vendor', views.become_vendor, name='become-vendor'),
    path('submit-staff-data/', views.submit_staff_data, name='submit_staff_data'),
    path('dashboard-panel', views.vendor_dashboard, name='vendorUpdate'),
    #logout
    path('logout-view', views.logout_view, name='logout-view'),









]