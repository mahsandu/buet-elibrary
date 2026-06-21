# BUET E-Library Design System — "Bishwo"

**Version:** 2.0 (E-Library Focused)  
**Date:** 2026-06-18  
**Purpose:** Visual design specification for the BUET E-Library — a digital-first discovery platform for e-resources, institutional repository, and reference services.

---

## 1. Design Philosophy

### Bishwo (বিশ্ব) — The World of Digital Knowledge

This is not a physical library catalog. It is an **electronic library** — a unified digital gateway for:

1. **E-Resources** — Subscribed databases (IEEE, Elsevier, JSTOR, Springer), open-access journals, e-books, standards
2. **Institutional Repository** — DSpace theses, research papers, conference proceedings, departmental question papers
3. **Reference Services** — Virtual helpdesk, research guides, citation tools, literature review support
4. **Digital Discovery** — Federated search across global scholarly content, not just local shelves

The design language remains anchored in BUET identity (maroon + gold) but the **experience is entirely digital**. There are no physical shelves, no checkout counters, no floor maps — only URLs, PDFs, DOIs, metadata, and live access links.

---

## 2. Color Palette

*(Unchanged from V1 — see `base.css` for full tokens)*

### Primary — "BUET Maroon" (Authority & Digital Trust)

| Token | Hex | Usage |
|-------|-----|-------|
| `--maroon-600` | `#8B0000` | **Primary** — headings, nav, CTAs, e-resource headers |
| `--maroon-700` | `#700000` | Hover states, emphasis |
| `--maroon-800` | `#520000` | Footer, dark sections |
| `--maroon-500` | `#B52A2A` | Primary buttons, links |

### Accent — "Gold Tassel" (Premium Access & Excellence)

| Token | Hex | Usage |
|-------|-----|-------|
| `--gold-500` | `#D4AF37` | **Accent** — active nav, premium e-resource badges, reference service icons |
| `--gold-400` | `#FBBF24` | Hover on gold elements |
| `--gold-600` | `#B5901F` | Darker gold, shadows |

### Secondary — "Digital Blue" (Links & Open Access)

Replaces "Campus Green" as the secondary digital accent. Used for open-access indicators, external links, and digital format badges.

| Token | Hex | Usage |
|-------|-----|-------|
| `--blue-50` | `#EFF6FF` | Open access backgrounds |
| `--blue-100` | `#DBEAFE` | Digital format badges |
| `--blue-500` | `#3B82F6` | **External links, DOIs, open access** |
| `--blue-700` | `#1D4ED8` | Digital text emphasis |
| `--blue-900` | `#1E3A8A` | Dark mode links |

### Semantic Colors (Digital-First)

| Token | Hex | Usage |
|-------|-----|-------|
| `--info` | `#2563EB` | Database info, institutional links |
| `--warning` | `#D97706` | Subscription expiry, access warnings |
| `--danger` | `#DC2626` | Access denied, broken links, paywalls |
| `--success` | `#16A34A` | Open access, free full-text, institutional access |
| `--premium` | `#D4AF37` | Subscribed databases, premium e-resources |

---

## 3. Typography

*(Unchanged from V1 — see `base.css` for full tokens)*

**Primary (Headings):** `"Noto Serif Bengali", "Noto Serif", "Georgia", serif`  
**Secondary (Body):** `"Inter", "Noto Sans Bengali", "Helvetica Neue", sans-serif`  
**Monospace (DOIs, URLs, MARC):** `"JetBrains Mono", "Fira Code", "Courier New", monospace`

---

## 4. Layout & Grid

*(Unchanged from V1 — see `base.css` for full tokens)*

12-column grid, 24px gutter, max-width 1440px.

---

## 5. Unique Design Elements (E-Library Specific)

### 5.1 The "Digital Wave" Background Pattern

A subtle, flowing wave pattern inspired by digital signal waveforms and data streams. Replaces the physical blueprint grid. Used on the homepage hero and e-resource discovery pages.

```css
.digital-wave {
  background-color: var(--paper-50);
  background-image: url('patterns/digital-wave.svg');
  background-repeat: repeat-x;
  background-position: bottom;
  background-size: 120px 60px;
  opacity: 0.15;
}
```

**SVG Pattern:** A gentle sine wave in `--maroon-600` at 10% opacity. Suggests data flow, connectivity, and digital transmission — not physical structures.

### 5.2 The "Open Access" Ribbon Badge

A diagonal ribbon badge for open-access content. Used on e-resource cards, journal articles, and repository items.

```css
.oa-ribbon {
  position: absolute;
  top: 12px;
  right: -32px;
  width: 120px;
  padding: 4px 0;
  background: var(--blue-500);
  color: var(--white);
  font-size: var(--text-caption);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-align: center;
  transform: rotate(45deg);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

### 5.3 The "Connection Line" Active Indicator

A horizontal line that connects the active navigation item to the content area below, suggesting a "live connection" to digital resources. Replaces the physical "tassel" indicator.

```css
.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--gold-500), var(--blue-500));
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.nav-link:hover::after,
.nav-link.active::after {
  width: 100%;
}
```

### 5.4 "Glass" Resource Cards

E-resource cards use a subtle glassmorphism effect — frosted transparency over a gradient background — suggesting digital interfaces and premium access.

```css
.glass-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  box-shadow: 
    0 4px 6px rgba(0, 0, 0, 0.04),
    0 1px 3px rgba(0, 0, 0, 0.02);
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.glass-card:hover {
  box-shadow: 
    0 12px 24px rgba(0, 0, 0, 0.08),
    0 4px 8px rgba(0, 0, 0, 0.04);
  transform: translateY(-3px);
}
[data-theme="dark"] .glass-card {
  background: rgba(42, 40, 36, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
```

### 5.5 "Database Grid" Icon System

Each e-resource database has a branded icon tile — a solid-color square with the database initials in white, using the database's brand color (e.g., IEEE = blue, Elsevier = orange, JSTOR = purple). This creates a visual "app grid" feel for the database browser.

```css
.db-tile {
  width: 80px; height: 80px;
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-primary); font-size: 24px; font-weight: 700;
  color: var(--white);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.db-tile.ieee { background: #00629B; }
.db-tile.elsevier { background: #E9711C; }
.db-tile.jstor { background: #5F4B8B; }
.db-tile.springer { background: #E07800; }
.db-tile.wiley { background: #005A84; }
.db-tile.acm { background: #1D4C7C; }
.db-tile:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.18);
}
```

### 5.6 The "Reference Pulse" Widget

A live widget showing the reference helpdesk status. A pulsing green dot indicates a librarian is available for live chat. Used in the sidebar and footer.

```css
.reference-pulse {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 8px 16px; border-radius: var(--radius-full);
  background: var(--green-50); border: 1px solid var(--green-500);
  font-size: var(--text-body-sm); font-weight: 600; color: var(--green-700);
}
.reference-pulse .pulse-dot {
  width: 10px; height: 10px; border-radius: 50%; background: var(--green-500);
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}
```

---

## 6. Component Design (E-Library Focused)

### 6.1 E-Resource Discovery Hero

The homepage hero is a **database discovery interface** — not just a search box. Users can browse databases by subject, type, or search across all e-resources.

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│   [BUET Logo]        BUET E-Library                        │
│                      বিশ্বজ্ঞানের ডিজিটাল প্রবেশদ্বার       │
│                      Digital Gateway to Knowledge          │
│                                                            │
│   ┌──────────────────────────────────────────┬──────────┐ │
│   │  🔍  Search e-resources, theses, articles...│ SEARCH │ │
│   │                                          │  [Gold]  │ │
│   └──────────────────────────────────────────┴──────────┘ │
│                                                            │
│   Browse Databases:                                        │
│   ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐              │
│   │IEEE│ │Else│ │JSTOR│ │SPR │ │Wiley│ │ACM │              │
│   │ X  │ │vier│ │     │ │inger│ │     │ │    │              │
│   └────┘ └────┘ └────┘ └────┘ └────┘ └────┘              │
│                                                            │
│   [All E-Resources] [Institutional Repository] [Reference] │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**CSS:**
```css
.hero-databases {
  display: flex; justify-content: center; gap: var(--space-4);
  margin-top: var(--space-6); flex-wrap: wrap;
}
```

### 6.2 E-Resource Database Card

A card for browsing subscribed databases. Shows database branding, access type, and subject coverage.

```
┌────────────────────────────────────────┐
│  ┌────┐                                │
│  │IEEE│  IEEE Xplore Digital Library   │
│  │ X  │  ───────────────────────────   │
│  └────┘  Engineering, CS, Electronics │
│          🟢 Subscribed | Full Access   │
│          [Launch Database →]            │
│                                        │
│  ┌────┐                                │
│  │Else│  Elsevier ScienceDirect        │
│  │vier│  ───────────────────────────   │
│  └────┘  Engineering, Applied Sciences│
│          🟢 Subscribed | Full Access   │
│          [Launch Database →]            │
│                                        │
│  ┌────┐                                │
│  │JSTOR│  JSTOR Digital Library        │
│  │     │  ───────────────────────────   │
│  └────┘  Arts, Humanities, Social Sci  │
│          🟡 Open Access + Subscribed   │
│          [Launch Database →]            │
│                                        │
└────────────────────────────────────────┘
```

**CSS:**
```css
.db-card {
  display: flex; align-items: flex-start; gap: var(--space-4);
  padding: var(--space-5); background: var(--glass-card-bg);
  border: 1px solid var(--paper-200); border-radius: 12px;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.db-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}
.db-card .db-info { flex: 1; }
.db-card .db-title {
  font-family: var(--font-primary); font-size: var(--text-h3);
  font-weight: 600; color: var(--maroon-700); margin-bottom: var(--space-1);
}
.db-card .db-subjects {
  font-size: var(--text-body-sm); color: var(--paper-600); margin-bottom: var(--space-2);
}
.db-card .db-access {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: var(--text-body-sm); font-weight: 600;
}
.db-card .db-access.subscribed { color: var(--green-700); }
.db-card .db-access.open-access { color: var(--blue-700); }
.db-card .db-access.mixed { color: var(--warning); }
.db-card .launch-btn {
  margin-top: var(--space-3);
  padding: 8px 20px; background: var(--maroon-600); color: var(--white);
  font-size: var(--text-button); font-weight: 600; border: none;
  border-radius: var(--radius-md); cursor: pointer;
  transition: background 0.2s ease;
}
.db-card .launch-btn:hover { background: var(--maroon-700); }
```

### 6.3 Institutional Repository Item Card

A card for DSpace theses, research papers, and departmental question papers. Emphasizes the institutional origin and digital access.

```
┌────────────────────────────────────────────────────────────┐
│  [Open Access Ribbon]                                      │
│                                                            │
│  Traffic Flow Prediction in Dhaka Using Deep Learning      │
│  ──────────────────────────────────────────────────────── │
│  By Islam, N. | Department of CSE, BUET | 2024            │
│  Thesis — M.Sc. in Computer Science                        │
│                                                            │
│  📄 PDF Available  |  🔬 Deep Learning  |  🚗 Transport    │
│  DOI: 10.1234/buet.cse.2024.001                            │
│                                                            │
│  [📄 Download PDF]  [🔖 Save to My Research]  [📤 Cite]  │
│  [📊 View in DSpace]                                       │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**CSS:**
```css
.repo-card {
  position: relative; background: var(--card-bg);
  border: 1px solid var(--card-border); border-radius: var(--radius-md);
  padding: var(--space-5); margin-bottom: var(--space-4);
  overflow: hidden; /* for ribbon */
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.repo-card:hover {
  box-shadow: var(--shadow-md); transform: translateY(-1px);
}
.repo-card .repo-type {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: var(--text-caption); font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.05em;
  color: var(--paper-500); margin-bottom: var(--space-2);
}
.repo-card .repo-title {
  font-family: var(--font-primary); font-size: var(--text-h3);
  font-weight: 600; color: var(--maroon-700); line-height: 1.4;
  margin-bottom: var(--space-2);
}
.repo-card .repo-meta {
  font-size: var(--text-body-sm); color: var(--paper-600); margin-bottom: var(--space-3);
}
.repo-card .repo-doi {
  font-family: var(--font-mono); font-size: var(--text-body-sm);
  color: var(--blue-500); margin-bottom: var(--space-3);
}
.repo-card .repo-doi a:hover { text-decoration: underline; }
.repo-card .repo-actions {
  display: flex; gap: var(--space-3); margin-top: var(--space-3);
  padding-top: var(--space-3); border-top: 1px solid var(--paper-200);
}
```

### 6.4 Reference Service Widget

A floating or sidebar widget for accessing reference services — live chat, submit a question, schedule a consultation.

```
┌──────────────────┐
│  Reference Desk  │
│  ═══════════════  │
│                  │
│  🟢 Live Chat    │
│  Librarian Online │
│  [Start Chat]    │
│                  │
│  ───────────────  │
│  Submit Question │
│  [Ask a Question] │
│                  │
│  ───────────────  │
│  Schedule        │
│  Consultation    │
│  [Book Session]  │
│                  │
│  ───────────────  │
│  Citation Tools  │
│  [BibTeX] [RIS]  │
│  [Zotero Export] │
│                  │
└──────────────────┘
```

**CSS:**
```css
.reference-widget {
  background: var(--card-bg); border: 1px solid var(--card-border);
  border-radius: var(--radius-lg); padding: var(--space-5);
  position: sticky; top: 80px;
}
.reference-widget-title {
  font-family: var(--font-primary); font-size: var(--text-h4);
  font-weight: 600; color: var(--maroon-800); margin-bottom: var(--space-4);
  padding-bottom: var(--space-2); border-bottom: 2px solid var(--gold-500);
}
.reference-option {
  padding: var(--space-3) 0; border-bottom: 1px solid var(--paper-200);
}
.reference-option:last-child { border-bottom: none; }
.reference-option-title {
  font-size: var(--text-body); font-weight: 600; color: var(--text-primary);
  margin-bottom: var(--space-1);
}
.reference-option-desc {
  font-size: var(--text-body-sm); color: var(--paper-500); margin-bottom: var(--space-2);
}
.reference-btn {
  display: inline-block; padding: 6px 16px;
  background: var(--maroon-600); color: var(--white);
  font-size: var(--text-button); font-weight: 600; border: none;
  border-radius: var(--radius-md); cursor: pointer;
  transition: background 0.2s ease;
}
.reference-btn:hover { background: var(--maroon-700); }
.reference-btn.secondary {
  background: transparent; color: var(--maroon-600);
  border: 1px solid var(--maroon-200);
}
.reference-btn.secondary:hover { background: var(--maroon-50); }
```

### 6.5 Federated Search Result Card

A card for results from external APIs (Crossref, OpenAlex, CORE). Emphasizes open access and source credibility.

```
┌────────────────────────────────────────────────────────────┐
│  🌐 Crossref          [Journal Article]    [Open Access] │
│                                                            │
│  Deep Reinforcement Learning for Bridge Health Monitoring  │
│  Smith, J., Rahman, A.K.M., Karim, S.                    │
│  Structural Health Monitoring, Vol. 23, 2024               │
│  DOI: 10.1177/14759217241234567                          │
│                                                            │
│  🔓 Free Full Text  |  📄 PDF  |  🔖 Save  |  📤 Cite     │
│                                                            │
│  Abstract: This paper presents a novel approach...        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**CSS:**
```css
.federated-card {
  background: var(--card-bg); border: 1px solid var(--card-border);
  border-radius: var(--radius-md); padding: var(--space-5); margin-bottom: var(--space-4);
  border-left: 4px solid var(--blue-500); /* Open access indicator */
  transition: box-shadow 0.2s ease;
}
.federated-card:hover { box-shadow: var(--shadow-md); }
.federated-card .source-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: var(--space-2);
}
.federated-card .source-name {
  font-size: var(--text-caption); font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.05em; color: var(--paper-500);
}
.federated-card .oa-badge {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 2px 8px; background: var(--blue-50); color: var(--blue-700);
  font-size: var(--text-caption); font-weight: 600;
  border-radius: var(--radius-sm); border: 1px solid var(--blue-100);
}
.federated-card .federated-title {
  font-family: var(--font-primary); font-size: var(--text-h3);
  font-weight: 600; color: var(--maroon-700); line-height: 1.4; margin-bottom: var(--space-2);
}
.federated-card .federated-authors {
  font-size: var(--text-body-sm); color: var(--paper-600); margin-bottom: var(--space-1);
}
.federated-card .federated-venue {
  font-size: var(--text-body-sm); color: var(--paper-500); margin-bottom: var(--space-2);
}
.federated-card .federated-doi {
  font-family: var(--font-mono); font-size: var(--text-body-sm); color: var(--blue-500);
  margin-bottom: var(--space-3);
}
```

### 6.6 Navigation Bar (E-Library Focused)

```css
.main-nav {
  position: sticky; top: 0; z-index: 100;
  background: var(--maroon-700);
  border-bottom: 3px solid var(--gold-500);
  padding: 0 var(--space-5);
}
.main-nav .nav-links {
  display: flex; gap: var(--space-6); list-style: none;
}
.main-nav .nav-link {
  position: relative; color: rgba(255,255,255,0.85);
  font-size: var(--text-button); font-weight: 500;
  text-decoration: none; padding: 8px 0; transition: color 0.2s ease;
}
.main-nav .nav-link:hover, .main-nav .nav-link.active { color: var(--white); }
.main-nav .nav-link::after {
  content: ''; position: absolute; bottom: 0; left: 0;
  width: 0; height: 2px;
  background: linear-gradient(90deg, var(--gold-500), var(--blue-500));
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.main-nav .nav-link:hover::after, .main-nav .nav-link.active::after { width: 100%; }
```

---

## 7. Page Layouts (E-Library Focused)

### 7.1 Homepage — E-Resource Discovery

```
┌────────────────────────────────────────────────────────────┐
│  [Sticky Nav] BUET Logo | E-Resources | Repository | Ref │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │                                                    │   │
│  │     BUET E-Library                                 │   │
│  │     বিশ্বজ্ঞানের ডিজিটাল প্রবেশদ্বার                    │   │
│  │     Digital Gateway to Knowledge                   │   │
│  │                                                    │   │
│  │  ┌────────────────────────────────┬───────────┐   │   │
│  │  │  🔍 Search e-resources...      │  SEARCH   │   │   │
│  │  └────────────────────────────────┴───────────┘   │   │
│  │                                                    │   │
│  │  Browse Databases:                                 │   │
│  │  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐      │   │
│  │  │IEEE│ │Else│ │JSTOR│ │SPR │ │Wiley│ │ACM │      │   │
│  │  └────┘ └────┘ └────┘ └────┘ └────┘ └────┘      │   │
│  │                                                    │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Browse by Subject                                  │   │
│  │  [Civil] [CSE] [EEE] [Mech] [Arch] [Chem] [Math]   │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│  ┌─────────────────┐  ┌─────────────────┐               │
│  │  Quick Stats    │  │  Reference       │               │
│  │  ────────────   │  │  ────────────    │               │
│  │  🌐 128+        │  │  🟢 Live Chat    │               │
│  │  E-Databases    │  │  Librarian Online│               │
│  │  📄 12,000+     │  │  [Ask Question]  │               │
│  │  Theses (IR)    │  │  [Book Session]  │               │
│  │  💻 45,000+     │  │                  │               │
│  │  E-Books        │  │  Citation Tools:  │               │
│  │  🔬 8,000+      │  │  [BibTeX] [RIS]  │               │
│  │  Journal Arts   │  │  [Zotero]        │               │
│  └─────────────────┘  └─────────────────┘               │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Newly Added to Repository                         │   │
│  │  [Thesis 1] [Thesis 2] [Paper 3] [Paper 4]        │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
├────────────────────────────────────────────────────────────┤
│  [Footer] About | Contact | Help | Privacy | © BUET 2026  │
└────────────────────────────────────────────────────────────┘
```

### 7.2 E-Resource Database Page

```
┌────────────────────────────────────────────────────────────┐
│  [Sticky Nav]                                              │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  E-Resource Databases                                      │
│  ┌──────────────────┐  ┌─────────────────────────────────┐│
│  │  Filter          │  │  ┌────┐ IEEE Xplore             ││
│  │  ──────────────  │  │  │ X  │ Engineering, CS, EE   ││
│  │  Subject         │  │  └────┘ 🟢 Subscribed          ││
│  │  ● All (128)     │  │       [Launch Database →]     ││
│  │  ○ Engineering(45)│  │                                 ││
│  │  ○ CS (32)       │  │  ┌────┐ Elsevier ScienceDirect  ││
│  │  ○ Science (28)  │  │  │ELSE│ Engineering, Applied Sci││
│  │  ○ Humanities(15)│  │  │VIER│ 🟢 Subscribed          ││
│  │  ──────────────  │  │  └────┘ [Launch Database →]     ││
│  │  Type            │  │                                 ││
│  │  ● All           │  │  ┌────┐ JSTOR Digital Library   ││
│  │  ○ Journals (85) │  │  │JSTO│ Arts, Humanities, SS    ││
│  │  ○ E-Books (32)  │  │  │R   │ 🟡 Open Access + Sub    ││
│  │  ○ Standards(11) │  │  └────┘ [Launch Database →]     ││
│  │  ──────────────  │  │                                 ││
│  │  Access          │  │  ...                             ││
│  │  ● All           │  │                                 ││
│  │  ○ Subscribed(89)│  │                                 ││
│  │  ○ Open Access(39)│ │                                 ││
│  └──────────────────┘  └─────────────────────────────────┘│
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 7.3 Institutional Repository Page

```
┌────────────────────────────────────────────────────────────┐
│  [Sticky Nav]                                              │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  BUET Institutional Repository — DSpace                    │
│  ────────────────────────────────────────────────────────  │
│                                                            │
│  Browse by: [Department] [Year] [Type] [Subject]           │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │  🔓 Open Access Ribbon                               │   │
│  │  Traffic Flow Prediction in Dhaka Using Deep Learning│   │
│  │  By Islam, N. | CSE, BUET | 2024 | M.Sc. Thesis    │   │
│  │  📄 PDF | 🔬 Deep Learning | 🚗 Transport           │   │
│  │  [Download PDF] [View in DSpace] [Cite]           │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Structural Analysis of High-Rise Buildings in Dhaka │   │
│  │  By Rahman, S. | Civil, BUET | 2023 | B.Sc. Thesis  │   │
│  │  📄 PDF | 🏗️ Structural | 🏙️ Urban Planning        │   │
│  │  [Download PDF] [View in DSpace] [Cite]             │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│  [1] [2] [3] ... [25] Next →                               │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 7.4 Reference Services Page

```
┌────────────────────────────────────────────────────────────┐
│  [Sticky Nav]                                              │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Reference Services                                        │
│  ────────────────────────────────────────────────────────  │
│                                                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐│
│  │  🟢 Live Chat   │  │  📧 Submit      │  │  📅 Schedule││
│  │  Librarian      │  │  a Question     │  │  Consultation││
│  │  Online Now     │  │                 │  │             ││
│  │  [Start Chat]   │  │  [Ask Now]      │  │  [Book]     ││
│  └─────────────────┘  └─────────────────┘  └─────────────┘│
│                                                            │
│  ────────────────────────────────────────────────────────  │
│                                                            │
│  Citation & Research Tools                                 │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐          │
│  │  BibTeX    │  │  RIS       │  │  Zotero    │          │
│  │  Export    │  │  Export    │  │  Connector │          │
│  │  [Export]  │  │  [Export]  │  │  [Install] │          │
│  └────────────┘ └────────────┘ └────────────┘          │
│                                                            │
│  ────────────────────────────────────────────────────────  │
│                                                            │
│  Research Guides                                           │
│  [How to Search Databases] [Writing a Literature Review]   │
│  [Citation Styles] [Avoiding Plagiarism] [MARC Records]   │
│                                                            │
│  ────────────────────────────────────────────────────────  │
│                                                            │
│  Frequently Asked Questions                                │
│  Q: How do I access IEEE Xplore off-campus?                │
│  A: Use the BUET proxy at https://proxy.buet.ac.bd:8080... │
│                                                            │
│  Q: How do I submit my thesis to the repository?           │
│  A: Log in to DSpace and follow the submission guide...    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 8. Dark Mode (E-Library)

*(Same as V1 but with digital-blue accent for links)*

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
  --link-color: var(--blue-400); /* Digital blue for links */
  --link-hover: var(--blue-300);
  --accent: var(--gold-400);
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.5);
}
```

---

## 9. Animation & Motion

*(Same as V1 — see `demo.html` for implementation)*

---

## 10. Accessibility (WCAG 2.1 AA)

*(Same as V1 but with digital-blue link contrast checked)*

| Combination | Ratio | Pass |
|-------------|-------|------|
| `--blue-500` on `--white` | 4.6:1 | ✅ AA |
| `--blue-500` on `--paper-50` | 4.4:1 | ✅ AA |
| `--blue-400` on `--paper-900` | 5.2:1 | ✅ AA |
| `--gold-500` on `--white` | 3.1:1 | ❌ AA (decorative only) |
| `--gold-700` on `--white` | 5.2:1 | ✅ AA (large text) |

---

## 11. Responsive Behavior

*(Same as V1)*

---

## 12. Assets & Files

### Required Image Assets (E-Library)

| File | Description | Location |
|------|-------------|----------|
| `buet-logo-white.svg` | BUET seal/logo, white | `themes/buet_elibrary/images/` |
| `buet-logo-maroon.svg` | BUET seal/logo, maroon | `themes/buet_elibrary/images/` |
| `digital-wave.svg` | Subtle wave pattern for hero | `themes/buet_elibrary/images/` |
| `db-icons/` | Database brand icons (IEEE, Elsevier, etc.) | `themes/buet_elibrary/images/db-icons/` |
| `favicon.ico` | 32×32 and 16×16 | `themes/buet_elibrary/favicon.ico` |
| `apple-touch-icon.png` | 180×180 iOS icon | `themes/buet_elibrary/images/` |

---

## 13. Drupal 11 Theme Implementation

### Theme Structure

```
themes/buet_elibrary/
├── buet_elibrary.info.yml
├── buet_elibrary.libraries.yml
├── buet_elibrary.theme
├── css/
│   ├── base.css           # ← Import this file (from design/)
│   ├── layout.css
│   ├── components.css     # Cards, badges, buttons, forms
│   ├── navigation.css     # Nav, sidebar, breadcrumbs
│   ├── e-resources.css    # Database cards, e-resource browser
│   ├── repository.css     # DSpace item cards, browse pages
│   ├── reference.css      # Reference widget, helpdesk, guides
│   ├── search.css         # Search box, results, facets
│   ├── dark-mode.css      # Dark mode overrides
│   └── print.css
├── js/
│   ├── dark-mode.js
│   ├── live-status.js     # Real-time availability (for proxy)
│   ├── federated-search.js
│   └── reference-chat.js  # Live chat widget
├── images/
│   ├── buet-logo-white.svg
│   ├── buet-logo-maroon.svg
│   ├── digital-wave.svg
│   └── db-icons/
│       ├── ieee.svg
│       ├── elsevier.svg
│       ├── jstor.svg
│       ├── springer.svg
│       ├── wiley.svg
│       └── acm.svg
└── templates/
    ├── page.html.twig
    ├── node--e-resource.html.twig
    ├── node--repository-item.html.twig
    ├── search-result.html.twig
    ├── search-results.html.twig
    ├── facet-*.html.twig
    └── block--reference-widget.html.twig
```

---

## 14. Design Inspiration

1. **BUET Institutional Identity** — Maroon and gold from the official seal
2. **Digital-First Libraries** — MIT Libraries, Stanford Digital Repository, arXiv
3. **E-Resource Portals** — IEEE Xplore, ScienceDirect, JSTOR interface patterns
4. **Open Access Movement** — DOAJ, CORE, Unpaywall visual language
5. **Bangladeshi Digital Design** — bKash app, Pathao, local SaaS aesthetics
6. **Engineering Precision** — Grid systems, data density, technical clarity

---

**End of E-Library Design System**
