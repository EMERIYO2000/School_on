from django.db import models
from utilisateurs.models import CustomUser
from courses.models import Category
# Create your models here.

class ForumThread(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='forum_threads')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='forum_threads')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
class ForumPost(models.Model):
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='forum_posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted_solution = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Réponse de {self.author.username} sur le fil {self.thread.id}"