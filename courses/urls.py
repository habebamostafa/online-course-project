from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Course URLs
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    
    # Assessment URLs
    path('course/<int:course_id>/exam/', views.exam_form, name='exam_form'),
    path('course/<int:course_id>/submit/', views.submit_exam, name='submit_exam'),
    path('result/<int:submission_id>/', views.show_exam_result, name='show_exam_result'),
    
    # Lesson URLs (if needed)
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
]