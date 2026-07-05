from state_manager import init_state, apply_event
from event_generator import generate_event
from event_publisher import publish_event

from config import MIN_DELAY_SECONDS, MAX_DELAY_SECONDS

import time
import random

state = init_state()

try:
      while True:
            event = generate_event(state)
            success = publish_event(event)
            if not success:
                  print(f"Failed to publish event: {event['event_id']}..")
                  continue
            apply_event(state, event)
            print(f"[{event['event_type']}] " f"{event['lot_id']} - {event['slot_id']}")
            time.sleep(random.randint(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS))
except KeyboardInterrupt:
      print("\nParkflow simulation stopping..")
      time.sleep(1)
      print("Parkflow simulation finished!")