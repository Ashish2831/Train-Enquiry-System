from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home, name='Home' ),
  path('contact/', views.Contact, name='Contact'),
  path('enquiry/', views.Enquiry, name='Enquiry'),
  path('status/', views.Status, name='Status'),
  path('pnrcheck/', views.PnrCheck, name='PnrCheck'),
  path('login/', views.Login, name='Login'),
  path('register/', views.Register, name='Register'),
  path('logout/', views.Logout, name='Logout'),
]
