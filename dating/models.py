from django.db import models

class Client(models.Model):
    """
    Участник
    """

    gender_choices = (
        ('m', 'male'),
        ('f', 'female'),
    )

    email = models.EmailField(max_length=255, unique=True, verbose_name='Почта')
    name = models.CharField(max_length=20, verbose_name='Имя')
    surname = models.CharField(max_length=20, verbose_name='Фамилия')
    password = models.CharField(max_length=128, verbose_name='Пароль')
    gender = models.CharField(max_length=1, choices=gender_choices, verbose_name='Пол',
                              help_text='Введите m(male) или f(female)', )
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', verbose_name='Аватарка')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
