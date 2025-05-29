-- Toronto zones tables for the Ontario Driving School Manager

-- Zones table
CREATE TABLE IF NOT EXISTS zones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Zone boundaries table
CREATE TABLE IF NOT EXISTS zone_boundaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_id INTEGER NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    sequence INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (zone_id) REFERENCES zones(id)
);

-- Zone pricing table
CREATE TABLE IF NOT EXISTS zone_pricing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_id INTEGER NOT NULL,
    lesson_type TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (zone_id) REFERENCES zones(id)
);

-- Zone availability table
CREATE TABLE IF NOT EXISTS zone_availability (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_id INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (zone_id) REFERENCES zones(id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_zones_name ON zones(name);
CREATE INDEX IF NOT EXISTS idx_zone_boundaries_zone ON zone_boundaries(zone_id);
CREATE INDEX IF NOT EXISTS idx_zone_pricing_zone ON zone_pricing(zone_id);
CREATE INDEX IF NOT EXISTS idx_zone_availability_zone ON zone_availability(zone_id);
CREATE INDEX IF NOT EXISTS idx_zone_availability_day ON zone_availability(day_of_week); 