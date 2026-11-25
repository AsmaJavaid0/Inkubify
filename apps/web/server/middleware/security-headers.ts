export default defineEventHandler((event) => {
  setResponseHeader(event, 'X-Frame-Options', 'DENY')
  setResponseHeader(event, 'X-Content-Type-Options', 'nosniff')
  setResponseHeader(event, 'Referrer-Policy', 'strict-origin-when-cross-origin')
  setResponseHeader(
    event,
    'Content-Security-Policy',
    [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
      "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
      "font-src 'self' https://fonts.gstatic.com data:",
      "img-src 'self' data: blob: https://*.supabase.co http://127.0.0.1:54321",
      "connect-src 'self' https://*.supabase.co wss://*.supabase.co http://localhost:8000 http://127.0.0.1:54321",
      "frame-ancestors 'none'",
    ].join('; '),
  )
})
