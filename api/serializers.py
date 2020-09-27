from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .custom_authentication import AuthenticationWithoutPassword
from .models import User, Review, Comment, Category, Genre, Title


class UserAllSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', )


class TokenWithoutPasswordSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_code = kwargs['data']['confirmation_code']
        self.fields['password'].required = False

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass
        self.user = AuthenticationWithoutPassword().authenticate(
            **authenticate_kwargs
        )
        if self.user.confirmation_key != self.request_code:
            data = {'error': 'confirmation_code is not valid'}
        else:
            refresh = self.get_token(self.user)
            data = {'token': str(refresh.access_token)}
        return data


class ReviewSerializer(serializers.ModelSerializer):
    title_id = serializers.SlugRelatedField(
        many=False,
        slug_field='pk',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        many=False,
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = ('id', 'title_id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(
        allow_blank=False,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.CharField(
        allow_blank=False,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


