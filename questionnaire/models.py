from django.db import models

# #Create your models here.



class Questions(models.Model):
    '''問卷問題表'''
    caption = models.CharField(max_length=32,verbose_name="問題題目")
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.caption
    class Meta:
        verbose_name_plural = "問卷問題表"
class Answer(models.Model):
    '''問卷回答表'''   
    question = models.ForeignKey(to="Questions",verbose_name="所屬問題",on_delete=models.CASCADE,related_name='answer_question')
    option = models.ForeignKey(to="Option",null=True,blank=True,on_delete=models.CASCADE,related_name='answer_option')
    val = models.IntegerField(null=True,blank=True,verbose_name="數字答案")
    content = models.CharField(max_length=255,null=True,blank=True,verbose_name="文本答案")
    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = "問卷回答表"
class Option(models.Model):
    '''
    單選題的選項
    '''
    option_name = models.CharField(max_length=32,verbose_name='選項名稱')
    option_type = models.CharField(max_length=32,null=True)
    question = models.ForeignKey(to=Questions,verbose_name='所在的問題',on_delete=models.CASCADE,related_name='question_option')
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return self.option_name
# class QuesModel(models.Model):
#     question = models.CharField(max_length=200,null=True)
#     op1 = models.CharField(max_length=200,null=True)
#     op2 = models.CharField(max_length=200,null=True)
#     op3 = models.CharField(max_length=200,null=True)
#     op4 = models.CharField(max_length=200,null=True)
#     ans = models.CharField(max_length=200,null=True)
#     is_verified = models.BooleanField(default=False)
#     def __str__(self):
#         return self.question

