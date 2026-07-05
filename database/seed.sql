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