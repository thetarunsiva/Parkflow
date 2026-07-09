from state_manager import init_state, apply_event
from event_generator import generate_events
from event_publisher import publish_event

from config import MIN_DELAY_SECONDS, MAX_DELAY_SECONDS

import os
import time
import random

owned = os.getenv("OWNED_LOTS")
owned_lots = owned.split(",") if owned else None
state = init_state(owned_lots)

EVENTS_PER_SECOND = 10

try:
      while True:
            events = generate_events(state, EVENTS_PER_SECOND)
            success = publish_event(events)
            if not success:
                  print(f"Failed to publish events..")
                  continue
            for event in events:
                  apply_event(state, event)
                  print(f"[{event['event_type']}] " f"{event['lot_id']} - {event['slot_id']}")
            time.sleep(1)
except KeyboardInterrupt:
      print("\nParkflow simulation stopping..")
      time.sleep(1)
      print("Parkflow simulation finished!")