# Accessibility audit

Target: WCAG 2.2 AA. **Not yet claimed.** The automated checks below find only part of the issues; the manual checks are still to do.

## Automated results (25 Nov 2026)
- **axe-core (wcag2a, wcag2aa, wcag21a/aa, wcag22aa, best-practice), jsdom:** 0 violations on 9 views and 3 interaction scenarios (after a search, after a keyword search in Documents, coverage with assessments). Initial run found heading-order and landmark problems; fixed.
- **Colour contrast (`tests/contrast.py`):** all text pairs pass 4.5:1 in light and dark. The first run showed form control borders at 1.5:1 (WCAG 1.4.11 needs 3:1); a darker control border token fixed this (5.4:1 light, 6.7:1 dark).
- **Not covered by these tools:** real-browser contrast on every state, focus visibility on sticky header, zoom reflow, screen-reader behaviour.

## Manual checklist (to do)
| Test | What to check |
|---|---|
| Keyboard only | Every link, select, checkbox, button, details and "Show more" reachable and operable; focus order; no traps |
| Focus not obscured | Focused items are not hidden under the sticky header (scroll-padding is set to 84px; confirm) |
| Screen readers (NVDA/JAWS, VoiceOver) | Headings, table headers, `details` summaries, search result announcements (live regions) |
| Zoom 200% and 400% | No loss of content; wide tables scroll inside their container |
| Mobile | Navigation wraps; tables usable |
| Dark mode | Contrast and readability across all views |
| Status not by colour | Every status has a symbol and a text label (done in design; confirm in use) |
| Reduced motion | No animation (none used) |
| Source documents | Many linked PDFs may not be accessible; note where known |

## Known issues to watch
- The coverage matrix is a wide table. It scrolls horizontally; consider a stacked layout on small screens.
- Highlighted search terms use `<mark>`; confirm screen readers handle it acceptably.
