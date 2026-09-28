from django.contrib import admin
# Register your models here.
from .models import Mock_Test, Question, Test_Attempt, Answer
admin.site.register(Mock_Test)
admin.site.register(Question)
admin.site.register(Test_Attempt)
admin.site.register(Answer)
