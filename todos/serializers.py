from django.db import models
from rest_framework import serializers
from todos.models import Todo

class Todoserializer(serializers.ModelSerializer):
    todo = serializers.ReadOnlyField()
    class Meta:
        model = Todo
        fields = '__all__'