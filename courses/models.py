from django.db import models
from utilisateurs.models import CustomUser

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='taught_courses')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cours'
        verbose_name_plural = 'Cours'
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title



class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    xp_reward = models.PositiveIntegerField(default=10)
    
    class Meta:
        verbose_name_plural = 'Quizzes'
        verbose_name = 'Quiz'
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    
    def __str__(self):
        return f"{self.quiz.title} - Question {self.order}"
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Choix'
        verbose_name = 'Choix'
    
    def __str__(self):
        return f"{self.question.text} - {self.text}"
    

class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('expired', 'Expiré'),
        ('pending', 'En attente de paiement'),
    ]
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        verbose_name = 'Inscription'
        verbose_name_plural = 'Inscriptions'
        ordering = ['-enrollment_at']
        unique_together = ('student', 'course')
        
    def __str__(self):
        return f"{self.student.username} -> {self.course.title}"

class LessonProgress(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_progress')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('student', 'lesson')
        verbose_name = 'Progression de la leçon'
        verbose_name_plural = 'Progressions des leçons'

    def __str__(self):
        return f"{self.student.username} - {self.lesson.title} - {'Completed' if self.is_completed else 'In Progress'}"

class QuizAttempt(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_attempts')
    score = models.FloatField()
    attempted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Tentative de quiz'
        verbose_name_plural = 'Tentatives de quiz'
        unique_together = ('student', 'quiz')
        ordering = ['-attempted_at']
        
    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} - Score: {self.score}"