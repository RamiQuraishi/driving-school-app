-- Compliance tables for the Ontario Driving School Manager

-- Compliance records table
CREATE TABLE IF NOT EXISTS compliance_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_type TEXT NOT NULL,
    record_date DATE NOT NULL,
    expiry_date DATE,
    status TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Instructor compliance table
CREATE TABLE IF NOT EXISTS instructor_compliance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instructor_id INTEGER NOT NULL,
    compliance_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    verification_date DATE,
    verified_by INTEGER,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (instructor_id) REFERENCES instructors(id),
    FOREIGN KEY (compliance_id) REFERENCES compliance_records(id),
    FOREIGN KEY (verified_by) REFERENCES users(id)
);

-- Vehicle compliance table
CREATE TABLE IF NOT EXISTS vehicle_compliance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    compliance_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    verification_date DATE,
    verified_by INTEGER,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
    FOREIGN KEY (compliance_id) REFERENCES compliance_records(id),
    FOREIGN KEY (verified_by) REFERENCES users(id)
);

-- School compliance table
CREATE TABLE IF NOT EXISTS school_compliance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    compliance_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    verification_date DATE,
    verified_by INTEGER,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (compliance_id) REFERENCES compliance_records(id),
    FOREIGN KEY (verified_by) REFERENCES users(id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_compliance_records_type ON compliance_records(record_type);
CREATE INDEX IF NOT EXISTS idx_compliance_records_date ON compliance_records(record_date);
CREATE INDEX IF NOT EXISTS idx_instructor_compliance_instructor ON instructor_compliance(instructor_id);
CREATE INDEX IF NOT EXISTS idx_vehicle_compliance_vehicle ON vehicle_compliance(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_school_compliance_verification ON school_compliance(verification_date); 