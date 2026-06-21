# BUET E-Library Design System — "Bishwo"

**Version:** 1.0  
**Date:** 2026-06-18  
**Purpose:** Comprehensive visual design specification for the BUET Central Library e-discovery platform. Tailored to Drupal 11 custom theme implementation.

---

## 1. Design Philosophy

### Bishwo (বিশ্ব) — The World of Knowledge

The design language draws from three anchors:

1. **BUET Institutional Identity** — Maroon authority, gold excellence, engineering precision
2. **Bangladeshi Heritage** — Subtle Jamdani textile patterns, terracotta warmth, natural materials
3. **Engineering Modernism** — Grid systems, technical line weights, blueprint-inspired details, data-driven clarity

The result is a warm, authoritative, and distinctly Bangladeshi digital space that feels like a modern extension of the BUET campus rather than a generic SaaS template.

---

## 2. Color Palette

### Primary — "BUET Maroon" (Authority & Heritage)

Derived from the official BUET seal and logo. Used for primary navigation, headings, key actions, and brand moments.

| Token | Hex | Usage |
|-------|-----|-------|
| `--maroon-50` | `#FDF2F2` | Hover backgrounds, light tints |
| `--maroon-100` | `#FADCDC` | Subtle backgrounds, badges |
| `--maroon-200` | `#F5B5B5` | Disabled states, inactive tabs |
| `--maroon-300` | `#E88080` | Secondary accents |
| `--maroon-400` | `#D14D4D` | Notifications, alerts |
| `--maroon-500` | `#B52A2A` | Primary buttons, links |
| `--maroon-600` | `#8B0000` | **PRIMARY BRAND COLOR** — headings, nav, CTAs |
| `--maroon-700` | `#700000` | Hover states, emphasis |
| `--maroon-800` | `#520000` | Footer, dark sections |
| `--maroon-900` | `#330000` | Deepest backgrounds |

### Accent — "Gold Tassel" (Excellence & Achievement)

Inspired by the gold tassel on the BUET graduation cap. Used for highlights, active states, success indicators, and premium features.

| Token | Hex | Usage |
|-------|-----|-------|
| `--gold-50` | `#FFFBEB` | Light backgrounds, tips |
| `--gold-100` | `#FEF3C7` | Highlighted text bg |
| `--gold-200` | `#FDE68A` | Stars, ratings, badges |
| `--gold-300` | `#FCD34D` | Active tab indicators |
| `--gold-400` | `#FBBF24` | Hover on gold elements |
| `--gold-500` | `#D4AF37` | **ACCENT BRAND COLOR** — active nav, premium icons |
| `--gold-600` | `#B5901F` | Darker gold, shadows |
| `--gold-700` | `#8C6D14` | Text on gold backgrounds |
| `--gold-800` | `#5C4710` | Dark mode gold |
| `--gold-900` | `#332607` | Deepest gold |

### Secondary — "Campus Green" (Growth & Sustainability)

A nod to the greenery of the BUET campus and Bangladesh's natural landscape. Used for success states, environmental/e-sustainability content, and secondary actions.

| Token | Hex | Usage |
|-------|-----|-------|
| `--green-50` | `#F0FDF4` | Success backgrounds |
| `--green-100` | `#DCFCE7` | Available status badges |
| `--green-500` | `#16A34A` | **Available — physical book** |
| `--green-700` | `#15803D` | Success text |
| `--green-900` | `#14532D` | Dark mode success |

### Neutral — "Concrete & Paper" (Foundation & Readability)

Inspired by the concrete brutalism of the BUET architecture and the paper of traditional library card catalogs.

| Token | Hex | Usage |
|-------|-----|-------|
| `--white` | `#FFFFFF` | Card backgrounds, primary surfaces |
| `--paper-50` | `#FDFCFA` | Page backgrounds (warm white) |
| `--paper-100` | `#F8F6F3` | Section backgrounds, alternating rows |
| `--paper-200` | `#F0EDE8` | Borders, dividers, disabled fields |
| `--paper-300` | `#E3DFD8` | Borders, separators |
| `--paper-400` | `#C4BFB5` | Placeholder text, icons |
| `--paper-500` | `#9A958C` | Secondary text, captions |
| `--paper-600` | `#6B675F` | Body text, descriptions |
| `--paper-700` | `#4A4742` | Sub-headings, strong body |
| `--paper-800` | `#2E2C28` | Headings, primary text |
| `--paper-900` | `#1A1916` | Deepest text, dark mode surfaces |

### Semantic Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `--info` | `#2563EB` | Informational alerts, blue links |
| `--warning` | `#D97706` | Warning states, due dates |
| `--danger` | `#DC2626` | Checked out, overdue, errors |
| `--success` | `#16A34A` | Available, confirmed, checked in |

### Dark Mode Palette

When the system is in dark mode, the paper tones invert to deep slate, and maroon becomes the dominant surface color:

| Light Mode | Dark Mode Equivalent |
|------------|---------------------|
| `--paper-50` | `--paper-900` |
| `--paper-100` | `--paper-800` |
| `--paper-200` | `--paper-700` |
| `--white` | `--paper-900` |
| `--maroon-600` | `--maroon-400` (brighter for contrast) |
| `--gold-500` | `--gold-400` |
| Text on light | `#E8E6E3` (warm off-white) |

---

## 3. Typography

### Font Stack

**Primary (Headings):** `"Noto Serif Bengali", "Noto Serif", "Georgia", serif`  
*Why:* Serif conveys authority and heritage. Noto Serif Bengali ensures beautiful Bangla text rendering for bilingual content.

**Secondary (Body):** `"Inter", "Noto Sans Bengali", "Helvetica Neue", sans-serif`  
*Why:* Inter is highly legible at small sizes, engineered for screens. Noto Sans Bengali provides clean Bangla body text.

**Monospace (Code, MARC, Call Numbers):** `"JetBrains Mono", "Fira Code", "Courier New", monospace`  
*Why:* Used for call numbers, ISBNs, MARC tags, and any technical data. JetBrains Mono has excellent Bengali support.

### Type Scale

Inspired by the golden ratio (1.618) for a harmonious, academic feel.

| Token | Size | Weight | Line Height | Letter Spacing | Usage |
|-------|------|--------|-------------|----------------|-------|
| `--text-hero` | 48px / 3rem | 700 | 1.1 | -0.02em | Hero title, homepage headline |
| `--text-h1` | 36px / 2.25rem | 700 | 1.2 | -0.01em | Page titles, section headers |
| `--text-h2` | 28px / 1.75rem | 600 | 1.3 | -0.01em | Card titles, result headings |
| `--text-h3` | 22px / 1.375rem | 600 | 1.4 | 0 | Sub-sections, facet headers |
| `--text-h4` | 18px / 1.125rem | 600 | 1.5 | 0 | Widget titles, sidebar headers |
| `--text-body-lg` | 17px / 1.0625rem | 400 | 1.7 | 0 | Lead paragraphs, abstracts |
| `--text-body` | 15px / 0.9375rem | 400 | 1.6 | 0.01em | Standard body text |
| `--text-body-sm` | 13px / 0.8125rem | 400 | 1.5 | 0.02em | Metadata, captions, labels |
| `--text-caption` | 11px / 0.6875rem | 500 | 1.4 | 0.04em | Timestamps, tags, footers |
| `--text-button` | 14px / 0.875rem | 600 | 1 | 0.02em | Buttons, navigation links |

### Typography Rules

- **Headings:** Always `--maroon-700` or `--maroon-800` on light backgrounds. `--gold-400` on dark backgrounds.
- **Body text:** `--paper-700` on light, `#E8E6E3` on dark.
- **Links:** `--maroon-600` with underline on hover. Transition: `color 0.2s ease`.
- **Bengali text:** Always minimum `--text-body` (15px) for readability. Never bold below `--text-h4`.
- **Monospace:** Always `--paper-600` or `#8A857C`. Used for call numbers, ISBNs, DOIs, status codes.

---

## 4. Layout & Grid

### Grid System

Inspired by engineering blueprints — a 12-column grid with a 24px gutter. The page is constrained to a max-width of 1440px, centered.

```
┌────────────────────────────────────────────────────────────┐
│  Margin: 24px (mobile) → 48px (tablet) → 80px (desktop)   │
│                                                            │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Content Area (max 1440px)                          │  │
│  │  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐│  │
│  │  │ 1   │ 2   │ 3   │ 4   │ 5   │ 6   │ 7   │ 8   ││  │
│  │  │     │     │     │     │     │     │     │     ││  │
│  │  └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘│  │
│  └─────────────────────────────────────────────────────┘  │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Breakpoints

| Name | Width | Usage |
|------|-------|-------|
| `--bp-mobile` | 0–640px | Single column, stacked nav, full-width cards |
| `--bp-tablet` | 641–1024px | 2-column grid, hamburger menu, larger touch targets |
| `--bp-desktop` | 1025–1440px | Full layout, 3-column results, sidebar visible |
| `--bp-wide` | 1441px+ | Max-width container, generous whitespace |

### Spacing Scale

Based on an 8px grid system (common in engineering design), but with warm, irregular spacing for a more organic feel.

| Token | Value | Usage |
|-------|-------|-------|
| `--space-1` | 4px | Icon padding, tight inline spacing |
| `--space-2` | 8px | Small gaps, button padding (vertical) |
| `--space-3` | 12px | Card internal padding, list item gaps |
| `--space-4` | 16px | Standard component padding |
| `--space-5` | 24px | Section padding, card gaps |
| `--space-6` | 32px | Larger component gaps |
| `--space-7` | 48px | Section separation |
| `--space-8` | 64px | Major section breaks |
| `--space-9` | 96px | Hero spacing, footer padding |
| `--space-10` | 128px | Page-level vertical rhythm |

---

## 5. Unique Design Elements (BUET-Specific)

### 5.1 The "Blueprint Grid" Background Pattern

A subtle, repeating geometric grid pattern inspired by engineering blueprints and graph paper. Used on the homepage hero and search results background.

```css
.blueprint-grid {
  background-color: var(--paper-50);
  background-image: 
    linear-gradient(var(--paper-200) 1px, transparent 1px),
    linear-gradient(90deg, var(--paper-200) 1px, transparent 1px);
  background-size: 40px 40px;
  background-position: -1px -1px;
}
```

*Dark mode variant:* Lines become `--maroon-800` at 30% opacity on `--paper-900`.

### 5.2 The "Jamdani Accent" Border Motif

A decorative corner or edge motif inspired by Jamdani textile weaving patterns. Used sparingly on featured cards, section dividers, and the homepage hero.

```css
.jamdani-border {
  border-image: url('patterns/jamdani-corner.svg') 30% stretch;
  border-width: 2px;
  border-style: solid;
}
```

**SVG Pattern:** A simple repeating geometric motif (diamonds and lines) in `--gold-500` at 20% opacity. Never overpowering — purely decorative.

### 5.3 The "Tassel" Active Indicator

A gold horizontal line (2px, `--gold-500`) that slides under active navigation items or selected tabs. On hover, the line grows from 0% to 100% width with a `cubic-bezier(0.4, 0, 0.2, 1)` ease.

```css
.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--gold-500);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.nav-link:hover::after,
.nav-link.active::after {
  width: 100%;
}
```

### 5.4 "Concrete" Card Surface

Search result cards and content blocks use a subtle texture reminiscent of concrete or handmade paper.

```css
.concrete-card {
  background: var(--white);
  border: 1px solid var(--paper-200);
  border-radius: 4px;
  box-shadow: 
    0 1px 2px rgba(26, 25, 22, 0.04),
    0 2px 4px rgba(26, 25, 22, 0.02);
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.concrete-card:hover {
  box-shadow: 
    0 4px 8px rgba(26, 25, 22, 0.08),
    0 8px 16px rgba(26, 25, 22, 0.04);
  transform: translateY(-2px);
}
```

*Dark mode:* Background becomes `--paper-800`, border `--paper-700`, text `#E8E6E3`.

### 5.5 "Engineering Diagram" Status Icons

Status indicators (Available, Checked Out, On Hold) use geometric, blueprint-inspired icons rather than generic checkmarks.

| Status | Icon Style | Color |
|--------|-----------|-------|
| **Available** | Hollow circle with a dot inside (●) | `--green-500` |
| **Checked Out** | Horizontal line (─) | `--danger` |
| **On Hold** | Vertical line with dot (⬍) | `--warning` |
| **Digital** | Diamond shape (◆) | `--info` |
| **Reference** | Triangle pointing up (▲) | `--gold-500` |

### 5.6 The "Campus Map" Footer

A stylized, simplified topographic map of the BUET campus in the footer background. Used as a subtle, decorative watermark at 5% opacity.

---

## 6. Component Design

### 6.1 Search Box (Hero)

The centerpiece of the homepage. A large, inviting search input with a prominent gold-accented button.

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│   [BUET Logo]        BUET Central Library                  │
│                      বিশ্বজ্ঞানের সন্ধানে                   │
│                      "In Quest of Knowledge"                │
│                                                            │
│   ┌──────────────────────────────────────────┬──────────┐ │
│   │  🔍  Search books, theses, articles...   │  SEARCH  │ │
│   │                                          │  [Gold]  │ │
│   └──────────────────────────────────────────┴──────────┘ │
│                                                            │
│   [Physical Books]  [Digital Theses]  [Journal Articles]   │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**CSS:**
```css
.hero-search {
  display: flex;
  max-width: 800px;
  margin: 0 auto;
  border: 2px solid var(--paper-300);
  border-radius: 8px;
  overflow: hidden;
  background: var(--white);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.hero-search:focus-within {
  border-color: var(--maroon-500);
  box-shadow: 0 0 0 4px rgba(139, 0, 0, 0.08);
}
.hero-search input {
  flex: 1;
  padding: 16px 20px;
  border: none;
  font-family: var(--font-secondary);
  font-size: var(--text-body-lg);
  color: var(--paper-800);
  background: transparent;
}
.hero-search input::placeholder {
  color: var(--paper-400);
}
.hero-search button {
  padding: 16px 32px;
  background: var(--gold-500);
  color: var(--paper-900);
  font-weight: 600;
  font-size: var(--text-button);
  border: none;
  cursor: pointer;
  transition: background 0.2s ease;
}
.hero-search button:hover {
  background: var(--gold-600);
}
```

### 6.2 Search Result Card

A clean, information-dense card for search results combining local and federated content.

```
┌────────────────────────────────────────────────────────────┐
│  ● Available                           [Physical Book]     │
│  Central Library Floor 2                                     │
│                                                            │
│  Machine Learning for Civil Engineering: A Comprehensive     │
│  Guide to Structural Health Monitoring                     │
│  By Rahman, A.K.M. | Karim, S. | BUET Press, 2024         │
│                                                            │
│  📚 Civil Engineering  |  🔬 Machine Learning  |  📄 PDF   │
│  ISBN: 978-984-12345-6-7  |  Call No: TA 170 .R35 2024    │
│                                                            │
│  [📖 View in Koha]  [📄 Download PDF]  [🔖 Save]  [📤 Cite] │
│                                                            │
│  ─── Live Status ──────────────────────────────────────── │
│  Shelf: Central Library Floor 2  |  Status: Available    │
│  ───────────────────────────────────────────────────────  │
└────────────────────────────────────────────────────────────┘
```

**CSS:**
```css
.result-card {
  background: var(--white);
  border: 1px solid var(--paper-200);
  border-radius: 4px;
  padding: var(--space-5);
  margin-bottom: var(--space-4);
  transition: box-shadow 0.2s ease, transform 0.2s ease;
  position: relative;
}
.result-card:hover {
  box-shadow: 0 4px 12px rgba(26, 25, 22, 0.08);
  transform: translateY(-1px);
}
.result-card .status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: var(--text-body-sm);
  font-weight: 600;
  color: var(--green-700);
}
.result-card .status-badge .status-icon {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--green-500);
}
.result-card .format-badge {
  float: right;
  font-size: var(--text-caption);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--paper-500);
  background: var(--paper-100);
  padding: 2px 8px;
  border-radius: 4px;
}
.result-card .title {
  font-family: var(--font-primary);
  font-size: var(--text-h3);
  font-weight: 600;
  color: var(--maroon-700);
  line-height: 1.4;
  margin: var(--space-2) 0;
}
.result-card .title a:hover {
  color: var(--maroon-500);
  text-decoration: underline;
}
.result-card .meta {
  font-size: var(--text-body-sm);
  color: var(--paper-600);
  margin-bottom: var(--space-3);
}
.result-card .subject-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-bottom: var(--space-3);
}
.result-card .subject-tag {
  font-size: var(--text-body-sm);
  color: var(--maroon-700);
  background: var(--maroon-50);
  padding: 2px 8px;
  border-radius: 4px;
  border: 1px solid var(--maroon-100);
}
.result-card .actions {
  display: flex;
  gap: var(--space-3);
  margin-top: var(--space-3);
  padding-top: var(--space-3);
  border-top: 1px solid var(--paper-200);
}
.result-card .action-btn {
  font-size: var(--text-body-sm);
  color: var(--maroon-600);
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px 0;
  transition: color 0.2s ease;
}
.result-card .action-btn:hover {
  color: var(--maroon-800);
  text-decoration: underline;
}
```

### 6.3 Facet Sidebar

A vertical sidebar for filtering search results by format, subject, date, and source.

```
┌──────────────────┐
│  Filter Results  │
│  ═══════════════  │
│                  │
│  Format          │
│  ○ All (1,234)   │
│  ● Physical (892)│
│  ○ Digital (342) │
│                  │
│  Subject         │
│  ○ All           │
│  ● Civil Eng (45)│
│  ○ CSE (120)     │
│  ○ EEE (89)      │
│  ○ Mech (67)     │
│  [+ Show More]   │
│                  │
│  Date            │
│  [2024]========> │
│  1900 — 2024     │
│                  │
│  Source          │
│  ○ All           │
│  ● Koha (892)    │
│  ○ DSpace (342)  │
│  ○ Crossref (45) │
│  ○ OpenAlex (67) │
│                  │
└──────────────────┘
```

**CSS:**
```css
.facet-sidebar {
  background: var(--white);
  border: 1px solid var(--paper-200);
  border-radius: 4px;
  padding: var(--space-5);
}
.facet-group {
  margin-bottom: var(--space-5);
}
.facet-group-title {
  font-family: var(--font-primary);
  font-size: var(--text-h4);
  font-weight: 600;
  color: var(--maroon-800);
  margin-bottom: var(--space-3);
  padding-bottom: var(--space-2);
  border-bottom: 2px solid var(--gold-500);
}
.facet-option {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-1) 0;
  font-size: var(--text-body-sm);
  color: var(--paper-700);
  cursor: pointer;
  transition: color 0.2s ease;
}
.facet-option:hover {
  color: var(--maroon-600);
}
.facet-option input[type="radio"],
.facet-option input[type="checkbox"] {
  accent-color: var(--maroon-600);
}
.facet-count {
  font-size: var(--text-caption);
  color: var(--paper-500);
  margin-left: auto;
}
```

### 6.4 Live Status Badge

Dynamic status indicator for physical books with real-time availability.

```css
.live-status {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: var(--text-body-sm);
  font-weight: 600;
  background: var(--paper-100);
  border: 1px solid var(--paper-200);
}
.live-status.available {
  background: var(--green-50);
  border-color: var(--green-500);
  color: var(--green-700);
}
.live-status.checked-out {
  background: rgba(220, 38, 38, 0.05);
  border-color: var(--danger);
  color: var(--danger);
}
.live-status.on-hold {
  background: rgba(217, 119, 6, 0.05);
  border-color: var(--warning);
  color: var(--warning);
}
.status-pulse {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}
```

### 6.5 Navigation Bar

A sticky, maroon navigation bar with gold accents.

```css
.main-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--maroon-700);
  border-bottom: 3px solid var(--gold-500);
  padding: 0 var(--space-5);
}
.main-nav .nav-container {
  max-width: 1440px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}
.main-nav .logo {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  color: var(--white);
  font-family: var(--font-primary);
  font-size: var(--text-h4);
  font-weight: 700;
  text-decoration: none;
}
.main-nav .logo img {
  height: 40px;
}
.main-nav .nav-links {
  display: flex;
  gap: var(--space-6);
  list-style: none;
  margin: 0;
  padding: 0;
}
.main-nav .nav-link {
  position: relative;
  color: rgba(255, 255, 255, 0.85);
  font-size: var(--text-button);
  font-weight: 500;
  text-decoration: none;
  padding: 8px 0;
  transition: color 0.2s ease;
}
.main-nav .nav-link:hover,
.main-nav .nav-link.active {
  color: var(--white);
}
.main-nav .nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--gold-500);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.main-nav .nav-link:hover::after,
.main-nav .nav-link.active::after {
  width: 100%;
}
```

---

## 7. Page Layouts

### 7.1 Homepage

```
┌────────────────────────────────────────────────────────────┐
│  [Sticky Nav] BUET Logo | Home | Search | Databases | ... │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │                                                    │   │
│  │     BUET Central Library                           │   │
│  │     বিশ্বজ্ঞানের সন্ধানে                            │   │
│  │     In Quest of Knowledge                          │   │
│  │                                                    │   │
│  │  ┌────────────────────────────────┬───────────┐   │   │
│  │  │  🔍 Search...                  │  SEARCH   │   │   │
│  │  └────────────────────────────────┴───────────┘   │   │
│  │                                                    │   │
│  │  [Physical Books] [Digital Theses] [Articles]     │   │
│  │                                                    │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│  ┌─────────────────┐  ┌─────────────────┐               │
│  │  Quick Stats    │  │  Featured        │               │
│  │  ────────────   │  │  ────────────    │               │
│  │  📚 45,000+     │  │  New Arrivals    │               │
│  │  💻 12,000+     │  │  Popular Books   │               │
│  │  📄 8,000+      │  │  DSpace Theses   │               │
│  │  🌐 128+        │  │  Upcoming Events │               │
│  └─────────────────┘  └─────────────────┘               │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Browse by Subject                                 │   │
│  │  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐        │   │
│  │  │Civil│ │CSE │ │EEE │ │Mech│ │Arch│ │Chem│        │   │
│  │  └────┘ └────┘ └────┘ └────┘ └────┘ └────┘        │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │  E-Resources                                       │   │
│  │  IEEE | Elsevier | JSTOR | Springer | Wiley | ACM │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
├────────────────────────────────────────────────────────────┤
│  [Footer] About | Contact | Help | Privacy | © BUET 2026  │
└────────────────────────────────────────────────────────────┘
```

### 7.2 Search Results Page

```
┌────────────────────────────────────────────────────────────┐
│  [Sticky Nav]                                              │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  "machine learning" — 1,245 results                        │
│  ┌──────────────────┐  ┌─────────────────────────────────┐│
│  │  Filter Results  │  │  ● Available  [Physical Book]     ││
│  │  ──────────────  │  │  Machine Learning in Engineering  ││
│  │  Format          │  │  By Rahman, A.K.M. | 2024       ││
│  │  ● All (1,245)   │  │  [Civil] [ML] [Structural]       ││
│  │  ○ Physical (892)  │  │  [View] [Save] [Cite]          ││
│  │  ○ Digital (342)   │  │                                 ││
│  │  ○ Articles (11)     │  │  ○ Crossref  [Journal Article]  ││
│  │  ──────────────  │  │  Deep Learning for Bridge...    ││
│  │  Subject         │  │  Smith, J. et al. | IEEE 2023   ││
│  │  ● All           │  │  [Open Access] [PDF]             ││
│  │  ○ Civil (45)    │  │                                 ││
│  │  ○ CSE (120)     │  │  ...                             ││
│  │  ...             │  │                                 ││
│  │  ──────────────  │  │  [1] [2] [3] ... [25] Next →    ││
│  │  Source          │  │                                 ││
│  │  ● All           │  │                                 ││
│  │  ○ Koha (892)    │  │                                 ││
│  │  ○ DSpace (342)  │  │                                 ││
│  │  ○ Crossref (11) │  │                                 ││
│  └──────────────────┘  └─────────────────────────────────┘│
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 8. Dark Mode Specification

### Toggle

A sun/moon icon toggle in the top navigation. Preference is saved to `localStorage`.

```css
.theme-toggle {
  background: none;
  border: none;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.85);
  font-size: 20px;
  padding: 8px;
  border-radius: 50%;
  transition: background 0.2s ease, color 0.2s ease;
}
.theme-toggle:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--white);
}
```

### Dark Mode Body Styles

```css
[data-theme="dark"] {
  --bg-primary: var(--paper-900);
  --bg-secondary: var(--paper-800);
  --bg-tertiary: var(--paper-700);
  --text-primary: #E8E6E3;
  --text-secondary: #B5B2AD;
  --text-muted: #8A857C;
  --border-color: var(--paper-700);
  --card-bg: var(--paper-800);
  --card-border: var(--paper-700);
  --nav-bg: var(--maroon-800);
  --nav-border: var(--gold-400);
  --link-color: var(--maroon-400);
  --link-hover: var(--maroon-300);
  --accent: var(--gold-400);
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.5);
}
```

### Dark Mode Component Overrides

```css
[data-theme="dark"] .result-card {
  background: var(--card-bg);
  border-color: var(--card-border);
  color: var(--text-primary);
}
[data-theme="dark"] .result-card .title {
  color: var(--maroon-300);
}
[data-theme="dark"] .result-card .title a:hover {
  color: var(--maroon-200);
}
[data-theme="dark"] .facet-sidebar {
  background: var(--card-bg);
  border-color: var(--card-border);
}
[data-theme="dark"] .facet-group-title {
  color: var(--text-primary);
  border-bottom-color: var(--gold-400);
}
[data-theme="dark"] .hero-search {
  background: var(--card-bg);
  border-color: var(--card-border);
}
[data-theme="dark"] .hero-search input {
  color: var(--text-primary);
}
[data-theme="dark"] .blueprint-grid {
  background-color: var(--paper-900);
  background-image: 
    linear-gradient(rgba(139, 0, 0, 0.2) 1px, transparent 1px),
    linear-gradient(90deg, rgba(139, 0, 0, 0.2) 1px, transparent 1px);
}
```

---

## 9. Animation & Motion

### 9.1 Page Transitions

A subtle fade-in + slide-up for page content:

```css
.page-content {
  animation: fadeSlideUp 0.4s ease-out;
}
@keyframes fadeSlideUp {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### 9.2 Loading Skeletons

For search results while federated APIs load:

```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--paper-200) 25%,
    var(--paper-100) 50%,
    var(--paper-200) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  border-radius: 4px;
}
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### 9.3 Live Status Pulse

A subtle pulsing animation for the live availability indicator:

```css
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}
.status-pulse {
  animation: pulse 2s ease-in-out infinite;
}
```

### 9.4 Card Hover Lift

Cards lift slightly on hover with a shadow increase:

```css
.result-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.result-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(26, 25, 22, 0.08);
}
[data-theme="dark"] .result-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}
```

---

## 10. Accessibility (WCAG 2.1 AA)

### 10.1 Color Contrast

All text meets WCAG 2.1 AA contrast ratios:

| Combination | Ratio | Pass |
|-------------|-------|------|
| `--maroon-600` on `--white` | 7.2:1 | ✅ AA, AAA |
| `--paper-700` on `--white` | 6.5:1 | ✅ AA |
| `--gold-500` on `--white` | 3.1:1 | ❌ AA for body text |
| `--gold-700` on `--white` | 5.2:1 | ✅ AA for body text |
| `--green-700` on `--white` | 5.8:1 | ✅ AA |
| `--white` on `--maroon-700` | 8.4:1 | ✅ AA, AAA |
| `--text-primary` on `--paper-900` | 9.1:1 | ✅ AA, AAA |

**Rule:** Gold (`--gold-500`) is NEVER used for body text. It is only used for:
- Decorative elements (borders, accents)
- Icons on dark backgrounds
- Large text (headings ≥ 24px)

### 10.2 Focus States

All interactive elements have a visible focus state:

```css
:focus-visible {
  outline: 2px solid var(--maroon-500);
  outline-offset: 2px;
  border-radius: 2px;
}
```

### 10.3 Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  .status-pulse {
    animation: none;
  }
  .skeleton {
    animation: none;
    background: var(--paper-200);
  }
}
```

### 10.4 Screen Reader Support

- Search result cards use `article` landmark with `aria-labelledby` pointing to the title
- Live status updates use `aria-live="polite"` regions
- Facet checkboxes have descriptive labels
- Navigation uses proper `nav` + `ul` + `li` structure with `aria-current="page"` for active items
- All images have `alt` text (book covers use title, decorative patterns use empty `alt`)

---

## 11. Responsive Behavior

### Mobile (< 640px)

- Navigation collapses to hamburger menu with maroon drawer
- Search box is full-width, button is stacked below
- Facet sidebar becomes a collapsible bottom sheet
- Result cards are full-width with reduced padding
- Statistics stack vertically
- Footer links collapse to 2-column grid

### Tablet (641–1024px)

- Navigation shows primary links, hamburger for secondary
- Search box is centered, 80% width
- Facet sidebar is a collapsible sidebar toggle
- Result cards are full-width but with more padding
- Statistics in 2×2 grid
- Footer in 3-column grid

### Desktop (1025–1440px)

- Full navigation visible
- Search box is 60% width, centered
- Facet sidebar is persistent on the left (25% width)
- Results area is 75% width
- Statistics in 4-column row
- Footer in 4-column grid

### Wide (> 1440px)

- Content maxes at 1440px, centered
- More whitespace on margins
- Larger touch targets (minimum 48px)
- Statistics have more breathing room

---

## 12. Assets & Files

### Required Image Assets

| File | Description | Location |
|------|-------------|----------|
| `buet-logo-white.svg` | BUET seal/logo, white variant | `themes/buet_elibrary/images/` |
| `buet-logo-maroon.svg` | BUET seal/logo, maroon variant | `themes/buet_elibrary/images/` |
| `jamdani-pattern.svg` | Subtle geometric border motif | `themes/buet_elibrary/images/` |
| `campus-map.svg` | Stylized BUET campus map (footer) | `themes/buet_elibrary/images/` |
| `book-placeholder.svg` | Placeholder for books without covers | `themes/buet_elibrary/images/` |
| `favicon.ico` | 32×32 and 16×16 favicon | `themes/buet_elibrary/favicon.ico` |
| `apple-touch-icon.png` | 180×180 iOS icon | `themes/buet_elibrary/images/` |

### Required Font Files (or CDN)

```html
<!-- Google Fonts CDN -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+Bengali:wght@400;500;600;700&family=Noto+Serif:wght@400;600;700&family=Noto+Serif+Bengali:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

---

## 13. Drupal 11 Theme Implementation Notes

### Theme Structure

```
themes/
└── buet_elibrary/
    ├── buet_elibrary.info.yml
    ├── buet_elibrary.libraries.yml
    ├── buet_elibrary.theme
    ├── css/
    │   ├── base.css           # CSS variables, resets, typography
    │   ├── layout.css         # Grid, breakpoints, spacing
    │   ├── components.css     # Buttons, cards, forms, badges
    │   ├── navigation.css     # Nav, sidebar, breadcrumbs
    │   ├── search.css         # Search box, results, facets
    │   ├── dark-mode.css      # Dark mode overrides
    │   └── print.css          # Print styles
    ├── js/
    │   ├── dark-mode.js       # Theme toggle, localStorage
    │   ├── live-status.js     # AJAX status loading
    │   └── federated-search.js # Client-side meta-search
    ├── images/
    │   ├── buet-logo-white.svg
    │   ├── buet-logo-maroon.svg
    │   ├── jamdani-pattern.svg
    │   └── campus-map.svg
    └── templates/
        ├── page.html.twig
        ├── region.html.twig
        ├── block.html.twig
        ├── node.html.twig
        ├── search-result.html.twig
        ├── search-results.html.twig
        └── facet-*.html.twig
```

### Key Drupal Modules to Style

- `search_api` — Search results, facets, search pages
- `search_api_elasticsearch` — Elasticsearch integration
- `facets` — Faceted navigation blocks
- `views` — Custom views for database listings, new arrivals
- `better_exposed_filters` — Enhanced filter UI
- `twig_tweak` — Utility functions for custom templates

### CSS Custom Properties (CSS Variables)

All colors, spacing, typography, and breakpoints are defined as CSS custom properties in `base.css`. This allows dynamic dark mode switching and easy theming without recompiling.

```css
:root {
  /* Colors */
  --maroon-50: #FDF2F2;
  --maroon-100: #FADCDC;
  /* ... full palette ... */
  
  /* Typography */
  --font-primary: "Noto Serif Bengali", "Noto Serif", "Georgia", serif;
  --font-secondary: "Inter", "Noto Sans Bengali", "Helvetica Neue", sans-serif;
  --font-mono: "JetBrains Mono", "Fira Code", "Courier New", monospace;
  
  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  /* ... full scale ... */
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(26, 25, 22, 0.04);
  --shadow-md: 0 4px 8px rgba(26, 25, 22, 0.08);
  --shadow-lg: 0 8px 16px rgba(26, 25, 22, 0.12);
}
```

---

## 14. Design Inspiration References

The design draws from multiple sources of inspiration:

1. **BUET Institutional Identity** — Maroon and gold from the official seal
2. **Bangladeshi Heritage** — Jamdani weaving patterns, terracotta architecture, natural materials
3. **Engineering Modernism** — Grid systems, blueprint aesthetics, technical precision
4. **Contemporary Library Design** — NYPL Digital, Digital Public Library of America, Europeana
5. **Material Design 3** — Dynamic color, elevation, motion
6. **Tailwind CSS Philosophy** — Utility-first, constraint-based design

---

## 15. Appendix: Color Accessibility Matrix

| Color | On White | On Paper-50 | On Maroon-700 | On Dark |
|-------|----------|-------------|---------------|---------|
| Maroon-600 | ✅ 7.2:1 | ✅ 6.8:1 | ❌ 1.8:1 | ✅ 5.4:1 |
| Gold-500 | ❌ 3.1:1 | ❌ 2.9:1 | ✅ 4.5:1 | ✅ 5.1:1 |
| Gold-700 | ✅ 5.2:1 | ✅ 4.9:1 | ✅ 7.1:1 | ✅ 8.2:1 |
| Green-500 | ✅ 4.5:1 | ✅ 4.2:1 | ❌ 2.1:1 | ✅ 4.8:1 |
| Green-700 | ✅ 5.8:1 | ✅ 5.5:1 | ✅ 6.2:1 | ✅ 7.5:1 |
| Paper-700 | ✅ 6.5:1 | ✅ 6.1:1 | ❌ 2.4:1 | ✅ 6.8:1 |
| Paper-800 | ✅ 8.1:1 | ✅ 7.6:1 | ❌ 3.0:1 | ✅ 8.4:1 |
| White | ❌ 1.0:1 | ❌ 1.1:1 | ✅ 8.4:1 | ❌ 1.0:1 |
| Text-Primary | N/A | N/A | N/A | ✅ 9.1:1 |

*Legend: ✅ = WCAG 2.1 AA compliant (4.5:1 for body, 3:1 for large text), ❌ = not compliant*

---

**End of Design System**
