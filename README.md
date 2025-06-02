# Ontario Driving School Manager

A comprehensive management system for driving schools in Ontario, Canada.

## Features

- User Management
  - Role-based access control (Admin, Instructor, Student)
  - Secure authentication with JWT
  - Two-factor authentication
  - Session management
  - CSRF protection
  - XSS prevention

- School Management
  - School profile
  - License management
  - Contact information
  - Location management

- Vehicle Management
  - Vehicle inventory
  - Maintenance tracking
  - Availability status
  - License plate tracking

- Scheduling System
  - Lesson scheduling
  - Instructor availability
  - Vehicle availability
  - Conflict detection
  - Calendar integration

## Requirements

- Python 3.9+
- Poetry
- SQLAlchemy
- Pydantic
- Alembic
- Electron
- React

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ontario-driving-school-manager.git
cd ontario-driving-school-manager
```

2. Install dependencies:
```bash
poetry install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize the database:
```bash
poetry run python -m ontario_driving_school_manager
```

## Development

1. Start the development server:
```bash
poetry run python -m ontario_driving_school_manager
```

2. Run tests:
```bash
poetry run pytest
```

3. Run linting:
```bash
poetry run flake8
poetry run black .
poetry run isort .
```

## Security

This application implements several security measures:

- JWT-based authentication
- Two-factor authentication
- Session management
- CSRF protection
- XSS prevention
- Password hashing
- Input validation
- SQL injection prevention

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Rami Drive School

## Acknowledgments

- Ontario Ministry of Transportation
- Driving School Association of Ontario

```

