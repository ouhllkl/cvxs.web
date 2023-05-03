
from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('<int:university_id>/', view_university, name='view_university'),
    path('all/', view_universities, name='view_universities'),
    path('add/', add_university, name='add_university'),
    path('<int:university_id>/edit/', edit_university, name='edit_university'),
    

    path('scholarship/<int:scholarship_id>/', view_scholarship, name='view_scholarship'),
    path('<int:university_id>/scholarship/add/', add_scholarship, name='add_scholarship'),
    path('scholarship/<int:scholarship_id>/edit', edit_scholarship, name='edit_scholarship'),



    path('scholarship/<int:scholarship_id>/add_session/', add_scholarship_session, name='add_scholarship_session'),
    path('scholarship_session/<int:session_id>/edit/', edit_scholarship_session, name='edit_scholarship_session'),
    #edit_scholarship_session


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

