import type { PageLoad } from './$types';
import { fetchCurrentStory, fetchHistory, fetchMeta } from '$lib/api';

export const load: PageLoad = async ({ fetch }) => {
  const [storyRes, historyRes, metaRes] = await Promise.all([
    fetch('/api/story/current').then((r) => r.json()).catch(() => fetchCurrentStory()),
    fetch('/api/story/history?limit=10').then((r) => r.json()).catch(() => fetchHistory()),
    fetch('/api/meta').then((r) => r.json()).catch(() => fetchMeta())
  ]);

  return {
    current: storyRes,
    history: historyRes,
    meta: metaRes
  };
};
