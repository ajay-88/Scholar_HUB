from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from .serializers import*
from .models import *
from django.http import Http404
from rest_framework import status
from django.contrib.auth import login,logout
from rest_framework.authtoken.models import Token
from scholarhub.models import Profiledb 
from rest_framework import authentication,permissions
from django.conf import settings
from django.core.mail import send_mail






# def superuser(fn):

#     def wrapper(request,*args,**kwargs):
#         if request.user.is_superuser:
#             return fn(request,*args,**kwargs)
#         else:
#             print("get out")
#     return wrapper
# Create your views here.
class AdminRegistrationview(APIView):
    serializer_class=AdminRegistrationserializer
    def post(self,request):
        serializer=AdminRegistrationserializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["is_admin"]=True
            user=Profiledb.objects.create_user(**serializer.validated_data)
            return Response({'msg':'admin registered succcessfully'},status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class StudentRegistrationView(APIView):
    serializer_class=StudentRegistrationserializer
    def post(self,request):
        serializer=StudentRegistrationserializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['is_student']=True
            user=Profiledb.objects.create_user(**serializer.validated_data)
            return Response({'msg':'student registered successfully'},status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class LoginAPI(APIView):
    serializer_class=Commonloginserializer
    def post(self,request):
        serializer=Commonloginserializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user=serializer.validated_data['user']
            login(request,user)
            data={
                'id':user.id,
                'username':request.user.username,
                'is_student':request.user.is_student,
                'is_admin':request.user.is_admin,
                
            }
            token,created=Token.objects.get_or_create(user=user)
            return Response({'message':'logged in successfully', 'token':token.key,'data':data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
 
# class AddScholarship(APIView):
#      def post(self,request,*args,**kwargs):
#          serializer=ScholarshipSerializer(data=request.data)
#          if serializer.is_valid():
#              serializer.save()
#              return Response(data=serializer.data)
#          else:
#              return Response(serializer.errors)

# class AddScholarship(APIView):  # view for admin to add scholarship
#     def post(self, request, *args, **kwargs):
#         if request.user.is_superuser:
#         # Retrieve the logged-in user
#         # user = request.user
#          message_data = {
#             'name':  request.data.get('name',request.data),
#             'description': request.data.get('description',request.data),
#             'eligibility':  request.data.get('eligibility',request.data),
#             'amount': request.data.get('amount',request.data),
#             'user': request.user.id,
#             'duration': request.data.get('duration',request.data),
#             'deadline': request.data.get('deadline',request.data)

#          }
#         else:
#             print("get out")
        
        
#         serializer = ScholarshipSerializer(data=message_data)
        
#         if serializer.is_valid():
#                 serializer.save()
#                 return Response(data=serializer.data)
#         else:
#                 return Response(serializer.errors)
class AddScholarshipView(APIView):
    def post(self, request):
        if request.user.is_superuser:
        # Get data from the request
         message_data = request.data
        else:
            print("get out")

        # Initialize the serializer with the data
        serializer = ScholarshipSerializer(data=request.data)

        # Validate the serializer data
        if serializer.is_valid():
            # Save the valid data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return the errors if the data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



class ListScholarshipforadmin(APIView): # view for list all scholarship by admin

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:

        # Retrieve projects uploaded by the currently authenticated user
         projects = Scholarship.objects.all()
         serializer = ScholarshipSerializer(projects, many=True)
         return Response(serializer.data)
        else:
            print("get out")



# class ViewAppliedStudents(APIView):
#     def list (self,request,*args,**kwargs):
#         list=StudentApplication.objects.all()
#         serializer=StudentApplicationSerializer(list,many=True)
#         return Response(serializer.data)

class Admin_stud_ApplicationView(ViewSet):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    def list (self,request,*args,**kwargs):
        list=StudentApplication.objects.all()
        serializer=StudentApplicationSerializer(list,many=True)
        return Response(serializer.data)

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        list=StudentApplication.objects.get(id=id)
        serializer=StudentApplicationSerializer(list)
        return Response(serializer.data)
    
    def update(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=StudentApplication.objects.get(id=id)
        serializers=StudentApplicationSerializerUP(data=request.data,instance=qs)
        if serializers.is_valid():
            serializers.save()
            
            email=qs.email
            print(email)
            subject='status'
            if qs.status=="rejected":
                message=f'hii ur status has been rejected'
            else:
                message=f'hii ur status has been accepted'
            email_from= settings.EMAIL_HOST_USER
            recipient_list = [email,]
            send_mail(subject,message,email_from,recipient_list)
            


            return Response(data=serializers.data)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    

    

    
    













#student side






class StudentApply(APIView):
    def post(self, request, *args, **kwargs):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        # Ensure Profiledb instance exists and has required fields
        try:
            student_profile = Profiledb.objects.get(pk=request.user.pk)
            if not student_profile.address:
                return Response({"error": "User profile address is missing"}, status=status.HTTP_400_BAD_REQUEST)
        except Profiledb.DoesNotExist:
            return Response({"error": "Profiledb instance not found for the authenticated user"}, status=status.HTTP_404_NOT_FOUND)

        # Populate message_data with the Profiledb instance
        message_data = {
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'phone': request.data.get('phone'),
            'student': student_profile.id,
            'application_date': request.data.get('application_date'),
            'certificate': request.data.get('certificate'),
            'identity': request.data.get('identity'),
            'photo': request.data.get('photo'),
            'scholarship': request.data.get('scholarship')
        }

        # Serialize and save the StudentApplication instance
        serializer = StudentApplicationSerializer(data=message_data)
        if serializer.is_valid():
            user=serializer.validated_data['student']=request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







class ListScholarshipforStudents(APIView): # view for list all scholarship for  students

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    def get(self, request, *args, **kwargs):
        # Retrieve projects uploaded by the currently authenticated user
        projects = Scholarship.objects.all()
        serializer = ScholarshipSerializer(projects, many=True)
        return Response(serializer.data)
    

class ViewAppliedScholarship(APIView): #to view each students applied list of scholarship
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=StudentApplication.objects.filter(student=id)
        serializer = StudentApplicationSerializer(qs, many=True)
        return Response(serializer.data)
    
    # def get(self,request,*args,**kwargs):

    #     qs=StudentApplication.objects.all()
    #     serializer = StudentApplicationSerializer(qs, many=True)
    #     return Response(serializer.data)

    


    




    # def get(self, request, *args, **kwargs):  # fuction for list each shoclarship
    #     id=kwargs.get("pk")
    #     Scholarship = Scholarship.objects.filter(id=id)
    #     serializer = Scholarship(Scholarship, many=True)
    #     return Response(serializer.data)

class RetrieveScholarship(APIView):  # to view each scholarship one by one for students

    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        qs=Scholarship.objects.get(id=id)

        serializer=ScholarshipSerializer(qs)

        return Response(serializer.data)
    
    
    def put(self,request,*args,**kwargs): #only for admin

        id=kwargs.get('pk')
        if request.user.is_superuser:
            qs=Scholarship.objects.filter(scholarship_id=id)
            serializer=ScholarshipSerializer(data=request.data,instance=qs)
            if serializer.is_valid():
                serializer.save()
            return Response(data=serializer.data)
        else:
            print("get out")

         

         
         
