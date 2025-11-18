<svelte:head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;600&family=Space+Grotesk:wght@400;500&display=swap"
    rel="stylesheet"
  />
</svelte:head>

<slot />

<style>
  :global(body) {
    margin: 0;
    font-family: 'EB Garamond', serif;
    background: #fdfdfb;
    color: #111;
  }

  :global(*) {
    box-sizing: border-box;
  }
</style>
