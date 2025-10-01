from django.contrib.auth.models import BaseUserManager

class MyUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        # creating model
        # first normalize email, and then pass the rest keyvalue pairs to the model using - **extra_fields
        user = self.model(
            email = self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        # if value for this field present - return that value
        # else - add this field with this default value in dictionary
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(email, password, **extra_fields)