from django.urls import path
from .views import JobPostingCreateView, JobPostingDetailView, JobPostingUpdateView, \
    JobApplicationCreateView, LocationCreateView, LocationUpdateView, LocationDetailView, \
    LocationDeleteView, JobPostingDeleteView, JobApplicationListView, JobApplicationDetailView, JobApplicationUpdateView
from . import views

app_name = 'staffing'
urlpatterns = [
    # home page
    path('', views.home, name='home'),

    # Location URLS
    path('staffing/location/<int:pk>/', LocationDetailView.as_view(), name='location-detail'),
    path('staffing/create_location/', LocationCreateView.as_view(), name='locations-create'),
    path('staffing/update_location/<int:pk>/', LocationUpdateView.as_view(), name='locations-update'),
    path('staffing/location/<int:pk>/delete/', LocationDeleteView.as_view(), name='location-delete'),

    # JobPosting URLS
    path('staffing/new_job/', JobPostingCreateView.as_view(), name='job-create'),
    path('staffing/<int:pk>/', JobPostingDetailView.as_view(), name='job-detail'),
    path('staffing/<int:pk>/update_job/', JobPostingUpdateView.as_view(), name='job-update'),
    path('staffing/<int:pk>/delete/', JobPostingDeleteView.as_view(), name='job-delete'),

    # JobApplication URLS
    path('staffing/applications/<int:pk>/', JobApplicationListView.as_view(), name='job-applications'),
    path('staffing/applications/read/<int:pk>/', JobApplicationDetailView.as_view(), name='job-application-read'),
    path('staffing/applications/update/<int:pk>/', JobApplicationUpdateView.as_view(), name='job-application-update'),
    path('<int:restaurant_id>/jobs/<int:job_posting_id>/apply', JobApplicationCreateView.as_view(), name='job-application'),
]
