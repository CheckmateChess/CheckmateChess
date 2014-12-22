from django.shortcuts import render
from checkmateclient.forms import startForm, connectForm
from socket import *
from json import *

# Create your views here.

def home(request):
	return render(request,'index.html')



def start(request):
	form = startForm()
	context = { 'form' : form }
	return render(request,'start.html', context )

def connect(request):
	form = connectForm()
	context = { 'form' : form }
	return render(request,'connect.html', context )

def play(request):
	data = request.POST
	if not data:
		return render(request,'play.html' )
	if data['operation'] == 'Start':
		if request.FILES.get('book'):
			with open('/tmp/asd',"wb+") as myfile:
				for i in request.FILES.get('book').chunks():
					myfile.write(i)

		s = socket(AF_INET, SOCK_STREAM)
		s.connect(("0.0.0.0", 20000))
		s.send( '{"op":"start" , "color":"%s","params":["%s","%s","%s"]}' % ( data.get('color') , data.get('mode') , data.get('difficulty') , data.get('book') )  )
		print "------->",loads(s.recv(4096))
		s.close()
	elif data['operation'] == 'Connect':
		pass
	return render(request,'play.html' )
