from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Products(models.Model):
    product_id = models.IntegerField()
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()

class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**other_fields):
        if not email:
            raise ValueError("No email provided")
        user = self.model(email= self.normalize_email(email),**other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"

