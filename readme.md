# Django - Travelary

## - templates

```python
{% load staticfiles %}
```

정적 파일

웹 페이지를 랜더링 하는데 필요한 파일들을 로드(자바스크립트, CSS, 이미지 등)

일반적으로 장고 프로젝트 안에 static 이라는 폴더를 만들어 그 안에 넣는다.

프로젝트의 settings.py 에서 STATICFILES_DIRS 에서 경로를 지정해 주어야 한다.

프로젝트의 각 App 마다 Static 폴더를 지정할 수 있는데 이 때에는 steeings.py 에서 STATICFILES_FINDERS 변수를 설정해야 한다.

```python
STATICFILES_FINDERS =(
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
```

장고에서는 각 App의 static 폴더를 'App명/static/App명' 으로 둘 것을 권장한다. 이는 각 App 안의 static 폴더 밑의 내용을 그대로 복사하므로 동일한 이름의 파일들이 충돌하지 않게 하기 위함이다.

```python
{% load 장고 라이브러리명 %}
```

장고 라이브러리 로드

실제 설치한 라이브러리명과 사용되는 라이브러리명이 다르기도 하나?

{% load bootstrap3 %} 의 경우에는 라이브러리에도 django-bootstrap3 인데
{% load socialaccount %} 의 경우는 django-allauth 이다. allauth 안에 있는 socialaccount 를 불러온다.



```python
{% extends '상속받을 템플릿명' %}
{%extends 'base.html'%}
```

상속의 개념

동일한 스타일 등의 중복되는 HTML/CSS 코드가 많을 때 사용.

```python
{% block '블럭명' %}
{% endblock %}
{%block body%}
{%endblock%}
```

페이지에 구멍을 내는 것이라고 생각.

템플릿(A)에서 다른 템플릿(B)을 상속 받으면 상속받은 B가 A를 덮어 A가 보이지 않게 된다.

그래서 템플릿 B에 미리 block 으로 구멍(block_C)을 뚫어 놓고 A 에 상속을 하면 다른 부분은 B 가 덮고 있지만 block_C 는 구멍이 뚫려 있으므로 이 부분을 통해 템플릿 A를 볼 수 있게 된다.

구멍을 여러개 뚫는 것도 가능하며, 상속할 템플릿에 구멍을 만들어 놓고(B)

{%block body%}
{%endblock%}

상속받는 템플릿에서 그 구멍에 맞춘 후 그 안에 코딩을 하면 된다.(A)

{%block body%}

템플릿 A에서 사용할 코드

{%endblock%}

```python
is_authenticated
is_anonymous
{% if user.is_authenticated %}
{% if user.is_anonymous %}

is_active
{% if user.is_active %}
```

is_authenticated - 로그인 여부 체크

is_anonymous - 로그아웃 여부 체크

is_active - 유저의 활성, 비활성 여부 체크

```python
csrf_token
{%csrf_token%}
```

**CSRF 공격이란?**
CSRF 공격(Cross Site Request Forgery)은 웹 어플리케이션 취약점 중 하나로, 인터넷 사용자(희생자)가 자신의 의지와는 무관하게 공격자가 의도한 행위(수정, 삭제, 등록 등)를 특정 웹사이트에 요청하게 만드는 공격

이러한 공격으로부터 POST 방식의 폼 전송에 임의의 키 값을 넣어 유효한지 확인한 후 처리하게 한다.

form 안에  {%csrf_token%} 를 넣어 사용하면 된다.

프로젝트 settings.py 의 MIDDLEWARE 변수에 'django.middleware.csrf.CsrfViewMiddleware' 를 추가.( 장고 프로젝트를 만들어 이미 추가 되어 있을 것이다. )

```python
providers_media_js
{% providers_media_js %}
```

페이스북, 구글 등 다른 계정으로 로그인 할 수 있게 만들 때 쓰임. 자바스크립트를 사용.

그 외에도 아마존, 다음, 드랍박스, 깃허브, 네이버 스팀, 트위터, 트위치 등도 사용가능( 각 사이트의 개발자 페이지에서 작업 필요 )



## - model

#### user_profile


장고에서　pk　값을　지정하지　않을　경우　별도로　id　값을　만들어　pk로　지정한다．
models 의 model 을 상속받아 사용. ( content, age, gender 필드 )

django.contrib.auth.models 의 User모델을 유저모델로 사용.

imagekit.models 의 ProcessedImageField 를 사용하여 이미지필드 사용.
imagekit.processors 의 ResizeToFill 을 사용하여 이미지 리사이즈 처리.

django.core.validators 의 MinValueValidator, MaxValueValidator

최소값, 최대값.

from django.urls import reverse ----- ???????????????????????



#### accounts

auth 에 있는 auth.models.User, auth.models.PermissionsMixin 을 그대로 사용??



#### data

models 의 model 을 상속받아 사용.

id 는 primary key 로 지정, 다른 변수들(menu, name 등)도 각각 지정



#### Review

데이터 앱 안에 같이 있음. (따로 만들었으면 나중에 재사용하기가 더 편했을듯)

models 의 model 을 상속받아 사용.

Data, settings.AUTH_USER_MODEL 을 외래키로 사용

 (Data 자체를 외래키로 사용하는건가? id 를 사용하는거 아닌가? 왜 그냥 Data 로 되어있나?, 

settings.AUTH_USER_MODEL 는 뭐였지? accounts 모델이 아니고 왜 settings.AUTH_USER_MODEL 를 외래키로 사용하는거지?)



## - urls

##### 트레블러리

admin 페이지

메인페이지

accounts 페이지

data 페이지

user_profile페이지

timetable페이지(사용 X)

의 URL 패턴을 '앱명/', include('앱명.urls') 를 사용하여 하위 앱들에 있는 URL 패턴까지 모두 등록?사용? -> 앱 폴더에 있는 urls.py 안의 url 패턴을 가져와 사용하는듯

accounts 의 경우에는 allauth.urls 를 사용하였는데 어떻게 작동하는지 ???

어디서 가져오느지를 모르겠다...

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) ----- ???



##### accounts

register: views의 SignUp클래스의 as_view() 호출

signin: 임포트한 라이브러리 auth_views.LoginView.as_view() 메소드를 호출하여 'accounts/signin.html' 템플릿에 담아 전달

( register의 경우 views 에서 정의를 하고 링크를 클릭 하였을 때 views에 정의한 클래스, 메소드를 호출하면 그 안에서 템플릿에 넣어서 전달해 줬는데 signin의 경우 urls 에서 바로 라이브러리를 임포트 하여 views 까지 가지 않고 바로 메소드를 호출하여 전달하였다. )

1. register 와 같이 라이브러리를 views 에서 임포트 하고 urls 에서는 호출만하고 view에 대한 처리는 views 에서 하면 안되나? -> 될것으로 보이긴 함.
2.  signin 처리를 지금처럼 하는 경우 views.py 에 갔다오지 않아도 되므로 앱이 조금더 빠르지 않을까? 라는 생각은 든다, 반면에 urls.py 에서 메소드를 호출만 하는 경우와. 메서드 호출, 템플릿 처리를 한번에 하는 경우가 섞여 있기 때문에 재사용시에도 불편할 수 있고 수정, 코드 가독성, 이해가 떨어 질 수 있을 것 같다. 

signout: 임포트한 라이브러리 auth_views.LogoutView.as_view() 메서드 호출하여 처리.



##### data

list - 트레블러리 메인페이지, 데이터 리스트 페이지에서 검색 할 때 ( 값은 자바스크립트에서 긁어와서 views.py 에 주는데, 어떻게 주는지 모르겠다. 회원가입 시에도 그렇고 어떤 입력이 있는 페이지에서 입력 후 버튼 등을 누르면 그 값을 urls -> views 에 넘겨 주어야 하는데 템플릿에는 그런게 안보이고 어디있는 건지 안보인다.... )

get_context_data 함수 사용 떄문인지

장고에서 template_name 속성을 지정하지 않으면 장고는 템플릿을 유추해서 사용한다고 한다. 그래서 템플릿 지정 없이도 동작하는 것 같다. 

detail - 지점 클릭시 지점의 id(pk)값을 넣어 views.py의 DataDetail.as_view() 함수 호출 ( DataDetail 클래스 안의 as_view()함수 - 상속받은 DetailView 안에 있음. )

reviewcreate - 지점id/reviewcreate/유저id url 로 views.py의 ReviewCreate.as_view() 함수 호출 ( ReviewCreate 클래스 안의 as_view()함수 - 상속받은 CreateView 클래스 안에 있음. ) 상속받은 다른 클래스 LoginRequiredMixin 은 로그인 여부에 사용하는듯?

reviewlist - views.py의　ReviewList클래스의　as_view()함수　호출．

##### user_profile
base - views.py의　ProfileList클래스의　as_view()　호출
create - create/ url로　views.py의　ProfileCreate클래스의　as_view()　호출
update - update/id url로　views.py의　ProfileUpdate클래스의　as_view()　호출
delete - delete/id url로　views.py의　ProfileDelete클래스의　as_view()　호출



## - view

##### 트레블러리

django.views.generic 에 있는 TemplateView 를 임포트, 상속받아 메인페이지 사용(사용된 템플릿은 index.html)



##### accounts

SignUp 클래스 - accounts 에서 register url로 요청을 받아 'accounts/register.html' 템플릿에 forms.UserCreateForm (forms.py) 넣어 전달해줌

장고(django.views.generic)의 CreateView를 상속받아 만듬, 

forms의 UserCreateForm을 사용

'accounts/register.html' 템플릿 사용

reverse_lazy사용( 정확히 무슨역할이었지? )



##### data

DataList - ListView 클래스를 상속받아 사용, urls.py 에서 넘어오면? ( 여기서 넘어오는 것으로 보임.. ) 

model 로 Data( data 앱의 Data 클래스 ) 사용 

paginate_by - 한 페이지에 30개씩

get_context_data ?? 정확하게 무슨역할?

self.request.Get.get 을 사용하여 자바스크립트로 긁어온 name과 location 변수를 얻어와 Data 모델에 쿼리

모델명.objects.all() 은 모든  데이터를 가져오는것

모델명.objects.filter() 는 조건 검색

Q 는 쿼리를 날리는 명령 name__contains=self.request.GET['name'] 은 모델 안의 name 속성에서 self.request.GET 한 'name' 변수가 포함된 (완전일치가 아니라 포함, 완전일치일 경우 name=self.request.GET['name']) 데이터를 가져온다.

& 는 and 연산자, | 는 or 연산자.

list_exam.order_by('-totalReviewCount') 에서 order_by 는 데이터의 변수 'totalReviewCount' 를 기준으로 정렬, - 는 내림차순 정렬.

self.request.GET.get('menu', False) == '1':

self.request.GET.get('menu', False) == '2':

self.request.GET.get('menu', False) == '19': 

가 있는 것은 트레블러리 메인 페이지에서 검색 아래에 있는 레스토랑, 카페, 호텔 클릭시 검색

그 밑 else 문은 아무것도 입력하지 않고 검색 했을 시 모든 데이터.

여기서도 의문점??? urls.py -> views.py -> 리턴 하는데 data_detail.html 템플릿을 읽어오는 코드가 안보인다. 어디서 이 일을 하고 있는가? 

-> urls.py 에 적어두었다.

context['list_exams'] = file_exams 에서 은 paginate 30개씩 한 결과물이고 context['list_exams'] 은 data_detail.html 에 있는  {%for data in list_exams%} 에 데이터를 넣는 코드

그 후 context 를 리턴.

DataDetail - DetailView 클래스 상속

model 로 Data 클래스 사용

다른 함수나 리턴 없이 작동하는 것으로 보면 삭속받은 DetailView 클래스 에서 data_detail.html 알아서 잘 가져와 사용하는듯....

ReviewCreate - LoginRequiredMixin, CreateView 클래스 상속받아 사용
모델 - models.py의 Review사용
폼플래스 - forms.py 의 ReviewForm사용

ReviewList - Listview　상속받아　사용
모델 - models.py의　Review사용

##### user_profile

ProfileList - LoginRequiredMixin, ListView상속
LoginRequiredMixin　－　로그인　여부
model - Timetable 모델　사용
template_name = 'user_profile/user_profile_list.html'　으로　템플릿　지정．
다행히　여기　클래스에서는　view에서　템플릿을　지정해줬다（안헷갈린다）
ProfileCreate - LoginRequiredMixin, CreateView상속
model - User_Profile모델　사용（User_Profile 앱에있는　모델）
forms.py가　없는데　여기서　처리하는건가？

ProfileUpdate - LoginRequiredMixin, UpdateView상속
model - User_Profile모델　사용
ProfileDelete - LoginRequiredMixin, DeleteView상속
success_url = reverse_lazy('user_profile:base')　－＞　reverse_lazy 알아보자


## - forms

##### 트레블러리

##### accounts

UserCreationForm 임포트 하여 사용.

fields 로 username, email, password1, password2 사용.

model 로 get_user_model() 임포트 하여 사용.

-> 여기서 입력을 하고 회원가입을 누르면 어떻게 작동하는지 모르겠다. 

views.py에 success_url = reverse_lazy('accounts:signin') 과 연관되어 있는것 같은데??

또 데이터가 어떻게 전달되고 어디로 전달되는지 보이지가 않는데 어떻게 전달되서 저장이 되는건지 모르겠다. 

{% bootstrap_form form %} 에 담겨서 전달하나?

##### data

ReviewForm

ImageForm





앱(, data, )

user_profile　－＞　forms.py가　없다？？？





## - settings.py

INSTALLED_APPS

내가 만든 앱 + 만들 때 임포트 했던 라이브러리들 까지도 추가해 줘야 하는듯



시간설정(한국시간, 모델에서도 설정한 시간 사용)

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False



데이터 업로드시 제한 설정(기본값은 더 낮음-제한을 높임)

DATA_UPLOAD_MAX_NUMBER_FIELDS = 200000
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800

##
##
##

# 지금　헷갈리는것
urls.py 에서　views.py로　넘기는　인자가　없는데　어떻게　동작하고　있는거지？
views.py에서는　함수들　선언　후　호출하는　작업이　없는에　어떻게　함수들이　동작하고　있는거？


내가　이해하고있는　장고　mvc　작업은　이건데　url에서　템플릿　지정이　없고，　넘겨주는　인자도　없고
view 에서　함수　선언만　있고　호출작업이　없는데　어떻게　작업해서　리턴하는건지　모르겠다．

|url|view|model|
|---:|---:|---:|
|요청(인자)　->|SQL(인자)(장고에서는 request로　사용)->|받은　인자로　데이터　검색，수정，입력　등　작업|
|템플릿지정，해당　url로　템플릿　받음|템플릿＋데이터　리턴|＜－데이터　등　결과물　리턴|

userprofile　앱은　forms.py도　없는데？　
view.py 에　있는　create, update 는　상속받은　CreateView，UpdateView　에　fields　변수에　필드값　지정하여　바로　처리　하는듯..
그래도　헷갈리는건　data나　accounts에　forms.py 보면　상속받을떄도　ModelForm，UserCreationForm　같은　폼을　상속받는데.... 얘는　왜？？？