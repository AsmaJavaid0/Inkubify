// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: false },

  modules: [
    '@nuxt/eslint',
    '@nuxtjs/tailwindcss',
    '@nuxtjs/supabase',
    '@pinia/nuxt',
    '@nuxtjs/google-fonts',
  ],

  typescript: {
    strict: true,
    typeCheck: false, // Run explicitly via `npm run typecheck`
  },

  css: ['~/assets/css/main.css'],

  googleFonts: {
    families: {
      'Plus Jakarta Sans': [400, 500, 600, 700],
      Inter: [400, 500, 600, 700],
    },
    display: 'swap',
  },

  supabase: {
    redirect: false,
  },

  // Automatically overridden by NUXT_PUBLIC_SITE_URL and NUXT_PUBLIC_API_BASE_URL
  runtimeConfig: {
    public: {
      siteUrl: 'http://localhost:3000',
      apiBaseUrl: 'http://localhost:8000/api/v1',
    },
  },

  app: {
    head: {
      htmlAttrs: { lang: 'en' },
      title: 'Inkubify — Ideas → Plans → Reality',
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content:
            'Inkubify helps founders in Pakistan go from idea to a running business.',
        },
        { name: 'theme-color', content: '#142535' },
      ],
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/brand/favicon.svg' },
      ],
    },
  },
})
