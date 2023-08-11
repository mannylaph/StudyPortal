from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view( ['GET'])

def getRoute(request):
    routes = [
        'GET/api',
        'GET/api/rooms',
        'GET/api/romms/:id'

    ]    
    return Response(routes)


#logic to get rooms
@api_view (['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serialzer = RoomSerializer(rooms, many=True)
    
    return Response(serialzer.data)


@api_view (['GET'])
def getRoom(request,pk):
    room = Room.objects.get(id=pk)
    serialzer = RoomSerializer(room, many=False)    
    return Response(serialzer.data)