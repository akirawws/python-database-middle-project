
from rest_framework import serializers
from datetime import datetime
from .models import Author, Genre, Client, Book, BookLoan, Publisher, Review


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ['id']


class AuthorNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']


class GenreNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['title_genre']


class PublisherNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['name']


class ClientNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['full_name']


class BookNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'year']


class AuthorSerializer(BaseSerializer):
    books_count = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = Author
        fields = ['name', 'books_count']

    def get_books_count(self, obj):
        return obj.book_set.count()

    def validate_name(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Имя должно содержать минимум 2 символа")
        return value.strip()


class GenreSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Genre
        fields = ['title_genre']

    def validate_title_genre(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Название жанра должно содержать минимум 2 символа")
        return value.strip()


class PublisherSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Publisher
        fields = ['name']

    def validate_name(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Название издательства должно содержать минимум 2 символа")
        return value.strip()


class BookSerializer(BaseSerializer):
    author = AuthorNestedSerializer()
    genre = GenreNestedSerializer(required=False, allow_null=True)
    publisher = PublisherNestedSerializer(required=False, allow_null=True)

    class Meta(BaseSerializer.Meta):
        model = Book
        fields = [
            'title', 'author', 'genre', 'publisher',
            'year', 'is_available', 'is_available_prime',
            'price', 'age_min'
        ]
        extra_kwargs = {
            'title': {'required': True, 'max_length': 100},
            'year': {'min_value': 1000, 'max_value': 2100},
            'is_available': {'default': True},
            'is_available_prime': {'default': True},
        }

    def validate_title(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Название книги должно содержать минимум 2 символа")
        return value.strip()

    def validate_year(self, value):
        current_year = datetime.now().year
        if value > current_year + 1:
            raise serializers.ValidationError("Год не может быть больше текущего + 1")
        if value < 1000:
            raise serializers.ValidationError("Год не может быть меньше 1000")
        return value

    def validate_price(self, value):
        if value:
            try:
                float_value = float(value.replace(',', '.'))
                if float_value < 0:
                    raise serializers.ValidationError("Цена не может быть отрицательной")
            except (ValueError, AttributeError):
                raise serializers.ValidationError("Неверный формат цены")
        return value

    def validate_age_min(self, value):
        if value:
            valid_ages = ['0+', '6+', '12+', '16+', '18+']
            if value not in valid_ages:
                raise serializers.ValidationError(f"Возраст должен быть одним из: {', '.join(valid_ages)}")
        return value

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        genre_data = validated_data.pop('genre', None)
        publisher_data = validated_data.pop('publisher', None)

        author, _ = Author.objects.get_or_create(name=author_data['name'])
        genre = Genre.objects.get_or_create(title_genre=genre_data['title_genre'])[0] if genre_data else None
        publisher = Publisher.objects.get_or_create(name=publisher_data['name'])[0] if publisher_data else None

        return Book.objects.create(
            author=author,
            genre=genre,
            publisher=publisher,
            **validated_data
        )

    def update(self, instance, validated_data):
        author_data = validated_data.pop('author', None)
        genre_data = validated_data.pop('genre', None)
        publisher_data = validated_data.pop('publisher', None)

        if author_data:
            author, _ = Author.objects.get_or_create(name=author_data['name'])
            instance.author = author

        if genre_data:
            genre, _ = Genre.objects.get_or_create(title_genre=genre_data['title_genre'])
            instance.genre = genre
        elif genre_data is None and 'genre' not in validated_data:
            pass
        else:
            instance.genre = None

        if publisher_data:
            publisher, _ = Publisher.objects.get_or_create(name=publisher_data['name'])
            instance.publisher = publisher
        elif publisher_data is None and 'publisher' not in validated_data:
            pass
        else:
            instance.publisher = None

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ClientSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Client
        fields = ['full_name', 'age', 'prime_status']
        extra_kwargs = {
            'full_name': {'required': True, 'max_length': 100},
            'age': {'min_value': 0, 'max_value': 120, 'allow_null': True},
            'prime_status': {'default': False},
        }

    def validate_full_name(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Имя должно содержать минимум 2 символа")
        return value.strip()

    def validate_age(self, value):
        if value is not None and (value < 0 or value > 120):
            raise serializers.ValidationError("Возраст должен быть от 0 до 120")
        return value


class ReviewSerializer(BaseSerializer):
    book = BookNestedSerializer()
    client = ClientNestedSerializer()

    class Meta(BaseSerializer.Meta):
        model = Review
        fields = ['book', 'client', 'text', 'rate']
        extra_kwargs = {
            'text': {'required': True, 'max_length': 1000},
            'rate': {'min_value': 1, 'max_value': 5, 'required': True},
        }

    def validate_text(self, value):
        if not value or len(value.strip()) < 5:
            raise serializers.ValidationError("Текст отзыва должен содержать минимум 5 символов")
        return value.strip()

    def validate_rate(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Оценка должна быть от 1 до 5")
        return value

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            book_data = data.get('book')
            if book_data:
                book = Book.objects.filter(title=book_data.get('title')).first()
                if book and Review.objects.filter(book=book, client=request.user).exists():
                    raise serializers.ValidationError("Вы уже оставили отзыв на эту книгу")
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        book_data = validated_data.pop('book')
        client_data = validated_data.pop('client')

        book = Book.objects.filter(title=book_data['title']).first()
        if not book:
            raise serializers.ValidationError({"book": "Книга не найдена"})

        client = Client.objects.filter(full_name=client_data['full_name']).first()
        if not client:
            raise serializers.ValidationError({"client": "Клиент не найден"})

        if request and hasattr(request, 'user'):
            client = request.user

        return Review.objects.create(book=book, client=client, **validated_data)


class BookLoanSerializer(BaseSerializer):
    client = ClientNestedSerializer()
    book = BookNestedSerializer()

    class Meta(BaseSerializer.Meta):
        model = BookLoan
        fields = ['client', 'book', 'date_taken', 'date_returned']
        read_only_fields = ['date_taken']
        extra_kwargs = {
            'date_returned': {'required': False, 'allow_null': True},
        }

    def validate(self, data):
        request = self.context.get('request')
        book_data = data.get('book')
        client_data = data.get('client')

        if book_data:
            book = Book.objects.filter(title=book_data.get('title')).first()
            if not book:
                raise serializers.ValidationError({"book": "Книга не найдена"})
            if not book.is_available:
                raise serializers.ValidationError({"book": "Книга недоступна для выдачи"})

        if request and hasattr(request, 'user'):
            active_loans = BookLoan.objects.filter(client=request.user, date_returned__isnull=True).count()
            if active_loans >= 5:
                raise serializers.ValidationError("Превышен лимит книг (5)")

        date_returned = data.get('date_returned')
        if date_returned:
            date_taken = self.instance.date_taken if self.instance else datetime.now().date()
            if date_returned < date_taken:
                raise serializers.ValidationError({"date_returned": "Дата возврата не может быть раньше даты выдачи"})

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        client_data = validated_data.pop('client')
        book_data = validated_data.pop('book')

        client = Client.objects.filter(full_name=client_data['full_name']).first()
        if not client:
            raise serializers.ValidationError({"client": "Клиент не найден"})

        book = Book.objects.filter(title=book_data['title']).first()
        if not book:
            raise serializers.ValidationError({"book": "Книга не найдена"})

        if request and hasattr(request, 'user'):
            client = request.user

        book.is_available = False
        book.save()

        return BookLoan.objects.create(client=client, book=book, **validated_data)

    def update(self, instance, validated_data):
        date_returned = validated_data.get('date_returned')
        if date_returned:
            instance.book.is_available = True
            instance.book.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
