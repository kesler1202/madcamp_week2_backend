from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Custom User Manager
# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password, name, nickname, class_group, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        if not password:
            raise ValueError('The Password must be set')
        if not name:
            raise ValueError('The Name must be set')
        if not nickname:
            raise ValueError('The Nickname must be set')
        if not class_group:
            raise ValueError('The Class Group must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, nickname=nickname, class_group=class_group, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, name, nickname, class_group, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, name, nickname, class_group, **extra_fields)

# User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=30, unique=True)
    class_group = models.CharField(max_length=10,
                                   choices=[('1', 'Group 1'), ('2', 'Group 2'), ('3', 'Group 3'), ('4', 'Group 4')],
                                   default='1')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    post_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'nickname', 'class_group']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        """
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        # Simplest possible answer: Yes, always
        return True

# Post Model
class Post(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Comment Model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.writer} on {self.post}'