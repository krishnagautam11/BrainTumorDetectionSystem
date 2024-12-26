from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/',views.about,name='about'), 
    path('Admin_login/',views.Admin_login,name='Admin_login'), 
    path('User_login/',views.User_login,name='User_login'), 
    path('Register/',views.Register,name='Register'),  
    path('logout/',views.logout,name='logout'), 
    path('ChangePassword/',views.ChangePassword,name='ChangePassword'), 

    path('Analyze/', views.Analyze, name='Analyze'),
    path('AddDoctor/', views.AddDoctor, name='AddDoctor'),
    path('ViewDoctor/', views.ViewDoctor, name='ViewDoctor'),
    path('WriteFeedback/', views.WriteFeedback, name='WriteFeedback'),
    path('ViewFeedback/', views.ViewFeedback, name='ViewFeedback'),
    path('ViewUser/', views.ViewUser, name='ViewUser'),
    path('AddTrainingData/', views.AddTrainingData, name='AddTrainingData'),
    path('get_response/', views.get_response, name='get_response'),
 
]

