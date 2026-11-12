#!/usr/bin/env node
/**
 * Headless regression for: Android keyboard resize must not close the match picker.
 * Runs against a live local server (default http://localhost:3000).
 *
 * Usage: node scripts/verify-picker-resize.mjs
 */
import { chromium } from 'playwright';

const BASE = process.env.MF_BASE_URL || 'http://localhost:3000';

async function main() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    hasTouch: true,
    isMobile: true,
    userAgent:
      'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
  });
  const page = await context.newPage();

  await page.addInitScript(() => {
    Object.defineProperty(navigator, 'maxTouchPoints', { get: () => 5 });
  });

  await page.goto(`${BASE}/index.html?group=magic-friendz`, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForFunction(() => typeof window.openLogMatchModal === 'function', null, { timeout: 20000 });

  const result = await page.evaluate(async () => {
    window.canWrite = () => true;
    window.openLogMatchModal();

    const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
    await sleep(50);

    const modal = document.getElementById('view-log-match');
    if (!modal || modal.classList.contains('hidden')) {
      return { ok: false, reason: 'modal-hidden' };
    }

    // Force wizard chrome even if group data is still loading.
    window._logMatchWizardLatched = true;
    modal.classList.add('mf-log-match-wizard', 'mf-touch-pickers');
    document.querySelectorAll('.log-match-step-panel').forEach((p) => p.classList.remove('is-wizard-active'));
    const winner = document.querySelector('.winner-slot');
    if (winner) {
      winner.classList.add('log-match-step-panel', 'is-wizard-active');
    }

    const btn = document.querySelector(
      '.winner-slot .mf-mobile-field-picker[data-picker-kind="player"], .mf-mobile-field-picker[data-picker-kind="player"]'
    );
    if (!btn) return { ok: false, reason: 'no-pilot-button', html: modal.innerHTML.slice(0, 200) };

    window.mfOpenMobileFieldPicker(btn);
    if (!modal.classList.contains('mf-picker-open')) {
      return { ok: false, reason: 'picker-did-not-open' };
    }

    // Burst of resizes like Android keyboard open/close.
    for (let i = 0; i < 10; i++) {
      window.dispatchEvent(new Event('resize'));
      await sleep(130);
    }

    const stillOpen = modal.classList.contains('mf-picker-open');
    const verify = typeof window.__mfVerifyPickerSurvivesResize === 'function'
      ? window.__mfVerifyPickerSurvivesResize(5)
      : null;

    return {
      ok: stillOpen && (!verify || verify.ok),
      reason: stillOpen ? 'survived-resize-burst' : 'closed-after-resize',
      stillOpen,
      verify,
      version: document.querySelector('meta[name="mf-app-version"]')?.content || '',
      latched: window._logMatchWizardLatched,
      classes: [...modal.classList]
    };
  });

  await browser.close();

  if (!result.ok) {
    console.error('FAIL', JSON.stringify(result, null, 2));
    process.exit(1);
  }
  console.log('PASS', JSON.stringify(result, null, 2));
}

main().catch((err) => {
  console.error('FAIL', err);
  process.exit(1);
});
