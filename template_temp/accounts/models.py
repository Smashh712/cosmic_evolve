from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, student_id, date_of_birth, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not student_id:
            raise ValueError("Users must have an email address")

        user = self.model(
            student_id=student_id,
            date_of_birth=date_of_birth,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_id, date_of_birth, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            student_id=student_id,
            password=password,
            date_of_birth=date_of_birth,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    student_id = models.IntegerField(verbose_name="학번", unique=True)
    name = models.CharField(max_length=10, verbose_name="이름")
    date_of_birth = models.DateField(verbose_name="가입일")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "student_id"
    REQUIRED_FIELDS = ["name", "date_of_birth"]

    def __str__(self):
        return str(self.student_id)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
