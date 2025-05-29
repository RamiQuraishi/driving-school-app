-- Cancellation tracking tables for the Ontario Driving School Manager

-- Cancellations table
CREATE TABLE IF NOT EXISTS cancellations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson_id INTEGER NOT NULL,
    cancelled_by_id INTEGER NOT NULL,
    cancellation_type TEXT NOT NULL,
    reason TEXT,
    cancelled_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id),
    FOREIGN KEY (cancelled_by_id) REFERENCES users(id)
);

-- Cancellation policies table
CREATE TABLE IF NOT EXISTS cancellation_policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    hours_before_lesson INTEGER NOT NULL,
    fee_amount DECIMAL(10,2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Cancellation fees table
CREATE TABLE IF NOT EXISTS cancellation_fees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cancellation_id INTEGER NOT NULL,
    policy_id INTEGER NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status TEXT NOT NULL,
    paid_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cancellation_id) REFERENCES cancellations(id),
    FOREIGN KEY (policy_id) REFERENCES cancellation_policies(id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_cancellations_lesson ON cancellations(lesson_id);
CREATE INDEX IF NOT EXISTS idx_cancellations_cancelled_by ON cancellations(cancelled_by_id);
CREATE INDEX IF NOT EXISTS idx_cancellation_fees_cancellation ON cancellation_fees(cancellation_id);
CREATE INDEX IF NOT EXISTS idx_cancellation_fees_policy ON cancellation_fees(policy_id); 