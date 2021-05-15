from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class BlogUser(AbstractUser):
    YEAR_CHOICE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )

    SEM_CHOICE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
    )

    GENDER_CHOICE = (
        ('male', 'male'),
        ('female', 'female'),
    )

    mobile_no = models.CharField(max_length=20)
    en_no = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to="media/%y")
    year = models.CharField(
        choices=YEAR_CHOICE, max_length=50, blank=True, null=True)
    sem = models.CharField(
        choices=SEM_CHOICE, max_length=50, blank=True, null=True)
    gender = models.CharField(
        choices=GENDER_CHOICE, max_length=50, blank=True, null=True)
