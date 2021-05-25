from dashboard.models import *
from api.serializers import *
from django.shortcuts import get_object_or_404

# Rest Framework - Token Authentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token


# Create your views here.


@csrf_exempt
@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None and password is None:
        return Response({'error': 'Please provide username and password'},
                        status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid credentials'},
                        status=status.HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token':token.key},
                    status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def register(request):

    email = request.data.get("email")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    password = request.data.get("password")
    is_client = request.data.get("is_client")

    if email is None and password is None and first_name is None and last_name is None and is_client is None:
        return Response({'error': 'Please provide email, name, user type and password'},
                        status=status.HTTP_400_BAD_REQUEST)

    else:
        if is_client == "True":
            serializer = ClientRegSerializer(data=request.data)
        else:
            serializer = DriverRegSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': 'Fields not found'}, status=status.HTTP_400_BAD_REQUEST)


class ClientViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ClientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Client.objects.all()
        client = get_object_or_404(queryset, pk=pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def update(self, request, pk=None):
        client = Client.objects.get(pk=pk)
        serializer = ClientSerializer(client, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DriverViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = DriverSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Driver.objects.all()
        driver = get_object_or_404(queryset, pk=pk)
        serializer = DriverSerializer(driver)
        return Response(serializer.data)

    def update(self, request, pk=None):
        driver = Driver.objects.get(pk=pk)
        serializer = DriverSerializer(driver, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        driver = Driver.objects.get(pk=pk)
        driver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RideViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        rides = Ride.objects.all()
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = RideSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Ride.objects.all()
        rides = get_object_or_404(queryset, pk=pk)
        serializer = RideSerializer(rides)
        return Response(serializer.data)

    def update(self, request, pk=None):
        rides = Ride.objects.get(pk=pk)
        serializer = RideSerializer(rides, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        rides = Ride.objects.get(pk=pk)
        rides.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LocationViewSet(viewsets.ViewSet):
    def list(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Location.objects.all()
        locations = get_object_or_404(queryset, pk=pk)
        serializer = LocationSerializer(locations)
        return Response(serializer.data)


class ClientRegViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = ClientSerializer(data=request.data)
        user_validator(serializer)


class DriverRegViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = DriverSerializer(data=request.data)
        user_validator(serializer)


def user_validator(serializer):
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': 'Fields not found'}, status=status.HTTP_400_BAD_REQUEST)


"""class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)"""

"""def TokenAuthentication():
    """