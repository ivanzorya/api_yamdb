from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,  email, username=None, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        if not username:
            username = email
        user.username = username
        user.save(using=self._db)
        return user


class User(SimpleEmailConfirmationUserMixin, AbstractBaseUser):

    class Role(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    first_name = models.TextField(null=True)
    last_name = models.TextField(null=True)
    username = models.TextField(null=True, unique=True)
    bio = models.TextField(null=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
    )
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField()
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2500)
        ]
    )
    rating = models.PositiveIntegerField(null=True)
    description = models.TextField(null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(Genre)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Review(models.Model):

    class Score(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
        SIX = 6
        SEVEN = 7
        EIGHT = 8
        NINE = 9
        TEN = 10

    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    score = models.IntegerField(choices=Score.choices)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ["-pub_date"]
        unique_together = ('title_id', 'author')

    def __str__(self):
        return self.text


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        null=True
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text


class Rate(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL, blank=True, null=True
    )
    sum_vote = models.PositiveIntegerField(default=0)
    count_vote = models.PositiveIntegerField(default=0)

