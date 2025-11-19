import adapter from '@sveltejs/adapter-static';

const config = {
  kit: {
    adapter: adapter({
      // Emit an SPA-style index.html so the Docker container can serve
      // the client app without falling back to a directory listing.
      fallback: 'index.html'
    }),
    alias: {
      $lib: 'src/lib'
    }
  }
};

export default config;
