export type StoryVersion = {
  id: number;
  created_at: string;
  full_text: string;
  summary: string;
  context_summary?: string | null;
};

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000/api';

export async function fetchCurrentStory() {
  const res = await fetch(`${API_BASE}/story/current`);
  if (!res.ok) throw new Error('Failed to load story');
  return (await res.json()) as StoryVersion;
}

export async function fetchHistory(limit = 10, offset = 0) {
  const res = await fetch(`${API_BASE}/story/history?limit=${limit}&offset=${offset}`);
  if (!res.ok) throw new Error('Failed to load history');
  return (await res.json()) as StoryVersion[];
}

export async function fetchMeta() {
  const res = await fetch(`${API_BASE}/meta`);
  if (!res.ok) throw new Error('Failed to load meta');
  return res.json();
}
