# This is my core views file

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.db.models import Q
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

    if request.method == 'POST':
        username = request.POST.get('username')
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


    context ={}
    return render(request, 'base/login_register.html',context)

#logic for user logout
def logoutUser(request):
    logout(request)
    return redirect('Homepage')

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
    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room =i
    context = {'room':room}
    return render(request, 'base/room.html',context)



#Chat page logic
def chats(request):
    return render(request,'base/chats.html')


# Logic for creating new room
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
def updateRoom(request, pk):
    room = Room.objects.get(id =pk)
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance =room)
        if form.is_valid:
            form.save()
            return redirect("Homepage")

    context = {'form':form}
    return render(request, 'base/room_form.html',context)
    
#logic for deleting rooms

def deleteRoom(request,pk):
    room =Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect("Homepage")
    return render(request, 'base/delete.html', {'obj':room})
   