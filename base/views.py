# This is my core views file

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from base.models import Room, Topic
from base.forms import RoomForm


# Create your views here.

# rooms = [
#     {"id":1, "name":"Let's Learn Python"},
#     {"id":2, "name":"Let's Learn MySQL"},
#     {"id":3, "name":"Let's Learn Javascript"},
#     {"id":4, "name":"Let's Learn React"},
# ]


#logic for login page
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('Homepage')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password = password)

        if user is not None:
            login(request, user)
            return redirect("Homepage")
        else:
            messages.error(request, 'Username or Password does not exist')


    context ={'page':page}
    return render(request, 'base/login_register.html',context)



#logic for user logout
def logoutUser(request):
    logout(request)
    return redirect('Homepage')

#logic for registration
def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('Homepage')

        else:
            messages.error(request, "An error occured during registration")
            
    return render(request, 'base/login_register.html',{'form':form})



#Home page logic
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
            Q(topic__name__icontains = q) |
            Q(name__icontains =q) |
            Q(description__icontains =q)
    )
    
    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms':rooms, 'topics': topics, 'room_count':room_count}
    return  render(request, 'base/home.html',context)




#Room room page logic
def room(request,pk):
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all().order_by('created')
    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room =i
    context = {'room':room, 'room_messages':room_messages}
    return render(request, 'base/room.html',context)



#Chat page logic
def chats(request):
    return render(request,'base/chats.html')


# Logic for creating new room
@login_required(login_url ='/login') # Restricts this function to authenicated users only
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("Homepage")
    context = {'form':form}
    return render(request, 'base/room_form.html', context)


#Logic for updating room
@login_required(login_url ='/login') # Restricts this function to authenicated users only
def updateRoom(request, pk):
    room = Room.objects.get(id =pk)
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)

    #Prevents non-super admins from using this function
    if request.user != room.host:
        return HttpResponse('You have no permission to do this')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance =room)
        if form.is_valid:
            form.save()
            return redirect("Homepage")

    context = {'form':form}
    return render(request, 'base/room_form.html',context)
    
#logic for deleting rooms
@login_required(login_url ='/login') # Restricts this function to authenicated users only
def deleteRoom(request,pk):
    room =Room.objects.get(id=pk)

        #Prevents non-super admins from using this function
    if request.user != room.host:
        return HttpResponse('You have no permission to do this')
    
    if request.method == 'POST':
        room.delete()
        return redirect("Homepage")
    return render(request, 'base/delete.html', {'obj':room})
   