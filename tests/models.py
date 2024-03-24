from django.db import models

# Create your models here.
class TestCase(models.Model):
    task = models.TextField('Вопрос')
    answer = models.CharField('Ответ', max_length=2048)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f"Задание №{self.pk}"
