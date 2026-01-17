
# Meeting Scheduler API

## 🎯 Overview

A production-ready Django REST API for scheduling meetings with automatic conflict detection, email notifications, and calendar export functionality.

**Key Features:**
- ✅ Create meetings with multiple participants
- ✅ Automatic conflict detection (prevent double-booking)
- ✅ Email notifications for meeting invitations
- ✅ Export meetings as RFC 5545 compliant ICS files
- ✅ RESTful API with Swagger/OpenAPI documentation
- ✅ Docker-ready deployment configuration

---

## 🛠 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Django 5.2+ |
| **REST API** | Django REST Framework 3.16+ |
| **API Documentation** | drf-spectacular (Swagger/OpenAPI) |
| **Database** | SQLite (Development) / PostgreSQL (Production) |
| **Calendar Format** | iCalendar (RFC 5545) |
| **Email Service** | Django SMTP backend |
| **Containerization** | Docker & Docker Compose |
| **Server** | Gunicorn |
| **Static Files** | WhiteNoise |

---

## 📁 Project Structure

```
project/
├── db.sqlite3                    # SQLite database
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
├── docker-compose.yml            # Docker configuration (if applicable)
├── Dockerfile                    # Docker image definition (if applicable)
│
├── project/                      # Main project configuration
│   ├── __init__.py
│   ├── settings.py              # Django settings & configuration
│   ├── urls.py                  # Main URL routing
│   ├── asgi.py                  # ASGI configuration
│   ├── wsgi.py                  # WSGI configuration
│   └── __pycache__/
│
└── apps/
    └── meting/                  # Meeting scheduling app
        ├── migrations/          # Database migrations
        │   ├── 0001_initial.py
        │   └── __pycache__/
        ├── __init__.py
        ├── admin.py             # Django admin configuration
        ├── apps.py              # App configuration
        ├── models.py            # Database models (Meeting, Participant)
        ├── serializers.py       # DRF serializers
        ├── views.py             # API views/endpoints
        ├── services.py          # Business logic (conflict detection, email)
        ├── urls.py              # App URL routing
        ├── tests.py             # Unit tests
        └── __pycache__/
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip or conda
- PostgreSQL (recommended for production)
- Docker & Docker Compose (optional)

### Option 1: Local Development Setup

1. **Clone/Navigate to the project directory**
   ```bash
   cd project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

   The API will be available at: `http://localhost:8000`

### 📚 Access API Documentation

After starting the server, access the interactive API documentation:

Swagger UI: [http://localhost:8000/api/schema/swagger/]
ReDoc (Alternative): [http://localhost:8000/api/schema/redoc/]
OpenAPI JSON Schema: [http://localhost:8000/api/schema/]
Postman API Collections : [https://documenter.getpostman.com/view/48223835/2sBXVifovy]



## 🏗 Architecture & Design Decisions

### Layered Architecture

```
┌─────────────────────────────────────────────────┐
│         API Layer (views.py)                    │
│  - Handles HTTP requests/responses              │
│  - Routes incoming data                         │
│  - Returns appropriate status codes             │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│    Serialization Layer (serializers.py)         │
│  - Validates input data schema                  │
│  - Formats output data                          │
│  - Handles nested relationships                 │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│    Business Logic Layer (services.py)           │
│  - Conflict detection algorithm                 │
│  - Email notifications                          │
│  - Calendar export logic                        │
│  - Complex business rules                       │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│    Data Access Layer (models.py)                │
│  - Meeting & Participant models                 │
│  - Database queries via Django ORM              │
│  - Data validation                              │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│      Database (SQLite/PostgreSQL)               │
│  - Persistent data storage                      │
└─────────────────────────────────────────────────┘
```

### Key Components

#### 1. **API Views** ([apps/meting/views.py](apps/meting/views.py))
- `MeetingCreateView` - POST endpoint for creating meetings
- `MeetingListView` - GET endpoint for listing meetings
- `MeetingDetailView` - GET endpoint for meeting details
- `AddParticipantView` - PATCH endpoint for adding participants
- `MeetingICSView` - GET endpoint for ICS export

#### 2. **Serializers** ([apps/meting/serializers.py](apps/meting/serializers.py))
- `MeetingSerializer` - Full meeting serialization with participants
- `MeetingListSerializer` - Lightweight meeting serialization
- `MeetingDetailSerializer` - Detailed meeting with participants
- `ParticipantSerializer` - Participant data serialization

#### 3. **Business Logic** ([apps/meting/services.py](apps/meting/services.py))
- `has_conflict()` - Checks for scheduling conflicts
- `send_meeting_email()` - Sends email notifications to participants

#### 4. **Models** ([apps/meting/models.py](apps/meting/models.py))
- `Meeting` - Meeting entity with title, description, times, participants
- `Participant` - Participant entity with email

### Design Patterns Used

1. **Separation of Concerns**: Business logic in `services.py`, presentation in `views.py`, data in `models.py`
2. **Serializers Pattern**: DRF serializers for validation and transformation
3. **APIView Pattern**: Class-based views for modularity and reusability
4. **Many-to-Many Relationship**: Flexible participant-meeting associations

### Design Decisions

#### 1. **Conflict Detection Algorithm**
```python
# Uses Django ORM for efficient queries
Meeting.objects.filter(
    participants__in=participants,  # Same participants
    start_time__lt=end,              # Meeting starts before our meeting ends
    end_time__gt=start               # Meeting ends after our meeting starts
).exists()
```
**Why:** 
- Efficient database-level filtering
- Detects overlapping time ranges correctly
- Scalable for large participant bases

#### 2. **Email Notifications**
- Sent after participant addition
- Uses Django's `send_mail()` with SMTP backend
- Includes meeting details for context

**Why:**
- Standard Django email infrastructure
- Easy to upgrade to Celery for async operations
- Configurable via environment variables

#### 3. **ICS Export (RFC 5545)**
- Uses `icalendar` library for standards compliance
- Compatible with all calendar applications
- Includes all meeting metadata

**Why:**
- Universal calendar format
- Works with Outlook, Google Calendar, Apple Calendar
- Industry standard format

#### 4. **Participant Deduplication**
- Emails are globally unique
- Uses `get_or_create()` pattern
- Prevents duplicate participant entries

**Why:**
- Clean data model
- Automatic deduplication
- Simplified queries

#### 5. **SQLite for Development**
- Simple setup, no external dependencies
- Django migrations built-in
- Easy to seed with test data

**Why:**
- Fast development iteration
- Portable database
- Production-ready migration path to PostgreSQL

---

## 💡 Assumptions

1. **Email Configuration**: Django email backend must be properly configured (see Environment Variables section)
2. **Timezone Handling**: All timestamps use UTC (`USE_TZ=True` in settings)
3. **Participant Uniqueness**: Each email address represents a unique participant
4. **Time Validation**: End time must be after start time (enforced at serializer level)
5. **No User Authentication**: API is open (no authentication required for MVP)
6. **Synchronous Operations**: Email sending is synchronous (can be upgraded to async with Celery)
7. **Email Reliability**: Using `fail_silently=False` to catch email failures
8. **Database Connection**: Using persistent SQLite connection for development

---

## 🔍 Notable Limitations & Future Improvements

### Current Limitations

1. **No User Authentication**
   - Currently anyone can create/access meetings
   - **Future:** Implement JWT tokens or OAuth2

2. **No User Roles**
   - No distinction between meeting organizer and participants
   - **Future:** Add user-based access control

3. **Synchronous Email**
   - Email sending blocks the API response
   - **Future:** Integrate Celery for background tasks

4. **No Conflict Resolution**
   - System only detects conflicts, doesn't suggest alternatives
   - **Future:** Add meeting time recommendation algorithm

5. **Limited Notifications**
   - Only email notifications (no SMS, Slack, calendar sync)
   - **Future:** Support multiple notification channels

6. **No Meeting Updates**
   - Can't modify meeting details after creation
   - **Future:** Add PUT/PATCH endpoints for updates

7. **No Meeting Deletion**
   - No soft/hard delete functionality
   - **Future:** Add deletion with cascade handling

8. **No Pagination**
   - List endpoints return all records
   - **Future:** Implement cursor/offset pagination

### Suggested Future Improvements

1. **Search & Filtering**
   ```bash
   GET /api/meetings/?participant=alice@example.com&date=2024-02-20
   ```

2. **Meeting Recurrence**
   - Support recurring meetings (daily, weekly, monthly)
   - Requires changes to models and conflict detection

3. **Rate Limiting**
   - Prevent API abuse
   - Use `django-ratelimit` package

4. **Audit Logging**
   - Track all API operations
   - Store user actions and timestamps

5. **Webhook Support**
   - Notify external systems of meeting events
   - Useful for calendar sync

6. **Time Zone Support**
   - Store participant time zones
   - Convert times based on location

7. **Analytics Dashboard**
   - Meeting statistics and trends
   - Participant availability patterns

8. **Bulk Operations**
   - Create multiple meetings at once
   - Batch add participants

---

## 🗄 Database Schema

### Database Diagram
Interactive diagram: [DBDiagram Link](https://dbdiagram.io/d/696b7847d6e030a02450d6c2)

### Tables

#### `meting_participant`
| Column | Type | Constraints |
|--------|------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO INCREMENT |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL |

**Purpose:** Stores participant information with unique email addresses.

#### `meting_meeting`
| Column | Type | Constraints |
|--------|------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO INCREMENT |
| `title` | VARCHAR(200) | NOT NULL |
| `description` | TEXT | NULLABLE |
| `start_time` | DATETIME | NOT NULL |
| `end_time` | DATETIME | NOT NULL |
| `created_at` | DATETIME | AUTO SET, NOT NULL |

**Purpose:** Stores meeting details with timestamps.

#### `meting_meeting_participants` (Many-to-Many Junction Table)
| Column | Type | Constraints |
|--------|------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO INCREMENT |
| `meeting_id` | INTEGER | FOREIGN KEY → meting_meeting.id |
| `participant_id` | INTEGER | FOREIGN KEY → meting_participant.id |

**Purpose:** Links meetings to participants (supports multiple participants per meeting).

### Relationships
- **One Meeting → Many Participants** (1:N through M2M junction table)
- **One Participant → Many Meetings** (1:N through M2M junction table)

### Key Constraints
- Participant emails are globally unique
- Meeting times are required and validated
- Automatic timestamps for audit trail

---

## 🌍 Environment Variables & Configuration

### Development Configuration

Create a `.env` file in the project root:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration (Gmail Example)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Database (leave empty for SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Loading Environment Variables

The project uses Python's `python-decouple` library (add to requirements if using):
```python
from decouple import config
DEBUG = config('DEBUG', default=False, cast=bool)
```

---

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t meeting-scheduler:latest .
```

### Run with Docker Compose
```bash
docker-compose up -d
```

### Production Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations and start server
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## 🚀 Production Deployment Checklist

- [ ] Set `DEBUG=False` in settings
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure email service (SendGrid, AWS SES, etc.)
- [ ] Enable HTTPS/SSL
- [ ] Set up proper CORS origins
- [ ] Configure logging
- [ ] Set up monitoring and error tracking
- [ ] Run security checks: `python manage.py check --deploy`

---

## ✨ Features

### 1. **Conflict Detection**
- Automatically detects overlapping meetings for participants
- Prevents double-booking participants
- Returns clear error messages when conflicts are detected

### 2. **Email Notifications**
- Sends email confirmation when meetings are created
- Sends notifications when participants are added
- Email includes meeting details and meeting summary

### 3. **Calendar Export (ICS)**
- Generate RFC 5545 compliant ICS files
- Compatible with Outlook, Google Calendar, Apple Calendar
- One-click calendar integration

### 4. **Participant Management**
- Automatic participant deduplication via unique email
- Add participants to existing meetings
- Support for multiple participants per meeting

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test apps.meting

# Run with verbose output
python manage.py test apps.meting -v 2

# Run specific test
python manage.py test apps.meting.tests.MeetingTest.test_create_meeting
```

### Test Coverage

The project includes automated tests in [apps/meting/tests.py](apps/meting/tests.py):
- `MeetingTest.test_create_meeting()` - Validates meeting creation with participants

**Test Output:**
```
Ran 1 test in 0.045s

OK
```

### Running Tests with Coverage Report

```bash
pip install coverage
coverage run --source='apps' manage.py test apps.meting
coverage report
coverage html  # Generate HTML report
```

---


## 📝 API Endpoints & Usage Examples

### Create a Meeting with cURL
```bash
curl -X POST http://localhost:8000/api/meetings/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Meeting",
    "description": "Weekly team sync",
    "start_time": "2024-02-20T10:00:00Z",
    "end_time": "2024-02-20T11:00:00Z",
    "participants": [
      {"email": "alice@example.com"},
      {"email": "bob@example.com"}
    ]
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Team Meeting",
  "description": "Weekly team sync",
  "start_time": "2024-02-20T10:00:00Z",
  "end_time": "2024-02-20T11:00:00Z",
  "participants": [
    {"id": 1, "email": "alice@example.com"},
    {"id": 2, "email": "bob@example.com"}
  ],
  "created_at": "2024-02-20T09:30:00Z"
}
```

### List All Meetings
```bash
curl http://localhost:8000/api/meetings/
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Team Meeting",
    "start_time": "2024-02-20T10:00:00Z",
    "end_time": "2024-02-20T11:00:00Z",
    "participants_count": 2
  }
]
```

### Get Meeting Details
```bash
curl http://localhost:8000/api/meetings/1/
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Team Meeting",
  "description": "Weekly team sync",
  "start_time": "2024-02-20T10:00:00Z",
  "end_time": "2024-02-20T11:00:00Z",
  "participants": [
    {"id": 1, "email": "alice@example.com"},
    {"id": 2, "email": "bob@example.com"}
  ],
  "created_at": "2024-02-20T09:30:00Z"
}
```

### Add Participants to Existing Meeting
```bash
curl -X PATCH http://localhost:8000/api/meetings/1/add-participants/ \
  -H "Content-Type: application/json" \
  -d '{
    "participants": [
      {"email": "charlie@example.com"}
    ]
  }'
```

**Response (200 OK):**
```json
{
  "message": "Participants added successfully"
}
```

**Error Response (409 Conflict):**
```json
{
  "error": "Participant has a conflicting meeting."
}
```

### Download Meeting as ICS
```bash
curl -O http://localhost:8000/api/meetings/1/ics/
# Downloads meeting_1.ics file
```

### Using Postman
Import the collection: [Meeting_Scheduler_API.postman_collection.json](Meeting_Scheduler_API.postman_collection.json)

Available endpoints in collection:
- `POST /api/meetings/create/` - Create new meeting
- `GET /api/meetings/` - List all meetings
- `GET /api/meetings/{id}/` - Get meeting details
- `PATCH /api/meetings/{id}/add-participants/` - Add participants
- `GET /api/meetings/{id}/ics/` - Export as ICS file

---


## � Dependencies

See `requirements.txt` for complete list:

```
Django>=4.2
djangorestframework
psycopg2-binary
icalendar
drf-spectacular
drf-spectacular[sidecar]
```

### Package Descriptions

| Package | Purpose |
|---------|---------|
| `Django` | Web framework and ORM |
| `djangorestframework` | REST API toolkit for DRF |
| `drf-spectacular` | OpenAPI 3.0 schema generation and Swagger UI |
| `drf-spectacular[sidecar]` | Enhanced schema generation with sidecar support |
| `icalendar` | ICS file format generation (RFC 5545) |
| `psycopg2-binary` | PostgreSQL database adapter |

---

## 📦 Dependencies

All dependencies are listed in [requirements.txt](requirements.txt).

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 5.2.10 | Web framework and ORM |
| djangorestframework | 3.16.1 | REST API toolkit for DRF |
| drf-spectacular | 0.29.0 | OpenAPI 3.0 schema generation |
| icalendar | 6.3.2 | ICS file format generation (RFC 5545) |
| psycopg2-binary | 2.9.11 | PostgreSQL database adapter |
| gunicorn | 23.0.0 | WSGI HTTP server |
| whitenoise | 6.11.0 | Static files serving |
| django-cors-headers | latest | CORS support |

### Installation

```bash
pip install -r requirements.txt
```

---

## 📄 Project Files

### Core Application Files
- [manage.py](manage.py) - Django management script
- [requirements.txt](requirements.txt) - Python dependencies
- [db.sqlite3](db.sqlite3) - SQLite database (development)
- [Dockerfile](Dockerfile) - Docker image configuration
- [README.md](README.md) - This file

### Project Configuration
- [project/settings.py](project/settings.py) - Django settings
- [project/urls.py](project/urls.py) - Main URL routing
- [project/wsgi.py](project/wsgi.py) - WSGI application
- [project/asgi.py](project/asgi.py) - ASGI application

### Application Files
- [apps/meting/models.py](apps/meting/models.py) - Database models
- [apps/meting/views.py](apps/meting/views.py) - API views
- [apps/meting/serializers.py](apps/meting/serializers.py) - DRF serializers
- [apps/meting/services.py](apps/meting/services.py) - Business logic
- [apps/meting/urls.py](apps/meting/urls.py) - App URL routing
- [apps/meting/tests.py](apps/meting/tests.py) - Unit tests
- [apps/meting/admin.py](apps/meting/admin.py) - Django admin configuration
- [apps/meting/migrations/](apps/meting/migrations/) - Database migrations

---

## 📋 Summary

This Meeting Scheduler API provides a robust, production-ready solution for:
- **Creating meetings** with multiple participants
- **Detecting scheduling conflicts** to prevent double-booking
- **Sending notifications** to participants
- **Exporting calendar events** in standard ICS format
- **Managing participants** with email deduplication

Built with **Django** and **Django REST Framework**, the project follows best practices for clean architecture, scalability, and maintainability.

---

**Last Updated:** January 17, 2026  
**Status:** Production Ready ✅
