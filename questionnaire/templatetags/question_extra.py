from django import template

register = template.Library()

@register.filter
def correct_option(question):
    return question.question_option.filter(is_correct=1)



from django.template.defaulttags import register
...
@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)