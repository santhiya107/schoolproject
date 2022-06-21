from urllib import response
from . forms import *
from django.shortcuts import render,redirect
from .models import *
import requests
import json
def simple(request):    
    form=Loginform(data=request.POST)
    if request.method=='POST' and form.is_valid():
        url='http://127.0.0.1:8000/auth/login2/'
        param={'email':form.cleaned_data['email'],'phone':form.cleaned_data['phone']}
        response=requests.post(url,param).json()
        # print(response)
        return render(request,'base.html',{'response':response})
    context={'form':form}
    return render(request,'accounts/login.html',context)
def gradeview(request): 
    form=grade_form()
    if request.method=='POST':       
        if form.is_valid(): 
            form.save()
    response=requests.get('http://127.0.0.1:8000/academics/grades/?format=json')
    grade=response.json()    
    return render(request,'academics/grade.html',{'grade':grade,'form':form})
def subjectcreateview(request): 
    form=subject_form(data=request.POST ) 
    if request.method=='POST':       
        if form.is_valid(): 
            form.save()
    response=requests.get('http://127.0.0.1:8000/academics/subjects/?format=json')
    subject=response.json()    
    return render(request,'academics/subjectcreate.html',{'subject':subject,'form':form})
def subjectEdit(request,pk):
     tasks=Subject.objects.get(id=pk)
     form=subject_form(instance=tasks)
     if request.method=='POST':
        form=subject_form(request.POST,instance=tasks)
        if form.is_valid():
            form.save()
        return redirect('/')         
     context={'form':form}
     return render(request,'academics/updatechapter.html',context)
def subjectdelete(request,pk):
    item=Subject.objects.get(id=pk)
    if request.method=='POST':
        item.delete()
        return redirect('/')      
    context={'item':item} 
    return render(request,'deletesubject.html',context) 
def chaptercreateview(request): 
    form=chapter_form(data=request.POST or None)    
    if request.method=='POST':       
        if form.is_valid():          
            form.save()      
            return redirect('chaptercreateview')      
    context={'form':form}  
    return render(request,'academics/chapter.html',context)
def chapterEdit(request,pk):
     tasks=Chapter.objects.get(id=pk)
     form=chapter_form(instance=tasks)
     if request.method=='POST':
        form=chapter_form(request.POST,instance=tasks)
        if form.is_valid():
            form.save()
        return redirect('/')         
     context={'form':form}
     return render(request,'academics/updatechapter.html',context)
def chapterlistview(request):
    form=chapterlist_form(data=request.POST )
    if request.method=='POST':    
        if form.is_valid():
            grade= form.cleaned_data["grade"]
            subject=form.cleaned_data['subject']
            print(grade)
            print(subject)
            url='http://127.0.0.1:8000/academics/chapter-list/'
            params={'grade':str(grade),'subject':str(subject)}
            rec=requests.get(url,params).json()      
            print(rec)
            return render(request,'academics/chapterlist.html',{'form':form,'rec':rec})             
    return render(request,'academics/chapterlist.html',{'form':form})
def questioncreationview(request): 
    form=question_form()
    if request.method=='POST':       
        if form.is_valid(): 
            form.save()
    response=requests.get('http://127.0.0.1:8000/academics/question/')
    question=response.json()    
    return render(request,'academics/question.html',{'question':question,'form':form})

    # form=question_form(data=request.POST or None)
    # if request.method=='POST':
    #     if form.is_valid():
    #         form.save()      
    #         return redirect('questioncreationview')      
    # context={'form':form}  
    # return render(request,'academics/question.html',context)
def questionlistview(request):  
    subject=request.POST.get('subject')
    grade=request.POST.get('grade')
    if request.method=='POST':
        grade = Grade.objects.get(grade=grade)
        subject = Subject.objects.get(name=subject,grade=grade.id)
        question = Question.objects.filter(grade=grade.id,subject=subject.id)
        context={'question':question}  
        return render(request,'academics/questionlist.html',context)
    return render(request,'academics/questionlist.html')