from django.urls import path
from . import views

app_name = 'mocktests'

urlpatterns = [
    path('mock_tests/', views.mocktest_view, name='mock_tests'),
    path('test_selection/', views.test_selection_view, name='test_selection'),
    path('take_test/<int:test_id>/', views.take_test_view, name='take_test'),
    path('submit_test/', views.submit_test_view, name='submit_test'),

    # Analysis
    path('analysis/<int:attempt_id>/', views.test_analysis_view, name='test_analysis'),
    path('analysis/<int:attempt_id>/questions/', views.test_questions_view, name='test_questions'),
    path('analysis/<int:attempt_id>/leaderboard/', views.test_leaderboard_view, name='test_leaderboard'),

    # Past attempts history
    path('history/', views.attempt_history_view, name='attempt_history'),
]