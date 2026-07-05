export type LotOccupancy = {
  lot_id: string;
  lot_name: string;
  occupied_slots: number;
  available_slots: number;
  total_slots: number;
  occupancy_percentage: number;
};

export type DashboardSummary = {
  total_lots: number;
  total_slots: number;
  occupied_slots: number;
  available_slots: number;
  occupancy_percentage: number;
};

export type DashboardResponse = {
  summary: DashboardSummary;
  lots: LotOccupancy[];
};

export type SlotEvent = {
  event_id: string;
  slot_id: string;
  lot_id: string;
  event_type: string;
  event_time: string;
};

export type SlotOccupancy = {
  slot_id: string;
  lot_id: string;
  occupied: boolean;
  last_event_id: string;
  last_event_time: string;
};