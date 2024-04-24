from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view
from rest_framework import status,filters
from .serializers import *
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics,mixins,viewsets

# Create your views here.

######1 whithout rest and no model

def no_rest_no_model(request):
    guests=[
        {
            'id':1,
            'name':"Omar",
            'mobile':1324,
            
        },
        {
            'id':2,
            'name':"ahmad",
            'mobile':4532,
            
        },
    ]
    return JsonResponse(guests,safe=False)
    
    
    
######2 whithout rest and from model
def no_rest_from_model(request):

    data = Guest.objects.all()
    response = {
        'guests':list(data.values('name','mobile'))
    }
    return JsonResponse(response)


#####3 function based viwes 
# 3 GET POST 

@api_view(['GET','POST'])
def fbv_list(request):
    
    #GET
    if request.method=='GET':
        guests=Guest.objects.all()
        serializer=Guestserializer(guests,many=True)
       
        return Response(serializer.data)
    #POST
    elif request.method=='POST':
        serializer=Guestserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

# 3 GET DELETE PUT 
@api_view(['GET','PUT','DELETE'])
def fdv_pk(request,pk):
    try:
        guest=Guest.objects.get(pk=pk)
    except:
        Guest.DoesNotExist
        return Response(status=status.HTTP_404_NOT_FOUND)
   #GET
    if request.method=='GET':
        serializer=Guestserializer(guest)
        return Response(serializer.data)
    #PUT
    elif request.method=='PUT':
        serializer=Guestserializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    #DELETE
    elif request.method=='DELETE':
      guest.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)



####4
#cbv 4 list and create  GET and POST

class cbv_list(APIView):
    def get(self,request):
        guests=Guest.objects.all()
        serializer=Guestserializer(guests,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        
        serializer=Guestserializer(data=request.data,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
        
        
#cbv 4 PUT DELETE GET
class cbv_pk(APIView):
    def get_object(self,pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
        
    def get(self,request,pk):
        guest=self.get_object(pk)
        serializer=Guestserializer(guest)
        return Response(serializer.data)
    
    def put(self,request,pk):
        guest=self.get_object(pk)   
        serializer=Guestserializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def DELETE(self,request,pk):
        guest=self.get_object(pk) 
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# 5 mixing
class mixing_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class=Guestserializer
    
    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)
    

class mixing_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class=Guestserializer
    
    def get(self,request,pk):
        return self.retrieve(request)   
    def put(self,request,pk):
        return self.update(request)
    def delete(self,request,pk):
        return self.destory(request)
# 6 generics
class generics_list(generics.ListCreateAPIView):
    queryset=Guest.objects.all()
    serializer_class=Guestserializer
    
    
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset=Guest.objects.all()
    serializer_class=Guestserializer
    
    
#7 viewset
class viewsets_guests(viewsets.ModelViewSet):
    queryset=Guest.objects.all()
    serializer_class=Guestserializer
    
    

class viewsets_movie(viewsets.ModelViewSet):
    queryset=Movie.objects.all()
    serializer_class=Movieserializer
    filter_backend=[filters.SearchFilter]
    serarch_fielde=['movie']

class viewsets_reservation(viewsets.ModelViewSet):
    queryset=Reservation.objects.all()
    serializer_class=Reservationserializer


#8  find movie

api_view(['GET'])
def find_movie(request):
    movie=Movie.objects.filter(
        hall=request.data['hall'],
        movie=request.data['movie']
    )
    serializer=Movieserializer(movie,many=True)
    return Response(serializer.data)

#9

@api_view(['POST'])
def new_reservation(request):
   
    try:
        movie = Movie.objects.get(
            hall=request.data['hall'],
            movie=request.data['movie'],
        )
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()

    # Correct status code
    return Response(status=status.HTTP_201_CREATED)