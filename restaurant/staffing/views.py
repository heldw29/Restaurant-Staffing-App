from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from restaurant import settings
from .models import Location, JobPosting, JobApplication
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail


class JobPostingDetailView(DetailView):
    model = JobPosting


class JobPostingCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = JobPosting
    fields = ['location', 'title', 'description']
    success_url = '/'

    # overriding the get_form method so restaurant admins can only create jobs at their restaurant locations
    def get_form(self, *args, **kwargs):
        form = super(JobPostingCreateView, self).get_form(*args, **kwargs)
        form.fields['location'].queryset = Location.objects.filter(restaurant=self.request.user.profile.restaurant)
        return form

    # Permission check, to only allow restaurant admins to create job posts
    def test_func(self):
        if self.request.user.profile.restaurant:
            return True
        else:
            return False


class JobPostingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JobPosting
    fields = ['title', 'description', 'location']
    success_url = '/'

    # overriding the get_form method so restaurant admins can only update jobs to their restaurant locations
    def get_form(self, *args, **kwargs):
        form = super(JobPostingUpdateView, self).get_form(*args, **kwargs)
        form.fields['location'].queryset = Location.objects.filter(restaurant=self.request.user.profile.restaurant)
        return form

    def test_func(self):
        job_posting = self.get_object()
        # if the user is a restaurant admin for this job posting's restaurant then return true
        if self.request.user.profile.restaurant == job_posting.location.restaurant:
            return True
        else:
            return False


class JobPostingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = JobPosting
    success_url = '/'

    def test_func(self):
        job_posting = self.get_object()
        # if the user is a restaurant admin for this job posting's restaurant then return true
        if self.request.user.profile.restaurant == job_posting.location.restaurant:
            return True
        else:
            return False


class JobApplicationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = JobApplication

    def test_func(self):
        # if the user is a hiring manager then let them access the job applications for their location
        job_postings = JobPosting.objects.filter(location=self.request.user.profile.location)
        allowed_ids = set()

        for job in job_postings:
            allowed_ids.add(job.id)

        if self.request.user.profile.location and self.kwargs['pk'] in allowed_ids:
            return True
        else:
            return False

    def get_queryset(self):
        # need to get only the job applications that are associated with the requested job and the hiring managers location
        queryset = JobApplication.objects.filter(job_posting=self.kwargs['pk'])
        return queryset


class JobApplicationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = JobApplication

    def test_func(self):
        # check if the user is a hiring manager for this job application
        job_postings = JobPosting.objects.filter(location=self.request.user.profile.location)

        # get the job application, back track to job post and check if it matches with this hiring manager
        for job_post in job_postings:
            if JobApplication.objects.filter(pk=self.kwargs['pk'], job_posting=job_post):
                return True
            else:
                return False


class JobApplicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JobApplication
    fields = ['status']
    success_url = '/'

    # Email the job applicant when the hiring manager updates a job application to 'A' for Accept or 'R' for reject.
    def form_valid(self, form):

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [form.instance.email, ]
        if form.instance.status == 'A':
            subject = f'Welcome to {form.instance.job_posting.location}!'
            message = f'Dear {form.instance.first_name} {form.instance.last_name},' \
                      f' we would like to formally extend you a job offer for the {form.instance.job_posting} position' \
                      f' at {form.instance.job_posting.location}!'
            send_mail(subject, message, email_from, recipient_list)

        elif form.instance.status == 'R':
            subject = f' Your {form.instance.job_posting} Application'
            message = f'Dear {form.instance.first_name} {form.instance.last_name},' \
                      f' we regret to inform you that you have not been select for the {form.instance.job_posting} position' \
                      f' at {form.instance.job_posting.location}.'
            send_mail(subject, message, email_from, recipient_list)

        return super(JobApplicationUpdateView, self).form_valid(form)

    def test_func(self):
        # check if the user is a hiring manager for this job application
        job_postings = JobPosting.objects.filter(location=self.request.user.profile.location)

        # get the job application, back track to job post and check if it matches with this hiring manager
        for job_post in job_postings:
            if JobApplication.objects.filter(pk=self.kwargs['pk'], job_posting=job_post):
                return True
            else:
                return False


class JobApplicationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = JobApplication
    fields = ['first_name', 'last_name', 'address', 'phone_number', 'email', 'resume']
    success_url = '/'

    def get_initial(self):
        return {'email': self.request.user.email}

    def test_func(self):
        # 403 Forbid users to apply to the same job more than once
        job_application = JobApplication.objects.filter(job_posting=self.kwargs['job_posting_id'],
                                                        applicant=self.request.user)
        if not job_application:
            return True
        else:
            return False

    def form_valid(self, form):
        form.instance.job_posting_id = self.kwargs['job_posting_id']
        form.instance.applicant = self.request.user
        messages.success(self.request,
                         f'Congrats, {self.request.user}! You have successfully submitted your job application!')
        return super(JobApplicationCreateView, self).form_valid(form)


class LocationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Location

    # Getting the list of all job postings that are from the requested location
    def get_context_data(self, *args, **kwargs):
        print(self.kwargs['pk'])
        context = super(LocationDetailView, self).get_context_data(*args, **kwargs)
        context['job_posting_list'] = JobPosting.objects.filter(location_id=self.kwargs['pk'])
        return context

    # Allow Restaurant admins to access only their locations
    def test_func(self):
        my_restaurant = self.request.user.profile.restaurant
        location = self.get_object()

        if location.restaurant == my_restaurant:
            return True
        else:
            return False


class LocationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Location
    fields = ['address']
    success_url = '/'

    def test_func(self):
        if self.request.user.profile.restaurant:
            return True
        else:
            return False

    def form_valid(self, form):
        messages.success(self.request,
                         f'Congrats, {self.request.user}! You have successfully created a new {self.request.user.profile.restaurant} location!')
        form.instance.restaurant = self.request.user.profile.restaurant
        return super(LocationCreateView, self).form_valid(form)


class LocationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Location
    fields = ['address']
    success_url = '/'

    def test_func(self):
        location = self.get_object()
        # if the user is a restaurant admin, then let them access their location update form page
        if self.request.user.profile.restaurant == location.restaurant:
            return True
        else:
            return False


class LocationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Location
    success_url = '/'

    def test_func(self):
        location = self.get_object()
        # if the user is a restaurant admin, then let them delete the requested location its their restaurant
        if self.request.user.profile.restaurant == location.restaurant:
            return True
        else:
            return False


def home(request):
    location_list = Location.objects.all()
    job_posting_list = JobPosting.objects.all()

    if request.user.is_anonymous:
        return render(request, 'staffing/home.html',
                      {'location_list': location_list, 'job_posting_list': job_posting_list})

    # The user is a restaurant admin
    elif request.user.profile.restaurant:
        return render(request, 'staffing/location_list.html', {'object_list': location_list})

    # The user is a hiring manager so direct to the job posting list page
    elif request.user.profile.location:
        return render(request, 'staffing/jobPosting_list.html', {'object_list': job_posting_list})
    else:
        return render(request, 'staffing/home.html',
                      {'location_list': location_list, 'job_posting_list': job_posting_list})
