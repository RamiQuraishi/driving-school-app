-- MTO export tracking tables for the Ontario Driving School Manager

-- MTO exports table
CREATE TABLE IF NOT EXISTS mto_exports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    export_type TEXT NOT NULL,
    export_date TIMESTAMP NOT NULL,
    status TEXT NOT NULL,
    file_path TEXT,
    record_count INTEGER NOT NULL DEFAULT 0,
    created_by_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by_id) REFERENCES users(id)
);

-- MTO export records table
CREATE TABLE IF NOT EXISTS mto_export_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    export_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    record_type TEXT NOT NULL,
    record_data TEXT NOT NULL,
    status TEXT NOT NULL,
    error_message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (export_id) REFERENCES mto_exports(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- MTO export logs table
CREATE TABLE IF NOT EXISTS mto_export_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    export_id INTEGER NOT NULL,
    log_level TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (export_id) REFERENCES mto_exports(id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_mto_exports_type ON mto_exports(export_type);
CREATE INDEX IF NOT EXISTS idx_mto_exports_date ON mto_exports(export_date);
CREATE INDEX IF NOT EXISTS idx_mto_exports_status ON mto_exports(status);
CREATE INDEX IF NOT EXISTS idx_mto_export_records_export ON mto_export_records(export_id);
CREATE INDEX IF NOT EXISTS idx_mto_export_records_student ON mto_export_records(student_id);
CREATE INDEX IF NOT EXISTS idx_mto_export_logs_export ON mto_export_logs(export_id);
CREATE INDEX IF NOT EXISTS idx_mto_export_logs_level ON mto_export_logs(log_level); 