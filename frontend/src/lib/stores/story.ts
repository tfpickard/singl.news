import { writable } from 'svelte/store';
import type { StoryVersion } from '$lib/api';

export const currentStory = writable<StoryVersion | null>(null);
export const history = writable<StoryVersion[]>([]);
export const hasNewUpdate = writable(false);
export const autoScroll = writable(true);
