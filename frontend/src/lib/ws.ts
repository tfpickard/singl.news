import type { StoryVersion } from '$lib/api';
import { currentStory, history, hasNewUpdate } from '$lib/stores/story';

const WS_BASE = import.meta.env.VITE_WS_BASE ?? 'ws://localhost:8000/ws/story';

let socket: WebSocket | null = null;
let reconnectTimeout: ReturnType<typeof setTimeout> | null = null;

function connect() {
  socket = new WebSocket(WS_BASE);

  socket.addEventListener('message', (event) => {
    const payload = JSON.parse(event.data);
    if (payload.type === 'initial' || payload.type === 'update') {
      handleStory(payload.story as StoryVersion, payload.type === 'update');
    }
  });

  socket.addEventListener('close', () => {
    if (reconnectTimeout) clearTimeout(reconnectTimeout);
    reconnectTimeout = setTimeout(connect, 3000);
  });
}

function handleStory(story: StoryVersion, isUpdate: boolean) {
  currentStory.set(story);
  if (isUpdate) {
    history.update((items) => [story, ...items]);
    hasNewUpdate.set(true);
  }
}

export function initSocket() {
  if (socket) return;
  connect();
}
