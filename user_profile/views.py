from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from data.models import Data
from .models import User_Profile
from data.models import Review
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from timetable.models import Timetable
# Create your views here.

class ProfileList(LoginRequiredMixin,ListView):
    model = Timetable
    paginate_by = 30
    template_name = 'user_profile/user_profile_list.html'
    
    # def get_queryset(self):
    #     data = Data.objects.filter(name=self.request.GET['name'])
    #     # paginator = Paginator(data, 5)
    #     # page = self.request.GET.get('page')
    #     # datas = paginator.get_page(page)
    #     return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        # list_exam = Data.objects.all()
        user = self.request.user
        timetable_current = Timetable.objects.filter(user=user)
        list_exam = Data.objects.filter(Q(timetable__in=timetable_current))
        paginator = Paginator(list_exam, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
        context['list_exams'] = file_exams
        try:
            context['user_profile'] = self.request.user.user_profile
        except User_Profile.DoesNotExist:
            pass
        
        context['review_list'] = Review.objects.filter(user=self.request.user)
        
        return context



class ProfileCreate(LoginRequiredMixin,CreateView):
    model = User_Profile
    fields = ['image_profile','age','gender', 'content']
    
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        
        return super().form_valid(form)
    
class ProfileUpdate(LoginRequiredMixin,UpdateView):
    model = User_Profile
    fields = ['image_profile','age','gender', 'content']
    
class ProfileDelete(LoginRequiredMixin,DeleteView):
    model = User_Profile
    success_url = reverse_lazy('user_profile:base')