# Cosmic Consultancy — Website

Marketing site for Cosmic Consultancy Services — a full-spectrum technology partner
covering cloud, AI integration, cyber security, data analytics, CRM, ERP,
app & web development, and quality assurance.

## Tech

Static site — no build step, no backend required.

- **HTML** — page structure (21 pages: home, services, industries, case studies, about, contact)
- **CSS** — `assets/styles.css` (design system, light-blue brand, responsive)
- **JavaScript** — `assets/app.js` (3D hero, scroll animations, contact form), `assets/i18n.js` (EN / ES / Tigrinya)
- **Libraries (CDN, no install):** Three.js, GSAP + ScrollTrigger

## Run locally

No server needed — just open `index.html` in a browser, or double-click `start-site.bat`.

For clean `localhost` URLs instead:

```bash
python -m http.server 8000
# then open http://localhost:8000
```

## Project structure

```
ccs-site/
├── index.html              # Homepage
├── services.html           # Services overview
├── services/               # 9 individual service pages
├── industries.html
├── case-studies.html
├── about.html
├── contact.html
└── assets/
    ├── styles.css
    ├── app.js
    └── i18n.js
```

## Still to do

- Fill `[REAL DATA]` placeholders (stats, case studies, About bios, phone, address)
- Add images to `assets/img/` (team photos, case-study visuals)
- Add Web3Forms access key for the contact form (falls back to a mailto link until then)

## Deploy

Static hosting — upload `ccs-site/` contents to any host (Hostinger `public_html`,
Netlify, Vercel, or Cloudflare Pages).

---
© 2026 Cosmic Consultancy Services. All rights reserved.
