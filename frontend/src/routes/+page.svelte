<script lang="ts">
  import dayjs from 'dayjs';
  import { onMount } from 'svelte';
  import { initSocket } from '$lib/ws';
  import { currentStory, history as historyStore, hasNewUpdate, autoScroll } from '$lib/stores/story';
  import type { PageData } from './$types';
  import { get } from 'svelte/store';

  export let data: PageData;

  const { current, history, meta } = data;
  currentStory.set(current);
  historyStore.set(history.slice(1));

  let mastheadVisible = true;

  onMount(() => {
    initSocket();
    const unsub = currentStory.subscribe((story) => {
      if (!story) return;
      if (get(autoScroll)) {
        document.getElementById('latest')?.scrollIntoView({ behavior: 'smooth' });
        hasNewUpdate.set(false);
      }
    });
    return () => unsub();
  });

  $: latest = $currentStory;
  $: scrollback = $historyStore;
</script>

<div class="page">
  <header class="masthead">
    <div>
      <h1>Singl News</h1>
      <p class="tagline">Global Continuity Desk · The world, one story at a time.</p>
    </div>
    <div class="meta">
      <p>Feeds monitored: {meta.feeds.length}</p>
      <p>Updated every {meta.update_minutes} min</p>
    </div>
  </header>

  {#if $hasNewUpdate}
    <button class="update-banner" on:click={() => hasNewUpdate.set(false)}>
      New update received · jump to latest
    </button>
  {/if}

  <section class="story" id="latest">
    <p class="timestamp">Updated {dayjs(latest?.created_at).format('MMMM D, YYYY h:mm A z')}</p>
    <article>
      {#if latest}
        {#each latest.full_text.split('\n') as paragraph}
          {#if paragraph.trim().length}
            <p>{paragraph}</p>
          {/if}
        {/each}
      {:else}
        <p>The record waits for its next dispatch.</p>
      {/if}
    </article>
  </section>

  <section class="history">
    {#each scrollback as past, index}
      <article class="past">
        <div class="timestamp">{dayjs(past.created_at).format('MMMM D, YYYY h:mm A z')}</div>
        {#each past.full_text.split('\n') as paragraph}
          {#if paragraph.trim().length}
            <p>{paragraph}</p>
          {/if}
        {/each}
      </article>
      {#if index < scrollback.length - 1}
        <div class="divider"></div>
      {/if}
    {/each}
  </section>
</div>

<style>
  .page {
    max-width: 840px;
    margin: 0 auto;
    padding: 2rem 1.5rem 4rem;
  }

  .masthead {
    display: flex;
    justify-content: space-between;
    border-bottom: 2px solid #111;
    padding-bottom: 1rem;
  }

  h1 {
    margin: 0;
    font-size: 2.6rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .tagline {
    margin: 0.25rem 0 0;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }

  .meta {
    text-align: right;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.85rem;
    color: #444;
  }

  .story {
    margin-top: 2rem;
  }

  .timestamp {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.85rem;
    color: #6b6b6b;
    text-transform: uppercase;
    letter-spacing: 0.15em;
  }

  article {
    line-height: 1.8;
    font-size: 1.1rem;
  }

  .history {
    margin-top: 3rem;
    border-top: 1px solid #ddd;
  }

  .past {
    padding: 2rem 0;
  }

  .divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #aaa, transparent);
  }

  .update-banner {
    width: 100%;
    margin-top: 1rem;
    padding: 0.5rem;
    font-family: 'Space Grotesk', sans-serif;
    border: 1px solid #111;
    background: #fff8e5;
    cursor: pointer;
  }

  @media (max-width: 640px) {
    .masthead {
      flex-direction: column;
      gap: 1rem;
    }

    .meta {
      text-align: left;
    }
  }
</style>
