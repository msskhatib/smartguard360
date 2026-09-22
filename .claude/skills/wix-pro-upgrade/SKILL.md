---
name: wix-pro-upgrade
description: "One-stop orchestrator that takes an existing Wix site from amateur to professional — audits it, then fixes it, end to end. Runs a structured pass over branding & visual design, copy & messaging, images, SEO & metadata, site structure & navigation, business apps (store, bookings, forms, blog), accessibility, performance and trust signals, using the Wix MCP server and the installed wix-* skills for every live change and the banana skill for any image work. Use whenever the user wants their Wix site to look, read or perform more professionally, or asks to improve, upgrade, polish, modernise, redesign, optimise, audit, refresh, rebrand or 'make it look premium'. Triggers on: make my Wix site professional, improve my website, upgrade my site, my site looks cheap, site audit, polish the homepage, better SEO for my Wix site, fix my site's images, modernise the design, get more customers from my site."
argument-hint: "[audit|plan|execute|verify] <site name or URL> [--focus seo|design|copy|images|apps|a11y]"
compatibility: Needs the Wix MCP server (authorised) for live reads/writes. Delegates to wix-manage, wix-docs, wix-headless / wix-app when code is involved, and banana for images.
metadata:
  version: "1.0.0"
  author: Team SmartGuard360
  scope: existing Wix sites (Editor, Studio, or Headless)
---

# Wix Pro Upgrade

A single entry point that turns "make my Wix site more professional" into a repeatable, evidence-based programme. It never guesses — it reads the live site through the Wix MCP server, scores it against the checklist in `references/pro-checklist.md`, agrees a plan with the owner, then executes each fix through the specialist skill that owns it.

**Guiding rule:** this skill is the conductor, not the orchestra. It decides *what* to change and in *what order*; the actual API calls, code and images come from the skills listed under Routing. Never write a Wix API call from memory — open `wix-docs` or the `wix-manage` recipe first.

## Modes

| Mode | What happens | Output |
|---|---|---|
| `audit` (default first run) | Read the live site, score every checklist area 1–5, list concrete findings with evidence | `Site Audit` report (chat + `wix-pro-upgrade/audit-<site>.md`) |
| `plan` | Turn findings into a prioritised backlog: impact × effort, grouped into sprints | `Upgrade Plan` with owner approval gate |
| `execute` | Apply the approved sprint, one area at a time, confirming before anything visible changes | Change log with before/after |
| `verify` | Re-run the audit, diff the scores, flag regressions | `Verification` report |

Run in order. Never `execute` without an approved `plan`.

## Workflow

### 0 · Preconditions
1. Confirm the Wix MCP server is authorised (`ListWixSites` succeeds). If not, stop and tell the user to authorise Wix in claude.ai connector settings — nothing else works without it.
2. Identify the target site (`ListWixSites` → confirm with the user if more than one). Capture: site type (Editor / Studio / Headless), business vertical, primary goal (leads, sales, bookings, portfolio), target audience, language(s), and brand assets the user already has (logo, colours, fonts, photos).
3. Ask the user for the **one sentence** the site must make a visitor believe. Everything downstream serves that sentence.

### 1 · Audit (read-only)
Pull, via `GetSiteContext` / `wix-manage` recipes, everything you can read without changing it:
- **Structure:** pages, navigation, footer, 404, legal pages present?
- **SEO:** per-page titles, meta descriptions, OG tags, H1 usage, alt text coverage, sitemap/robots, canonical, indexing status (`wix-manage/references/seo/manage-seo-tags.md`).
- **Content:** headline clarity, value proposition above the fold, CTA presence/consistency, tone, spelling, filler text ("Lorem", "Welcome to my site"), outdated dates.
- **Visual:** logo quality, colour palette count (>3 primaries is a smell), font count (>2 families is a smell), image quality/consistency, whitespace, alignment, mobile view.
- **Images:** resolution, aspect consistency, stock-photo tells, missing hero image, watermarks.
- **Business apps:** which are installed vs. what the goal needs (store, bookings, forms, chat, blog, members, pricing plans). Are they configured or empty shells?
- **Trust:** contact details, physical address (if relevant), reviews/testimonials, privacy policy, secure checkout, real photos of people/premises, social links that resolve.
- **Accessibility:** `wix-manage/references/accessibility/scan-site-accessibility.md` — contrast, alt text, heading order, focus states, form labels.
- **Performance signals:** oversized media, unused apps, autoplay video, excessive fonts.
- **Analytics:** is tracking connected? Any traffic data to inform priorities?

Score each area 1–5 using `references/pro-checklist.md`. Every score below 4 must carry at least one *specific* finding with evidence (page, element, current value). No vague "could be better".

### 2 · Plan
Convert findings to a backlog table: `#`, `Area`, `Finding`, `Fix`, `Impact (H/M/L)`, `Effort (S/M/L)`, `Owner skill`, `Needs user input?`. Order by impact ÷ effort. Group into:
- **Sprint 1 — Foundations (do first, low risk):** SEO metadata, alt text, broken links, legal pages, contact info, analytics.
- **Sprint 2 — Message & conversion:** hero headline, value proposition, CTAs, page structure, trust elements.
- **Sprint 3 — Visual identity:** palette and type consolidation, logo, imagery, spacing, mobile fixes.
- **Sprint 4 — Business capability:** configure or add the apps the goal needs; seed real content.
- **Sprint 5 — Polish:** micro-copy, animations, favicon, social previews, 404 page.

Present the plan and **wait for explicit approval** of which sprints/items to run. Flag every item that changes visible content or requires the user's brand decisions (colours, photos, prices, wording).

### 3 · Execute
For each approved item, in order:
1. State what will change and where (page, section, field).
2. Route to the owner skill (table below). Read its recipe/schema **before** calling.
3. Prefer reversible changes first. For content edits, keep the previous value in the change log.
4. For copy, draft it, show it, get a nod, then write it — never publish wording the owner hasn't seen.
5. For images, brief `banana` with the brand direction captured in step 0 (see `references/image-brief-template.md`); generate, show, get a nod, then `UploadImageToWixSite`.
6. After each area, publish (if the user wants live updates) or leave in draft and say so.
7. Append to the change log: item, page, before, after, timestamp.

### 4 · Verify
Re-run the audit. Present a before/after score table, list anything that regressed, and hand over a short **maintenance checklist** (monthly: check analytics, refresh one testimonial, update seasonal imagery; quarterly: re-audit SEO).

## Routing

| Need | Skill / tool | Note |
|---|---|---|
| Read site, pages, apps, settings | Wix MCP `GetSiteContext`, `ListWixSites`, `ManageWixSite` | read first, always |
| Any REST change (SEO tags, site properties, CMS, store, bookings, forms, blog, media, analytics, accessibility scan) | `wix-manage` → open the recipe → `CallWixSiteAPI` / `ExecuteWixAPI` | never guess payloads |
| Confirm an endpoint or field | `wix-docs` | before any unfamiliar call |
| Token expired / no auth | `wix-auth` | |
| Generate or edit images (hero, banners, product shots, team portraits, favicon) | `banana` | use the image-brief template |
| Upload images | Wix MCP `UploadImageToWixSite` | after user approves the image |
| New site sections that need code (Studio / Headless) | `wix-headless`, `wix-headless-fast`, `wix-design-system` | |
| Custom dashboard/app functionality | `wix-app` | rare for a polish job |
| Moving content in from another platform | `wix-replatform` | out of scope unless asked |
| Polished PDF/Word report of the audit | `pdf` / `docx` | on request |

## Hard rules
- **Read before write. Show before publish.** No visible change without the owner seeing it first.
- **Brand decisions belong to the owner.** Propose two or three options for palette, type and imagery; do not pick silently.
- **No fabricated trust signals.** Never invent testimonials, review counts, client logos, awards, or team members. If the site lacks them, add a placeholder section and tell the owner what real material to supply.
- **No placeholder copy left live.** Every "Lorem", "Your text here", or "Welcome to my site" is a Sprint 1 fix.
- **Keep what works.** If an area already scores 4–5, leave it alone and say so.
- **One area at a time.** Finish, log, and confirm before moving on.
- **Respect the language.** Audit and write in the site's language(s); for Arabic/English bilingual sites check RTL rendering explicitly.

## Quick start (what to say)
- `/wix-pro-upgrade audit` — "audit my site and tell me what's unprofessional"
- `/wix-pro-upgrade plan` — "turn the audit into a prioritised plan"
- `/wix-pro-upgrade execute sprint 1` — "apply the foundations sprint"
- `/wix-pro-upgrade --focus seo` — "just fix the SEO"
- `/wix-pro-upgrade --focus images` — "replace the weak images with professional ones"
