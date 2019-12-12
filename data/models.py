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
    sum_review_score = models.FloatField(default=0)
    review_count = models.IntegerField(default=0)
    average_review_score = models.FloatField(default=0)

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
    def save(self, *args, **kwargs):
        if not self.pk:
            Data.objects.filter(pk=self.data_id).update(review_count=F('review_count')+1)
            Data.objects.filter(pk=self.data_id).update(sum_review_score=F('sum_review_score')+self.rate)
            Data.objects.filter(pk=self.data_id).update(average_review_score=Round(F('sum_review_score')/F('review_count'), 1))
        super().save(*args, **kwargs)
    
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
    

