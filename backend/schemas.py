from pydantic import BaseModel
from datetime import datetime

class LotOccupancy(BaseModel):
      lot_id: str
      occupied_slots: int
      available_slots: int
      total_slots: int
      occupancy_percentage: float

class SlotEvents(BaseModel):
      event_id: str
      slot_id: str
      lot_id: str
      event_type: str
      event_time: datetime

class SlotOccupancy(BaseModel):
      slot_id: str
      lot_id: str
      occupied: bool
      last_event_id: str
      last_event_time: datetime

class DashboardSummary(BaseModel):
      total_lots: int
      total_slots: int
      occupied_slots: int
      available_slots: int
      occupancy_percentage: float

class DashboardResponse(BaseModel):
      summary: DashboardSummary
      lots: list[LotOccupancy]
