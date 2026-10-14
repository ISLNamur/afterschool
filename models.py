# This file is part of HappySchool.
#
# HappySchool is the legal property of its developers, whose names
# can be found in the AUTHORS file distributed with this source
# distribution.
#
# HappySchool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HappySchool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with HappySchool.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from core.models import TeachingModel, StudentModel


class AfterschoolSettingsModel(models.Model):
    teachings = models.ManyToManyField(TeachingModel, default=None)
    show_by_teaching = models.BooleanField(default=False)
    email_subscription_warning = models.CharField(
        max_length=500,
        help_text="Semi-colon separated values",
        blank=True,
    )


class ActivityModel(models.Model):
    name = models.CharField(max_length=200)
    animator = models.CharField(max_length=200, blank=True)
    age = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=5000, blank=True)
    day = models.PositiveSmallIntegerField()
    no_subscription = models.BooleanField(default=False)
    is_full = models.BooleanField(default=False)
    teaching = models.ForeignKey(TeachingModel, on_delete=models.CASCADE)
    priority = models.PositiveSmallIntegerField(default=0)
    timerange = models.CharField(max_length=100, blank=True)
    date_start = models.DateField()
    date_stop = models.DateField()
    next_week_sub = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.age}"


class ActivitySubscriptionModel(models.Model):
    PAYEMENT_CHOICES = [
        ("1x", "Je paie en 1 fois, en septembre"),
        ("2x", "Je paie en 2 fois, la moitié maintenant et le solde en janvier"),
    ]

    activity = models.ForeignKey(ActivityModel, on_delete=models.CASCADE)
    student_firstname = models.CharField(max_length=200)
    student_lastname = models.CharField(max_length=200)
    classe = models.CharField(max_length=200)
    birth = models.DateField("birth")
    family = models.CharField(max_length=200, blank=True)
    resp_firstname = models.CharField(max_length=200)
    resp_lastname = models.CharField(max_length=200)
    resp_address = models.CharField(max_length=400, blank=True)
    resp_email = models.EmailField()
    resp_email_2 = models.EmailField(null=True, blank=True)
    resp_phone = models.CharField(max_length=200)
    resp_phone_2 = models.CharField(max_length=200, blank=True)
    resp_payement = models.CharField(
        max_length=20, choices=PAYEMENT_CHOICES, default="1x"
    )
    datetime_inscription = models.DateTimeField("Creation date", auto_now_add=True)
    answered = models.BooleanField(default=False)
    payed = models.BooleanField(default=False)
    student = models.ForeignKey(
        StudentModel, default=None, blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.student_firstname} {self.student_lastname}"
