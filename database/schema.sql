CREATE TABLE IF NOT EXISTS slot_events (
      event_id UUID PRIMARY KEY,
      slot_id VARCHAR(50) NOT NULL,
      lot_id VARCHAR(50) NOT NULL,
      event_type VARCHAR(10) NOT NULL,
      event_time TIMESTAMPTZ NOT NULL,
      created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO slot_events (event_id, slot_id, lot_id, event_type, event_time) VALUES (
      '11111111-1111-1111-1111-111111111111', 'T1', 'LOT_1', 'ENTRY', CURRENT_TIMESTAMP
);