import { useEffect, useMemo, useState } from 'react';
import { getDashboardWithAbort, getLot, getLotHistory, getLots, getSlotStatus } from './services/api';
import type { DashboardResponse, LotOccupancy, SlotEvent, SlotOccupancy } from './types';

const POLL_INTERVAL_MS = 3000;
const SLOTS_PER_LOT = 20;
const SLOT_IDS = Array.from({ length: SLOTS_PER_LOT }, (_, i) => `T${i + 1}`);
const TIME_ZONE = 'Asia/Kolkata';

const EMPTY_DASHBOARD: DashboardResponse = {
  summary: { total_lots: 0, total_slots: 0, occupied_slots: 0, available_slots: 0, occupancy_percentage: 0 },
  lots: []
};

const formatTime = (value: string) =>
  new Date(value).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', timeZone: TIME_ZONE });

const formatSlotTime = (value?: string) => (value ? formatTime(value) : '—');

const displayLotName = (lot?: LotOccupancy | null) => lot?.lot_name ?? lot?.lot_id ?? '—';

const loadFactor = (lot: LotOccupancy) => {
  const ratio = lot.total_slots === 0 ? 0 : lot.occupied_slots / lot.total_slots;
  if (ratio >= 0.8) return 'High pressure';
  if (ratio >= 0.5) return 'Balanced';
  return 'Light load';
};

const isAbortError = (error: unknown) => error instanceof DOMException && error.name === 'AbortError';

export default function App() {
  const [dashboard, setDashboard] = useState(EMPTY_DASHBOARD);
  const [lots, setLots] = useState<LotOccupancy[]>([]);
  const [history, setHistory] = useState<SlotEvent[]>([]);
  const [lotDetail, setLotDetail] = useState<LotOccupancy | null>(null);
  const [slotDetail, setSlotDetail] = useState<SlotOccupancy | null>(null);

  const [selectedLot, setSelectedLot] = useState('LOT_1');
  const [selectedSlot, setSelectedSlot] = useState('T1');

  const [dashboardLoading, setDashboardLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(true);
  const [refreshTick, setRefreshTick] = useState(0);

  // Dashboard + lot list polling
  useEffect(() => {
    const controller = new AbortController();

    const load = async () => {
      try {
        const [dashboardPayload, lotsPayload] = await Promise.all([
          getDashboardWithAbort(controller.signal),
          getLots(controller.signal)
        ]);
        setDashboard(dashboardPayload);
        setLots(lotsPayload);
      } catch (error) {
        if (!isAbortError(error)) {
          setDashboard(EMPTY_DASHBOARD);
          setLots([]);
        }
      } finally {
        if (!controller.signal.aborted) setDashboardLoading(false);
      }
    };

    load();
    const timer = window.setInterval(load, POLL_INTERVAL_MS);

    return () => {
      controller.abort();
      window.clearInterval(timer);
    };
  }, [refreshTick]);

  // Selected lot/slot detail polling
  useEffect(() => {
    const controller = new AbortController();
    setDetailLoading(true);

    const load = async () => {
      try {
        const [historyPayload, lotPayload, slotPayload] = await Promise.all([
          getLotHistory(selectedLot, controller.signal),
          getLot(selectedLot, controller.signal),
          getSlotStatus(selectedLot, selectedSlot, controller.signal)
        ]);
        setHistory(historyPayload);
        setLotDetail(lotPayload);
        setSlotDetail(slotPayload);
      } catch (error) {
        if (!isAbortError(error)) {
          setHistory([]);
          setLotDetail(null);
          setSlotDetail(null);
        }
      } finally {
        if (!controller.signal.aborted) setDetailLoading(false);
      }
    };

    load();
    const timer = window.setInterval(load, POLL_INTERVAL_MS);

    return () => {
      controller.abort();
      window.clearInterval(timer);
    };
  }, [selectedLot, selectedSlot, refreshTick]);

  useEffect(() => setSelectedSlot('T1'), [selectedLot]);

  const visibleLots = lots.length ? lots : dashboard.lots;

  const selectedLotData = useMemo(
    () => lotDetail ?? visibleLots.find((lot) => lot.lot_id === selectedLot) ?? null,
    [lotDetail, visibleLots, selectedLot]
  );

  const totalLots = dashboard.summary.total_lots || visibleLots.length;
  const liveLots = visibleLots.filter((lot) => lot.occupancy_percentage > 0).length;
  const activeSlotCount = visibleLots.find((lot) => lot.lot_id === selectedLot)?.total_slots ?? SLOTS_PER_LOT;
  const selectedLotLabel = displayLotName(selectedLotData);

  const handleRefresh = () => setRefreshTick((tick) => tick + 1);

  return (
    <div className="shell">
      <main className="dashboard">
        <section className="hero card">
          <div className="eyebrow">Parkflow live control</div>
          <div className="hero-grid">
            <div>
              <h1>Parking events, lots, and slot pressure in one screen.</h1>
              <p>
                Live control room for the FastAPI backend, polling REST endpoints every 3 seconds.
                Layout is ready for websockets or NL2SQL later.
              </p>
              <div className="actions">
                <button className="primary" onClick={handleRefresh}>
                  Refresh live data
                </button>
              </div>
              <div className="runtime-note">
                Simulator is assumed to be running externally. Set VITE_API_BASE_URL to point at the backend.
              </div>
            </div>

            <div className="hero-stats">
              <div>
                <span>Total lots</span>
                <strong>{dashboardLoading ? '—' : totalLots}</strong>
              </div>
              <div>
                <span>Active lots</span>
                <strong>{dashboardLoading ? '—' : liveLots}</strong>
              </div>
              <div>
                <span>Occupancy</span>
                <strong>{dashboardLoading ? '—' : `${dashboard.summary.occupancy_percentage.toFixed(2)}%`}</strong>
              </div>
            </div>
          </div>
        </section>

        <section className="metric-row">
          <article className="card metric">
            <span>Total slots</span>
            <strong>{dashboard.summary.total_slots}</strong>
          </article>
          <article className="card metric">
            <span>Occupied</span>
            <strong>{dashboard.summary.occupied_slots}</strong>
          </article>
          <article className="card metric">
            <span>Available</span>
            <strong>{dashboard.summary.available_slots}</strong>
          </article>
          <article className="card metric">
            <span>Selected lot</span>
            <strong>{selectedLotLabel}</strong>
          </article>
        </section>

        <section className="content-grid">
          <div className="card panel">
            <div className="panel-head">
              <h2>Lot overview</h2>
              <span>Polling every 3 seconds</span>
            </div>
            <div className="lot-list">
              {visibleLots.map((lot) => {
                const percent = lot.total_slots === 0 ? 0 : (lot.occupied_slots / lot.total_slots) * 100;

                return (
                  <button
                    key={lot.lot_id}
                    className={`lot-card ${lot.lot_id === selectedLot ? 'active' : ''}`}
                    onClick={() => setSelectedLot(lot.lot_id)}
                  >
                    <div className="lot-copy">
                      <strong>{displayLotName(lot)}</strong>
                      <span>{lot.lot_id}</span>
                    </div>
                    <div className="lot-counts">
                      <span>{lot.occupied_slots} occupied</span>
                      <span>{lot.available_slots} free</span>
                    </div>
                    <div className="bar">
                      <div className="bar-fill" style={{ width: `${percent}%` }} />
                    </div>
                    <div className="lot-foot">
                      <span>{lot.occupancy_percentage.toFixed(2)}%</span>
                      <span>{loadFactor(lot)}</span>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          <div className="card panel">
            <div className="panel-head">
              <h2>Selected lot feed</h2>
              <span>{selectedLotLabel}</span>
            </div>

            {detailLoading && <div className="loading-state">Loading selected lot…</div>}

            <div className="selected-summary">
              <div>
                <span>Occupied</span>
                <strong>{selectedLotData?.occupied_slots ?? 0}</strong>
              </div>
              <div>
                <span>Available</span>
                <strong>{selectedLotData?.available_slots ?? 0}</strong>
              </div>
              <div>
                <span>Rate</span>
                <strong>{selectedLotData?.occupancy_percentage?.toFixed(2) ?? '0.00'}%</strong>
              </div>
            </div>

            <div className="event-list">
              {history.length === 0 ? (
                <div className="empty-state">No recent lot events returned yet.</div>
              ) : (
                history.map((event) => (
                  <article key={event.event_id} className="event-item">
                    <div>
                      <strong>{event.event_type}</strong>
                      <span>{event.slot_id}</span>
                    </div>
                    <time>{formatTime(event.event_time)}</time>
                  </article>
                ))
              )}
            </div>

            <div className="slot-panel">
              <div className="panel-head compact">
                <h3>Slot inspector</h3>
                <span>{selectedSlot}</span>
              </div>

              <div className="slot-grid">
                {SLOT_IDS.slice(0, activeSlotCount).map((slotId) => (
                  <button
                    key={slotId}
                    className={`slot-chip ${slotId === selectedSlot ? 'active' : ''}`}
                    onClick={() => setSelectedSlot(slotId)}
                  >
                    {slotId}
                  </button>
                ))}
              </div>

              <div className="slot-detail">
                <div>
                  <span>Status</span>
                  <strong>{slotDetail ? (slotDetail.occupied ? 'Occupied' : 'Available') : '—'}</strong>
                </div>
                <div>
                  <span>Last event</span>
                  <strong>{slotDetail?.last_event_id ?? '—'}</strong>
                </div>
                <div>
                  <span>Updated</span>
                  <strong>{formatSlotTime(slotDetail?.last_event_time)}</strong>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="card chatbot">
          <div className="panel-head">
            <h2>Chat lane</h2>
            <span>Reserved for NL2SQL and future query execution</span>
          </div>
          <div className="chat-placeholder">
            <p>
              Reserved for a future natural-language query interface with background SQL execution
              and human-readable results.
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}