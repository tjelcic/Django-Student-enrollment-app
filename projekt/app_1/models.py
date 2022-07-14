from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Korisnik(AbstractUser):
    ADMIN = 'ADMIN'
    PROFESOR = 'PROFESOR'
    STUDENT = 'STUDENT'
    ROLES = (
        (ADMIN, 'Admin'),
        (PROFESOR,'Profesor'), 
        (STUDENT,'Student'),
    )

    NONE = 'NONE'
    REDOVNI = 'REDOVNI'
    IZVANREDNI = 'IZVANREDNI'
    STATUS = (
        (NONE,'None'),
        (REDOVNI, 'Redovni'),
        (IZVANREDNI, 'Izvanredni'),
    )
    role = models.CharField(max_length=16, choices=ROLES, default=STUDENT)
    status = models.CharField(max_length=20, choices=STATUS, default=NONE)


    def __str__(self):
        return ('%s %s') % (self.first_name, self.last_name)


class Predmeti(models.Model):
    IZBORNI = (('DA', 'da'), ('NE', 'ne'))
    name = models.CharField(max_length=255)
    kod = models.CharField(max_length=16)
    program = models.TextField(max_length=50,null=False)
    ects = models.PositiveIntegerField(null=False)
    sem_red = models.PositiveIntegerField(null=False)
    sem_izv = models.PositiveIntegerField(null=False)
    izborni = models.CharField(max_length=50, choices=IZBORNI)
    nositelj = models.ForeignKey(Korisnik, limit_choices_to={'role':'PROFESOR'}, on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return self.name

class Upisi(models.Model):
    student_id = models.ForeignKey(Korisnik, on_delete=models.CASCADE)
    predmet_id = models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    status = models.CharField(max_length=64)

    def __str__(self):
        return self.status