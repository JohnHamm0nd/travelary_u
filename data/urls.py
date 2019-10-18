from django.urls import path
from . import views


app_name="data"

urlpatterns = [
    path('',views.DataList.as_view(),name='list'),
    path('<int:pk>/', views.DataDetail.as_view(), name='detail'),
    path('<int:data_id>/reviewcreate/<int:user_id>', views.ReviewCreate.as_view(), name='reviewcreate'),
    path('reviewlist', views.ReviewList.as_view(), name='reviewlist')
]


