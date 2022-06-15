from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    ListAPIView,
    )
from accounts.permission import IsAdminUser, IsStaffUser
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,HTTP_201_CREATED
)
from django.conf import settings
from django.core.mail import send_mail
import random
from .serializers import (
    SubjectSerializer,
    ChapterSerializer,
    GradeSerializer,
    ChapterViewSerializer,
    QuestionAnswerSerializer,
    QuestionGetSerializer,
    QuestionSerializer,
    )
from .models import Question, Subject,Grade,Chapter
from accounts.models import User
from .utils import render_to_pdf

# Create your views here.


class GradeView(ListCreateAPIView):
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self,request):
        queryset = self.get_queryset()
        serializer = GradeSerializer(queryset,many=True)
        return Response(serializer.data)

    def create(self,request):
        serializer = GradeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success",'data':serializer.data})
        return Response({"status": "failure", "data": serializer.errors})


class SubjectCreateView(ListCreateAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self,request):
        queryset = self.get_queryset()
        serializer = SubjectSerializer(queryset,many=True)
        return Response(serializer.data)

    def create(self,request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if self.request.user.user_type == 'is_staff':
                user = self.request.user
                gradeid = serializer.data['grade']
                grade = Grade.objects.get(id=gradeid)
                subjects = serializer.data['name']
                admin = User.objects.get(user_type='is_admin')
                subject = 'Subject creation'
                message = f'{user.profile.full_name} HAD CREATED,ON GRADE : {grade.grade} SUBJECT : {subjects}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [admin.email,]
                send_mail(subject,message,email_from,recipient_list)
            
            return Response({"status": "subject created",'data':serializer.data})
        return Response({"status": "failure", "data": serializer.errors})


class SubjectEditView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request,pk):
        try:
            queryset = Subject.objects.get(pk=pk)
        except:
            return Response({"status": "Subject doesn't exists"}, status=HTTP_400_BAD_REQUEST)
        serializer = SubjectSerializer(queryset)
        return Response(serializer.data)
    
    def update(self,request,pk):
        subject = Subject.objects.get(pk=pk)
        serializer = SubjectSerializer(subject,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "subject updated",'data':serializer.data})
        return Response({"status": "failure", "data": serializer.errors})


class ChaptersCreateView(CreateAPIView):

    serializer_class=ChapterSerializer
    queryset= Chapter.objects.all()
    permission_classes=[IsAuthenticated]

    def get(self, request, format=None):
        queryset= Chapter.objects.all()
        serializer = ChapterSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "chapter created",'data':serializer.data})   
        return Response({"status": "failure", "data": serializer.errors})


class ChapterEditView(RetrieveUpdateDestroyAPIView):

    serializer_class=ChapterSerializer
    permission_classes=[IsAuthenticated]
    queryset = Chapter.objects.all()

    def retrive(self,request,pk):
        try:
            queryset = Chapter.objects.get(pk=pk)
        except:
            return Response({"status": "Chapter doesn't exists"}, status=HTTP_400_BAD_REQUEST)
        serializer = ChapterSerializer(queryset)
        return Response(serializer.data)

    def update(self,request,pk):
        subject = Chapter.objects.get(pk=pk)
        serializer = ChapterSerializer(subject,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "chapter updated",'data':serializer.data})   
        return Response({"status": "failure", "data": serializer.errors})
        

class ChapterListView(APIView):
    serializer_class=ChapterViewSerializer

    def post(self,request):
        grade = request.data.get('grade')
        subject=(request.data.get('subject')).capitalize()
        if subject:
            data = []
            try:
                grade = Grade.objects.get(grade=grade)
                subject = Subject.objects.get(name=subject,grade=grade.grade)
                chapters = Chapter.objects.filter(subject=subject)
                for object in chapters:
                    data.append( {
                    "subject" : subject.name,
                    "grade" :subject.grade.grade,
                    "name": object.name,
                    "chapter_no": object.chapter_no,
                    "description": object.description,
                    })
                host = request.get_host()
                context = {'data':data}
                filename,status = render_to_pdf('academics/chapter.html','chapter_files',context)
                if not status:
                    return Response({'status':'given details incorrect'}) 

                return Response({'path':f'{host}/media/chapter_files/{filename}.pdf'})
            except:
                return Response({"status": "Not found"}, status=HTTP_404_NOT_FOUND)
        return Response({"status": "failed"}, status=HTTP_400_BAD_REQUEST)


class SubjectListView(ListAPIView):
    serializer_class=SubjectSerializer

    def get_queryset(self):
        queryset = Subject.objects.all()
        grade = self.request.query_params.get('grade')
        if grade is not None:
            try:
                queryset = queryset.filter(grade=grade)
            except :
                return Response({'status':'failed','error':'grade does not exists'})

    def list(self,request):
        queryset = self.get_queryset()
        serializer = SubjectSerializer(queryset,many=True)
        return Response(serializer.data)


class QuestionCreateView(CreateAPIView):
    serializer_class= QuestionAnswerSerializer

    def post(self, request):
        serializer = QuestionAnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Registered succesfull",'data':serializer.data},status=HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors})

class QuestionEditView(RetrieveUpdateDestroyAPIView):
    serializer_class= QuestionAnswerSerializer
    permission_classes = [IsAuthenticated]
    queryset=Question.objects.all()

    def retrieve(self,request,pk):
        try:
            question = Question.objects.get(pk=pk)
            serializer = QuestionAnswerSerializer(question)
            return Response(serializer.data)
        except:
            return Response({"status": "Question doesn't exists"}, status=HTTP_400_BAD_REQUEST)


class QuestionList(APIView):
    serializer_class = QuestionGetSerializer
    permission_classes = [IsAuthenticated]

    def post(self,request):
        grade = request.data.get('grade')
        subject=request.data.get('subject')
        number_of_questions = int(request.data.get('number_of_questions')) 
        try:
            grade = Grade.objects.get(grade=grade)
            subject = Subject.objects.get(name=subject,grade=grade.id)
            questions = Question.objects.filter(grade=grade.id,subject=subject.id)
            total_questions = questions.count()
            questions =(sorted(questions,key=lambda x: random.random()))
            host = request.get_host()
            if number_of_questions <= total_questions:
                questions = questions[:number_of_questions]
            else:
                return Response({'status':'given number questions is higher then the actual number of questions '})
            serializer = QuestionSerializer(questions,many=True)
            context = {'data':serializer.data,'grade':grade.grade,'subject':subject.name}
            filename,status = render_to_pdf('academics/question.html','question_files',context)
            if not status:
                return Response({'status':'given details incorrect'}) 
            return Response({'path':f'{host}/media/question_files/{filename}.pdf'})
        except:
            return Response({"status": "given details are incorrect"}, status=HTTP_400_BAD_REQUEST)
