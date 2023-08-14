# This is my core views file

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
# from django.contrib.auth.forms import UserCreationForm
from base.models import Room, Topic, Message , User
from base.forms import RoomForm, UserForm, MyUserCreationForm


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
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email = email)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, email=email, password = password)

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
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
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
    
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages =Message.objects.filter(Q(room__name__icontains=q))

    context = {'rooms':rooms, 'topics': topics, 'room_count':room_count,'room_messages':room_messages}
    return  render(request, 'base/home.html',context)




#Room room page logic
def room(request,pk):
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('the_room', pk=room.id)


    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room =i
    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html',context)



#Chat page logic
def chats(request):
    return render(request,'base/chats.html')

#logic for user profile
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    room_count = rooms.count()
    context ={'user':user, 'rooms':rooms, 'room_count':room_count, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'base/profile.html',context)



# Logic for creating new room
@login_required(login_url ='/login') # Restricts this function to authenicated users only
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description= request.POST.get('description'),
        )
   
        return redirect("Homepage")
    context = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)


#Logic for updating room
@login_required(login_url ='/login') # Restricts this function to authenicated users only
def updateRoom(request, pk):
    room = Room.objects.get(id =pk)
    topics = Topic.objects.all()
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)

    #Prevents non-super admins from using this function
    if request.user != room.host:
        return HttpResponse('You have no permission to do this')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')

        # form = RoomForm(request.POST, instance =room)
        # if form.is_valid:
        #     form.save()
        return redirect("Homepage")

    context = {'form':form, 'topics':topics, 'room':room}
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
   


   #logic for deleting Messages
@login_required(login_url ='/login') # Restricts this function to authenicated users only
def deleteMessage(request,pk):
    message =Message.objects.get(id=pk)

        #Prevents non-super admins from using this function
    if request.user != message.user:
        return HttpResponse('You have no permission to do this')
    
    if request.method == 'POST':
        message.delete()
        return redirect("Homepage")
    return render(request, 'base/delete.html', {'obj':message})


#logic for user update
@login_required(login_url='/login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request,'base/update-user.html',{'form':form})



#logic for topics
def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html',{'topics':topics})


#logic for Activities
def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html',{'room_messages':room_messages})

