from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
app_name = 'timetable'

urlpatterns = [
    path('', views.Timetable_Base.as_view(), name='base'),
    path('list/', views.Timetable_List.as_view(), name='list'),
    path('<int:pk>/wish/', views.wish , name='wish'),
    

]

