"""Replace the entire inline <style> block in site/index.html with a clean white design."""
import re, pathlib

NEW_CSS = """
    /* =============================================
       MyKutch Homepage – Clean White Design
       ============================================= */

    /* ── Variables ──────────────────────────────── */
    :root {
      --text:          #1a3a4a;
      --muted:         #4d7080;
      --accent:        #1a7fa0;
      --accent-strong: #0e5f7a;
      --heading:       #0a3d5c;
      --border:        rgba(0, 90, 120, 0.12);
      --shadow-sm:     0 2px 8px  rgba(0, 60, 90, 0.07);
      --shadow-md:     0 8px 24px rgba(0, 60, 90, 0.10);
      --shadow-lg:     0 20px 50px rgba(0, 60, 90, 0.13);
      --radius:        16px;
      --radius-xl:     24px;
      --max-w:         1400px;
      --t:             180ms ease;
    }

    /* ── Reset ──────────────────────────────────── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html  { scroll-behavior: smooth; }
    body  {
      background: #ffffff;
      color: var(--text);
      font-family: 'Sora', system-ui, sans-serif;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }
    img   { max-width: 100%; display: block; }
    a     { color: inherit; text-decoration: none; }
    button, a, input, select { font: inherit; cursor: pointer; }
    button { border: 0; background: none; padding: 0; }
    a:focus-visible, button:focus-visible {
      outline: 2px solid var(--accent);
      outline-offset: 3px;
      border-radius: 4px;
    }

    /* ── Container ──────────────────────────────── */
    .container {
      width: min(var(--max-w), calc(100% - 40px));
      margin: 0 auto;
    }

    /* ── Page shell (no decorative pseudo-elements) */
    .page-shell               { min-height: 100vh; }
    .page-shell::before,
    .page-shell::after        { display: none; }

    /* ── Header / Nav ────────────────────────────── */
    .site-header {
      position: sticky;
      top: 0;
      z-index: 100;
      background: #ffffff;
      border-bottom: 1px solid var(--border);
      transition: box-shadow var(--t);
    }
    .site-header.is-scrolled  { box-shadow: var(--shadow-md); }

    .nav-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1.5rem;
      height: 68px;
    }

    .brand {
      display: inline-flex;
      align-items: center;
      gap: 0.75rem;
      flex-shrink: 0;
    }
    .brand-mark {
      width: 38px;
      height: 38px;
      border-radius: 12px;
      background: var(--accent);
      display: grid;
      place-items: center;
    }
    .brand-mark img {
      width: 22px;
      height: 22px;
      object-fit: contain;
    }
    .brand-text   { display: flex; flex-direction: column; }
    .brand-title  {
      font-family: 'Cormorant Garamond', serif;
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--heading);
      line-height: 1;
    }
    .brand-subtitle {
      display: block;
      font-size: 0.6rem;
      font-weight: 600;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: var(--muted);
      margin-top: 0.2rem;
    }

    .desktop-nav {
      display: flex;
      align-items: center;
      gap: 0.25rem;
      flex: 1;
      justify-content: center;
    }
    .desktop-nav a {
      color: var(--muted);
      font-size: 0.875rem;
      font-weight: 500;
      padding: 0.5rem 0.75rem;
      border-radius: 8px;
      transition: color var(--t), background var(--t);
    }
    .desktop-nav a:hover { color: var(--heading); background: #f4f8fa; }

    /* ── Buttons ─────────────────────────────────── */
    .nav-cta,
    .button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      min-height: 42px;
      padding: 0.6rem 1.25rem;
      border-radius: 999px;
      border: 1px solid transparent;
      font-size: 0.875rem;
      font-weight: 600;
      transition: transform var(--t), box-shadow var(--t), background var(--t);
      white-space: nowrap;
    }
    .nav-cta {
      background: var(--accent);
      color: #ffffff;
    }
    .nav-cta:hover {
      background: var(--accent-strong);
      transform: translateY(-1px);
      box-shadow: var(--shadow-md);
    }
    .button-primary {
      background: var(--accent);
      color: #ffffff;
      font-weight: 700;
    }
    .button-primary:hover {
      background: var(--accent-strong);
      transform: translateY(-2px);
      box-shadow: var(--shadow-lg);
    }
    .button-secondary {
      background: #ffffff;
      color: var(--accent);
      border-color: var(--border);
    }
    .button-secondary:hover {
      background: #f4f8fa;
      transform: translateY(-1px);
    }

    /* ── Mobile nav ──────────────────────────────── */
    .mobile-toggle {
      display: none;
      width: 44px;
      height: 44px;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: #ffffff;
      color: var(--heading);
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .mobile-toggle svg { width: 22px; height: 22px; }
    .mobile-panel      { display: none; padding: 0 0 1rem; }
    .mobile-panel.is-open { display: block; }
    .mobile-panel-inner {
      display: grid;
      gap: 0.25rem;
      padding: 0.75rem;
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: var(--radius-xl);
      box-shadow: var(--shadow-lg);
    }
    .mobile-panel-inner a {
      padding: 0.85rem 1rem;
      border-radius: 10px;
      color: var(--text);
      font-weight: 500;
      font-size: 0.9rem;
      transition: background var(--t);
    }
    .mobile-panel-inner a:hover { background: #f4f8fa; }
    .mobile-panel-inner .nav-cta { margin-top: 0.25rem; }

    /* ── Hero ────────────────────────────────────── */
    .hero { padding: 5rem 0 4rem; }

    /* hero uses .container.hero-grid – apply grid directly on it */
    .hero-grid {
      display: grid;
      grid-template-columns: 1fr min(360px, 38%);
      gap: 3rem;
      align-items: start;
    }

    .hero-panel {
      position: relative;
      display: flex;
      align-items: flex-start;
      min-height: unset;
      background: transparent;
    }
    .hero-copy {
      width: 100%;
      padding: 0;
      background: none;
      border: none;
      box-shadow: none;
    }

    /* ── Typography helpers ──────────────────────── */
    .eyebrow,
    .mini-kicker,
    .section-kicker {
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--accent);
    }
    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      margin-bottom: 1rem;
    }
    .eyebrow::before {
      content: "";
      width: 28px;
      height: 2px;
      background: var(--accent);
      border-radius: 2px;
      flex-shrink: 0;
    }

    /* Shared serif headings */
    .hero h1,
    .section-head h2,
    .aside-title,
    .planner-card h3,
    .community-card h2,
    .cta-band h2,
    .destination-body h3,
    .craft-card-body h3,
    .fact h3,
    .tip-item strong,
    .planner-item strong,
    .footer-card h3,
    .footer-brand strong {
      font-family: 'Cormorant Garamond', serif;
      letter-spacing: -0.02em;
      color: var(--heading);
    }

    .hero h1 {
      font-size: clamp(3rem, 6vw, 5.5rem);
      line-height: 1;
      font-weight: 700;
    }
    .hero-tagline {
      display: inline-block;
      margin-top: 0.5rem;
      font-size: 0.78rem;
      font-weight: 600;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--accent);
      font-family: 'Sora', sans-serif;
    }
    .hero-subtitle {
      margin-top: 0.75rem;
      font-size: 0.9rem;
      font-weight: 600;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: var(--heading);
    }
    .hero-desc {
      max-width: 52ch;
      margin-top: 1rem;
      color: var(--muted);
      font-size: 1rem;
      line-height: 1.7;
    }

    .hero-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-top: 2rem;
    }

    /* ── Metrics ─────────────────────────────────── */
    .metrics {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1rem;
      margin-top: 2.5rem;
    }
    .metric {
      padding: 1rem 1.1rem;
      border-radius: var(--radius);
      background: #ffffff;
      border: 1px solid var(--border);
      box-shadow: var(--shadow-sm);
    }
    .metric strong {
      display: block;
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--heading);
    }
    .metric span {
      display: block;
      margin-top: 0.3rem;
      color: var(--muted);
      font-size: 0.78rem;
      line-height: 1.5;
    }

    /* ── Hero aside ──────────────────────────────── */
    .hero-aside {
      position: static;
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .aside-card {
      padding: 1.25rem;
      border-radius: var(--radius-xl);
      background: #ffffff;
      border: 1px solid var(--border);
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    .aside-card-header { display: grid; gap: 0.4rem; }
    .aside-title {
      font-size: 1.3rem;
      line-height: 1.2;
      color: var(--heading);
    }
    .aside-copy {
      font-size: 0.84rem;
      color: var(--muted);
      line-height: 1.6;
    }

    .hero-aside .mini-kicker,
    .hero-aside .aside-copy,
    .hero-aside .trip-brief-copy,
    .hero-aside .trip-brief-meta { color: var(--muted); }
    .hero-aside .trip-brief-value,
    .hero-aside .trip-brief-strong { color: var(--heading); }

    .trip-brief { display: grid; gap: 0.75rem; }
    .trip-brief-item {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 0.5rem;
      align-items: start;
      padding: 0.85rem 1rem;
      border-radius: 12px;
      background: #f8fbfd;
      border: 1px solid var(--border);
    }
    .hero-aside .trip-brief-item { background: #f8fbfd; }

    .trip-brief-copy { min-width: 0; display: grid; gap: 0.25rem; }
    .trip-brief-label {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0.3rem 0.65rem;
      border-radius: 999px;
      background: #e3f4fa;
      color: var(--accent-strong);
      font-size: 0.63rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      white-space: nowrap;
    }
    .trip-brief-value,
    .trip-brief-strong {
      display: block;
      font-size: 0.9rem;
      line-height: 1.35;
      font-weight: 600;
      color: var(--heading);
    }
    .trip-brief-meta {
      font-size: 0.79rem;
      line-height: 1.55;
      color: var(--muted);
      overflow-wrap: anywhere;
    }
    .trip-brief-footer {
      padding-top: 0.5rem;
      border-top: 1px solid var(--border);
    }
    .trip-brief-footer p {
      margin: 0;
      color: var(--muted);
      font-size: 0.78rem;
      line-height: 1.55;
    }

    .aside-map {
      position: relative;
      min-height: 180px;
      overflow: hidden;
      border-radius: var(--radius-xl);
      background: #f4f8fa;
      border: 1px solid var(--border);
    }
    .aside-map img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    .aside-map-label {
      position: absolute;
      right: 0.75rem;
      bottom: 0.75rem;
      max-width: 180px;
      padding: 0.6rem 0.75rem;
      border-radius: 12px;
      background: #ffffff;
      color: var(--heading);
      box-shadow: var(--shadow-md);
    }
    .aside-map-label strong {
      display: block;
      margin-bottom: 0.2rem;
      font-size: 0.82rem;
    }
    .aside-map-label span {
      display: block;
      color: var(--muted);
      font-size: 0.68rem;
      line-height: 1.55;
    }

    /* ── Section base ────────────────────────────── */
    .section { padding: 5rem 0; }

    .section-head {
      display: grid;
      gap: 0.75rem;
      margin-bottom: 2.5rem;
    }
    .section-head.centered {
      text-align: center;
      justify-items: center;
    }
    .section-head h2 {
      font-size: clamp(2.2rem, 4.5vw, 3.8rem);
      line-height: 1;
      max-width: 16ch;
    }
    .section-head p {
      margin: 0;
      max-width: 60ch;
      font-size: 1rem;
      color: var(--muted);
      line-height: 1.7;
    }

    /* ── Fact band ───────────────────────────────── */
    .fact-band { padding: 3rem 0 1.5rem; }
    .fact-band .container {
      display: flex;
      justify-content: center;
    }

    .fact-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 1rem;
      width: 100%;
    }

    .fact {
      display: grid;
      grid-template-columns: auto auto 1fr;
      align-items: center;
      gap: 0.75rem;
      padding: 1.25rem;
      border-radius: var(--radius);
      background: #ffffff;
      border: 1px solid var(--border);
      box-shadow: var(--shadow-sm);
    }
    .fact::after { display: none; }
    .fact-top { display: contents; }
    .fact-icon {
      width: 40px;
      height: 40px;
      border-radius: 12px;
      display: grid;
      place-items: center;
      background: #eef6fb;
      color: var(--accent);
      flex-shrink: 0;
    }
    .fact-icon svg {
      width: 20px;
      height: 20px;
      stroke: currentColor;
      fill: none;
      stroke-width: 1.8;
      stroke-linecap: round;
      stroke-linejoin: round;
    }
    .fact-body {
      display: flex;
      flex-direction: column;
      gap: 0.2rem;
      min-width: 0;
    }
    .fact-index {
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--accent);
    }
    .fact h3 {
      font-size: 0.97rem;
      line-height: 1.2;
      white-space: nowrap;
    }
    .fact p {
      color: var(--muted);
      font-size: 0.8rem;
      line-height: 1.3;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .fact-coast,
    .fact-hills,
    .fact-mystery,
    .fact-spirit { background: #ffffff; }

    /* ── Story section ───────────────────────────── */
    .story-section .container { display: block; }
    .story-card {
      padding: 2rem;
      border-radius: var(--radius-xl);
      background: #ffffff;
      border: 1px solid var(--border);
      box-shadow: var(--shadow-sm);
    }
    .story-card::after { display: none; }
    .story-note { color: var(--accent); font-weight: 600; }
    .story-section .story-card { max-width: 1180px; margin: 0 auto; }
    .story-section .section-head h2 { max-width: none; text-align: center; }
    .story-section-title-line  { display: block; white-space: nowrap; }
    .story-section-title-accent {
      margin-top: 0.35em;
      font-size: 0.7em;
      color: #c0273a;
    }
    .story-card p {
      color: var(--muted);
      line-height: 1.7;
    }
    .story-grid,
    .community-grid {
      display: grid;
      grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
      gap: 2rem;
      align-items: start;
    }
    .story-facts {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: var(--radius-xl);
      box-shadow: var(--shadow-sm);
      padding: 1.5rem;
    }
    .snapshot-item > div:last-child { min-width: 0; }

    /* ── Destinations ────────────────────────────── */
    .destination-grid {
      display: grid;
      grid-template-columns: repeat(12, minmax(0, 1fr));
      gap: 1.25rem;
    }
    .destination-card {
      grid-column: span 4;
      border-radius: var(--radius-xl);
      background: #ffffff;
      border: 1px solid var(--border);
      box-shadow: var(--shadow-sm);
      overflow: hidden;
      transition: transform var(--t), box-shadow var(--t);
    }
    .destination-card-featured { grid-column: span 7; }
    .destination-card-wide     { grid-column: span 5; }

    .destination-card:hover,
    .destination-card:focus-within {
      transform: translateY(-4px);
      box-shadow: var(--shadow-lg);
    }
    .destination-card-link {
      display: flex;
      flex-direction: column;
      height: 100%;
      color: inherit;
    }
    .destination-media {
      position: relative;
      aspect-ratio: 1.24 / 1;
      overflow: hidden;
      flex-shrink: 0;
    }
    .destination-card-featured .destination-media,
    .destination-card-wide .destination-media { aspect-ratio: 1.7 / 1; }

    .destination-media img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 300ms ease;
    }
    .destination-card:hover .destination-media img,
    .destination-card:focus-within .destination-media img { transform: scale(1.05); }

    .destination-overlay {
      position: absolute;
      inset: auto 0.75rem 0.75rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .category-pill {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0.35rem 0.75rem;
      border-radius: 999px;
      font-size: 0.72rem;
      font-weight: 700;
      background: #ffffff;
      color: var(--accent-strong);
      box-shadow: var(--shadow-sm);
      min-height: 28px;
    }
    .tag {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0.35rem 0.75rem;
      border-radius: 999px;
      font-size: 0.72rem;
      font-weight: 700;
      background: #eef6fb;
      color: var(--accent-strong);
      min-height: 28px;
    }
    .tags { display: flex; flex-wrap: wrap; gap: 0.4rem; }

    .destination-body {
      display: grid;
      gap: 0.75rem;
      padding: 1.1rem;
      flex: 1;
    }
    .destination-body h3 {
      font-size: 1.75rem;
      line-height: 1;
    }
    .destination-body p {
      color: var(--muted);
      font-size: 0.875rem;
      line-height: 1.6;
    }
    .destination-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
      padding-top: 0.25rem;
      margin-top: auto;
    }
    .destination-link {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      color: var(--accent);
      font-size: 0.875rem;
      font-weight: 700;
    }
    .destination-link svg {
      width: 14px;
      height: 14px;
      transition: transform var(--t);
    }
    .destination-card:hover .destination-link svg,
    .destination-card:focus-within .destination-link svg { transform: translateX(3px); }

    .section-head-destinations h2 {
      max-width: none;
      font-size: clamp(1.6rem, 3vw, 3.4rem);
    }

    /* ── CTA band ────────────────────────────────── */
    .cta-band {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 1.5rem;
      align-items: center;
      padding: 2.5rem;
      border-radius: var(--radius-xl);
      background: #ffffff;
      border: 1px solid var(--border);
      box-shadow: var(--shadow-md);
    }
    .cta-band .section-kicker { color: var(--muted); }
    .cta-band h2 {
      font-size: clamp(2rem, 3.5vw, 3rem);
      line-height: 1;
      margin-top: 0.5rem;
    }
    .cta-band p {
      margin-top: 0.75rem;
      max-width: 54ch;
      font-size: 0.95rem;
      color: var(--muted);
    }
    .cta-band .button-primary { min-width: 200px; }

    /* ── Craft grid ──────────────────────────────── */
    .craft-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 1rem;
    }
    .craft-card {
      border-radius: var(--radius-xl);
      background: #ffffff;
      border: 1px solid var(--border);
      box-shadow: var(--shadow-sm);
      overflow: hidden;
      transition: transform var(--t), box-shadow var(--t);
    }
    .craft-card:hover,
    .craft-card:focus-visible {
      transform: translateY(-4px);
      box-shadow: var(--shadow-lg);
    }
    .craft-card img {
      width: 100%;
      aspect-ratio: 1.1 / 1;
      object-fit: cover;
      transition: transform 300ms ease;
    }
    .craft-card:hover img { transform: scale(1.05); }
    .craft-card-body {
      display: grid;
      gap: 0.5rem;
      padding: 1rem 1.1rem 1.25rem;
    }
    .craft-card-body h3 {
      font-size: 1.1rem;
      line-height: 1.3;
    }
    .craft-card-body p {
      margin: 0;
      color: var(--muted);
      font-size: 0.84rem;
      line-height: 1.5;
    }

    /* ── Planner ─────────────────────────────────── */
    .planner-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 1.25rem;
    }
    .planner-card {
      padding: 1.75rem;
      border-radius: var(--radius-xl);
      background: #ffffff;
      border: 1px solid var(--border);
      box-shadow: var(--shadow-sm);
    }
    .planner-card.wide { grid-column: 1 / -1; }
    .planner-card h3   { font-size: 2rem; line-height: 1; }
    .planner-topline {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      flex-wrap: wrap;
    }
    .planner-list { display: grid; gap: 0.75rem; margin-top: 1rem; }
    .planner-item {
      padding: 0.85rem 1rem;
      border-radius: 12px;
      background: #f8fbfd;
      border: 1px solid var(--border);
    }
    .planner-item strong {
      display: block;
      font-size: 0.95rem;
      line-height: 1.35;
    }
    .planner-item p {
      margin-top: 0.25rem;
      color: var(--muted);
      font-size: 0.84rem;
      line-height: 1.55;
    }

    .tips-list {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 1rem;
      margin-top: 1.25rem;
    }
    .tip-item {
      padding: 0.85rem 1rem;
      border-radius: 12px;
      background: #f8fbfd;
      border: 1px solid var(--border);
    }
    .tip-item strong {
      display: block;
      font-size: 0.95rem;
      line-height: 1.35;
    }
    .tip-item p {
      margin-top: 0.25rem;
      color: var(--muted);
      font-size: 0.84rem;
      line-height: 1.55;
    }

    /* ── Community ───────────────────────────────── */
    .community-card {
      padding: 2rem;
      border-radius: var(--radius-xl);
      background: #ffffff;
      border: 1px solid var(--border);
      box-shadow: var(--shadow-sm);
    }
    .community-card h2 {
      font-size: clamp(2.2rem, 3.5vw, 3.2rem);
      line-height: 1;
      margin-top: 0.5rem;
    }
    .community-card p {
      color: var(--muted);
      line-height: 1.7;
    }
    .community-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-top: 1.5rem;
    }
    .community-actions .button-secondary {
      color: var(--accent);
      border-color: var(--border);
      background: #ffffff;
    }
    .community-details {
      display: grid;
      gap: 0.35rem;
      margin-top: 1.5rem;
      color: var(--muted);
      font-size: 0.875rem;
    }
    .community-details a {
      color: var(--accent);
      font-weight: 600;
    }
    .map-card {
      border-radius: var(--radius-xl);
      background: #f4f8fa;
      border: 1px solid var(--border);
      overflow: hidden;
    }
    .map-card iframe {
      width: 100%;
      min-height: 320px;
      border: 0;
      display: block;
    }

    /* ── Footer ──────────────────────────────────── */
    .footer { padding: 0 0 2rem; }
    .footer-card {
      display: grid;
      grid-template-columns: minmax(0, 1.2fr) repeat(3, minmax(0, 0.7fr));
      gap: 2rem;
      padding: 2.5rem;
      border-radius: var(--radius-xl);
      background: #ffffff;
      border: 1px solid var(--border);
      box-shadow: var(--shadow-sm);
    }
    .footer-card h3 {
      font-family: 'Sora', sans-serif;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      font-size: 0.8rem;
      margin-bottom: 0.75rem;
      color: var(--heading);
    }
    .footer-brand { display: grid; gap: 1rem; max-width: 28rem; }
    .footer-brand-top {
      display: flex;
      align-items: center;
      gap: 0.9rem;
    }
    .footer-brand-top img {
      width: 52px;
      height: 52px;
      object-fit: contain;
      border-radius: 14px;
      border: 1px solid var(--border);
      padding: 0.35rem;
    }
    .footer-brand strong {
      display: block;
      font-size: 1.6rem;
      line-height: 1;
    }
    .footer-brand span {
      display: block;
      margin-top: 0.2rem;
      color: var(--muted);
      font-size: 0.7rem;
      letter-spacing: 0.16em;
      text-transform: uppercase;
    }
    .footer-brand p {
      color: var(--muted);
      font-size: 0.875rem;
      line-height: 1.7;
    }
    .footer-meta {
      margin-top: 0.75rem;
      padding-top: 0.75rem;
      border-top: 1px solid var(--border);
      color: var(--muted);
      font-size: 0.8rem;
      line-height: 1.75;
    }
    .footer-column { display: grid; gap: 0.75rem; }
    .footer-column a,
    .footer-column span {
      display: block;
      color: var(--muted);
      font-size: 0.875rem;
      transition: color var(--t);
    }
    .footer-column a:hover { color: var(--heading); }

    /* ── Reveal animation ────────────────────────── */
    .reveal {
      opacity: 0;
      transform: translateY(24px);
      transition: opacity 600ms ease, transform 600ms ease;
    }
    .reveal.is-visible {
      opacity: 1;
      transform: none;
    }

    /* ── Responsive ──────────────────────────────── */
    @media (max-width: 1080px) {
      .desktop-nav { display: none; }
      .mobile-toggle { display: inline-flex; }

      .hero-grid,
      .story-grid,
      .community-grid,
      .footer-card {
        grid-template-columns: 1fr;
      }
      .hero-aside { position: static; width: 100%; }
      .craft-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .fact-grid  { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .destination-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .destination-card,
      .destination-card-featured,
      .destination-card-wide { grid-column: span 1; }
      .tips-list { grid-template-columns: 1fr; }
      .cta-band  { grid-template-columns: 1fr; }
      .section-head-destinations h2 { font-size: clamp(1.4rem, 4vw, 2.4rem); white-space: normal; }
    }

    @media (max-width: 820px) {
      .hero      { padding: 3.5rem 0 3rem; }
      .fact-band { padding: 2rem 0 1rem; }
      .section   { padding: 3.5rem 0; }
      .story-card,
      .planner-card,
      .community-card,
      .footer-card,
      .cta-band  { padding: 1.5rem; }
      .metrics,
      .destination-grid,
      .craft-grid,
      .planner-grid,
      .fact-grid { grid-template-columns: 1fr; }
      .fact      { grid-template-columns: auto auto 1fr; }
      .fact h3,
      .fact p    { white-space: normal; }
      .container { width: min(100%, calc(100% - 24px)); }
    }

    @media (max-width: 640px) {
      .nav-bar    { height: 60px; }
      .brand-title { font-size: 1.3rem; }
      .hero h1    { font-size: clamp(2.4rem, 12vw, 3.5rem); }
      .hero-subtitle { font-size: 0.85rem; }
      .button,
      .nav-cta,
      .community-actions .button,
      .community-actions .button-secondary { width: 100%; }
    }

    @media (prefers-reduced-motion: reduce) {
      html { scroll-behavior: auto; }
      *, *::before, *::after {
        animation: none !important;
        transition-duration: 0.01ms !important;
        transition-delay: 0ms !important;
      }
      .reveal,
      .reveal.is-visible {
        opacity: 1;
        transform: none;
      }
    }
"""

path = pathlib.Path("site/index.html")
html = path.read_text(encoding="utf-8")

# Replace the entire <style>...</style> block
new_html = re.sub(
    r'<style>[\s\S]*?</style>',
    "<style>" + NEW_CSS + "  </style>",
    html,
    count=1
)

if new_html == html:
    print("ERROR: pattern not matched – no replacement made")
else:
    path.write_text(new_html, encoding="utf-8")
    print("Done – style block replaced successfully")
