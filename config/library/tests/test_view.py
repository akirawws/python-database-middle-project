# tests.py
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import date
from library.models import Author, Genre, Client, Book, BookLoan, Publisher, Review
from library.serializers import BookSerializer, AuthorSerializer, GenreSerializer, ClientSerializer, BookLoanSerializer, PublisherSerializer, ReviewSerializer
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def author():
    return Author.objects.create(name="Игорь Рызов")

@pytest.fixture
def genre():
    return Genre.objects.create(title_genre="Роман")

@pytest.fixture
def publisher():
    return Publisher.objects.create(name="Азбука")

@pytest.fixture
def client():
    return Client.objects.create(full_name="Игорь Рызов", age=30, prime_status=True)

@pytest.fixture
def book(author, genre, publisher):
    return Book.objects.create(
        title="Война и мир",
        author=author,
        genre=genre,
        publisher=publisher,
        year=1869,
        is_available=True,
        is_available_prime=True,
        price="1200.50",
        age_min="18+"
    )

@pytest.fixture
def book_loan(book, client):
    return BookLoan.objects.create(
        client=client,
        book=book,
        date_taken=date.today()
    )

@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpass123")

@pytest.mark.django_db
def test_book_list(api_client, book):
    """Тест: получение списка книг"""
    response = api_client.get('/api/books/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['title'] == "Война и мир"

@pytest.mark.django_db
def test_book_create(api_client, author, genre, publisher, user):
    """Тест: создание книги через API"""
    data = {
        "title": "Новая книга",
        "author": {"name": "Новый автор"},
        "genre": {"title_genre": "Детектив"},
        "publisher": {"name": "Новое издательство"},
        "year": 2024,
        "is_available": True,
        "is_available_prime": True,
        "price": "1500.00",
        "age_min": "16+"
    }

    response = api_client.post('/api/books/', data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Book.objects.count() == 1 
    assert response.data['title'] == "Новая книга"

@pytest.mark.django_db
def test_book_retrieve(api_client, book):
    """Тест: получение одной книги по ID"""
    response = api_client.get(f'/api/books/{book.id}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == "Война и мир"

@pytest.mark.django_db
def test_book_update(api_client, book, author, genre, publisher, user):
    """Тест: обновление книги"""
    api_client.force_authenticate(user=user)

    data = {
        "title": "Обновленное название",
        "author": {"name": "Игорь Рызов"},
        "genre": {"title_genre": "Детектив"},
        "publisher": {"name": "Новое издательство"},
        "year": 2025,
        "is_available": False,
        "is_available_prime": False,
        "price": "1800.00",
        "age_min": "16+"
    }

    response = api_client.put(f'/api/books/{book.id}/', data, format='json')
    assert response.status_code == status.HTTP_200_OK
    book.refresh_from_db()
    assert book.title == "Обновленное название"
    assert book.year == 2025
    assert book.is_available == False

@pytest.mark.django_db
def test_book_delete(api_client, book, user):
    """Тест: удаление книги"""
    api_client.force_authenticate(user=user)

    response = api_client.delete(f'/api/books/{book.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Book.objects.count() == 0

@pytest.mark.django_db
def test_author_list(api_client, author):
    """Тест: получение списка авторов"""
    response = api_client.get('/api/authors/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == "Игорь Рызов"

@pytest.mark.django_db
def test_author_create(api_client, user):
    """Тест: создание автора через API"""
    api_client.force_authenticate(user=user)

    data = {"name": "Новый автор"}
    response = api_client.post('/api/authors/', data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Author.objects.count() == 1
    assert response.data['name'] == "Новый автор"

@pytest.mark.django_db
def test_genre_list(api_client, genre):
    """Тест: получение списка жанров"""
    response = api_client.get('/api/genres/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['title_genre'] == "Роман"

@pytest.mark.django_db
def test_genre_create(api_client, user):
    """Тест: создание жанра через API"""
    api_client.force_authenticate(user=user)

    data = {"title_genre": "Фантастика"}
    response = api_client.post('/api/genres/', data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Genre.objects.count() == 1
    assert response.data['title_genre'] == "Фантастика"

@pytest.mark.django_db
def test_client_list(api_client, client):
    """Тест: получение списка клиентов"""
    response = api_client.get('/api/clients/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['full_name'] == "Игорь Рызов"

@pytest.mark.django_db
def test_client_create(api_client, user):
    """Тест: создание клиента через API"""
    api_client.force_authenticate(user=user)

    data = {
        "full_name": "Новый клиент",
        "age": 25,
        "prime_status": False
    }
    response = api_client.post('/api/clients/', data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Client.objects.count() == 1
    assert response.data['full_name'] == "Новый клиент"

@pytest.mark.django_db
def test_bookloan_list(api_client, book_loan):
    """Тест: получение списка выдач"""
    response = api_client.get('/api/bookloans/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['book']['title'] == "Война и мир"


@pytest.mark.django_db
def test_review_list(api_client, book, client):
    """Тест: получение списка отзывов"""
    response = api_client.get('/api/reviews/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0  
