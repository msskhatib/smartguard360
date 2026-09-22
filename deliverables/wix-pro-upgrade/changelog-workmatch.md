# Change log — WorkMatch upgrade (site 595b902b-f26f-4e45-950c-1277e7d7f576)

| # | Sprint | Item | Where | Before | After | When (UTC) |
|---|---|---|---|---|---|---|
| 1 | 1 | Regional settings | Site Properties | timeZone America/Chicago · currency USD | timeZone **Asia/Riyadh** · currency **SAR** (language en unchanged) — properties v14→v17 | 2026-09-22 |
| 2 | 1 | Homepage SEO (item STATIC_PAGE c1dmp) | SEO › Item tags | no custom tags (default "Home \| Workmatch", no description) | title **"WorkMatch \| Verified Local Workers, Matched by AI"** · meta description · og:title/og:description · twitter:title/description | 2026-09-22 |
| 3 | 1 | Site-level meta description | SEO › Site tags | description "" | same description as above | 2026-09-22 |
| 4 | 2 | Contact Us form | Wix Forms (New) | no forms | form **5eb8b8d6-f743-4e60-9973-9ac641b6e181** "Contact Us — WorkMatch": First name*, Last name, Email*, Phone/WhatsApp, What do you need?* (Hire a worker / Register as a worker / Partnership / Other), Tell us about the job*, Send request. Contact-mapped (creates CRM contact). Verified: 7/7 fields placed, summary 6 inputs, required flags correct. | 2026-09-22 |

Meta description used (150 chars): "Describe your job and WorkMatch's AI shortlists verified local workers in minutes. Secure payments and trusted talent for Saudi businesses and households."

Reversal notes: #1 PATCH back to USD/America/Chicago; #2 Reset Item SEO Tags To Default for c1dmp; #3 set description to ""; #4 form can be disabled/deleted from the Forms dashboard.
