from datetime import datetime
from typing import List

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import Answer, Question


def answ(answers: List[Answer]):
    answers_list = []
    for answer in answers:
        answers_list.append({'id': answer.id, 'name': answer.name})
    return answers_list

def quest(question: Question):
    return { 'id': question.id, 'name': question.name, 'publish_at': str(question.publish_at), 'answers': answ(question.answer_set.all())}

def questions(request):
    data = []
    for question in Question.objects.filter(publish_at__lt=datetime.now()):
        data.append(quest(question))
    return JsonResponse(data, safe=False)