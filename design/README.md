# BUET E-Library Design System — "Bishwo"

This folder contains the complete visual design specification for the BUET Central Library e-discovery platform. It is designed to be implemented as a **custom Drupal 11 theme**.

---

## Files

| File | Description |
|------|-------------|
| `design.md` | Complete design system — colors, typography, layout, components, dark mode, accessibility |
| `base.css` | CSS custom properties (variables) — all design tokens in one file |
| `demo.html` | **Interactive HTML demo** — open this in a browser to see the design in action (light/dark mode toggle, search cards, facets) |

---

## Design Philosophy: "Bishwo" (বিশ্ব — The World of Knowledge)

The design draws from three anchors:

1. **BUET Institutional Identity** — Maroon authority, gold excellence, engineering precision
2. **Bangladeshi Heritage** — Subtle Jamdani textile patterns, terracotta warmth, natural materials
3. **Engineering Modernism** — Grid systems, blueprint aesthetics, technical precision

The result is a warm, authoritative, and distinctly Bangladeshi digital space that feels like a modern extension of the BUET campus rather than a generic SaaS template.

---

## Quick Start for Developers

### 1. Preview the Design

Open `demo.html` in any modern browser. It includes:
- Responsive navigation with gold "tassel" active indicator
- Hero search with blueprint grid background
- Search result cards with live status badges
- Facet sidebar with Jamdani-inspired gold borders
- Dark mode toggle (☀️/🌙)
- Stats cards and footer

### 2. Use the CSS Variables

Import `base.css` into your Drupal theme to get all design tokens:

```css
@import url('base.css');

/* Now use the variables anywhere */
.my-component {
  background: var(--maroon-600);
  color: var(--white);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
}
```

### 3. Implement Dark Mode

Add the `data-theme` attribute to `<html>`:

```html
<html data-theme="dark">
```

Or toggle via JavaScript (see `demo.html` for the full implementation):

```javascript
document.documentElement.setAttribute('data-theme', 'dark');
```

### 4. Follow the Component Specs

The `design.md` file contains complete CSS specifications for:
- Navigation bar (sticky, maroon, gold accents)
- Hero search box (gold CTA button, focus states)
- Search result cards (status badges, subject tags, actions)
- Facet sidebar (gold-bordered group titles)
- Live status badges (pulsing animation for available items)
- Footer (maroon background, campus map watermark)

---

## Color Palette

### Primary: BUET Maroon

| Token | Hex | Usage |
|-------|-----|-------|
| `--maroon-600` | `#8B0000` | **Primary brand** — headings, nav, CTAs |
| `--maroon-700` | `#700000` | Hover states, emphasis |
| `--maroon-800` | `#520000` | Footer, dark sections |
| `--maroon-500` | `#B52A2A` | Primary buttons, links |

### Accent: Gold Tassel

| Token | Hex | Usage |
|-------|-----|-------|
| `--gold-500` | `#D4AF37` | **Accent** — active nav, premium icons, CTA buttons |
| `--gold-400` | `#FBBF24` | Hover on gold elements |
| `--gold-600` | `#B5901F` | Darker gold, shadows |

### Neutral: Concrete & Paper

| Token | Hex | Usage |
|-------|-----|-------|
| `--paper-50` | `#FDFCFA` | Page backgrounds (warm white) |
| `--paper-100` | `#F8F6F3` | Section backgrounds |
| `--paper-200` | `#F0EDE8` | Borders, dividers |
| `--paper-700` | `#4A4742` | Body text |
| `--paper-900` | `#1A1916` | Dark mode surfaces |

---

## Unique Design Elements

### 1. Blueprint Grid Background

Subtle engineering grid pattern on the hero section. See `design.md` §5.1 and `demo.html` hero section.

### 2. Jamdani Accent Borders

Gold-bordered section headers inspired by Jamdani textile weaving. See `design.md` §5.2 and facet sidebar in `demo.html`.

### 3. Tassel Active Indicator

Gold underline that slides in on hover/active navigation. See `design.md` §5.3.

```css
.nav-link::after {
  width: 0; height: 2px; background: var(--gold-500);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.nav-link:hover::after { width: 100%; }
```

### 4. Engineering Diagram Status Icons

Geometric icons instead of generic checkmarks:

| Status | Icon | Color |
|--------|------|-------|
| Available | ● dot | Green |
| Checked Out | ─ line | Red |
| On Hold | ⬍ vertical | Orange |
| Digital | ◆ diamond | Blue |
| Reference | ▲ triangle | Gold |

### 5. Concrete Card Surfaces

Cards lift slightly on hover with warm shadow:

```css
.result-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(26, 25, 22, 0.08);
}
```

---

## Typography

| Role | Font | Usage |
|------|------|-------|
| Headings | Noto Serif Bengali + Noto Serif | Page titles, card headings, nav |
| Body | Inter + Noto Sans Bengali | Body text, descriptions, metadata |
| Monospace | JetBrains Mono | Call numbers, ISBNs, MARC tags, DOIs |

**Headings:** Always serif, maroon, with slight letter-spacing tightening (`-0.01em` to `-0.02em`).

**Body:** Sans-serif, warm gray (`--paper-700`), generous line height (`1.6–1.7`).

**Bengali:** Minimum 15px for body text. Never bold below 18px.

---

## Responsive Breakpoints

| Name | Width | Key Changes |
|------|-------|-------------|
| Mobile | < 640px | Stacked nav, full-width cards, bottom sheet facets |
| Tablet | 641–1024px | Collapsible sidebar, 2-column stats |
| Desktop | 1025–1440px | Persistent sidebar, full grid |
| Wide | > 1440px | Max-width container, generous whitespace |

---

## Accessibility (WCAG 2.1 AA)

- All body text meets 4.5:1 contrast ratio
- Gold (`#D4AF37`) is **never** used for body text — only decorative accents and large headings
- Focus states: `outline: 2px solid var(--maroon-500)` with `outline-offset: 2px`
- `prefers-reduced-motion` disables all animations
- Screen reader support: `article` landmarks, `aria-live` for status updates, `aria-current` for active nav

---

## Dark Mode

Toggle via the ☀️/🌙 button in the navigation. Preference is saved to `localStorage`.

Dark mode swaps:
- Light paper backgrounds → deep slate (`--paper-800`, `--paper-900`)
- Maroon headings → brighter maroon (`--maroon-400`) for contrast
- Gold accents → slightly lighter gold (`--gold-400`)
- Text → warm off-white (`#E8E6E3`)

See `design.md` §8 and `demo.html` for full implementation.

---

## Implementation in Drupal 11

### Theme Structure

```
themes/buet_elibrary/
├── buet_elibrary.info.yml
├── buet_elibrary.libraries.yml
├── buet_elibrary.theme
├── css/
│   ├── base.css          # ← Import this file
│   ├── layout.css
│   ├── components.css
│   ├── navigation.css
│   ├── search.css
│   ├── dark-mode.css
│   └── print.css
├── js/
│   ├── dark-mode.js      # ← Copy from demo.html
│   ├── live-status.js
│   └── federated-search.js
├── images/
│   ├── buet-logo-white.svg
│   ├── buet-logo-maroon.svg
│   ├── jamdani-pattern.svg
│   └── campus-map.svg
└── templates/
    ├── page.html.twig
    ├── search-result.html.twig
    └── facet-*.html.twig
```

### Key Modules to Style

- `search_api` — Search results, facets, search pages
- `search_api_elasticsearch` — Elasticsearch integration
- `facets` — Faceted navigation blocks
- `views` — Custom views for database listings, new arrivals
- `better_exposed_filters` — Enhanced filter UI

---

## References & Inspiration

1. **BUET Institutional Identity** — Official seal colors (maroon + gold)
2. **Bangladeshi Heritage** — Jamdani weaving, terracotta architecture, natural materials
3. **Engineering Modernism** — Grid systems, blueprint aesthetics, technical precision
4. **Contemporary Library Design** — NYPL Digital, DPLA, Europeana
5. **Material Design 3** — Dynamic color, elevation, motion

---

**Questions or feedback?** Open an issue in the project repository or contact the BUET E-Library development team.
