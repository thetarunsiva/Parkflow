import uuid
import random
from datetime import datetime
from state_manager import partition_slots

def event(lot_id, slot_id, event_type):
      timestamp = datetime.now().isoformat()
      event = {
            "event_id": str(uuid.uuid4()),
            "slot_id": slot_id,
            "lot_id": lot_id,
            "event_type": event_type,
            "event_time": timestamp,
            "created_at": timestamp
      }
      return event

def generate_event(state):
      free_slots, occupied_slots = partition_slots(state)
      if (free_slots and occupied_slots):
            ch = random.randint(0, 1)
            if (ch == 0):
                  lot, slot = random.choice(free_slots)
                  return event(lot, slot, "ENTRY")
            else:
                  lot, slot = random.choice(occupied_slots)
                  return event(lot, slot, "EXIT")
      if (free_slots):
            lot, slot = random.choice(free_slots)
            return event(lot, slot, "ENTRY")
      elif (occupied_slots):
            lot, slot = random.choice(occupied_slots)
            return event(lot, slot, "EXIT")