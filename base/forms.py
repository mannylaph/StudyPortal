from django.forms import ModelForm
from base.models import Room, User
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2']


#logic for Room Form
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']



#logic for User Form
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','username','email','bio']
        
    