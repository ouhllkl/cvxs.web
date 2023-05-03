from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class SupportGourp(models.Model):
    name    = models.CharField(max_length=100)
    admin   = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    about   = models.TextField()

    def __str__(self):
        return self.name






class SupportGroupJoinRequest(models.Model):
    support_gourp   = models.ForeignKey(SupportGourp, on_delete=models.CASCADE)
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    message                 = models.TextField(blank=True)

    def __str__(self):
        return f'{self.support_gourp} - {self.user}'


class SupportGroupHelpRequest(models.Model):
    support_gourp   = models.ForeignKey(SupportGourp, on_delete=models.CASCADE)
    user                    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    about                   = models.TextField(blank=True)
    message                 = models.TextField(blank=True)
    helper                  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='helper', null=True)

    def __str__(self):
        return f'{self.support_gourp} - {self.user}'




class SupportGourpUser(models.Model):
    support_gourp   = models.ForeignKey(SupportGourp, on_delete=models.CASCADE)
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.support_gourp} - {self.user}'



class StudentStep(models.Model):
    id_name         = models.CharField(max_length=100)  
    name            = models.CharField(max_length=100)
    requirements    = models.TextField()
    notes           = models.TextField()
    support_gourp   = models.ForeignKey(SupportGourp, null=True, blank=True,  on_delete=models.SET_NULL)
    help_contacts   = models.TextField()
    
    def __str__(self):
        return self.name





    



class administration_profile(models.Model):
    user                    = models.OneToOneField(User, on_delete=models.CASCADE)
    notify_for_new_applications = models.BooleanField(default=0)
    accept_applications = models.BooleanField(default=0)
    cvx_acceptance_handler = models.BooleanField(default=0)
    change_current_procedures = models.BooleanField(default=1)
    add_university = models.BooleanField(default=1)


    def __str__(self) -> str:
        return str(self.user)



class Procedure(models.Model):
    name    = models.CharField(max_length=100)
    about               = models.TextField(blank=True)
    def __str__(self):
        return self.name



class ProcedureStep(models.Model):
    level = models.IntegerField(default=0)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    step = models.ForeignKey(StudentStep, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.procedure} ({self.level}) - {self.step}'




class Profile(models.Model):
    user                    = models.OneToOneField(User, on_delete=models.CASCADE)
    resedence               = models.CharField(max_length=100)
    cvx_acceptance          = models.IntegerField(default = 0)
    current_procedure       = models.ForeignKey(Procedure, null=True, blank=True, on_delete=models.SET_NULL)
    current_procedure_completed = models.BooleanField(default=0)
    current_procedure_step  = models.ForeignKey(ProcedureStep, null=True, blank=True, on_delete=models.SET_NULL)
    step_status             = models.IntegerField( default=1)
    step_note               = models.TextField(blank=True)
    steps_log               = models.JSONField(default=dict, blank=True)
    cv                      = models.URLField(blank=True)
    phone_numer             = models.CharField(max_length = 100 ,blank=True)
    study_log               = models.JSONField(default=dict, blank=True)
    followed_scholarships   = models.JSONField(default=dict, blank=True)
    earned_scholarships     = models.JSONField(default=dict, blank=True)
    branch_of_interest      = models.CharField(max_length = 100 ,blank=True)
    branch_of_interest_degree_type      = models.CharField(max_length = 100 , choices=[('Bachelor','Bachelor'), ('Master','Master'), ('PHD','PHD')],blank=True)

    

    @receiver(post_save, sender=User) 
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


    def __str__(self):
        return self.user.username