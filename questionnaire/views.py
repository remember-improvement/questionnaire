

from ssl import Options
from django.shortcuts import render, HttpResponse,redirect
from new_year.settings import RUN_ON_HEROKU, SECRET_KEY
from django.contrib.sessions.backends.db import SessionStore
import json
import new_year.settings
from questionnaire.models import Questions, Answer, Option, userProfile

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from questionnaire.forms import AnswerPostForm, LoginPostForm
from django.core.exceptions import ObjectDoesNotExist
import os
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from new_year.common.utils import send_success_email
import jwt
@csrf_exempt
def home(request):
    home_template_name = 'home.html'
    RUN_ON_HEROKU=os.getenv('RUN_ON_HEROKU')
    if request.method == 'GET':
        
        return render(request,home_template_name)
    if request.method == 'POST':
        form = LoginPostForm(request.POST)
        if form.is_valid():
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0] 
            else:
                ip = request.META.get('REMOTE_ADDR')
            username = form.cleaned_data['username']
            bankaccount = form.cleaned_data['bankaccount']
            user = User.objects.create(username=username)
            user.user_profile.create(bank_account=bankaccount,ip_address=ip)
            request.session["user_id"] = user.id
                
            start_pk_obj = Questions.objects.all()
            start_pk = start_pk_obj[0].id
            current_host = request.META['HTTP_HOST']
            if RUN_ON_HEROKU == '0':
                
                return redirect(f'http://{current_host}/questionnaire/{start_pk}')
                
            else:
                return redirect(f'https://{current_host}/questionnaire/{start_pk}')
@csrf_exempt
def get_questions(request, pk):
    question_template_name = 'question.html'
    RUN_ON_HEROKU=os.getenv('RUN_ON_HEROKU')
    if request.method == 'GET':

        current_host = request.META['HTTP_HOST']
        
        try:
            question = Questions.objects.get(id=pk)
        except ObjectDoesNotExist:
            if RUN_ON_HEROKU == '0':
                return redirect(f'http://{current_host}/done')
            else:
                return redirect(f'https://{current_host}/done')
        title = question.caption
        options = Option.objects.filter(question_id=pk)
        step = '下一題'
        options_list = []

        for op in options:
            options_list.append(op.option_name)
        if not Questions.objects.filter(id=pk+1).exists():
            step = '看結果'
        return render(request,question_template_name,{'title':title,'op0':'1：'+options_list[0],'op1':'2：'+options_list[1],'op2':'3：'+options_list[2],'op3':'4：'+options_list[3],'step':step})
    if request.method == 'POST':
        form = AnswerPostForm(request.POST)
        if form.is_valid():
            user_id= request.session["user_id"]
            option_type = form.cleaned_data['answer']
            option = Option.objects.filter(question_id=pk,option_type=option_type).first()
            question_id = option.question_id
            question = Questions.objects.get(id=question_id)
            answer = Answer.objects.filter(question_id=question_id,user_id=user_id)
            
            if answer.exists():
                answer_obj = answer.first()
                answer_obj.option_id = option.id
                answer_obj.content = option.option_name
                answer_obj.save()
            else:
                answer_obj = Answer.objects.create(option_id=option.id,question_id=question_id,content=option.option_name,user_id=user_id)
            if option.is_correct == True:
                answer_obj.is_verified=True
                answer_obj.save()
            else:
                answer_obj.is_verified = False
                answer_obj.save()
            new_pk = pk+1
            current_host = request.META['HTTP_HOST']
            if RUN_ON_HEROKU == '0':
                return redirect(f'http://{current_host}/questionnaire/{new_pk}')
            else:
                return redirect(f'https://{current_host}/questionnaire/{new_pk}')
            


@csrf_exempt
def make_question(request):
    payload = {
    "data":[{
        "question_caption":"test",
                        "questionnaire_id":1,
                        "options":[{"option":"test1","is_correct":True},
                        {"option":"test2","is_correct":False},
                        {"option":"test3","is_correct":False},
                        {"option":"test4","is_correct":False}
                        ]
                        
                        
    }]
    
    
}
    if request.method == 'POST':
        request_body = request.body
        request_json = json.loads(request_body)
        request_data = request_json['data']
        for data in request_data:
            caption = data['question_caption']
            option_list = data['options']
            q = Questions.objects.create(caption=caption)
            n=1
            for op in option_list: 
                Option.objects.create(option_name=op['option'],question_id=q.id,is_correct=op['is_correct'],option_type=n)
                n+=1
        return HttpResponse()

@csrf_exempt
def done(request):
    if request.method == 'GET':
        done_template_name = 'done.html'
        user_id = request.session["user_id"]
        question_is_verified = Answer.objects.filter(user_id=user_id,is_verified=True)
        #caption = question.caption
        correct_answer_num = question_is_verified.count()
        total_question = Questions.objects.all().count()
        question_is_not_verified = Answer.objects.filter(user_id=user_id,is_verified=False)
        
        
        # return HttpResponse(question_is_not_verified)
        
        option_correct_dict={}
        option_wrong_dict={}
        for qnv in question_is_not_verified:
            correct_option = Option.objects.filter(question_id=qnv.question_id,is_correct=True).first()#正確答案
           
            
            #caption = Questions.objects.get(id=qnv.question_id)
            option_correct_dict[qnv.content] = correct_option
            answer_content = qnv.content
            option_wrong_dict[qnv.content] = answer_content
        # return HttpResponse(option_correct_dict)
        user = User.objects.all().last()
        send_success_email(receiver_email=user.email,receiver_name=user.username)
        return render(request,done_template_name,{'correct_answer':correct_answer_num,'total_question':total_question,'wrong_answer_question_list': question_is_not_verified,'option_correct_dict':option_correct_dict, 'option_wrong_dict':option_wrong_dict})


@csrf_exempt
def delete_question(request):
    if request.method == 'DELETE':
        request_body = request.body
        request_json = json.loads(request_body)
        request_data = request_json['data']

        question_id = request_data["id"]
        answer = Answer.objects.filter(question_id=question_id).first()
        answer.delete()
        option_set = Option.objects.filter(question_id=question_id)
        for option in option_set:
            option.delete()
        question = Questions.objects.filter(id=question_id).first()
        question.delete()
    return HttpResponse(200)
@csrf_exempt
def update_question(request):
    if request.method == 'PATCH':
        request_body = request.body
        request_json = json.loads(request_body)
        request_data = request_json['data']
        question_id = request_data["id"]
        question_caption = request_data["question_caption"]
        question = Questions.objects.filter(id=question_id)
        question.update(caption=question_caption)
        return HttpResponse(200)

def qr_code(request):
    if request.method == 'GET':
        qr_code_template_name = 'qr_code.html'
        user = User.objects.all().last()
        return render(request,qr_code_template_name,{'username':user.username})

    


