# Claude Code Skills

This directory holds Claude Code skills for this repository. Every skill is a
folder containing a `SKILL.md` (with YAML frontmatter). Claude Code auto-loads
these on session start when working in this repo; on a personal machine you can
mirror them into `~/.claude/skills/` instead.

Total: **56 skills**.

---

## Skill groups

### Document generation (from anthropics/skills)
- `docx` — create/edit Word documents
- `pptx` — create/edit PowerPoint decks
- `xlsx` — create/edit Excel workbooks
- `pdf` — generate and manipulate PDFs

### Design & frontend (from anthropics/skills)
- `frontend-design` — front-end UI implementation
- `canvas-design` — canvas/graphic composition
- `theme-factory` — design themes
- `web-artifacts-builder` — build web artifacts
- `skill-creator` — scaffold new skills

### Image generation
- `banana` — AI image generation via Google Gemini (Nano Banana). See below.

### Blender / 3D (from roble3/cc-blender-skill and kevinbadi/blender-skills)
Modeling, rendering, cameras, lighting, materials, animation, UV, export, and
AI-assisted 3D reconstruction skills — e.g. `blender-modeling`,
`blender-rendering`, `blender-cameras`, `blender-lighting`, `blender-materials`,
`blender-animation`, `blender-export`, `blender-uv-texturing`,
`blender-pro-workflow`, `blender-toolkit`, `image-to-3d`, `multi-image-to-3d`,
`reference-to-3d`, `wireframe-to-3d`, `text-to-blender`, `threejs-export`,
`turntable`, `crane-shot`, `dolly-rotate`, `orbital-hud-motion`, `perfect-loop`,
`polyhaven-*` (HDRI/material/scene helpers), and the various fit/repair/QA
autoloops.

---

## Runtime dependencies

Most Blender and 3D skills need external tooling that is **not** bundled with
this repo. Install/configure these before use:

### Blender + Blender MCP addon
Required by all `blender-*` skills and the AI-to-3D skills (`image-to-3d`,
`multi-image-to-3d`, `reference-to-3d`, `wireframe-to-3d`, `text-to-blender`,
`polyhaven-*`, `turntable`, camera/animation motion skills, etc.).

- **Blender 4.x/5.x** installed locally.
- **Blender MCP addon** (`ahujasid/blender-mcp`) enabled and running inside
  Blender, listening on **port 9876** (default). The skills talk to Blender
  over this MCP bridge; if it isn't running they fail with
  *"Blender's MCP addon isn't running…"*.
- To wire it into Claude Code, add the `blender-mcp` server to your MCP config
  (see the `ahujasid/blender-mcp` README) and start Blender with the addon
  enabled.

> Note: Blender is a desktop app and is **not** available in the cloud/web
> sandbox. These skills run on a machine where Blender is installed.

### Python packages
Some skills shell out to Python for image/geometry work:
- `opencv-python`, `numpy`, `scipy`, `Pillow` — required by `wireframe-to-3d`,
  `contour-to-mesh`, and related mesh-fitting skills.
- `pytesseract`, `pdf2image` — used by some PDF/OCR paths.

Install on demand: `pip install opencv-python numpy scipy Pillow`

### API keys
- **Meshy AI** (`MESHY_API_KEY`) — required by `image-to-3d`,
  `multi-image-to-3d`, and other Meshy-backed reconstruction skills.
  Endpoint: `https://api.meshy.ai/openapi/v1/…`.
- **PolyHaven** — the `polyhaven-*` skills pull free CC0 HDRIs/materials/models
  from [polyhaven.com](https://polyhaven.com); no key required.
- **Google Gemini** (`GOOGLE_AI_API_KEY`) — required by the `banana` image
  skill. Configured via the `nanobanana-mcp` MCP server (default model
  `gemini-2.5-flash-image`). The key lives in your local Claude settings, not
  in this repo.

---

## Using the skills

- **This repo (cloud/web session):** skills auto-load — nothing to install.
- **New session on this repo:** skills load automatically on start.
- **Your own machine:** copy the folders you want into `~/.claude/skills/` and
  restart Claude Code so they register.

Each skill's own `SKILL.md` documents its exact triggers, inputs, and any
per-skill setup.
