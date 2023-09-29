from django.db import models
from django.utils.html import mark_safe
from .limit import SingletonModel

class the_product(models.Model):
    period_choices = (
        ('1',"one_months"),
        ('3',"three_months"),
        ('6',"six_months"),
    )
    users = (
        ('1','one'),
        ('2','two'),
        ('3','three'),
        ('4','four'),
        ('5','five'),
    )
    product = models.CharField(max_length=50, verbose_name="product")
    price = models.IntegerField(verbose_name="price",default=50)
    pic_sample = models.ImageField(upload_to="images", verbose_name='picture')
    description = models.TextField(verbose_name="description")
    period = models.CharField(max_length=1,choices=period_choices,verbose_name="period",default='1')
    max_users = models.CharField(max_length=1,choices=users,verbose_name="Users_in_same_time",default='1')
    def __str__(self):
        return self.product
    
    def pic_sample_preview(self):
        return mark_safe(f'<img src = "{self.pic_sample.url}" width = "120" height="120" style="border-radius: 5px"/>')
    pic_sample_preview.short_description = 'thumbnail'


class page_pic(SingletonModel):
    website_pic = models.ImageField(upload_to="images", verbose_name='website_pic')
    class Meta:
        verbose_name = 'website_pic'
        verbose_name_plural = 'website_pic'
    