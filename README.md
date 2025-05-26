Ontario Driving School Manager

A full-featured, compliance-driven management platform for Ontario-based driving schools. Built with Python, Electron, and React to meet MTO, PIPEDA, and AODA standards.

---

 📦 Key Features

- 🧑‍🎓 Student management, G1/G2/G tracking, and certificate generation
- 📅 Lesson scheduling with GPS tracking and conflict resolution
- 🧑‍🏫 Instructor credential and availability management
- 🚗 Vehicle maintenance, route tracking, and inspection history
- 💳 HST-compliant billing, Interac/Stripe/Square payments
- 📈 Advanced reports: MTO, Toronto, financial, progress
- 📱 Progressive web portal for students and instructors
- 📴 Offline-first support (SQLite with sync/resolve)
- 🔐 PIPEDA-compliant security: encryption, consent, audit trail
- 🧾 Legal documents: SR-LD-007, GPS consent, privacy impact
- 🌐 Bilingual UI (English/French), AODA accessible

---

 🔧 Requirements

| Component        | Version/Notes                   |
|------------------|----------------------------------|
| Python           | 3.11+                            |
| Node.js          | 18+ (Electron, React)           |
| PostgreSQL       | 14+ (Primary DB)                |
| Redis            | For caching and queuing         |
| Docker (Optional)| For containerized environments  |
| SQLite           | Embedded offline mode           |

---

 🚀 Quick Setup Guide

 1. Clone and Configure Environment

```bash
git clone https://github.com/your-org/ontario-driving-school-manager.git
cd ontario-driving-school-manager
cp .env.example .env
````

Edit `.env` to match your local or production configuration.

---

 2. Install Dependencies

 Backend (Python)

```bash
poetry install
poetry shell
```

 Frontend (Electron/React)

```bash
npm install
```

---

 3. Initialize the Database

```bash
docker-compose up -d postgres redis
alembic upgrade head
python scripts/init_db.py
python scripts/create_test_data.py
```

---

 4. Launch Application

 Backend API

```bash
uvicorn src.ontario_driving_school_manager.portal.app:app --reload
```

 Desktop UI (Electron)

```bash
npm run electron:dev
```

---

 ⚙️ Configuration Files

* `.env`: Environment variables (database URL, log levels, etc.)
* `src/ontario_driving_school_manager/config/logging.yaml`: Logging settings
* `docker-compose.*.yml`: Dev/test infrastructure
* `pyproject.toml`: Python dependencies via Poetry
* `package.json`: JS dependencies for Electron and React

---

 📋 Project Structure

```
src/
  ontario_driving_school_manager/
    core/           Analytics, monitoring, privacy, security
    data/           Repositories, schemas, migrations
    services/       Business logic and orchestration
    models/         SQLAlchemy models with compliance fields
    portal/         FastAPI for student/instructor portal
    update/         Auto-update system
    integrations/   MTO, GPS, Payment gateways
    config/         Settings, logging, feature flags

  renderer/         Electron React app
  electron/         Electron main and preload processes
  portal/           React PWA frontend (student/instructor access)
tests/              Unit, integration, E2E, compliance tests
scripts/            Dev tools, data sync, migrations
```

---

 🧪 Testing

```bash
 Run all test suites
poetry run pytest
```

* Unit tests, integration, and E2E tests (>80% coverage)
* PIPEDA, AODA, and MTO compliance test suites
* Security (XSS, CSRF, SQLi), GPS privacy tests

---

 📑 Documentation

* User Manual: `docs/manual/`
* API Reference: Swagger + Python docstrings
* Compliance: `docs/legal/`, `docs/privacy_impact_assessment.md`
* Migration: `docs/migration_guides/`
* Help & Training: `src/ontario_driving_school_manager/resources/help/`

---

 ✅ QA, Market Readiness, and Audit

* QA Checklist: [`QA.txt`](docs/QA.txt)
* Readiness: [`Market Readiness Checklist`](docs/MarketReadiness.md)
* Phase Docs: `docs/phases/phase_[00-20].md`

---

 📦 Deployment

```bash
 Build executables
python deployment/scripts/build_exe.py
 Generate installer
python deployment/scripts/build_installer.py
```

Includes embedded PostgreSQL/SQLite, NSIS installer (Windows), and auto-update support.

---

 👥 Contributing

1. Fork the repository
2. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature
   ```
3. Run tests and linters
4. Commit with conventional messages
5. Open a Pull Request with context

---

 🛡️ License

MIT — see `LICENSE.txt`

---

 📞 Contact

Visit [www.batanetworks.com](https://www.batanetworks.com) for support, training, or deployment inquiries.

---

```

