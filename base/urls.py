#This is my base app url file

from  django.urls import path
from .import views


urlpatterns =[
    path('login/', views.loginPage, name ="login"),
    path('logout/', views.logoutUser, name ="logout"),
    path('',views.home, name= "Homepage"),
    path('room/<str:pk>/', views.room, name="the_room"),
    path('chats/', views.chats, name= "chat_room"),

    path('create-room/',views.createRoom, name ="create-room"),
    path('update-room/<str:pk>',views.updateRoom, name ="update-room"),
    path('delete-room/<str:pk>',views.deleteRoom, name ="delete-room"),
]