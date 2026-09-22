# Change log — WorkMatch upgrade (site 595b902b-f26f-4e45-950c-1277e7d7f576)

| # | Sprint | Item | Where | Before | After | When (UTC) |
|---|---|---|---|---|---|---|
| 1 | 1 | Regional settings | Site Properties | timeZone America/Chicago · currency USD | timeZone **Asia/Riyadh** · currency **SAR** (language en unchanged) — properties v14→v17 | 2026-09-22 |
| 2 | 1 | Homepage SEO (item STATIC_PAGE c1dmp) | SEO › Item tags | no custom tags (default "Home \| Workmatch", no description) | title **"WorkMatch \| Verified Local Workers, Matched by AI"** · meta description · og:title/og:description · twitter:title/description | 2026-09-22 |
| 3 | 1 | Site-level meta description | SEO › Site tags | description "" | same description as above | 2026-09-22 |
| 4 | 2 | Contact Us form | Wix Forms (New) | no forms | form **5eb8b8d6-f743-4e60-9973-9ac641b6e181** "Contact Us — WorkMatch": First name*, Last name, Email*, Phone/WhatsApp, What do you need?* (Hire a worker / Register as a worker / Partnership / Other), Tell us about the job*, Send request. Contact-mapped (creates CRM contact). Verified: 7/7 fields placed, summary 6 inputs, required flags correct. | 2026-09-22 |

| 5 | 1 | Business contact | Site Properties › business-contact | email — · country — | email **abdallah.dwairy@sa.zain.com** · country **SA** (phone/city left blank — owner to supply) | 2026-09-22 |
| 6 | 3 | Media imported | Media Manager | — | logo `46fb57_e7d13059bba8411280b4f4605ff473de~mv2.png` · hero `46fb57_7770d393d11f4656b33b26e041822919~mv2.jpg` · OG share `46fb57_f7b65db99e3343abb2b0a03c29ed30d5~mv2.jpg` · favicon `46fb57_5aa658323c2c44f1be8a7d2c9b27ad0d~mv2.png` | 2026-09-22 |
| 7 | 2 | Owner-notification automation | Automations | — | API create rejected: Wix has deprecated the "Get an email" action for API use (`DEPRECATED_ACTION_NOT_ALLOWED`). Owner enables it in Dashboard › Automations (2-click, see hand-off). Submissions already land in Dashboard › Forms & Submissions and Inbox. | 2026-09-22 |
| 8 | 3 | Business profile | Site Properties › business-profile | logo old orange/teal mark; no description | logo **new WorkMatch mark** (`46fb57_e7d13059…~mv2.png`) · siteDisplayName/businessName **WorkMatch** · description set | 2026-09-22 |
| 9 | 1/3 | Homepage social image | SEO › Item tags c1dmp | no og:image | og:image + twitter:image = OG share JPG (1200×630); full 10-tag set re-written and published; verified live in page source | 2026-09-22 |

Meta description used (150 chars): "Describe your job and WorkMatch's AI shortlists verified local workers in minutes. Secure payments and trusted talent for Saudi businesses and households."

Reversal notes: #1 PATCH back to USD/America/Chicago; #2 Reset Item SEO Tags To Default for c1dmp; #3 set description to ""; #4 form can be disabled/deleted from the Forms dashboard.

## Editor hand-off (classic Editor content is not reachable by API)
Open: https://editor.wix.com/edit/od/f4a5efba-50cd-41c0-9dff-6481c9f8351a?metaSiteId=595b902b-f26f-4e45-950c-1277e7d7f576
1. Header logo → replace with Media Manager file `workmatch-logo.png` (new mark). Settings › Favicon → `workmatch-favicon.png` (needs a paid plan to show).
2. Hero background → replace AI mock-up with `workmatch-hero.jpg` (subject on right; keep headline on the left).
3. Add a "Contact" section at page bottom → Add › Contact & Forms › pick form **Contact Us — WorkMatch**. Add a page "Contact" with the same form.
4. Buttons: "Tell Us What You Need" → link to the Contact section anchor; "See How It Works" → anchor on "Why WorkMatch Works". Menu: Home · How it works · Why WorkMatch · Contact.
5. Footer: email abdallah.dwairy@sa.zain.com (mailto:), phone / WhatsApp (https://wa.me/966…), social links, Privacy & Terms pages.
6. Dashboard › Automations → "Get an email when a form is submitted" → recipient abdallah.dwairy@sa.zain.com → Activate.
