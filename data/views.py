from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from .models import Data, Review, Image
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReviewForm, ImageForm, ImageFormSet
from django.db import transaction

# Create your views here.

class DataList(ListView):
    model = Data
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

        if self.request.GET.get('name', False):
            if self.request.GET.get('location', False):
                list_exam = Data.objects.filter(Q(name__contains=self.request.GET['name']) & (Q(commonAddr__contains=self.request.GET['location'])|Q(addr__contains=self.request.GET['location'])))
                list_exam = list_exam.order_by('-totalReviewCount')
            else:
                list_exam = Data.objects.filter(name__contains=self.request.GET['name'])
                list_exam.order_by('-totalReviewCount')

        elif self.request.GET.get('location', False):
            list_exam = Data.objects.filter(Q(commonAddr__contains=self.request.GET['location'])|Q(addr__contains=self.request.GET['location']))
            list_exam = list_exam.order_by('-totalReviewCount')
        elif self.request.GET.get('menu', False) == '1':
            list_exam = Data.objects.filter(menu__in=[1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
            list_exam = list_exam.order_by('-totalReviewCount')
        elif self.request.GET.get('menu', False) == '2':
            list_exam = Data.objects.filter(menu__in=[2])
            list_exam = list_exam.order_by('-totalReviewCount')
        elif self.request.GET.get('menu', False) == '19':
            list_exam = Data.objects.filter(menu__in=[19])
            list_exam = list_exam.order_by('-totalReviewCount')
        else:
            list_exam = Data.objects.all()
            list_exam = list_exam.order_by('-totalReviewCount')

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

class DataDetail(DetailView):
    model = Data

class ReviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    # fields = ['image', 'content', 'rate']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_formset'] = ImageFormSet()
        return context

    def form_valid(self, form):
        image_formset = ImageFormSet(self.request.POST, self.request.FILES)

        with transaction.atomic():
            form.instance.user = self.request.user
            form.instance.data_id = self.kwargs.get('data_id')
            self.object = form.save()

            if image_formset.is_valid():
                image_formset.instance = self.object
                image_formset.save()

        return super().form_valid(form)

class ReviewList(ListView):
    model = Review
    paginate_by = 30
    
    def list(request):
        # 전체 목록을 보여주는 코드
        review_list = Review.objects.all()
        paginator = Paginator(review_list, 5)
        page = request.GET.get('page')
        
        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
        context['review_list'] = file_exams
        return context
        








    # def list(request):
    # # 전체 목록을 보여주는 코드
    # questions_list = Question.objects.all()
    # paginator = Paginator(questions_list, 5)
    # page = request.GET.get('page')
    # questions = paginator.get_page(page)
    # return render(request,'question/list.html',{'questions':questions})
    
    
    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['post_user'] = self.post_user 
    #     return context
