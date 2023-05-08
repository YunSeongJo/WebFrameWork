from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('list/',views.StaffList.as_view()),
    path('list/<int:pk>/',views.StaffCard.as_view()),
    path('list/<int:pk>/alter/',views.StaffCard2.as_view()),
    # path("list/", StaffList.as_view(), name="staff_list"),
    # path("<int:pk>/after/", StaffDetail.as_view(), name="after"),   
]
