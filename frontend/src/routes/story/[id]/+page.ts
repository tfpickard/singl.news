import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params }) => {
  const res = await fetch(`/api/story/${params.id}`);
  if (res.status === 404) {
    return { status: 404, error: new Error('Story not found') };
  }
  return { story: await res.json() };
};
