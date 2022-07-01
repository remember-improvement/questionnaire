from django.core.mail import EmailMessage, send_mail
#from django.conf import settings
from django.template.loader import render_to_string
from smtplib import SMTPException
from django.template.loader import get_template
from django.core.mail import EmailMessage

def render_and_il(subject, recipient_list, placeholders, template_name):
    sender ='chivestsai@gmail.com'
    plaintext = get_template(f'{template_name}.txt').render(placeholders)
    html = get_template(f'{template_name}.html').render(placeholders)
    send_mail(subject, plaintext, sender, recipient_list, html_message=html)
def send_success_email(receiver_email,receiver_name):
    subject = "在這重要的日子，獻上誠摯的祝福！"
    receiver_list = [receiver_email]
    content = {
        'username':receiver_name,
        
    }
    template_name = 'happy_birthday_letter'
    try:
        render_and_il(subject,receiver_list,content,template_name)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    send_success_email('wade8204@gmail.com','Lee')