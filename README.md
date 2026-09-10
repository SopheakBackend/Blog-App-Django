# Blog-App-Django

A basic web application featuring a fully functioning blog built using the **Django** framework.

##  Features
- **Blog Post Management:** Create, view, update, and manage blog posts.
- **Structured Layout:** Organized with decoupled configuration handles (`mysite/`) and application logic (`blog/`).
- **Pre-styled Templates:** Handled globally with explicit template directories and layout fragments.

##  Project Structure
```text
├── blog/                      # Main blog application logic (Models, Views, URLs)
├── mysite/                    # Project configuration and core settings
├── static/css/                # Global cascading stylesheets
├── templates/                 # Global HTML templates and layout fragments
├── db.sqlite3                 # Local development database
├── manage.py                  # Django administrative command-line utility
├── requirements.txt           # Python package dependencies
└── mysite_data.json           # Sample fixture/backup database data
```

##  Installation & Setup

Follow these steps to get the development environment running locally:

### 1. Clone the Repository
```bash
git clone https://github.com/SopheakBackend/Blog-App-Django.git
cd Blog-App-Django
```

### 2. Set Up a Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory (ensure it stays ignored by Git) and populate your required environment secrets:
```text
SECRET_KEY=your_django_secret_key_here
DEBUG=True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. (Optional) Load Sample Data
If you want to populate the blog with pre-existing sample data from the included fixtures:
```bash
python manage.py loaddata mysite_data.json
```

### 7. Launch the Development Server
```bash
python manage.py runserver
```
Once running, navigate to `http://127.0.0` in your browser to view the application.
