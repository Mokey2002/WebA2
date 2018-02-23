from django.urls import path
from . import views

urlpatterns = [ path('', views.HomePageView, name='home'),
                path('Barcode-detector/', views.Barcode, name='barcode'),
                path('login/',views.Login, name = 'login'),
                path('Employee/', views.EmployeeHome, name='employee'),
                path('logout/', views.Logout, name = 'logout'),
                path('Delete/', views.DeleteData, name = 'delete'),
                path('Process/', views.BarcodeProcess , name = 'BarcodeProcess'),
]

