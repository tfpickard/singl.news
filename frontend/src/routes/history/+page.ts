import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, url }) => {
  const limit = Number(url.searchParams.get('limit') ?? 30);
  const offset = Number(url.searchParams.get('offset') ?? 0);
  const res = await fetch(`/api/story/history?limit=${limit}&offset=${offset}`);
  const items = await res.json();
  return { items };
};
