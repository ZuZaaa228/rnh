from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Почта',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True,
                                    verbose_name='Активный')
    is_admin = models.BooleanField(default=False,
                                   verbose_name='Администратор')

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def str(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Appeal(models.Model):
    PRIORITY_CHOICES = (
        ('св', 'Самый высокий',),
        ('вы', 'Высокий',),
        ('ср', 'Средний',),
        ('ни', 'Низкий'),
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название обращения'
    )
    priority = models.CharField(
        choices=PRIORITY_CHOICES,
        max_length=3,
        default='ни'
    )
    text_appeal = models.TextField()
    author = models.OneToOneField(MyUser, on_delete=models.CASCADE,
                                  verbose_name='Клиент')
    is_activate = models.BooleanField(verbose_name='Активно ли обращение',
                                      default=True)

class Message(models.Model):
    appeal = models.OneToOneField(Appeal, on_delete=models.CASCADE)
    sender = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(editable=False,
                                auto_now_add=True)