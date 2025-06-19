# Recipe API

A comprehensive RESTful API for managing recipes, ingredients, and tags, built with Django and Django REST Framework. This project features user authentication, recipe filtering, image uploads, and is fully containerized with Docker for easy development and deployment.

## 🚀 Features

- **User Management**: Registration, authentication, and token-based authorization
- **Recipe Management**: Full CRUD operations for recipes with detailed information
- **Ingredients & Tags**: Organize recipes with custom ingredients and tags
- **Advanced Filtering**: Filter recipes by tags and ingredients
- **Image Uploads**: Upload and manage recipe images
- **API Documentation**: Interactive Swagger/OpenAPI documentation
- **Database**: PostgreSQL database with proper migrations
- **Containerized**: Docker and Docker Compose for easy setup

## 🛠 Tech Stack

- **Backend**: Python 3.11, Django 4.2
- **API Framework**: Django REST Framework
- **Database**: PostgreSQL 17
- **Authentication**: Token-based authentication
- **Documentation**: drf-spectacular (Swagger/OpenAPI)
- **Image Processing**: Pillow
- **Containerization**: Docker & Docker Compose
- **Database Adapter**: psycopg2-binary

## 📦 Installation & Setup

### Prerequisites

- Docker and Docker Compose installed on your system
- Git (to clone the repository)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Recipe_app_api
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

   This command will:
   - Build the Docker images
   - Start PostgreSQL database
   - Run database migrations
   - Start the Django development server

3. **Access the application**
   - API Base URL: http://localhost:8000/api/
   - Admin Interface: http://localhost:8000/admin/
   - API Documentation: http://localhost:8000/api/docs/schema/

### Manual Setup (without Docker)

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   export DB_HOST=localhost
   export DB_NAME=your_db_name
   export DB_USER=your_db_user
   export DB_PASS=your_db_password
   export DB_PORT=5432
   ```

4. **Run migrations and start server**
   ```bash
   cd app
   python manage.py migrate
   python manage.py runserver
   ```

## 🏗 Project Structure

```
Recipe_app_api/
├── app/                      # Django project root
│   ├── manage.py            # Django management script
│   ├── app/                 # Main Django application
│   │   ├── settings.py      # Django settings
│   │   ├── urls.py          # Main URL configuration
│   │   └── wsgi.py          # WSGI configuration
│   ├── core/                # Core application (models, management)
│   │   ├── models.py        # User, Recipe, Tag, Ingredient models
│   │   ├── admin.py         # Django admin configuration
│   │   └── management/      # Custom management commands
│   ├── user/                # User management API
│   │   ├── views.py         # User registration, authentication
│   │   ├── serializers.py   # User serializers
│   │   └── urls.py          # User URL patterns
│   └── recipe/              # Recipe management API
│       ├── views.py         # Recipe CRUD, filtering
│       ├── serializers.py   # Recipe serializers
│       └── urls.py          # Recipe URL patterns
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile              # Docker image definition
├── requirements.txt        # Python dependencies
└── requirements.dev.txt    # Development dependencies
```

## 🔧 API Endpoints

### Authentication
- `POST /api/user/create/` - Register new user
- `POST /api/user/token/` - Obtain authentication token
- `PUT /api/user/me/` - Update user profile

### Recipes
- `GET /api/recipes/` - List all recipes (authenticated user)
- `POST /api/recipes/` - Create new recipe
- `GET /api/recipes/{id}/` - Get recipe details
- `PUT /api/recipes/{id}/` - Update recipe
- `DELETE /api/recipes/{id}/` - Delete recipe
- `PATCH /api/recipes/{id}/upload-image/` - Upload recipe image

### Filtering
- `GET /api/recipes/filter/` - Filter recipes by tags and ingredients
  - Query parameters: `?tags=vegan,quick&ingredients=onion,tomato`

### Tags & Ingredients
- `GET /api/recipes/tags/` - List user's tags
- `POST /api/recipes/tags/` - Create new tag
- `GET /api/recipes/ingredients/` - List user's ingredients
- `POST /api/recipes/ingredients/` - Create new ingredient

## 📝 API Usage Examples

### Register a new user
```bash
curl -X POST http://localhost:8000/api/user/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your_password",
    "name": "Your Name"
  }'
```

### Get authentication token
```bash
curl -X POST http://localhost:8000/api/user/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your_password"
  }'
```

### Create a recipe
```bash
curl -X POST http://localhost:8000/api/recipes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your_token_here" \
  -d '{
    "title": "Delicious Pasta",
    "description": "A simple and tasty pasta recipe",
    "time_minutes": 30,
    "price": "12.50",
    "tags": [{"name": "italian"}, {"name": "quick"}],
    "ingredients": [{"name": "pasta"}, {"name": "tomato sauce"}]
  }'
```

### Filter recipes
```bash
curl "http://localhost:8000/api/recipes/filter/?tags=italian,quick&ingredients=pasta" \
  -H "Authorization: Token your_token_here"
```

## 🗄 Database Models

### User Model
- Custom user model with email as username
- Fields: email, name, is_active, is_staff

### Recipe Model
- Fields: title, description, time_minutes, price, link, image
- Relationships: user (ForeignKey), tags (ManyToMany), ingredients (ManyToMany)

### Tag Model
- Fields: name
- Relationship: user (ForeignKey)

### Ingredient Model
- Fields: name
- Relationship: user (ForeignKey)

## 🚀 Development

### Running Tests
```bash
docker-compose run --rm app sh -c "python manage.py test"
```

### Create Superuser
```bash
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```

### Access Database
```bash
docker-compose exec db psql -U postgres -d devdb
```

### View Logs
```bash
docker-compose logs -f app
```

## 🔒 Environment Variables

Configure these environment variables in your `docker-compose.yml` or `.env` file:

- `DB_HOST` - Database host
- `DB_NAME` - Database name
- `DB_USER` - Database user
- `DB_PASS` - Database password
- `DB_PORT` - Database port (default: 5432)
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)

## 📚 API Documentation

The API includes interactive documentation powered by drf-spectacular:

- **Swagger UI**: http://localhost:8000/api/docs/schema/swagger-ui/
- **ReDoc**: http://localhost:8000/api/docs/schema/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/docs/schema/
