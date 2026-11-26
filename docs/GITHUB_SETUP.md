# Putting this on GitHub

## Where it should live
- **A GitHub repository you or your organisation controls, private at first.** A personal account or a project organisation (for example `fet-detective`) both work.
- **Not under an ETB's official account** unless that ETB has agreed. The site describes itself as independent and not an official site of SOLAS, ETBI or any ETB. Hosting it under an employer's organisation can contradict that.
- Make it public only after you have decided the licence and checked the points under "Before going public".

## Set-up (about 10 minutes)
1. Create an empty repository on github.com (no README, no licence). Suggested name: `fet-detective`.
2. In this folder (the zip contains an initial commit):
   ```
   git remote add origin https://github.com/<you-or-org>/fet-detective.git
   git push -u origin main
   ```
3. **Settings > Pages > Source: GitHub Actions.** The `Deploy site` workflow publishes the site at `https://<you-or-org>.github.io/fet-detective/`.
4. **Settings > Actions > General > Workflow permissions: Read and write**, so the `Rebuild data` workflow can commit regenerated files, and tick "Allow GitHub Actions to create pull requests" for the link-check workflow.
5. **Settings > Branches > Add rule for `main`:** require a pull request and the `checks` status before merging. This gives you a review step and an audit trail for every change to the research.
6. Run **Actions > Link check > Run workflow** once. GitHub's runners can reach ETB sites; download the `link-report` artifact. Records marked "blocked" need a manual check in a browser.

## What the workflows do
| Workflow | When | What |
|---|---|---|
| Tests | every pull request and push | validates the data, checks generated files are current, colour contrast, axe accessibility checks |
| Rebuild data | a CSV or text file changes on `main` | regenerates `assets/js/data.js` and `fulltext.js` |
| Link check | Mondays, or on demand | tests every URL, attaches `link_report.csv` |
| Deploy site | push to `main` | publishes to GitHub Pages |

## Before going public
- **Licence.** Add a `LICENSE` file for the code (MIT is common). Your research data is separate: state how others may reuse it.
- **Extracted text.** `data/fulltext/` holds text extracted from other organisations' documents. Most ETB documents are public-sector publications, but check each one's terms. The site only shows short snippets with a page number and links to the original. If in doubt, keep that folder out of the public repository and index it privately.
- **Contact address** for corrections on the Method page (`meta.contact` in `tools/build.py`).
- **Sensitive data.** The repository must not contain personal data beyond names of public office-holders as published by the ETBs.
