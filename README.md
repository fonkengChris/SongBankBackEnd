---

# Song Library Project

## Project Overview

The Song Library project is a web application built with Python and Django, designed to manage a collection of songs. It includes features such as user authentication, song search, and filtering using MySQL full-text search, and supports CRUD operations through a RESTful API.

## Features

- User Authentication and Authorization
- Song Management (Create, Read, Update, Delete)
- Search and Filter Songs using MySQL Full-Text Search
- Token-based Authentication with JWT
- CORS support for frontend integration

## Installation Instructions

### Prerequisites

- Python 3.10+
- MySQL

### Setting Up the Project

1. **Clone the repository**:
   ```bash
   git clone https://github.com/fonkengChris/SongBankBackEnd.git
   cd SongBankBackEnd
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install the required dependencies**:
   ```bash
   pip install pipenv
   pipenv install
   ```

### Dependencies

The project dependencies are listed in the `Pipfile`:

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
django = "*"
django-debug-toolbar = "*"
mysqlclient = "*"
djangorestframework = "*"
django-countries = "*"
django-phonenumber-field = {extras = ["phonenumberslite"], version = "*"}
djoser = "*"
djangorestframework-simplejwt = "*"
drf-nested-routers = "*"
django-filter = "*"
pillow = "*"
python-magic = "*"
django-cors-headers = "*"
wand = "*"
pypdf2 = "*"
pdf2image = "*"
djangorestframework-jwt = "*"
django-extensions = "*"
gunicorn = "*"
dj-database-url = "*"
django-fulltext-search = {git = "https://github.com/confirm/django-fulltext-search.git"}
pyjwt = {extras = ["crypto"], version = "*"}
ipython = "*"
cryptography = "*"

[dev-packages]

[requires]
python_version = "3.10"

[pipenv]
allow_prereleases = true
```

### Configuration

1. **Database Setup**:
   Update the `DATABASES` settings in `settings.py` to configure MySQL:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'songBank',
           'HOST': 'localhost',
           'USER': 'root',
           'PASSWORD': 'your_password',
           'PORT': '3306',
       }
   }
   ```

2. **JWT Authentication**:
   Configure JWT settings in `settings.py`:

   ```python
   SIMPLE_JWT = {
       'AUTH_HEADER_TYPES': ('JWT',),
       'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
       'ALGORITHM': 'RS256',
       'SIGNING_KEY': private_key,
       'VERIFYING_KEY': public_key,
       'USER_ID_FIELD': 'id',
       'USER_ID_CLAIM': 'user_id',
       'AUTH_TOKEN_CLASSES': (
           'rest_framework_simplejwt.tokens.AccessToken',
       ),
       'TOKEN_TYPE_CLAIM': 'token_type',
   }
   ```

### Running the Project

1. **Apply database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

## Usage

### API Endpoints

1. **Get a list of songs**:
   ```http
   GET /api/songs/
   ```

2. **Add a new song**:
   ```http
   POST /api/songs/
   Content-Type: application/json
   {
       "title": "Song Title",
       "artist": "Artist Name",
       "album": "Album Name",
       "release_date": "2023-01-01"
   }
   ```

### Authentication

1. **User Registration**:
   ```http
   POST /auth/users/
   Content-Type: application/json
   {
       "username": "your_username",
       "password": "your_password"
   }
   ```

2. **Obtain JWT Token**:
   ```http
   POST /auth/jwt/create/
   Content-Type: application/json
   {
       "username": "your_username",
       "password": "your_password"
   }
   ```

### Full-Text Search

The full-text search functionality is provided by the custom `SearchQuerySet` and `SearchManager` classes. Here is an example of how to use these classes:

#### SearchQuerySet and SearchManager Implementation

```python
# library/models.py

from django.db import models
from .search import SearchManager

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    release_date = models.DateField()

    objects = SearchManager(fields=['title', 'artist', 'album'])

    def __str__(self):
        return self.title
```

#### Performing a Search

```python
# library/views.py

from rest_framework import generics
from .models import Song
from .serializers import SongSerializer

class SongSearchView(generics.ListAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Song.objects.search(query)
```

## Folder Structure

```plaintext
song-library/
├── manage.py
├── songBank/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── library/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   ├── search.py
│   └── migrations/
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── templates/
├── static/
└── Pipfile
```

## Contributing

To contribute to this project:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Open a pull request.

## License

This project is licensed under the MIT License.

---
