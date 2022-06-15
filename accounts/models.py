from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.validators import MinLengthValidator,MaxValueValidator
# Create your models here.

class MyUserManager(BaseUserManager):
   def create_user(self, email,phone,date_of_birth,register_number,is_data_entry):

       if not email:
           raise ValueError('Users must have an email address')
       if not phone:
           try:
               phone = int(phone)
           except:
                raise ValueError('Mobile number only number')
           raise ValueError('Users must have Mobile number')

       user = self.model(email=self.normalize_email(email))
       user.phone = phone
       user.date_of_birth = date_of_birth
       user.register_number = register_number
       user.is_data_entry = is_data_entry
       user.save(using=self._db)
       return user
 
   def create_superuser(self,email,phone,user_type,date_of_birth,register_number):

       user = self.create_user( email=email,phone=phone,user_type=user_type,
       date_of_birth=date_of_birth,register_number=register_number)

       if user_type == 'is_admin':
            user.user_type = 'is_admin'
       user.save(using=self._db)
       return user

   def create_staffuser(self,email,phone,user_type,date_of_birth,register_number):

       user = self.create_user(email=email,phone=phone,user_type=user_type,
       date_of_birth=date_of_birth,register_number=register_number)

       if user_type == 'is_staff':
            user.user_type = 'is_staff'
       user.save(using=self._db)
       return user


usertype_choice={
    ('-------','-------'),
    ('is_student','is_student'),
    ('is_staff','is_staff'),
    ('is_admin','is_admin'),
}




class User(AbstractBaseUser):
    register_number = models.CharField(max_length=15,unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(unique=True,
        default= 1234567890,
        max_length= 10,
        validators=[
            MinLengthValidator(10)
        ])
    date_of_birth = models.DateField(
        default= timezone.now
    )
    user_type = models.CharField(
        max_length=20,
        choices =usertype_choice,
        default='0',
        blank=True,
        null= True
    )
    is_data_entry = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.email

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
        return self.user_type == 'is_staff' or self.user_type == 'is_admin'

    @property
    def is_admin(self):
        return self.user_type == 'is_admin'


class Profile(models.Model):
    
    def upload_design_to(self, filename):
        return f'user_profile/{self.user.id}/{filename}'
    user = models.OneToOneField(User,on_delete=models.CASCADE,null =True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    full_name = models.CharField(max_length=30)
    profile_picture = models.ImageField(upload_to=upload_design_to,blank=False,null=True)
    standard = models.IntegerField(
        validators=[
            MaxValueValidator(12)
        ]
    )
    section = models.CharField(max_length=2)
    address = models.CharField(max_length=45)

    def __str__(self):
        return str(self.user)


class OTP(models.Model):

    email = models.EmailField()
    phone = models.CharField(
    default= 1234567890,
    max_length= 10,
    validators=[
    MinLengthValidator(10)
    ])
    otp = models.CharField(max_length=6)