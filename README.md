
## 🎯 Overview

This project is a backend scheduling service that allows users to:
- ✅ **Create meetings** with multiple participants
- ✅ **Prevent scheduling conflicts** automatically
- ✅ **Send email notifications** to participants
- ✅ **Export meetings as ICS files** (RFC 5545 compliant) for calendar integration

The system is designed as a clean, production-ready backend service with minimal dependencies and maximum reliability.

---

## 🛠 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Django 4.2+ |
| **REST API** | Django REST Framework |
| **API Documentation** | Swagger/OpenAPI (drf-spectacular) |
| **Database** | SQLite (Development) / PostgreSQL (Production) |
| **Calendar Format** | ICS (iCalendar - RFC 5545) |
| **Email Service** | SMTP (Gmail App Password) |
| **Containerization** | Docker & Docker Compose |

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



## 🏗 Architecture


```
┌─────────────────────────────────────────────────┐
│         API Layer (views.py)                    │
│  - Handles HTTP requests/responses              │
│  - Routes incoming data                         │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│    Serialization Layer (serializers.py)         │
│  - Validates input data                         │
│  - Formats output data                          │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│    Business Logic Layer (services.py)           │
│  - Conflict detection                           │
│  - Email notifications                          │
│  - Calendar export logic                        │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│    Data Access Layer (models.py)                │
│  - Meeting & Participant models                 │
│  - Database queries via ORM                      │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│         Database (SQLite/PostgreSQL)            │
└─────────────────────────────────────────────────┘
```

### Key Components

#### 1. **API Views** (`views.py`)
- `MeetingCreateView` - POST endpoint for creating meetings
- `MeetingListView` - GET endpoint for listing meetings
- `MeetingDetailView` - GET endpoint for meeting details
- `AddParticipantView` - PATCH endpoint for adding participants
- `MeetingICSView` - GET endpoint for ICS export

#### 2. **Serializers** (`serializers.py`)
- `MeetingSerializer` - Full meeting serialization with participants
- `MeetingListSerializer` - Lightweight meeting serialization
- `MeetingDetailSerializer` - Detailed meeting with participants
- `ParticipantSerializer` - Participant data serialization

#### 3. **Business Logic** (`services.py`)
- `has_conflict()` - Checks for scheduling conflicts
- `send_meeting_email()` - Sends email notifications to participants

#### 4. **Models** (`models.py`)
- `Meeting` - Meeting entity with title, description, times, participants
- `Participant` - Participant entity with email

---

## 🗄 Database Schema

Database Diagram : [https://dbdiagram.io/d/696b7847d6e030a02450d6c2]






## ✨ Features

### 1. **Conflict Detection**
- Automatically detects overlapping meetings for participants
- Prevents double-booking participants
- Returns clear error messages when conflicts are detected

### 2. **Email Notifications**
- Sends email confirmation when meetings are created
- Sends notifications when participants are added
- Email includes meeting details and ICS attachment

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

Run the test suite:

```bash
python manage.py test apps.meting
```

Run with verbose output:

```bash
python manage.py test apps.meting -v 2
```

---

## 📝 API Examples

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

### Download Meeting as ICS
```bash
curl -O http://localhost:8000/api/meetings/1/ics/
```

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
# Meeting-Scheduler
