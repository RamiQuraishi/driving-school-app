-- GPS retention tables for the Ontario Driving School Manager

-- GPS tracking table
CREATE TABLE IF NOT EXISTS gps_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    speed REAL,
    heading REAL,
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);

-- GPS retention policies table
CREATE TABLE IF NOT EXISTS gps_retention_policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    retention_days INTEGER NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- GPS retention logs table
CREATE TABLE IF NOT EXISTS gps_retention_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_id INTEGER NOT NULL,
    records_deleted INTEGER NOT NULL DEFAULT 0,
    execution_time REAL NOT NULL,
    status TEXT NOT NULL,
    error_message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (policy_id) REFERENCES gps_retention_policies(id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_gps_tracking_vehicle ON gps_tracking(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_gps_tracking_timestamp ON gps_tracking(timestamp);
CREATE INDEX IF NOT EXISTS idx_gps_retention_policies_active ON gps_retention_policies(is_active);
CREATE INDEX IF NOT EXISTS idx_gps_retention_logs_policy ON gps_retention_logs(policy_id);
CREATE INDEX IF NOT EXISTS idx_gps_retention_logs_status ON gps_retention_logs(status);

-- Create trigger for automatic cleanup
CREATE TRIGGER IF NOT EXISTS cleanup_old_gps_data
AFTER INSERT ON gps_tracking
BEGIN
    DELETE FROM gps_tracking
    WHERE timestamp < datetime('now', '-30 days');
END; 