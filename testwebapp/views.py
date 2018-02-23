from django.shortcuts import render
#from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from .form import CheckButton, BarcodeInfo, Employee_Info, Delete_Data, Barcode_Process
from django.core.files import File
import threading
import socket
import sys
import time
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from .models import users_data, employee
import datetime
from django.contrib.auth import authenticate, login, logout
import os


path = '/home/web/WebApp2/testwebapp/datafile.txt'
path2 = '/home/web/WebApp2/testwebapp/barcodefile.txt'

HOST = socket.gethostbyname("10.1.10.27")    # The remote host
PORT = 8001             # The same port as used by the server
maxconnections = 1
sem = threading.Semaphore()
# Create your views here.
global exists 
#exists = None


def handle_uploaded_file(f):
    with open('uploaded.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def HomePageView(request):

    if request.method == 'POST':
        form = CheckButton(request.POST, request.FILES)
     
        if form.is_valid():
            
            
            handle_uploaded_file(request.FILES['docfile'])
            #name = form.cleaned_data['your_name']
            email = form.cleaned_data['your_email']
            #serialnumber = form.cleaned_data['number']
            #print{name}
            
            
            #if name in ['YES', 'yes']:
                          
            f = open(path, 'w')
            filewithdata = open('uploaded.txt', 'r') 
            l = filewithdata.read(2048)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                try:
                    sem.acquire()
                    time.sleep(2)
                    s.connect((HOST, PORT))
                    #s.sendall(b's\r')
                    s.send(b'PRQ E<')
                    s.send(email.encode())
                    s.send(b'>')
                    s.send(b'D<')
                    s.sendall(l.encode())
                    s.send(b'>\r')
                    time.sleep(2)
                    data = s.recv(2048)
                    b = data.decode()
                    if("ERROR" in b): 
                        s.close()
                        f.close()
                        sem.release()
                        return render(request, 'ServerError.html')
                    
                    f.write(b[3:11:1])
                    #f.close()
                    s.close()
                    #f.open()
                    #datareceived = f.read(1024)
                    #for word in datareceived: 
                    #    if(word == "ERROR"):
                    #        return render(request, 'ServerError.html')
                    f.close()
                    sem.release()
           
                except socket.timeout:
                     sem.release()
                     return render(request,'ServerError.html') 
             
               
                #sem.release()
            #f = open(path, 'a') 
            #f.write('SERIAL NUMBER: ')
            #f.write(serialnumber)
            #f.close()
            #f = open(path, 'r') 
            #b = f.read()
            email = EmailMessage('Passcode', 'Passcode: ' + b[3:11:1] , to=[email])
            #email.attach('Passcode.txt',b[3:11:1])
            email.send() 
                #myfile = File(f)    
                #response = HttpResponse(myfile, content_type='text/plain')
                #response['Content-Disposition'] = 'attachment; filename= data.txt' 
                #return render('thankyou.html',respuesta)
                #return response
            return render(request,'thankyou.html')
               
            #else:
                
                #return render(request,'thankyou.html')

        #sem.release()    

    
    return render(request,'home.html')    

#template_name='home.html'

def Barcode(request):
    if request.method == 'POST':
        form = BarcodeInfo(request.POST)#, request.FILES)
     
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['your_email']
            company = form.cleaned_data['company']
            time  = str(datetime.datetime.now())
            new_user = users_data(email = email, name = name, company = company, date = time[:10])
            new_user.save()     
            
            return render(request,'BarcodeProcess.html')
        else:
            return render(request,'BarcodeInfo.html')

    return render(request,'BarcodeInfo.html')



def BarcodeProcess(request):

    if request.method == 'POST':

        form = Barcode_Process(request.POST, request.FILES)

        if form.is_valid():
            labware = form.cleaned_data['labware']
            docfile  = request.FILES['docfile']
           #os.system("bash test.sh -v /home/web/Desktop/bb.JPG")

            return render(request, 'thankyou.html')
        else:
            return render(request, 'home.html')

    return render(request, 'BarcodeInfo.html')


def Login(request):
    


    if request.user.is_authenticated:
        info = users_data.objects.all()
        user = {'action': "Display all", 'data':info} 
        return render(request,'EmployeeHome.html', user) 


    if request.method == 'POST':
        form = Employee_Info(request.POST)#, request.FILES)
        
        
        if form.is_valid():            
            name = form.cleaned_data['username']
            pwd  = form.cleaned_data['pss']
           
            exists = authenticate(request, username = name, password = pwd)
                
                
            if exists:
                login(request, exists)
                info = users_data.objects.all()
                user = {'action': "Display all", 'data':info} 
                
                return render(request,'EmployeeHome.html', user) 
            else:

                return render(request,'EmployeeLogin.html')

            return render(request,'BarcodeProcess.html')
        else:
            return render(request,'EmployeeLogin.html')

    return render(request,'EmployeeLogin.html')


def EmployeeHome(request):

    if 'data' in request.POST:
 
        return render(request, 'Delete.html') 

    else:
        
        return render(request,'EmployeeLogin.html')



def DeleteData(request):

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Delete_Data(request.POST)
            
            if form.is_valid():
                name_user = form.cleaned_data['name']
                company_user = form.cleaned_data['company']
                info = users_data.objects.filter(name=name_user).filter(company=company_user)
                info.delete()
                data = users_data.objects.all()
                user = {'action': "Display all", 'data':data} 

  
                return render(request,'EmployeeHome.html', user) 
            else:
                 return render(request, 'BarcodeInfo.html') 
        return render(request, 'Delete.html')

    else:
        
        return render(request,'EmployeeLogin.html')

def Logout(request):

    logout(request)

    return render(request,'EmployeeLogin.html')

    
    
