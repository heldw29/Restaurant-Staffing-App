from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Location(models.Model):
    address = models.CharField(max_length=200)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.restaurant.name + ", " + self.address


class JobPosting(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    #def get_absolute_url(self):
    #    return reverse('staffing:job-detail', kwargs={'pk': self.pk})



class JobApplication(models.Model):
    APPLICATION_STATUS = (
        ('A', 'Accepted'),
        ('R', 'Rejected'),
        ('P', 'In Progress'),
    )
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=12)
    email = models.CharField(max_length=200)
    resume = models.TextField()
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, default='P', choices=APPLICATION_STATUS)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.job_posting}'





#users
