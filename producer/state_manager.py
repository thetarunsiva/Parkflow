from config import LOTS

def init_state(owned_lots=None):
      if owned_lots is None:
            owned_lots = LOTS.keys()
      state = {}
      for lot in owned_lots:
            slot_count = LOTS[lot];
            state[lot] = {f"T{i}": False for i in range(1, slot_count + 1)}
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