<script lang="ts">
  import dayjs from 'dayjs';
  import type { PageData } from './$types';

  export let data: PageData;
</script>

<div class="page">
  <a class="back" href="/">← Return to live desk</a>
  <h1>Story #{data.story.id}</h1>
  <p class="timestamp">Captured {dayjs(data.story.created_at).format('MMMM D, YYYY h:mm A z')}</p>
  <article>
    {#each data.story.full_text.split('\n') as paragraph}
      {#if paragraph.trim().length}
        <p>{paragraph}</p>
      {/if}
    {/each}
  </article>
</div>

<style>
  .page {
    max-width: 760px;
    margin: 0 auto;
    padding: 2rem 1.5rem 4rem;
  }

  .back {
    display: inline-block;
    margin-bottom: 1rem;
    text-decoration: none;
    font-family: 'Space Grotesk', sans-serif;
    color: #111;
  }

  h1 {
    margin-bottom: 0.25rem;
  }

  .timestamp {
    font-size: 0.85rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #555;
  }

  article {
    line-height: 1.8;
    font-size: 1.1rem;
  }
</style>
