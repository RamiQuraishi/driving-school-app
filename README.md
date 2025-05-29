# Ontario Driving School Manager

A desktop application for managing Ontario driving schools, built with Python, FastAPI, SQLAlchemy, and Electron.

## Features

- Student management
- Instructor management
- Lesson scheduling
- Payment tracking
- Analytics and reporting
- Data export and backup
- Offline support
- Sync capabilities

## Prerequisites

- Python 3.9+
- Node.js 18+
- Poetry (Python package manager)
- npm (Node.js package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ontario-driving-school-manager.git
cd ontario-driving-school-manager
```

2. Install Python dependencies:
```bash
poetry install
```

3. Install Node.js dependencies:
```bash
npm install
```

4. Install React dependencies:
```bash
cd src/renderer
npm install
cd ../..
```

## Development

1. Start the Python backend:
```bash
poetry run python src/ontario_driving_school_manager/__main__.py
```

2. Start the React development server:
```bash
cd src/renderer
npm start
```

3. Start the Electron application:
```bash
npm run dev
```

## Building

1. Build the React application:
```bash
cd src/renderer
npm run build
cd ../..
```

2. Package the Electron application:
```bash
npm run package
```

The packaged application will be available in the `dist` directory.

## Testing

1. Run Python tests:
```bash
poetry run pytest
```

2. Run JavaScript tests:
```bash
npm test
```

## Project Structure

```
ontario-driving-school-manager/
├── src/
│   ├── electron/              # Electron main process
│   ├── renderer/              # React application
│   ├── shared/                # Shared code
│   └── ontario_driving_school_manager/  # Python backend
├── tests/                     # Test files
├── poetry.lock               # Poetry lock file
├── pyproject.toml            # Python project configuration
├── package.json              # Node.js project configuration
└── README.md                 # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Rami Drive School

## Acknowledgments

- FastAPI
- SQLAlchemy
- Electron
- React
- Poetry
- npm

```

