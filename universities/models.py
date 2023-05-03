from django.db import models

from django.contrib.auth.models import User



class University(models.Model):
    name            = models.CharField(max_length=100)
    city            = models.CharField(max_length=100)
    website         = models.URLField(default='https://www.youtube.com/')
    programmes_page = models.URLField(default='https://www.youtube.com/')
    

    def __str__(self):
        return f'{self.name} ({self.city})'



class Scholarship(models.Model):
    name            = models.CharField(max_length=100)
    university      = models.ForeignKey(University, on_delete=models.CASCADE)
    about           = models.TextField()
    support_contacts       = models.TextField()

    
    def __str__(self):
        return self.name



class ScholarshipSession(models.Model):
    
    scholarship  = models.ForeignKey(Scholarship, on_delete=models.CASCADE)
    session        = models.CharField(max_length=100)
    
    apply_link  = models.URLField()
    
    def __str__(self):
        return f'{self.scholarship} ({self.session})'


class ScholarshipFollower(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)

    
    def __str__(self):
        return f"{self.scholarship} - {self.user}"



