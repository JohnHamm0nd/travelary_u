from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.urls import reverse
from django.db.models import F, Func # 리뷰점수, 저장 계산을 위한 라이브러리

# Create your models here.Create
class Data(models.Model):
    
    menu = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100) 
    businessCategory = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    desc = models.CharField(max_length=100, null=True)
    microReview = models.CharField(max_length=100, null=True)
    tags = models.CharField(max_length=100, null=True)
    options = models.CharField(max_length=100)
    totalReviewCount = models.IntegerField()
    roadAddr = models.CharField(max_length=100)
    commonAddr = models.CharField(max_length=100)
    addr = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    x = models.FloatField()
    y = models.FloatField()
    imageSrc = models.CharField(max_length=300)
    # 리뷰점수(리뷰점수합, 카운트, 리뷰평균점수)
    sum_review_score = models.FloatField(default=0, null=True)
    review_count = models.IntegerField(default=0, null=True)
    average_review_score = models.FloatField(default=0, null=True)

def post_image_path(instance, filename):
    return 'reviews/{}/{}'.format(instance.review.pk, filename)
    
class Review(models.Model):
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    content = models.TextField()
    rate = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse('data:detail', kwargs={'pk': self.data_id})
    
    # 리뷰 카운트, 리뷰점수, 평균점수 저장을 위해 form save 방법 변경. update 를 사용하여 Data 모델에 있는 필드 값 변경
    # view에서 save함수를 두번 사용 하는 것을(사진이 있는 경우 form을 저장하고 image_formset을 저장) 수정해 사진이 있는 경우에도 한번에 저장하는 방법을 사용하려고 했으나 잘 안됨.
    # 다른방법(데이터에 있는 리뷰점수에서 자신의 이전 리뷰 점수를 빼고 새로 들어오는 리뷰 점수를 더한다 - 리뷰 수정하는 것을 구현하면 해결은 되는데 save함수를 두번 호출한다=비효율적)
    # 1. Date.sum_review_score에 review.rate(salf.rate)를 더함 -> 2. Date.sum_review_score에 review.rate(orm사용하여 Review db에서 가져온 rate)를 뺌
    # 3. Date.sum_review_score에 review.rate(salf.rate)를 더함
    # 리뷰를 새로 생성 할때에는 if, else문 - 수정 할 때에는 else문, else문 2번씩 실행하기 때문에 비효율적.(결과물에 이상은 없다)
    def save(self, *args, **kwargs):
        if not self.pk:
            Data.objects.filter(pk=self.data_id).update(review_count=F('review_count')+1)
            Data.objects.filter(pk=self.data_id).update(sum_review_score=F('sum_review_score')+self.rate)
            Data.objects.filter(pk=self.data_id).update(average_review_score=Round(F('sum_review_score')/F('review_count'), 1))
        else:
            pre_rate = Review.objects.get(pk=self.pk).rate
            Data.objects.filter(pk=self.data_id).update(sum_review_score=F('sum_review_score')-pre_rate+self.rate)
            Data.objects.filter(pk=self.data_id).update(average_review_score=Round(F('sum_review_score')/F('review_count'), 1))
        super().save(*args, **kwargs)
    
    # 리뷰 카운트, 리뷰점수, 평균점수 저장을 위해 form save 방법 변경. update 를 사용하여 Data 모델에 있는 필드 값 변경
    def delete(self, *args, **kwargs):
        Data.objects.filter(pk=self.data_id).update(review_count=F('review_count')-1)
        Data.objects.filter(pk=self.data_id).update(sum_review_score=F('sum_review_score')-self.rate)
        if Data.objects.get(pk=self.data_id).review_count == 0:
            Data.objects.filter(pk=self.data_id).update(average_review_score=0)
            Data.objects.filter(pk=self.data_id).update(sum_review_score=0)
        else:
            Data.objects.filter(pk=self.data_id).update(average_review_score=Round(F('sum_review_score')/F('review_count'), 1))
        super().delete(*args, **kwargs)
    
    
    class Meta:
        ordering = ['-created_at']

# Func 함수를 받아서 반올림 함수 만들어 사용
class Round(Func):
  function = 'ROUND'
  # arity = 2

class Image(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    image = ProcessedImageField(
                            upload_to=post_image_path,
                            blank = True,
                            null = True,
                            processors=[ResizeToFill(716,537)],
                            format="JPEG",
                            options={'quality':100},
                                    )
    

