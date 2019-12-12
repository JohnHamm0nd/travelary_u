from django.urls import path
from . import views
app_name='user_profile'
urlpatterns = [
    path('',views.ProfileList.as_view(),name='base'),
    path('create/',views.ProfileCreate.as_view(),name='create'),
    path('update/<int:pk>',views.ProfileUpdate.as_view(),name='update'),
    path('delete/<int:pk>',views.ProfileDelete.as_view(),name='delete'),
]
