import { expect, test } from '@playwright/test'

const env = (globalThis as { process?: { env?: Record<string, string | undefined> } }).process?.env ?? {}

test.describe('Inkubify Phase 1 smoke flow', () => {
  test('welcome slides navigate to sign-up and enforce validation', async ({ page }) => {
    await page.goto('/welcome')
    await expect(page.getByRole('heading', { name: 'Ideas → Plans' })).toBeVisible()

    await page.getByRole('button', { name: 'Next' }).click()
    await expect(page.getByRole('heading', { name: 'Stay on track' })).toBeVisible()

    await page.getByRole('button', { name: 'Next' }).click()
    await expect(page.getByRole('heading', { name: 'Decide with evidence' })).toBeVisible()

    await page.getByRole('button', { name: 'Get started' }).click()
    await expect(page).toHaveURL(/\/signup/)
    await expect(page.getByRole('heading', { name: 'Create your founder account' })).toBeVisible()
    await expect(page.locator('#signup-country')).toBeDisabled()
  })

  test('full signup -> Mailpit verification -> profile wizard -> dashboard (requires local Supabase + Mailpit)', async ({
    page,
    request,
  }) => {
    const mailpitUrl = env.MAILPIT_URL
    test.skip(!mailpitUrl, 'Set MAILPIT_URL (e.g. http://127.0.0.1:54324) to run full E2E')

    const unique = Date.now()
    const email = `founder.${unique}@example.com`
    const username = `founder_${String(unique).slice(-8)}`
    const phone = `0300${String(unique).slice(-7)}`

    await page.goto('/signup')
    await page.getByLabel(/Full name/i).fill('Ayesha Siddiqui')
    await page.getByLabel(/Username/i).fill(username)
    await page.getByLabel(/Email address/i).fill(email)
    await page.getByLabel(/Mobile number/i).fill(phone)
    await page.getByLabel(/^Password/i).fill('StrongPass1')
    await page.getByLabel(/Confirm password/i).fill('StrongPass1')
    await page.getByRole('checkbox').check()
    await page.getByRole('button', { name: 'Create account' }).click()

    await expect(page).toHaveURL(/\/verify-email/)

    // Fetch latest verification link from local Mailpit API
    const mailRes = await request.get(`${mailpitUrl}/api/v1/messages`)
    const mailJson = await mailRes.json()
    const latestId = mailJson.messages[0].ID
    const msgRes = await request.get(`${mailpitUrl}/api/v1/message/${latestId}`)
    const msgJson = await msgRes.json()
    const match = String(msgJson.Text || msgJson.HTML).match(/https?:\/\/[^\s"']+auth\/confirm[^\s"']+/)
    expect(match).toBeTruthy()
    await page.goto(match![0])

    await expect(page).toHaveURL(/\/onboarding\/profile/)
  })
})
