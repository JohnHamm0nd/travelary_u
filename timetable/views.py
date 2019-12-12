from django.shortcuts import render,get_object_or_404, resolve_url, redirect
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView
import json
from django.http import HttpResponse
from timetable.models import Timetable
from data.models import Data
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
# Create your views here.

class Timetable_Base(LoginRequiredMixin,TemplateView):
    template_name='timetable/timetable_base.html'

class Timetable_List(LoginRequiredMixin,ListView):
    model = Data
    template_name='timetable/timetable_list.html'
    paginate_by = 30
    
    # def get_queryset(self):
    #     data = Data.objects.filter(name=self.request.GET['name'])
    #     # paginator = Paginator(data, 5)
    #     # page = self.request.GET.get('page')
    #     # datas = paginator.get_page(page)
    #     return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        # list_exam = Data.objects.all()
        list_exam = Data.objects.filter(menu=self.request.GET['menu'])
        paginator = Paginator(list_exam, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
        context['list_exams'] = file_exams
        return context

    
@login_required
def wish(request,pk):
    if request.is_ajax():
        user = request.user
        data = Data.objects.get(pk=pk)
        # 사용자가 like를 눌렀으면 취소
        print(request.user)
        print(data)
        if Timetable.objects.filter(user=user).filter(data_origin=data).exists():
            print("지우자!!!!")
            Timetable.objects.filter(user=user).filter(data_origin=data).delete()
        # 안눌렀으면 좋아요
        else:
            tt = Timetable(user=user, data_origin=data)
            tt.save()
        data_wish = {'wishes_count' : Timetable.objects.filter(data_origin=data).count()}
        return HttpResponse(json.dumps(data_wish), content_type="application/json")
        
    else:
        return redirect(resolve_url('data:list',pk) )
        
