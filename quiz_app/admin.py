from django.contrib import admin
from .models import *
# Register your models here.

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4 

class QuestionAdmin(admin.ModelAdmin):
    inlines =[AnswerInline]

admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
