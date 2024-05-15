## SongBank: A Song Management Application

SongBank is a web application that allows users to store, manage, and listen to songs. Users can categorize songs, add lyrics and descriptions, and upload  related document (PDF) and audio (MP3) files. The application also supports searching for songs by title, author name, or lyrics using a full-text search mechanism.

**Features:**

* **Song Management:** Create, edit, and view songs.
* **Categories:** Organize songs into categories.
* **Lyrics and Descriptions:** Add lyrics and descriptions to songs.
* **File Uploads:** Upload PDF documents and MP3 audio files associated with songs.
* **Full-Text Search:** Search for songs by title, author name, or lyrics.
* **User Authentication:** Register and log in to manage your songs and view private information.
* **User Favoriting:** Like and unlike songs to create a favorites list (not fully implemented yet).

**Technology Stack:**

* Backend: Django (Python web framework)
* Database: MySQL (with Full-Text Search enabled)
* REST API: Django REST Framework

**Requirements:**

* Python 3.x
* Django
* django-fulltext-search
* Other dependencies as specified in `requirements.txt`

**Installation:**

1. Clone the repository:

```bash
git clone https://github.com/fonkengChris/SongBankBackEnd.git
```

2. Create a virtual environment and activate it.

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply database migrations:

```bash
python manage.py migrate
```

5. (Optional) Create a superuser account:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

**Usage:**

The SongBank application provides a REST API for interacting with songs and other data. You can use any REST client or HTTP library to interact with the API. Refer to the Django REST Framework documentation for details on using the API: [https://www.django-rest-framework.org/topics/browsable-api/](https://www.django-rest-framework.org/topics/browsable-api/)

**Contributing:**

We welcome contributions to the SongBank project! Please see the CONTRIBUTING.md file for guidelines on how to contribute.

**License:**

This project is licensed under the MIT License. See the LICENSE file for details.

**Contact**
For any concerns, contact the management team at [christianfonkeng@outlook.com]
