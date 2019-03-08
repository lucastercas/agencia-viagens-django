from django.urls import path
from . import views

app_name = "tours"
urlpatterns = [
    path('', views.ShowTours.as_view(), name='tours'),
    path('create_tour', views.TourCreate.as_view(), name='create_tour'),
    path('<int:pk>/', views.TourDetail.as_view(), name='tour'),
    path('<int:pk>/reserve', views.make_reserve, name='reserve'),
    path('<int:pk>/delete', views.TourDelete.as_view(), name='delete'),
    path('<int:pk>/edit', views.TourEdit.as_view(), name='edit')
]
