-- Version tracking tables for the Ontario Driving School Manager

-- Version tracking table
CREATE TABLE IF NOT EXISTS version_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    record_id INTEGER NOT NULL,
    version INTEGER NOT NULL,
    data TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(table_name, record_id, version)
);

-- Version conflicts table
CREATE TABLE IF NOT EXISTS version_conflicts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    record_id INTEGER NOT NULL,
    local_version INTEGER NOT NULL,
    server_version INTEGER NOT NULL,
    local_data TEXT NOT NULL,
    server_data TEXT NOT NULL,
    resolved_data TEXT,
    resolution_type TEXT,
    resolved_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Version sync logs table
CREATE TABLE IF NOT EXISTS version_sync_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    record_id INTEGER NOT NULL,
    operation TEXT NOT NULL,
    version INTEGER NOT NULL,
    status TEXT NOT NULL,
    error_message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_version_tracking_lookup ON version_tracking(table_name, record_id);
CREATE INDEX IF NOT EXISTS idx_version_tracking_version ON version_tracking(version);
CREATE INDEX IF NOT EXISTS idx_version_conflicts_lookup ON version_conflicts(table_name, record_id);
CREATE INDEX IF NOT EXISTS idx_version_conflicts_resolution ON version_conflicts(resolution_type);
CREATE INDEX IF NOT EXISTS idx_version_sync_logs_lookup ON version_sync_logs(table_name, record_id);
CREATE INDEX IF NOT EXISTS idx_version_sync_logs_status ON version_sync_logs(status);

-- Add version columns to core tables
ALTER TABLE users ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE students ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE instructors ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE vehicles ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE lessons ADD COLUMN version INTEGER NOT NULL DEFAULT 1;

-- Add version columns to compliance tables
ALTER TABLE compliance_records ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE instructor_compliance ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE vehicle_compliance ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE school_compliance ADD COLUMN version INTEGER NOT NULL DEFAULT 1;

-- Add version columns to zone tables
ALTER TABLE zones ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE zone_boundaries ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE zone_pricing ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE zone_availability ADD COLUMN version INTEGER NOT NULL DEFAULT 1;

-- Add version columns to cancellation tables
ALTER TABLE cancellations ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE cancellation_policies ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE cancellation_fees ADD COLUMN version INTEGER NOT NULL DEFAULT 1;

-- Add version columns to insurance and medical tables
ALTER TABLE insurance_policies ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE vehicle_insurance ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE medical_certificates ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE medical_conditions ADD COLUMN version INTEGER NOT NULL DEFAULT 1;

-- Add version columns to MTO export tables
ALTER TABLE mto_exports ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE mto_export_records ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE mto_export_logs ADD COLUMN version INTEGER NOT NULL DEFAULT 1;

-- Add version columns to GPS tables
ALTER TABLE gps_tracking ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE gps_retention_policies ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE gps_retention_logs ADD COLUMN version INTEGER NOT NULL DEFAULT 1; 