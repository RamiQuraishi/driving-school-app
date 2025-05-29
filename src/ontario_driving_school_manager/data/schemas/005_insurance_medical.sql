-- Insurance and medical tracking tables for the Ontario Driving School Manager

-- Insurance policies table
CREATE TABLE IF NOT EXISTS insurance_policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_number TEXT NOT NULL UNIQUE,
    provider TEXT NOT NULL,
    coverage_type TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    coverage_amount DECIMAL(10,2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Vehicle insurance table
CREATE TABLE IF NOT EXISTS vehicle_insurance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    policy_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
    FOREIGN KEY (policy_id) REFERENCES insurance_policies(id)
);

-- Medical certificates table
CREATE TABLE IF NOT EXISTS medical_certificates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    certificate_number TEXT NOT NULL,
    issue_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    issuing_authority TEXT NOT NULL,
    file_path TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- Medical conditions table
CREATE TABLE IF NOT EXISTS medical_conditions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    condition_type TEXT NOT NULL,
    description TEXT,
    severity TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_insurance_policies_number ON insurance_policies(policy_number);
CREATE INDEX IF NOT EXISTS idx_insurance_policies_dates ON insurance_policies(start_date, end_date);
CREATE INDEX IF NOT EXISTS idx_vehicle_insurance_vehicle ON vehicle_insurance(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_medical_certificates_student ON medical_certificates(student_id);
CREATE INDEX IF NOT EXISTS idx_medical_certificates_dates ON medical_certificates(issue_date, expiry_date);
CREATE INDEX IF NOT EXISTS idx_medical_conditions_student ON medical_conditions(student_id); 