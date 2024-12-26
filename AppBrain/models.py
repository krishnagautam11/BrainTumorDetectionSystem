from django.db import models

class Admin_Details(models.Model):
    Username = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'Admin_Details'  

class User_Details(models.Model):
    First_name = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    Dob = models.CharField(max_length=50,default=None)
    Gender = models.CharField(max_length=10)
    Phone = models.IntegerField(default=None)
    Email = models.EmailField()
    Username = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
      
    class Meta:
        db_table = 'User_Details'



class Feedback_details (models.Model):
    Feedback = models.CharField(max_length=100,default=None)
    Uid = models.CharField(max_length=500,default=None)
          
    class Meta:
        db_table = 'Feedback_details'




class Doctor_Details(models.Model):
    First_name = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    Dob = models.CharField(max_length=50,default=None)
    Gender = models.CharField(max_length=10)
    Phone = models.IntegerField(default=None)
    Email = models.EmailField()
    Username = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    Speciality = models.CharField(max_length=100,default=None)

    class Meta:
        db_table = 'Doctor_Details'


class TrainingData(models.Model):
    Headache = models.CharField(max_length=100,default=None)
    Seizures = models.CharField(max_length=100,default=None)
    Nausea = models.CharField(max_length=100,default=None)
    Vomiting = models.CharField(max_length=100,default=None)
    Fatique = models.CharField(max_length=100,default=None)
    Drowsiness = models.CharField(max_length=100,default=None)
    SleepProblem = models.CharField(max_length=100,default=None)
    MemoryProblem = models.CharField(max_length=100,default=None)
    ProblemInDailyActivity = models.CharField(max_length=100,default=None)
    DifficultyInFineMotorSkills = models.CharField(max_length=100,default=None)
    LossInVision = models.CharField(max_length=100,default=None)
    HearingIssue  = models.CharField(max_length=100,default=None)
    DifficultyInSwalling = models.CharField(max_length=100,default=None)
    BreathingIssue = models.CharField(max_length=100,default=None)
    Result = models.CharField(max_length=100,default=None)

    class Meta:
        db_table = 'TrainingData'

