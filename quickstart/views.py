from django.contrib.auth.models import User, Group
from .models import Event
from quickstart.serializers import UserSerializer, GroupSerializer, EventSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import get_user_model

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def partial_update(self, request, pk=None):
        """
        Patch endpoint to update events gone to the total points of a user
        """
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'points': 'totaled'})
        else:
            return Response(serializer.errors)

    @action(detail=True, methods=['PATCH'])
    def add_event(self, request, pk=None):
        """
        Patch event to add event to users list
        """
        user = self.get_object()
        event = Event.objects.get(id=request.data['id'])
        user.events.add(event)
        user.save()
        return Response({'it':'worked!'})

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Events
    """
    #permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(methods=['get'], detail=True)
    def get_code(self,  request, pk=None):
        if request.data:
            event = self.get_object()
            ev = EventSerializer(event)
            if ev.data['code']:
                if request.data['code'] == ev.data['code']:
                    return Response({'status': 'it worked'})
                else:
                    return Response({'status': 'wrong code'})
            else:
                return Response({'status':'no code is set'})
        else:
            return Response({'status': 'no request object given'})

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
