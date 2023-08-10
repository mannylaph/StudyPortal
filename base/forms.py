from django.forms import ModelForm
from base.models import Room
from django.contrib.auth.models import User


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
        fields = ['username','email']
        
    