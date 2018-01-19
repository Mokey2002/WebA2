from django.shortcuts import render
#from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from .form import CheckButton
from django.core.files import File
import threading
import socket
import sys
import time
from django.core.mail import EmailMessage
from django.shortcuts import redirect

path = '/home/web/WebApp/testwebapp/datafile.txt'

HOST = socket.gethostbyname("10.1.10.27")    # The remote host
PORT = 8001             # The same port as used by the server
maxconnections = 1
sem = threading.Semaphore()
# Create your views here.

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



