from django.contrib import admin

# Register your models here.
# todo_list/todo_app/admin.py

from django.contrib import admin
from todolist.models import ToDoItemList, ToDoList

admin.site.register(ToDoItemList)
admin.site.register(ToDoList)