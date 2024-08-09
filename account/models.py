from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, date_of_birth, password=None, password_confirmation=None):
        """
        Creates and saves a User with the given email, first name, last name, date of
        birth, password and password_confirmation.
        """
        if not email:
            raise ValueError("Users must have an email address")

        if password != password_confirmation:
            raise ValidationError("Passwords do not match")

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, first name, last name, date of
        birth, and password.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            password=password,
            password_confirmation=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "date_of_birth"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



# from django.db import models
# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# class MyUserManager(BaseUserManager):
#     def create_user(self, email, firstName, lastName, date_of_birth, password=None, password_confirmation=None):
#         """
#         Creates and saves a User with the given email, firstName, lastName, date of
#         birth, password and password_confirmation.
#         """
#         if not email:
#             raise ValueError("Users must have an email address")

#         user = self.model(
#             email=self.normalize_email(email),
#             date_of_birth=date_of_birth,
#             firstName=firstName,
#             lastName=lastName,
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, firstName, lastName, date_of_birth, password=None):
#         """
#         Creates and saves a superuser with the given email, firstName, lastName, date of
#         birth, password and password_confirmation.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#             firstName=firstName,
#             lastName=lastName,
#             date_of_birth=date_of_birth,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user


# class User(AbstractBaseUser):
#     email = models.EmailField(
#         verbose_name="email address",
#         max_length=255,
#         unique=True,
#     )
#     date_of_birth = models.DateField()
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     firstName = models.CharField(max_length=255)
#     lastName = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     objects = MyUserManager()

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["firstName", "lastName", "date_of_birth"]

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return self.is_admin

#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True

#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         # Simplest possible answer: All admins are staff
#         return self.is_admin
