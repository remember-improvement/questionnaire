"""new_year URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.etree.ElementInclude import include
from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from questionnaire import views

from questionnaire.views import get_questions, done, make_question, home, delete_question,qr_code,update_question
from questionnaire import urls as questionnaire_url


urlpatterns=[
    path('admin/', admin.site.urls),
    path('questionnaire/<int:pk>',get_questions),
    path('home',home),
    path('make_question',make_question),
    # path('questionnaire/',answer_question),
    path('done',done),
    path('delete_question',delete_question),
    path('update_question',update_question),
    path('qr_code',qr_code)
        ]