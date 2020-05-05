from datetime import datetime
from typing import List

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import Answer, Question


def answ(answers: List[Answer]):
    return [{ 'id': answer.id, 'name': answer.name} for answer in answers]

def quest(question: Question):
    return { 'id': question.id, 'name': question.name, 'publish_at': str(question.publish_at), 'answers': answ(question.answer_set.all())}

def questions(request):
    data = [quest(question) for question in Question.objects.filter(publish_at__gt=datetime.now())]
    return JsonResponse(data, safe = False)