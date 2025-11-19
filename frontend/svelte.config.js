import adapter from '@sveltejs/adapter-static';

const config = {
  kit: {
    adapter: adapter({
      fallback: '200.html'
    }),
    alias: {
      $lib: 'src/lib'
    }
  }
};

export default config;
