import type { DashboardResponse, LotOccupancy, SlotEvent, SlotOccupancy, NLQueryResponse } from '../types';

const baseUrl = import.meta.env.VITE_API_BASE_URL ?? '';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${baseUrl}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {})
    },
    ...init
  });

  if (!response.ok) {
    throw new Error(`Request failed with ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function getDashboard() {
  return request<DashboardResponse>('/api/dashboard');
}

export function getDashboardWithAbort(signal?: AbortSignal) {
  return request<DashboardResponse>('/api/dashboard', { signal });
}

export function getLots(signal?: AbortSignal) {
  return request<LotOccupancy[]>('/api/lots', { signal });
}

export function getLot(lotId: string, signal?: AbortSignal) {
  return request<LotOccupancy>(`/api/lots/${lotId}`, { signal });
}

export function getLotHistory(lotId: string, signal?: AbortSignal) {
  return request<SlotEvent[]>(`/api/lots/${lotId}/history`, { signal });
}

export function getSlotStatus(lotId: string, slotId: string, signal?: AbortSignal) {
  return request<SlotOccupancy>(`/api/lots/${lotId}/slots/${slotId}`, { signal });
}

export function askParkingQuestion(question: string) {
  return request<NLQueryResponse>('/api/query', {
    method: 'POST',
    body: JSON.stringify({
      question
    })
  });
}