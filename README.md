# Rami Drive School Management System

A comprehensive management system for Rami Drive School, built with Python, SQLAlchemy, Electron, and React.

## Features

- Student Management
- Course Scheduling
- Instructor Management
- Payment Processing
- Progress Tracking
- Reporting System

## Tech Stack

- Backend: Python 3.9+, FastAPI, SQLAlchemy
- Frontend: Electron, React 18+
- Database: SQLite
- Development: Poetry, Docker

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- Poetry
- Docker and Docker Compose (for containerized development)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ramidriveschool.git
cd ramidriveschool
```

2. Install Python dependencies:
```bash
poetry install
```

3. Install Node.js dependencies:
```bash
npm install
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Development

1. Start the backend server:
```bash
poetry run uvicorn ramidriveschool.main:app --reload
```

2. Start the Electron app in development mode:
```bash
npm run dev
```

## Testing

Run the test suite:
```bash
poetry run pytest
```

## Building

Build the production version:
```bash
npm run build
```

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Project Structure

```
ramidriveschool/
├── backend/              # Python backend code
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   └── api/             # API endpoints
├── frontend/            # Electron/React frontend
│   ├── src/            # React source code
│   └── public/         # Static assets
├── tests/              # Test suite
└── docs/              # Documentation
``` 