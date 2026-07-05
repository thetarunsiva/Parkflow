CREATE TABLE IF NOT EXISTS parking_lots (
      lot_id VARCHAR(50) PRIMARY KEY,
      lot_name VARCHAR(100) NOT NULL,
      created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS parking_slots (
      slot_id VARCHAR(50) NOT NULL,
      lot_id VARCHAR(50) NOT NULL,
      created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (slot_id, lot_id),
      FOREIGN KEY (lot_id) REFERENCES parking_lots(lot_id) ON DELETE CASCADE
);

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

INSERT INTO parking_lots (lot_id, lot_name) VALUES
('LOT_1', 'T Nagar Parking'),
('LOT_2', 'Ambattur Parking'),
('LOT_3', 'Neelankarai Parking'),
('LOT_4', 'Tambaram Parking'),
('LOT_5', 'IT Park Parking');

INSERT INTO parking_slots (slot_id, lot_id) SELECT
'T' || slot_number, lot_id
FROM parking_lots
CROSS JOIN generate_series(1, 20) AS slot_number;