import pytest
from book.models import Book
from author.models import Authors
from library.models import Library

@pytest.fixture
def author():
    authors = Authors.objects.create(
        name = "Test author"
    )
    return authors

@pytest.fixture
def book(author):
    book = Book.objects.create(
        title = "test book",
        author=author
    )
    return book

@pytest.fixture
def author_this_book():
    authors = Authors.objects.create(
        name="Бабиджон"
    )
    books = []
    for i in range(10):
        books.append(Book.objects.create(title = f"книга {i}",author=authors.name))
    return books

@pytest.fixture
def library_is_more_book():
    author = Authors.objects.create(name="Test author")
    library = Library.objects.create(
        title_library = "Test library"
    )
    books = []
    for i in range(10):
        books.append(Book.objects.create(title=f"книга {i}",author=author))
    