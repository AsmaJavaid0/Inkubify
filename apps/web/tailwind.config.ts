import type { Config } from 'tailwindcss'

export default <Partial<Config>>{
  content: [
    './components/**/*.{vue,js,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './composables/**/*.{js,ts}',
    './utils/**/*.{js,ts}',
    './app.vue',
  ],
  theme: {
    extend: {
      colors: {
        // Strict Inkubify brand tokens (§4.1) — derived variants use CSS color-mix
        'navy-900': 'var(--color-navy-900)', // #142535 — Page background & primary text on light/gold
        'navy-700': 'var(--color-navy-700)', // #23384B — Cards, inputs, panels, borders
        'navy-border': 'var(--color-navy-border)', // color-mix(#F7F7F7 14%, #23384B)
        'snow-100': 'var(--color-snow-100)', // #F7F7F7 — Primary text on dark, light surfaces
        'snow-muted': 'var(--color-snow-muted)', // color-mix(#F7F7F7 72%, #142535)
        'gold-500': 'var(--color-gold-500)', // #C19829 — Primary buttons, links, focus ring, active step
        'gold-hover': 'var(--color-gold-hover)', // color-mix(#C19829 88%, #F7F7F7)
        // Functional state colours (§4.1)
        danger: 'var(--color-danger)',
        success: 'var(--color-success)',
        warning: 'var(--color-warning)',
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'Inter', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        card: '16px',
        input: '12px',
        btn: '10px',
      },
    },
  },
}
