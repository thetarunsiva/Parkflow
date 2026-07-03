CREATE TABLE IF NOT EXISTS slot_events (
      event_id UUID PRIMARY KEY,
      slot_id VARCHAR(50) NOT NULL,
      lot_id VARCHAR(50) NOT NULL,
      event_type VARCHAR(10) NOT NULL,
      event_time TIMESTAMPTZ NOT NULL,
      created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS slot_status (
      slot_id VARCHAR(50) NOT NULL,
      lot_id VARCHAR(50) NOT NULL,
      occupied BOOLEAN NOT NULL,
      last_event_id UUID NOT NULL,
      last_event_time TIMESTAMPTZ NOT NULL,
      PRIMARY KEY (slot_id, lot_id)
);

CREATE TABLE IF NOT EXISTS lot_occupancy (
      lot_id VARCHAR(50) PRIMARY KEY,
      occupied_slots INT NOT NULL,
      available_slots INT NOT NULL,
      total_slots INT NOT NULL,
      occupancy_percentage FLOAT NOT NULL,
      last_updated TIMESTAMPTZ NOT NULL
);