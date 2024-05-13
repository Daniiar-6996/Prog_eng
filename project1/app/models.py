from django.db import models

# Create your models here.
class Articles(models.Model):
    create_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, verbose_name='Фамилия')
    name_2 = models.CharField(max_length=200, verbose_name='Имя, отчество', default="")
    position = models.CharField(max_length=200, verbose_name='Должность', default="")
    adress = models.CharField(max_length=200, verbose_name='Адресс', default="")
    ph_num = models.CharField(max_length=200, verbose_name='Номер телефона', default="")
    
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name='Работника'
        verbose_name_plural='Работники'
