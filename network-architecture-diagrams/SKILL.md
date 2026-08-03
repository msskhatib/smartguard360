---
name: network-architecture-diagrams
description: >-
  Create clear, professional network and cloud architecture diagrams as
  code — VPC/subnet layouts, 3-tier web apps, microservices, Kubernetes
  topologies, hub-and-spoke, hybrid on-prem-to-cloud, CI/CD, and data
  flows. Use this whenever the user wants to diagram, chart, visualize, or
  "draw" any kind of system, network, infrastructure, cloud, or deployment
  topology — including AWS/GCP/Azure architectures, network segmentation,
  security zones, or "how the services connect." Trigger even when the user
  doesn't say the word "diagram" — e.g. "show me how our infra fits
  together", "map out the request flow", "sketch the VPC layout", or "I need
  an architecture picture for the README/slides." Picks the right tool
  (Mermaid for embeddable/GitHub-native, the Python diagrams library for
  provider-icon PNGs, Graphviz for precise custom layouts) and applies
  layout conventions that make the result readable.
---

# Network & Architecture Diagrams

The goal is a diagram someone can read in ten seconds: traffic flows in an
obvious direction, related things sit together inside labeled boundaries,
and every edge says what actually travels over it. This skill helps you
choose the right rendering tool and then apply the layout conventions that
separate a clear diagram from a tangle of boxes.

## Step 1 — Choose the tool

Diagrams are code here, never hand-placed boxes. Three tools cover almost
everything; pick by what the diagram is *for*, not by habit.

| Use | When | Why |
|-----|------|-----|
| **Mermaid** (default) | The diagram lives in a README, PR, issue, docs site, or a Claude artifact; you want it editable by anyone; no special icons needed | Text-based, renders natively on GitHub/GitLab and in Markdown viewers with zero install. Start here unless you have a reason not to. |
| **Python `diagrams`** (mingrammer) | You need real AWS/GCP/Azure/Kubernetes provider icons, or a polished PNG/SVG for slides and formal docs | Produces presentation-quality images with official service glyphs. Needs Graphviz + a `pip install`. |
| **Graphviz DOT** | You need precise control over layout, ranking, or clustering and don't need provider icons | The layout engine underneath `diagrams`; use directly when you want the control without the icon set. |

If unsure, default to Mermaid — it is the lowest-friction option and the
user can always ask for provider icons afterward, which is the cue to
switch to `diagrams`.

Then read the matching reference for syntax, a node/icon catalog, and
copy-ready recipes:

- **`references/mermaid.md`** — `flowchart` (subgraphs for zones) and
  `architecture-beta` (cloud groups + icons), plus recipes for 3-tier apps,
  VPC layouts, microservices, and request flows.
- **`references/diagrams-python.md`** — setup, the import paths for AWS/GCP/
  Azure/K8s/on-prem nodes, `Cluster` grouping, and full runnable examples.
- **`references/graphviz.md`** — DOT idioms for subnets, ranking, and
  network topology.

## Step 2 — Gather what the diagram must show

Before drawing, pin down these four things — from the conversation, the
codebase (Terraform, `docker-compose.yml`, k8s manifests, IaC), or by
asking. A diagram invented without them is decoration, not documentation.

1. **Nodes** — the actual components (load balancer, 3 web servers, a
   Postgres primary + replica, a Redis cache, an S3 bucket…). Prefer real
   names/counts over generic "Server" boxes.
2. **Boundaries** — the trust or ownership zones the nodes live in: VPC,
   public vs. private subnet, availability zone, on-prem vs. cloud, a
   Kubernetes namespace, a security group. These become the visual groups.
3. **Edges** — what connects to what, and the **direction** of the request
   or data flow.
4. **Edge labels** — the protocol/port or purpose on each connection
   (`HTTPS 443`, `gRPC`, `TCP 5432`, `replication`, `async / SQS`). Unlabeled
   edges are the most common reason a diagram is ambiguous.

When the source is IaC or compose files, read them rather than guessing —
the boundaries and ports are already written down there.

## Step 3 — Apply the layout conventions

These are the rules of thumb that make any diagram, in any tool, readable.
Each earns its place; follow the reasoning, not just the rule.

- **Flow one direction, consistently.** Left-to-right for request/response
  pipelines (user → edge → app → data), top-to-bottom for layered stacks
  and org/hierarchy. Readers infer causality from direction; mixing
  directions forces them to trace every arrow by hand.
- **Group by boundary, and label the group.** Put nodes inside a visible
  box for their VPC/subnet/zone/namespace. The boundary is often the most
  important security fact in the picture — an unlabeled cluster wastes it.
- **Label every edge with protocol/port or intent.** This is what turns a
  connectivity sketch into something an engineer can act on. `443`, `5432`,
  `gRPC`, `async` — a couple of words each.
- **Show the entry point and direction of exposure.** Make it obvious what
  faces the internet (a client/Internet node up top or on the left) versus
  what is private. This is the first thing a reviewer looks for.
- **Keep one diagram to one concern.** A single picture that tries to show
  network topology *and* data flow *and* CI/CD becomes unreadable. Split
  into separate diagrams and reference them, rather than cramming.
- **Cap complexity.** Past ~15–20 nodes, collapse repetition ("Web tier
  ×3", one box for an auto-scaling group) or split the diagram. Density is
  the enemy of the ten-second read.
- **Add a legend only when symbols aren't self-evident** — e.g. dashed =
  async, red = public-facing. Don't add a legend that just restates obvious
  labels.

## Step 4 — Render and verify

- **Mermaid:** the fenced ```mermaid block renders as-is on GitHub and in
  artifacts — usually nothing more is needed. To produce a standalone PNG/
  SVG (for slides or when the target can't render Mermaid), use
  `scripts/render.py` (see below).
- **`diagrams` / Graphviz:** run the Python/DOT file to produce the image.
  `references/diagrams-python.md` and `references/graphviz.md` cover the
  exact commands and one-time setup (Graphviz + pip).

Always verify before handing off: check that arrow directions match the
real flow, every boundary is labeled, no edge is unlabeled without reason,
and — for rendered images — that the file was actually produced and looks
right (read it back / view it). A diagram with a backwards arrow is worse
than no diagram, because it will be trusted.

## `scripts/render.py`

A helper to turn a diagram source file into a PNG or SVG without
remembering each tool's invocation. It auto-detects the format and shells
out to the right renderer:

```bash
# Mermaid → PNG (uses npx @mermaid-js/mermaid-cli; no global install needed)
python scripts/render.py diagram.mmd -o diagram.png

# Graphviz DOT → SVG
python scripts/render.py topology.dot -o topology.svg

# Run a mingrammer `diagrams` Python script (it writes its own output file)
python scripts/render.py architecture.py
```

Run `python scripts/render.py --help` for options. The Mermaid path uses
`npx` (no global install) and passes `--no-sandbox`, so it works even as
root in containers/CI. If a Chromium is already installed, point puppeteer
at it with `PUPPETEER_EXECUTABLE_PATH=/path/to/chromium` to skip the
download. If a renderer isn't installed, the script prints the exact
install command for this environment rather than failing silently — read
`references/` for the setup details it points to.
