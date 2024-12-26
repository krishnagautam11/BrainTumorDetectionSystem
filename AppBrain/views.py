from django.shortcuts import render,redirect
from django import template
from django.contrib.sessions.models import Session
import string
from django.core.files.storage import FileSystemStorage
from django.utils.module_loading import import_string
from datetime import date
import datetime
from datetime import datetime
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db.models import Avg, Max, Min, Sum, Count

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


import pandas as pd
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from AppBrain.models import *
from random import randrange, uniform
import operator
import itertools  

import os
from django.conf import settings


from django.http import HttpResponse
from wsgiref.util import FileWrapper

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from django.db.models import Q



def home(request):
    return render(request,'home.html',{})


def about(request):
    return render(request,"about.html",{})


def Admin_login(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        password = request.POST['password']
        
        if Admin_Details.objects.filter(Username=Username, Password=password).exists():
                user = Admin_Details.objects.get(Username=Username, Password=password)
                request.session['type_id'] = 'Admin'
                request.session['username'] = Username
                request.session['login'] = 'Yes'
                return redirect('/')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/Admin_login/')
    else:
        return render(request, 'Admin_login.html', {})



def User_login(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        password = request.POST['password']
        
        if User_Details.objects.filter(Username=Username, Password=password).exists():
            user = User_Details.objects.all().filter(Username=Username, Password=password)
            request.session['User_id'] = str(user[0].id)
            request.session['type_id'] = 'User'
            request.session['username'] = Username
            request.session['login'] = 'Yes'
            return redirect('/')
            
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/User_login/')
    else:
        return render(request, 'User_login.html', {})

        




def ChangePassword(request):
    if request.method == 'POST':
        CurrentPassword = request.POST['CurrentPassword']
        NewPassword = request.POST['NewPassword']
        ConfirmPassword = request.POST['ConfirmPassword']

        uid = request.session['User_id']
        CurrUser = User_Details.objects.all().filter(id=uid)
        if CurrUser[0].Password == CurrentPassword:
            if NewPassword == ConfirmPassword:
                User_Details.objects.filter(id=uid).update(Password=NewPassword)
                messages.info(request,'Passwords Changed Successfully')
                return render(request, 'ChangePassword.html', {})
            else:
                messages.info(request,'New Passwords doesnt match')
                return render(request, 'ChangePassword.html', {})
        else:
            messages.info(request,'Current Password doesnt match')
            return render(request, 'ChangePassword.html', {})
        
    else:
        return render(request, 'ChangePassword.html', {})



def Register(request):
    if request.method == 'POST':
        First_name = request.POST['First_name']
        Last_name = request.POST['Last_name']
        Username = request.POST['Username']
        Dob = request.POST['Dob']
        Gender = request.POST['Gender']
        Phone = request.POST['Phone']
        Email = request.POST['Email']
        Password = request.POST['Password']
        final_address = request.POST['Address']
        City = request.POST['City']
        State = request.POST['State']
        

        if User_Details.objects.filter(Username=Username).exists():
            messages.info(request,'Username taken')
            return redirect('/AddOfficer/')

        elif User_Details.objects.filter(Email=Email).exists():
            messages.info(request,'Email Id taken')
            return redirect('/AddOfficer/')

        else:  
            register = User_Details( First_name=First_name, Last_name=Last_name, Dob=Dob, Gender=Gender ,Phone= Phone,Email= Email,Username= Username,Password=Password,Address=final_address,City=City,State=State)
            register.save()
            messages.info(request,'User Register Successfully')
            return redirect('/Register/')
    else:
        return render(request, 'register.html', {})



def logout(request):
    Session.objects.all().delete()
    return redirect('/')



def Analyze(request):
    return render(request, 'Analyze.html', {})

def AddDoctor(request):
    if request.method == 'POST':
        First_name = request.POST['First_name']
        Last_name = request.POST['Last_name']
        Username = request.POST['Username']
        Dob = request.POST['Dob']
        Gender = request.POST['Gender']
        Phone = request.POST['Phone']
        Email = request.POST['Email']
        Speciality = request.POST['Speciality']
        final_address = request.POST['Address']
        City = request.POST['City']
        State = request.POST['State']
        register = Doctor_Details( First_name=First_name, Last_name=Last_name, Dob=Dob, Gender=Gender ,Phone= Phone,Email= Email,Username= Username,Speciality=Speciality,Address=final_address,City=City,State=State)
        register.save()
        messages.info(request,'Doctor Added Successfully')
        return redirect('/AddDoctor/')
    else:
        return render(request, 'AddDoctor.html', {})


def ViewDoctor(request):
    if request.method == 'POST':
        pass
    else:
        Doctor = Doctor_Details.objects.all()
        return render(request, 'ViewDoctor.html', {'Doctor':Doctor})


def ViewFeedback(request):
    if request.method == 'POST':
        pass
    else:
        Feedb_det = Feedback_details.objects.all()
        return render(request, 'ViewFeedback.html', {'Feedb_det':Feedb_det})


def WriteFeedback(request):
    if request.method == 'POST':
        Feedbck = request.POST['Feedback']
        print()
        did = request.POST['hfuid']
        Feed = Feedback_details(Feedback=Feedbck, Uid=did)
        Feed.save()
        messages.info(request,'Feedback Saved')
        return redirect('/WriteFeedback/')

    else:
        did = request.session['User_id']
        return render(request, 'WriteFeedback.html', {'did':did})


def ViewUser(request):
    if request.method == 'POST':
        pass
    else:
        Users = User_Details.objects.all()
        return render(request, 'ViewUser.html', {'Users':Users})


def AddTrainingData(request):
    if request.method == 'POST':
        Headache = request.POST['Headache']
        Seizures = request.POST['Seizures']
        Nausea = request.POST['Nausea']
        Vomiting = request.POST['Vomiting']
        Fatique = request.POST['Fatique']
        Drowsiness = request.POST['Drowsiness']
        SleepProblem = request.POST['SleepProblem']
        MemoryProblem = request.POST['MemoryProblem']
        ProblemInDailyActivity = request.POST['ProblemInDailyActivity']
        DifficultyInFineMotorSkills = request.POST['DifficultyInFineMotorSkills']
        LossInVision = request.POST['LossInVision']
        HearingIssue = request.POST['HearingIssue']
        DifficultyInSwalling = request.POST['DifficultyInSwalling']
        BreathingIssue = request.POST['BreathingIssue']
        Result = request.POST['Result'] 

        register = TrainingData(Headache = Headache,Seizures = Seizures,Nausea = Nausea,Vomiting = Vomiting,Fatique = Fatique,Drowsiness = Drowsiness,SleepProblem = SleepProblem,MemoryProblem = MemoryProblem,ProblemInDailyActivity = ProblemInDailyActivity,DifficultyInFineMotorSkills = DifficultyInFineMotorSkills,LossInVision = LossInVision,HearingIssue  = HearingIssue,DifficultyInSwalling = DifficultyInSwalling,BreathingIssue = BreathingIssue,Result = Result)
        register.save()
        messages.info(request,'Data Added Successfully')
        return redirect('/AddTrainingData/')

    else:
        return render(request, 'AddTrainingData.html', {})




def get_response(request):

    Headache = request.POST.get('Headache')
    Seizures = request.POST.get('Seizures')
    Nausea = request.POST.get('Nausea')
    Vomiting = request.POST.get('Vomiting')
    Fatique = request.POST.get('Fatique')
    Drowsiness = request.POST.get('Drowsiness')
    SleepProblem = request.POST.get('SleepProblem')
    MemoryProblem = request.POST.get('MemoryProblem')
    ProblemInDailyActivity = request.POST.get('ProblemInDailyActivity')
    DifficultyInFineMotorSkills = request.POST.get('DifficultyInFineMotorSkills')
    LossInVision = request.POST.get('LossInVision')
    HearingIssue = request.POST.get('HearingIssue')
    DifficultyInSwalling = request.POST.get('DifficultyInSwalling')
    BreathingIssue = request.POST.get('BreathingIssue')



    count = TrainingData.objects.all().count()

    print(count)
    if count > 0:
        Packages = TrainingData.objects.all()
    
        ArrHeadache = []
        ArrSeizures = []
        ArrNausea = []
        ArrVomiting = []
        ArrFatique = []
        ArrDrowsiness = []
        ArrSleepProblem = []
        ArrMemoryProblem = []
        ArrProblemInDailyActivity = []
        ArrDifficultyInFineMotorSkills = []
        ArrLossInVision = []
        ArrHearingIssue = []
        ArrDifficultyInSwalling = []
        ArrBreathingIssue = []
        ArrResult = []



        Headache =format(Headache)
        Seizures =format(Seizures)
        Nausea =format(Nausea)
        Vomiting =format(Vomiting)
        Fatique =format(Fatique)
        Drowsiness =format(Drowsiness)
        SleepProblem =format(SleepProblem)
        MemoryProblem =format(MemoryProblem)
        ProblemInDailyActivity =format(ProblemInDailyActivity)
        DifficultyInFineMotorSkills =format(DifficultyInFineMotorSkills)
        LossInVision =format(LossInVision)
        HearingIssue =format(HearingIssue)
        DifficultyInSwalling =format(DifficultyInSwalling)
        BreathingIssue =format(BreathingIssue)



        for line in Packages:
            ArrHeadache.append(format(line.Headache))
            ArrSeizures.append(format(line.Seizures))
            ArrNausea.append(format(line.Nausea))
            ArrVomiting.append(format(line.Vomiting))
            ArrFatique.append(format(line.Fatique))
            ArrDrowsiness.append(format(line.Drowsiness))
            ArrSleepProblem.append(format(line.SleepProblem))
            ArrMemoryProblem.append(format(line.MemoryProblem))
            ArrProblemInDailyActivity.append(format(line.ProblemInDailyActivity))
            ArrDifficultyInFineMotorSkills.append(format(line.DifficultyInFineMotorSkills))
            ArrLossInVision.append(format(line.LossInVision))
            ArrHearingIssue.append(format(line.HearingIssue))
            ArrDifficultyInSwalling.append(format(line.DifficultyInSwalling))
            ArrBreathingIssue.append(format(line.BreathingIssue))
            ArrResult.append(format(line.Result))


        ArrHeadache.append(Headache)
        ArrSeizures.append(Seizures)
        ArrNausea.append(Nausea)
        ArrVomiting.append(Vomiting)
        ArrFatique.append(Fatique)
        ArrDrowsiness.append(Drowsiness)
        ArrSleepProblem.append(SleepProblem)
        ArrMemoryProblem.append(MemoryProblem)
        ArrProblemInDailyActivity.append(ProblemInDailyActivity)
        ArrDifficultyInFineMotorSkills.append(DifficultyInFineMotorSkills)
        ArrLossInVision.append(LossInVision)
        ArrHearingIssue.append(HearingIssue)
        ArrDifficultyInSwalling.append(DifficultyInSwalling)
        ArrBreathingIssue.append(BreathingIssue)


        le = preprocessing.LabelEncoder()

        Headache_encoded=le.fit_transform(ArrHeadache)
        last_Headache = Headache_encoded[-1]
        Headache_encoded = Headache_encoded[:-1]

        Seizures_encoded=le.fit_transform(ArrSeizures)
        last_Seizures = Seizures_encoded[-1]
        Seizures_encoded = Seizures_encoded[:-1]

        Nausea_encoded=le.fit_transform(ArrNausea)
        last_Nausea = Nausea_encoded[-1]
        Nausea_encoded = Nausea_encoded[:-1]

        Vomiting_encoded=le.fit_transform(ArrVomiting)
        last_Vomiting = Vomiting_encoded[-1]
        Vomiting_encoded = Vomiting_encoded[:-1]


        Fatique_encoded=le.fit_transform(ArrFatique)
        last_Fatique = Fatique_encoded[-1]
        Fatique_encoded = Fatique_encoded[:-1]

        Drowsiness_encoded=le.fit_transform(ArrDrowsiness)
        last_Drowsiness = Drowsiness_encoded[-1]
        Drowsiness_encoded = Drowsiness_encoded[:-1]

        SleepProblem_encoded=le.fit_transform(ArrSleepProblem)
        last_SleepProblem = SleepProblem_encoded[-1]
        SleepProblem_encoded = SleepProblem_encoded[:-1]

        MemoryProblem_encoded=le.fit_transform(ArrMemoryProblem)
        last_MemoryProblem = MemoryProblem_encoded[-1]
        MemoryProblem_encoded = MemoryProblem_encoded[:-1]

        ProblemInDailyActivity_encoded=le.fit_transform(ArrProblemInDailyActivity) 
        last_ProblemInDailyActivity = ProblemInDailyActivity_encoded[-1]
        ProblemInDailyActivity_encoded = ProblemInDailyActivity_encoded[:-1]


        DifficultyInFineMotorSkills_encoded=le.fit_transform(ArrDifficultyInFineMotorSkills) 
        last_DifficultyInFineMotorSkills = DifficultyInFineMotorSkills_encoded[-1]
        DifficultyInFineMotorSkills_encoded = DifficultyInFineMotorSkills_encoded[:-1]


        LossInVision_encoded=le.fit_transform(ArrLossInVision)
        last_LossInVision = LossInVision_encoded[-1]
        LossInVision_encoded = LossInVision_encoded[:-1]

        HearingIssue_encoded=le.fit_transform(ArrHearingIssue)
        last_HearingIssue = HearingIssue_encoded[-1]
        HearingIssue_encoded = HearingIssue_encoded[:-1]

        DifficultyInSwalling_encoded=le.fit_transform(ArrDifficultyInSwalling)
        last_DifficultyInSwalling = DifficultyInSwalling_encoded[-1]
        DifficultyInSwalling_encoded = DifficultyInSwalling_encoded[:-1]

        BreathingIssue_encoded=le.fit_transform(ArrBreathingIssue)
        last_BreathingIssue = BreathingIssue_encoded[-1]
        BreathingIssue_encoded = BreathingIssue_encoded[:-1]


        temp1 = list(zip(Headache_encoded,Seizures_encoded,Nausea_encoded,Vomiting_encoded,Fatique_encoded,Drowsiness_encoded,SleepProblem_encoded,MemoryProblem_encoded,ProblemInDailyActivity_encoded,DifficultyInFineMotorSkills_encoded,LossInVision_encoded,HearingIssue_encoded,DifficultyInSwalling_encoded,BreathingIssue_encoded))
        model = GaussianNB()
        model.fit(temp1,ArrResult)
        
        predicted= model.predict([[last_Headache,last_Seizures,last_Nausea,last_Vomiting,last_Fatique,last_Drowsiness,last_SleepProblem,last_MemoryProblem,last_ProblemInDailyActivity,last_DifficultyInFineMotorSkills,last_LossInVision,last_HearingIssue,last_DifficultyInSwalling,last_BreathingIssue]])

        print("Result :",predicted)

        result = predicted
        
        result = str(result)[2:-2]


        register = TrainingData(Headache = Headache,Seizures = Seizures,Nausea = Nausea,Vomiting = Vomiting,Fatique = Fatique,Drowsiness = Drowsiness,SleepProblem = SleepProblem,MemoryProblem = MemoryProblem,ProblemInDailyActivity = ProblemInDailyActivity,DifficultyInFineMotorSkills = DifficultyInFineMotorSkills,LossInVision = LossInVision,HearingIssue  = HearingIssue,DifficultyInSwalling = DifficultyInSwalling,BreathingIssue = BreathingIssue,Result = result)
        register.save()


        if result == "1":
            answer="HIGH"
        else:
            answer="LOW"
        print("answer",answer)

    else:
        answer = "No Data Found"
    
    data = {
        'respond': answer
        }
    
    return JsonResponse(data)




