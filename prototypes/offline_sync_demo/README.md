# Offline Sync Demo

This prototype demonstrates the offline synchronization capabilities of the driving school management system.

## Features

- Local SQLite database for offline storage
- Change tracking and conflict detection
- Automatic sync when online
- Conflict resolution strategies
- Sync status monitoring

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
python init_db.py
```

3. Run the demo:
```bash
python demo.py
```

## Testing

Run the test suite:
```bash
pytest tests/
```

## Architecture

The demo implements a simple offline-first architecture:

1. Local Storage
   - SQLite database
   - Change tracking
   - Sync queue

2. Sync Process
   - Change detection
   - Conflict resolution
   - Data synchronization

3. Monitoring
   - Sync status
   - Error handling
   - Performance metrics

## Usage

1. Start the demo application
2. Make changes while offline
3. Reconnect to see sync in action
4. Monitor sync status and conflicts

## Next Steps

1. Implement more conflict resolution strategies
2. Add real-time sync status updates
3. Improve error handling and recovery
4. Add data validation and integrity checks 