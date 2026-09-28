from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('', views.semester_list_view, name='semester_list'),
    path('semester/<int:semester_id>/', views.semester_detail_view, name='semester_detail'),
    path('semester/<int:semester_id>/course/<int:course_id>/', views.course_detail_view, name='course_detail'),
    path('subject/<int:subject_id>/', views.subject_detail_view, name='subject_detail'),
    path('subject/<int:subject_id>/slides/', views.slides_view, name='slides'),
    path('download/<int:link_id>/', views.download_view, name='download'),
    path('coming-soon/', views.coming_soon_view, name='coming_soon'),
]