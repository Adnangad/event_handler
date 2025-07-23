from django.db import models

# Create your models here.    

class User(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'Admin', 'ADMIN'
        NORMAL = 'Normal', 'NORMAL'
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.TextField()
    role = models.CharField(choices=Role.choices, default=Role.NORMAL)


class TimeTable(models.Model):
    class Days(models.TextChoices):
        SUN = 'SUNDAY', 'SUN', 'Sunday'
        MON = 'MONDAY', 'MON', 'Monday'
        TUE = 'TUESDAY', 'TUE', 'Tuesday'
        WED = 'WEDNESDAY', 'WED', 'Wednesday'
        THU = 'THURSDAY', 'THU', 'Thursday'
        FRI = 'FRIDAY', 'FRI', 'Friday'
        SAT = 'SATURDAY', 'SAT', 'Saturday'
    name = models.CharField()
    createdAt = models.DateTimeField(auto_created=True)
    dueDate = models.DateField()
    startTime = models.TimeField(null=True)
    endTime = models.TimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.TextField()
