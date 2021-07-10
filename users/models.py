from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
)

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User
        """
        if not email:
            raise ValueError("User must have an valid email")

        email = self.model(email=email, first_name=first_name, last_name=last_name)

        email.set_password(password)
        email.save(using=self._db)
        return email

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser/admin.
        """
        user = self.create_user(
            email,
            None,
            None,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Enter Email",
        max_length=100,
        unique=True,
    )
    first_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Enter First Name"
    )
    last_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Enter Last Name"
    )
    is_staff = models.BooleanField(default=False, verbose_name="Staff")
    is_superuser = models.BooleanField(default=False, verbose_name="Admin")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # class Meta:
    #    db_table = "login"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
