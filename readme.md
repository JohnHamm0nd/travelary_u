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
    'django.contrib.staticfiles.finders.FileSystemFinder'`
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

앱(, data, review, user_profile)





## - view

##### 트레블러리

django.views.generic 에 있는 TemplateView 를 임포트, 상속받아 메인페이지 사용(사용된 템플릿은 index.html)

##### accounts

SignUp 클래스 - accounts 에서 register url로 요청을 받아 'accounts/register.html' 템플릿에 forms.UserCreateForm (forms.py) 넣어 전달해줌

장고(django.views.generic)의 CreateView를 상속받아 만듬, 

forms의 UserCreateForm을 사용

'accounts/register.html' 템플릿 사용

reverse_lazy사용( 정확히 무슨역할이었지? )



앱(, data, review, user_profile)



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

tttttt

앱(, data, review, user_profile)







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