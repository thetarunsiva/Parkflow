from fastapi import FastAPI, HTTPException
from db import get_db_connection
from schemas import LotOccupancy, SlotOccupancy, SlotEvents, DashboardSummary, DashboardResponse

from psycopg2.extras import RealDictCursor

app = FastAPI()

@app.get("/")
def home():
      return {
            "message": "Welcomeee to Parkflowww Backend!"
      }

@app.get("/api/lots", response_model=list[LotOccupancy])
def get_lots():
      conn = get_db_connection()
      cursor = conn.cursor(cursor_factory=RealDictCursor)
      cursor.execute(
            """
            SELECT lot_id, occupied_slots, available_slots, total_slots, occupancy_percentage
            FROM lot_occupancy
            ORDER BY lot_id;
            """
      )
      rows = cursor.fetchall()
      cursor.close()
      conn.close()
      return rows

@app.get("/api/lots/{lot_id}", response_model=LotOccupancy)
def get_lot(lot_id: str):
      conn = get_db_connection()
      cursor = conn.cursor(cursor_factory=RealDictCursor)
      cursor.execute(
            """
            SELECT lot_id, occupied_slots, available_slots, total_slots, occupancy_percentage
            FROM lot_occupancy
            WHERE lot_id = %s;
            """,
            (lot_id,)
      )
      row = cursor.fetchone()
      if row is None:
            cursor.close()
            conn.close()
            raise HTTPException(
                  status_code=404,
                  detail="Given Parking lot not found!"
            )
      cursor.close()
      conn.close()
      return row

@app.get("/api/lots/{lot_id}/slots/{slot_id}", response_model=SlotOccupancy)
def get_slot_status(lot_id: str, slot_id: str):
      conn = get_db_connection()
      cursor = conn.cursor(cursor_factory=RealDictCursor)
      cursor.execute(
            """
            SELECT slot_id, lot_id, occupied, last_event_id, last_event_time
            FROM slot_status
            WHERE lot_id = %s AND slot_id = %s;
            """,
            (lot_id, slot_id)
      )
      row = cursor.fetchone()
      if row is None:
            cursor.close()
            conn.close()
            raise HTTPException(
                  status_code=404,
                  detail="Given parking lot or slot not found in db!"
            )
      cursor.close()
      conn.close()
      return row    

@app.get("/api/lots/{lot_id}/history", response_model=list[SlotEvents])
def get_lot_history(lot_id: str):
      conn = get_db_connection()
      cursor = conn.cursor(cursor_factory=RealDictCursor)
      cursor.execute(
            """
            SELECT 1 
            FROM parking_lots
            WHERE lot_id = %s;
            """,
            (lot_id,)
      )
      exists = cursor.fetchone()
      if exists is None:
            cursor.close()
            conn.close()
            raise HTTPException(
                  status_code=404,
                  detail="Given Parking lot not found!"
            )
      cursor.execute(
            """
            SELECT event_id, slot_id, lot_id, event_type, event_time
            FROM slot_events
            WHERE lot_id = %s
            ORDER BY event_time DESC 
            LIMIT 20;
            """,
            (lot_id,)
      )
      row = cursor.fetchall()
      cursor.close()
      conn.close()
      return row

@app.get("/api/dashboard", response_model=DashboardResponse)
def dashboard():
      conn = get_db_connection()
      cursor = conn.cursor(cursor_factory=RealDictCursor)
      cursor.execute(
            """
            SELECT 
            COUNT(*) AS total_lots,
            SUM(total_slots) AS total_slots,
            SUM(occupied_slots) AS occupied_slots,
            SUM(available_slots) AS available_slots,
            ROUND ((SUM(occupied_slots) * 100.0) / SUM(total_slots), 2) AS occupancy_percentage
            FROM lot_occupancy;
            """
      )
      summary = cursor.fetchone()
      cursor.execute(
            """
            SELECT lot_id, occupied_slots, available_slots, total_slots, occupancy_percentage
            FROM lot_occupancy
            ORDER BY lot_id;
            """
      )
      lots = cursor.fetchall()
      cursor.close()
      conn.close()
      return {
            "summary": summary,
            "lots": lots
      }