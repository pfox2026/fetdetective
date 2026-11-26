/* Automated accessibility checks (axe-core in jsdom) for every view. Run: npm install && npm run test:a11y
   jsdom cannot compute colours, so contrast is checked separately by tests/contrast.py. Automated checks find roughly a third of WCAG issues:
   keyboard, screen reader, 200%/400% zoom and content review still need a manual audit. */
const { JSDOM } = require("jsdom"), fs = require("fs"), path = require("path"), axe = require("axe-core");
const root = path.resolve(__dirname, ".."), views = ["home", "etbs", "etb-longford-westmeath", "etb-donegal", "compare", "policies", "gap", "strategy", "status"];
(async () => {
  const dom = await JSDOM.fromFile(path.join(root, "index.html"), { runScripts: "dangerously", resources: "usable", pretendToBeVisual: true, beforeParse(win) { win.scrollTo = () => {}; } });
  const w = dom.window; w.scrollTo = () => {}; await new Promise(r => w.addEventListener("load", r));
  w.eval(axe.source); let failed = 0;
  for (const v of views) {
    w.location.hash = v; await new Promise(r => setTimeout(r, 150));
    const res = await w.axe.run(w.document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"] }, rules: { "color-contrast": { enabled: false } } });
    console.log(`${v}: ${res.violations.length} violation(s), ${res.passes.length} rules passed`);
    for (const x of res.violations) { failed++; console.log(`  - [${x.impact}] ${x.id}: ${x.help} (${x.nodes.length} node(s))\n      e.g. ${x.nodes[0].html.slice(0, 140)}`); }
  }
  const scenarios = [["home after a search", "home", d => { d.querySelector("#q").value = "procurement"; d.querySelector("#sf").dispatchEvent(new w.Event("submit", { cancelable: true })); }],
    ["documents after a keyword search", "policies", d => { const k = d.querySelector("#pk"); k.value = "bullying"; k.dispatchEvent(new w.Event("input")); }],
    ["coverage with an assessment", "gap", d => { const s = d.querySelector("#gc"); s.value = "Governance and Corporate"; s.dispatchEvent(new w.Event("change")); }]];
  for (const [name, v, act] of scenarios) {
    w.location.hash = v; await new Promise(r => setTimeout(r, 200)); act(w.document); await new Promise(r => setTimeout(r, 700));
    const res = await w.axe.run(w.document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"] }, rules: { "color-contrast": { enabled: false } } });
    console.log(`${name}: ${res.violations.length} violation(s)`); for (const x of res.violations) { failed++; console.log(`  - [${x.impact}] ${x.id}: ${x.help}\n      e.g. ${x.nodes[0].html.slice(0, 140)}`); }
  }
  process.exit(failed ? 1 : 0);
})();
