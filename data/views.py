from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Data, Review, Image
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReviewForm, ImageForm, ImageFormSet
from django.db import transaction
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

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
                list_exam = list_exam.order_by('-review_count')
            else:
                list_exam = Data.objects.filter(name__contains=self.request.GET['name'])
                list_exam.order_by('-review_count')

        elif self.request.GET.get('location', False):
            list_exam = Data.objects.filter(Q(commonAddr__contains=self.request.GET['location'])|Q(addr__contains=self.request.GET['location']))
            list_exam = list_exam.order_by('-review_count')
        elif self.request.GET.get('menu', False) == '1':
            list_exam = Data.objects.filter(menu__in=[1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
            list_exam = list_exam.order_by('-review_count')
        elif self.request.GET.get('menu', False) == '2':
            list_exam = Data.objects.filter(menu__in=[2])
            list_exam = list_exam.order_by('-review_count')
        elif self.request.GET.get('menu', False) == '19':
            list_exam = Data.objects.filter(menu__in=[19])
            list_exam = list_exam.order_by('-review_count')
        else:
            list_exam = Data.objects.all()
            list_exam = list_exam.order_by('-review_count')

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


    # 문제 : 리뷰를 저장할때 폼을 저장하고 사진이 있으면 이미지 폼에 넣어 한번 더 저장하는데 model에서 save를 두번 하기 때문에(한번은 처음저장이라 pk가 없고 이미지폼 저장시에는 self.pk가 있음)
    # 리뷰 점수가 두번 업데이트 되는 문제가 발생.
    # model은 수정할 때 self.pk 여부에 따라서 작동해야 하므로 model은 유지하고 여기서 수정을 해야 할 것 같다.(한번에 저장하는 방법으로 변경)
    def form_valid(self, form):
        image_formset = ImageFormSet(self.request.POST, self.request.FILES)

        with transaction.atomic():
            """
            if image_formset.is_valid():            
                form.instance.user = self.request.user
                form.instance.data_id = self.kwargs.get('data_id')
                self.object = form.save()
                image_formset.instance = self.object
                image_formset.save()
            else :
                form.instance.user = self.request.user
                form.instance.data_id = self.kwargs.get('data_id')
                self.object = form.save()
            """
            form.instance.user = self.request.user
            form.instance.data_id = self.kwargs.get('data_id')
            self.object = form.save()

            if image_formset.is_valid():
                image_formset.instance = self.object
                image_formset.save()
        
        return super().form_valid(form)
        

class ReviewUpdate(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    # fields = ['image', 'content', 'rate']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_formset'] = ImageFormSet(instance=self.object) # instance로 self.object를 가져와 기존에 있던 파일을 가져옮(하지만 삭제, 수정이 안된다..)
        return context

    def form_valid(self, form):
        image_formset = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object) # instance=self.object 를 추가해야 수정이 된다.

        with transaction.atomic():
            form.instance.user = self.request.user
            form.instance.data_id = self.kwargs.get('data_id')
            self.object = form.save()

            if image_formset.is_valid():
                image_formset.instance = self.object
                image_formset.save()

        return super().form_valid(form)

class ReviewDelete(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'data/review_delete.html'
    
    def get_success_url(self): # 요청에 성공하였을 때 보낼 url - 아직 정확하게 어떤 함수인지 감이 덜왔음.
        return reverse('data:detail', kwargs={'pk': self.kwargs.get('data_id')})  # self에 kwargs에서 get을 사용하여 data_id를 가져와 data_id 디테일페이로 보냄.
    
    def dispatch(self, request, **kwargs): # 정확히 무슨 함수인지 모르겠다, 일단 템플릿 페이지에서 유저가 쓴 글이 아니면 수정, 삭제 버튼이 보이지 않게 하였지만, 이 함수에서 get_object의 유저와 request의 유저가 같은지 확인하여 진행한다.
        object = self.get_object()
        if object.user != request.user:
            messages.warning(request, '삭제할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else:
            return super(ReviewDelete, self).dispatch(request, **kwargs)
    
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
