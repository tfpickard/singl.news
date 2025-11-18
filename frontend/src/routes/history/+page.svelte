<script lang="ts">
  import dayjs from 'dayjs';
  import type { PageData } from './$types';

  export let data: PageData;
</script>

<div class="page">
  <header>
    <h1>Archive Ledger</h1>
    <p>Every dispatch preserved in order.</p>
  </header>

  <ul>
    {#each data.items as item}
      <li>
        <a href={`/story/${item.id}`}>
          <span class="time">{dayjs(item.created_at).format('MMM D, YYYY · HH:mm')}</span>
          <span class="summary">{item.summary}</span>
        </a>
      </li>
    {/each}
  </ul>
</div>

<style>
  .page {
    max-width: 760px;
    margin: 0 auto;
    padding: 2rem 1.5rem;
  }

  ul {
    list-style: none;
    padding: 0;
  }

  li {
    border-bottom: 1px solid #ddd;
  }

  a {
    display: flex;
    flex-direction: column;
    text-decoration: none;
    color: inherit;
    padding: 1rem 0;
  }

  .time {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.8rem;
    letter-spacing: 0.1em;
    color: #666;
  }

  .summary {
    font-size: 1.1rem;
  }
</style>
