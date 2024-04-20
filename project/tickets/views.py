from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view
from rest_framework import status,filters
from .serializers import *
from rest_framework.views import APIView
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
            
        }
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
# 3.1 GET POST 

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

# 3.1 GET DELETE PUT 
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
#cbv 4.1 list and create  GET and POST

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
        