from django.urls import path
from . import views


app_name="data"

urlpatterns = [
    path('',views.DataList.as_view(),name='list'),
    path('<int:pk>/', views.DataDetail.as_view(), name='detail'),
    path('<int:data_id>/reviewcreate/<int:user_id>', views.ReviewCreate.as_view(), name='reviewcreate'),
    path('<int:data_id>/reviewupdate/<int:user_id>/<int:pk>', views.ReviewUpdate.as_view(), name='reviewupdate'),
    path('<int:data_id>/reviewdelete/<int:user_id>/<int:pk>', views.ReviewDelete.as_view(), name='reviewdelete'),
    path('reviewlist', views.ReviewList.as_view(), name='reviewlist')
]


