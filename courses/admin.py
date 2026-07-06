from django.contrib import admin
from .models import Course, Lesson, Quiz, Question, Choice, Enrollment, LessonProgress, QuizAttempt
# Register your models here.

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Enrollment)
admin.site.register(LessonProgress)
admin.site.register(QuizAttempt)