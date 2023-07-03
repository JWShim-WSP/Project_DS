from django.db import models
# Create your models here.
from django.utils import timezone
from django.db import models
from django.urls import reverse

def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)

PriorityChoices = (
    ('1', 'High'),
    ('2', 'Middle'),
    ('3', 'Low'),
)

class ToDoList(models.Model):
    title = models.CharField(max_length=100, unique=True)
    priority = models.CharField(choices=PriorityChoices, default='High', max_length=10)

    def get_absolute_url(self):
        return reverse("todolist:todoitemlist", args=[self.id])

    def __str__(self):
        return self.title

class ToDoItemList(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateField(default=one_week_hence)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    priority = models.CharField(choices=PriorityChoices, default='High', max_length=10)
    item_completed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse(
            "todolist:item-update", args=[str(self.todo_list.id), str(self.id)]
        )

    def __str__(self):
        return f"{self.title}: due {self.due_date}, Completed: {self.item_completed}"

    class Meta:
        ordering = ["due_date"]
