from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView,DetailView
from .models import Staff

class StaffList(ListView): #얘는 그냥 post_list 변수를 받는다 
    model = Staff #post_list 변수 models.py에 있는 post
    template_name = 'midterm/list.html'
    

class StaffCard(DetailView): #예는 그냥 post 변수를 받아 온다 
    model = Staff
    template_name = 'midterm/name_card.html'
   
class StaffCard2(DetailView):
    model = Staff
    template_name = 'midterm/name_card2.html'

def index(request):
    return render(
        request,
        'midterm/index.html',
        {},
    )