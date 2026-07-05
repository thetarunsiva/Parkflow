from config import LOTS

def init_state():
      state = {}
      for lot, slot_count in LOTS.items():
            lot_state = {}
            for i in range(1, slot_count+1):
                  slot = f"T{i}"
                  lot_state[slot] = False
            state[lot] = lot_state
      return state

def apply_event(state, event):
      lot = event["lot_id"]
      slot = event["slot_id"]
      event_type = event["event_type"]
      if event_type == "ENTRY":
            state[lot][slot] = True
      elif event_type == "EXIT":
            state[lot][slot] = False

def partition_slots(state):
      free_slots = []
      occupied_slots = []
      for lot, lot_state in state.items():
            for slot, occupied in lot_state.items():
                  if not occupied:
                        ans = (lot, slot)
                        free_slots.append(ans)
                  else:
                        ans = (lot, slot)
                        occupied_slots.append(ans)

      return free_slots, occupied_slots