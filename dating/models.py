from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from dating.utils.watermark import create_watermark


class MyClientManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email должен быть установлен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class Client(AbstractBaseUser):
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
    is_superuser = models.BooleanField(default=False, help_text='У этого пользователя есть все разрешения',
                                       verbose_name='Суперпользователь')

    objects = MyClientManager()
    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        if self.avatar:
            avatar_with_watermark = create_watermark(self.avatar)
            temp_name = self.avatar.name

            self.avatar.save(
                temp_name,
                content=avatar_with_watermark,
                save=False
            )
            super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'


class Sympathy(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, related_name='client')
    client_liked = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, related_name='client_liked')
