# BUET E-Library Design System — "Bishwo"

This folder contains the complete visual design specification for the **BUET E-Library** — a digital-first discovery platform for e-resources, institutional repository, and reference services.

---

## Files

| File | Description |
|------|-------------|
| `design.md` | Complete design spec — e-library focused (40KB) |
| `base.css` | CSS custom properties — all design tokens + blue digital accent |
| `demo.html` | **Interactive HTML demo** — open in browser to see e-library UI |
| `README.md` | This file — quick start for developers |

---

## What's Different from a Physical Library Design?

This design is **exclusively for an electronic library** — no physical books, no shelves, no checkout counters. The UI focuses on:

1. **E-Resource Database Browser** — Visual grid of subscribed databases (IEEE, Elsevier, JSTOR, etc.) with branded icon tiles
2. **Institutional Repository** — DSpace theses and research papers with DOIs, open-access ribbons, PDF downloads
3. **Reference Services** — Live chat widget, question submission, consultation booking, citation tools
4. **Federated Search** — Results from Crossref, OpenAlex, CORE with open-access badges and external links

---

## Color Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| **Primary** | BUET Maroon | `#8B0000` | Headings, nav, brand |
| **Accent** | Gold Tassel | `#D4AF37` | CTAs, active states, premium badges |
| **Digital** | Open Access Blue | `#3B82F6` | **Links, DOIs, open-access badges** |
| **Success** | Campus Green | `#16A34A` | Subscribed access, free full-text |
| **Neutrals** | Concrete & Paper | `#FDFCFA` → `#1A1916` | Backgrounds, text, borders |

**Key change:** Links are **blue** (`#3B82F6`) instead of maroon — this is a digital library, so links should feel like hyperlinks, not physical labels.

---

## Unique Design Elements (E-Library)

| Element | What It Is | Where Used |
|---------|-----------|------------|
| **Digital Wave** | Sine wave background pattern | Hero section — suggests data flow |
| **Open Access Ribbon** | Diagonal blue ribbon badge | Repository cards, open-access content |
| **Connection Line** | Gold-to-blue gradient underline | Nav active states — "digital connection" |
| **Database Grid** | Branded icon tiles (IEEE blue, Elsevier orange) | Database browser homepage |
| **Reference Pulse** | Green pulsing dot + "Librarian Online" | Sidebar widget, footer |
| **Glass Cards** | Frosted transparency + backdrop blur | E-resource cards, premium feel |

---

## Typography

| Role | Font | Usage |
|------|------|-------|
| Headings | Noto Serif Bengali + Noto Serif | Bilingual, academic authority |
| Body | Inter + Noto Sans Bengali | Screen-optimized readability |
| Monospace | JetBrains Mono | DOIs, URLs, MARC tags, call numbers |

---

## Components (E-Library Focused)

### 1. Database Browser (Hero)

Grid of branded database tiles with access status:

```
┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐
│IEEE│ │Else│ │JSTOR│ │SPR │ │Wiley│ │ACM │
│ X  │ │vier│ │     │ │inger│ │     │ │    │
└────┘ └────┘ └────┘ └────┘ └────┘ └────┘
🟢 Subscribed    🔵 Open Access    🟢 Subscribed
```

### 2. Institutional Repository Card

```
┌────────────────────────────────────────┐
│  🔓 Open Access Ribbon (diagonal blue) │
│  Traffic Flow Prediction in Dhaka... │
│  By Islam, N. | CSE, BUET | 2024     │
│  DOI: 10.1234/buet.cse.2024.001      │
│  [📄 Download PDF] [🔖 Save] [📤 Cite]│
└────────────────────────────────────────┘
```

### 3. Reference Services Widget

```
┌──────────────────┐
│  🟢 Librarian    │
│     Online       │
│  [Start Chat]    │
│  ───────────────  │
│  📧 Ask Question │
│  📅 Book Session │
│  📎 Citation Tools│
└──────────────────┘
```

### 4. Federated Search Result

```
┌────────────────────────────────────────┐
│  🌐 Crossref    [Journal Article]     │
│  Deep Learning for Bridge Health...    │
│  Smith, J. et al. | 2024               │
│  DOI: 10.1177/14759217241234567      │
│  🔓 Open Access | [Full Text] [Cite]   │
└────────────────────────────────────────┘
```

---

## Dark Mode

Toggle via ☀️/🌙 button in the nav. Key dark mode changes:

| Light | Dark |
|-------|------|
| White background → Deep slate (`#1A1916`) |
| Maroon headings → Brighter maroon (`#D14D4D`) |
| **Blue links → Lighter blue (`#60A5FA`)** |
| Gold accents → Slightly brighter gold |
| Cards → Frosted glass effect on dark background |

See `demo.html` for the full interactive implementation.

---

## Quick Start

### 1. Preview

Open `demo.html` in a browser. It includes:
- Hero with database browser grid
- Stats + reference services widget
- Repository cards with open-access ribbons
- E-resource database list
- Federated search results
- Dark mode toggle
- Responsive layout

### 2. Use CSS Variables

```css
@import url('base.css');

.my-component {
  background: var(--maroon-600);
  color: var(--white);
  padding: var(--space-4);
  border-radius: var(--radius-md);
}
```

### 3. Enable Dark Mode

```html
<html data-theme="dark">
```

Or toggle via JavaScript (see `demo.html` for the toggle implementation).

---

## Drupal 11 Theme Implementation

### Theme Structure

```
themes/buet_elibrary/
├── css/
│   ├── base.css           # ← Import this file
│   ├── e-resources.css    # Database cards, browser
│   ├── repository.css     # DSpace item cards
│   ├── reference.css      # Helpdesk widget, guides
│   ├── search.css         # Federated search results
│   └── dark-mode.css
├── js/
│   ├── dark-mode.js
│   ├── federated-search.js
│   └── reference-chat.js
├── images/
│   ├── buet-logo-*.svg
│   └── db-icons/          # IEEE, Elsevier, JSTOR brand icons
└── templates/
    ├── node--e-resource.html.twig
    ├── node--repository-item.html.twig
    └── block--reference-widget.html.twig
```

### Key Modules

- `search_api` + `search_api_elasticsearch` — Discovery search
- `facets` — E-resource filtering
- `views` — Database listings, repository browse
- `webform` — Reference question submission

---

## Accessibility (WCAG 2.1 AA)

- All body text meets 4.5:1 contrast ratio
- Blue links (`#3B82F6` on white) = 4.6:1 ✅ AA
- Gold is **never** used for body text — only decorative accents and large headings
- Focus states: `outline: 2px solid var(--blue-500)`
- `prefers-reduced-motion` disables all animations

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| **2.0** | 2026-06-18 | **E-library focused redesign** — database browser, repository cards, reference widget, federated search, digital blue accent |
| 1.0 | 2026-06-18 | Initial design system with physical-library orientation |

---

**End of README**
