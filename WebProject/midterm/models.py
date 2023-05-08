from django.db import models

# Create your models here.
class Staff(models.Model):
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=30)
    rank = models.CharField(max_length=100)
    image = models.ImageField(upload_to='midterm/images/%Y/%m/%d/',blank=True) 

 #__str__() 메소드는 해당 객체를 출력할 때 출력될 문자열을 반환합니다. 
# 위 코드에서는 [해당 객체의 pk] 제목 형식의 문자열을 반환하도록 구현되어 있습니다.
    def __str__(self):
        return f'{self.name}[{self.rank}]'
 
 #메소드는 해당 Post 객체의 상세 페이지 URL을 반환하는 메소드입니다. 위 코드에서는 /blog/<게시물번호>/ 
 #형태로 반환하도록 구현되어 있습니다. 이를 urls.py와 연결하여 상세 페이지를 생성할 수 있습니다.
    
    def get_absolute_url(self):
        return f'/midterm/list/{self.pk}/'
    
    def get_absolute_url2(self):
        return f'/midterm/list/{self.pk}/alter/'
    