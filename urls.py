from django.urls import path
from . import views

urlpatterns = [
    path("input", views.input, name="input"),
    path("analysis_data", views.anlys_data, name="analysis_data"),
    path("analysis_chart", views.anlys_chr, name="analysis_chart"),
]