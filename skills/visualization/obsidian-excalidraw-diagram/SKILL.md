---
name: obsidian-excalidraw-diagram
description: Generate clean, engineering-style Excalidraw diagrams from text content, laid out across one or more A4-proportioned pages. Supports three output modes - Obsidian (.md), Standard (.excalidraw), and Animated (.excalidraw with animation order). Use this skill whenever the user asks to draw, sketch, diagram, or visualize something in Excalidraw, or mentions a flowchart, mind map, hierarchy, relationship map, comparison, timeline, matrix, or freeform layout, even if they do not say "Excalidraw" explicitly. Also triggers on "standard excalidraw", "animated diagram", and "animate".
---

# Excalidraw Diagram Generator

Create clean, engineering-style Excalidraw diagrams from text content, with multiple output formats. The defaults favor precision over a hand-drawn look: minimum sloppiness, readable non-handwritten fonts, a visible background grid, and a layout that spans one or more A4-proportioned pages.

## Output Modes

Select the output mode from the user's trigger words:

| Trigger words | Output mode | File format | Purpose |
|---------------|-------------|-------------|---------|
| `Excalidraw`, `diagram`, `flowchart`, `mind map` | **Obsidian** (default) | `.md` | Open directly inside Obsidian |
| `standard excalidraw`, `standard Excalidraw` | **Standard** | `.excalidraw` | Open / edit / share on excalidraw.com |
| `animated diagram`, `animate` | **Animated** | `.excalidraw` | Drop into excalidraw-animate to render an animation |

## Workflow

1. **Detect output mode** from trigger words (see Output Modes table above)
2. Analyze content - identify concepts, relationships, hierarchy
3. Choose diagram type (see Diagram Types below)
4. Plan the pages - split the story into A4 pages, one coherent section per page (see Page Layout)
5. Generate Excalidraw JSON (add animation order if Animated mode)
6. Output in the correct format for the mode
7. **Automatically save to the current working directory**
8. Notify the user with the file path and usage instructions

## Output Formats

### Mode 1: Obsidian Format (Default)

**Follow this structure exactly, with no modifications:**

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw]
---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'

# Excalidraw Data

## Text Elements
%%
## Drawing
```json
{full JSON data}
```
%%
```

**Key points:**
- Frontmatter must include `tags: [excalidraw]`
- The warning line must be complete
- The JSON must be wrapped by the `%%` markers
- Do not add any frontmatter beyond `excalidraw-plugin: parsed`
- **File extension**: `.md`

### Mode 2: Standard Excalidraw Format

Output a pure JSON file that opens on excalidraw.com:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [...],
  "appState": {
    "gridSize": 20,
    "gridStep": 5,
    "gridModeEnabled": true,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

**Key points:**
- `source` is `https://excalidraw.com` (not the Obsidian plugin)
- Pure JSON, no Markdown wrapper
- **File extension**: `.excalidraw`

### Mode 3: Animated Excalidraw Format

Same as the Standard format, but each element adds a `customData.animate` field to control the draw order:

```json
{
  "id": "element-1",
  "type": "rectangle",
  "customData": {
    "animate": {
      "order": 1,
      "duration": 500
    }
  },
  ...other standard fields
}
```

**Animation order rules:**
- `order`: draw sequence (1, 2, 3...); lower numbers appear first
- `duration`: draw time for the element in milliseconds (default 500)
- Elements that share an `order` appear at the same time
- Suggested order: title → main frame → connectors → detail text

**How to use:**
1. Generate the `.excalidraw` file
2. Drop it into https://dai-shi.github.io/excalidraw-animate/
3. Click Animate to preview, then export SVG or WebM

**File extension**: `.excalidraw`

---

## Diagram Types & Selection Guide

Pick the diagram form that makes the content easiest to understand.

| Type | Use case | Approach |
|------|----------|----------|
| **Flowchart** | Steps, workflows, execution order | Connect steps with arrows; show the direction of flow |
| **Mind Map** | Concept expansion, topic grouping, idea capture | Radiate outward from a central node |
| **Hierarchy** | Org structure, content levels, system breakdown | Build nodes top-down or left-to-right |
| **Relationship** | Influence, dependency, interaction between elements | Connect shapes with lines; label arrows |
| **Comparison** | Two or more options or viewpoints side by side | Two columns or a table; label the compared dimensions |
| **Timeline** | Event progression, project schedule, evolution | Use time as the axis; mark key points and events |
| **Matrix** | Two-dimension classification, prioritization, positioning | Build X and Y axes; place items on the plane |
| **Freeform** | Scattered notes, idea capture, early collection | No fixed structure; place blocks and arrows freely |

## Design Rules

### Text & Format
- **Regular text** uses `fontFamily: 6` (Nuno / Nunito) at **`fontSize: 20`** (the "Medium" preset). This is the default for titles, labels, and body text.
- **Code, identifiers, and monospaced text** use `fontFamily: 3` (Cascadia).
- Do not use the hand-drawn font (`fontFamily: 5`, Excalifont). These are engineering diagrams; keep the type clean and legible.
- Optional override: in Obsidian only, the plugin's "Local Font" (4th font, `fontFamily: 4`, configured here as JetBrains Mono) can be used instead of Cascadia for a mono look. It does not render on excalidraw.com, so do not use it for Standard or Animated modes.
- **Font size scale** (hard floor 16px; below that is unreadable at normal zoom):
  - Title: 28px (the "Large" preset)
  - Subtitle: 24px
  - Body / labels: 20px (Nuno Medium, the default)
  - Small caption: 16px (use sparingly)
- **Line height**: all text uses `lineHeight: 1.25`
- **Centering standalone text**: a standalone text element is not auto-centered; compute its `x` manually:
  - Estimate width: `estimatedWidth = text.length * fontSize * 0.5`
  - Centering formula: `x = centerX - estimatedWidth / 2`
  - Example: "Hello" (5 chars, fontSize 20) centered at x=300 → `estimatedWidth = 5 * 20 * 0.5 = 50` → `x = 300 - 25 = 275`

### Layout & Design
- **Sloppiness**: every element uses `roughness: 0` (Excalidraw's "Architect" / minimum). Edges stay crisp.
- **Pages**: lay the diagram out across one or more A4-proportioned pages, not crammed into one. Each page is one A4 unit; add pages as the story grows. See "Page Layout" below for sizes, tiling, and the page-origin formula.
- **Grid**: the background grid is always on (see appState). The grid spacing is 20px - align element coordinates to multiples of 20 where practical for a clean engineering look.
- **Inner margin**: keep content ~40px away from the page edges.
- **Minimum shape size**: rectangles / ellipses with text should be at least 120x60px
- **Element spacing**: at least 20-30px between elements to prevent overlap
- **Clear hierarchy**: use different colors and shapes to separate levels of information
- **Graphic elements**: use rectangles, ellipses, and arrows to organize information
- **No emoji**: do not put emoji in diagram text; use simple shapes (circles, squares, arrows) or color to mark things

### Page Layout (A4 pages)

A diagram is told across one or more A4-proportioned pages. An A4 page is the repeating unit; do not shrink everything to fit one page, add pages as the story grows.

- **Page size** (96 DPI A4): landscape `1123 x 794` (default), portrait `794 x 1123`. Pick one orientation for the whole diagram, preferring landscape; use portrait only for clearly tall content.
- **Tiling**: place pages in reading order, left to right, with an `80px` gutter between them. For a long story, wrap to a new row below using the same gutter. The background grid is continuous across all pages.
- **Page origin** for page `k` (0-indexed):
  - single row: `originX = k * (pageW + 80)`, `originY = 0`
  - grid of `cols` columns: `originX = col * (pageW + 80)`, `originY = row * (pageH + 80)`
- **Inside a page**: keep ~40px inner margin, place and center elements relative to the page origin, and align to the 20px grid.
- **One section per page**: give each page a single coherent part of the story (for example Overview, then Data flow, then Failure modes) and a short page title near its top-left.

**Page guide** (recommended, so the A4 pages are visible): draw one light, locked rectangle per page plus a title text. Sharp corners (`roundness: null`), a 1px light-gray stroke, and `locked: true` keep it as a clean, fixed page boundary.

```json
{
  "id": "page-1-guide",
  "type": "rectangle",
  "x": 0, "y": 0,
  "width": 1123, "height": 794,
  "angle": 0,
  "strokeColor": "#ced4da",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "groupIds": [],
  "roundness": null,
  "seed": 1001,
  "version": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": true
}
```

Excalidraw "frame" elements are an alternative if you want named, individually-exportable pages, but locked rectangles are simpler and render identically everywhere.

### Color Palette

**Text color (strokeColor for text):**

| Purpose | Hex | Note |
|---------|-----|------|
| Title | `#1e40af` | Deep blue |
| Subtitle / connectors | `#3b82f6` | Bright blue |
| Body text | `#374151` | Dark gray (on white, never lighter than `#757575`) |
| Emphasis | `#f59e0b` | Gold |

**Shape fill color (backgroundColor, fillStyle: "solid"):**

| Hex | Meaning | Use case |
|-----|---------|----------|
| `#a5d8ff` | Light blue | Input, data source, primary node |
| `#b2f2bb` | Light green | Success, output, done |
| `#ffd8a8` | Light orange | Warning, pending, external dependency |
| `#d0bfff` | Light purple | Processing, middleware, special item |
| `#ffc9c9` | Light red | Error, critical, alert |
| `#fff3bf` | Light yellow | Note, decision, planning |
| `#c3fae8` | Light cyan | Storage, data, cache |
| `#eebefa` | Light pink | Analysis, metrics, statistics |

**Region background color (large rectangle + opacity: 30, for layered diagrams):**

| Hex | Meaning |
|-----|---------|
| `#dbe4ff` | Frontend / UI layer |
| `#e5dbff` | Logic / processing layer |
| `#d3f9d8` | Data / tooling layer |

**Contrast rules:**
- On a white background, text is never lighter than `#757575`, or it becomes unreadable
- On a light fill, use a darker variant for text (e.g. on light green use `#15803d`, not `#22c55e`)
- Avoid light gray text (`#b0b0b0`, `#999`) on a white background

See [references/excalidraw-schema.md](references/excalidraw-schema.md).

## JSON Structure

**Obsidian mode:**
```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://github.com/zsviczian/obsidian-excalidraw-plugin",
  "elements": [...],
  "appState": { "gridSize": 20, "gridStep": 5, "gridModeEnabled": true, "viewBackgroundColor": "#ffffff" },
  "files": {}
}
```

**Standard / Animated mode:**
```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [...],
  "appState": { "gridSize": 20, "gridStep": 5, "gridModeEnabled": true, "viewBackgroundColor": "#ffffff" },
  "files": {}
}
```

## Element Template

Each element requires these fields (do NOT add extra fields like `frameId`, `index`, `versionNonce`, `rawText` -- they may cause issues on excalidraw.com. `boundElements` must be `null` not `[]`, `updated` must be `1` not timestamps):

```json
{
  "id": "unique-id",
  "type": "rectangle",
  "x": 100, "y": 100,
  "width": 200, "height": 60,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "groupIds": [],
  "roundness": {"type": 3},
  "seed": 123456789,
  "version": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false
}
```

`strokeStyle` values: `"solid"` (solid, default) | `"dashed"` | `"dotted"`. Dashed and dotted lines suit optional paths, async flows, and weak associations.

Text elements add:
```json
{
  "text": "Sample text",
  "fontSize": 20,
  "fontFamily": 6,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": null,
  "originalText": "Sample text",
  "autoResize": true,
  "lineHeight": 1.25
}
```

Use `fontFamily: 3` (Cascadia) instead of `6` for code or monospaced text.

**Animated mode adds** a `customData` field:
```json
{
  "id": "title-1",
  "type": "text",
  "customData": {
    "animate": {
      "order": 1,
      "duration": 500
    }
  },
  ...other fields
}
```

See [references/excalidraw-schema.md](references/excalidraw-schema.md) for all element types.

---

## Additional Technical Requirements

### Handling Text Elements
- The `## Text Elements` section in the Markdown **must be left empty**, with only `%%` as the delimiter
- The Obsidian Excalidraw plugin **populates text elements automatically** from the JSON data
- There is no need to list the text content manually

### Coordinates & Layout
- **Coordinate system**: the top-left corner is the origin (0,0)
- **Recommended range**: keep each page's elements within that page's A4 box (page `k` spans `originX,0 → originX+1123,794` in landscape). See "Page Layout" for the page-origin formula.
- **Element ID**: each element needs a unique `id` (a string such as "title", "box1", etc.)

### Required Fields for All Elements

**IMPORTANT**: Do NOT include `frameId`, `index`, `versionNonce`, or `rawText`. Use `boundElements: null` (not `[]`), and `updated: 1` (not timestamps).

```json
{
  "id": "unique-identifier",
  "type": "rectangle|text|arrow|ellipse|diamond",
  "x": 100, "y": 100,
  "width": 200, "height": 60,
  "angle": 0,
  "strokeColor": "#color-hex",
  "backgroundColor": "transparent|#color-hex",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid|dashed|dotted",
  "roughness": 0,
  "opacity": 100,
  "groupIds": [],
  "roundness": {"type": 3},
  "seed": 123456789,
  "version": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false
}
```

### Text-Specific Properties
Text elements (type: "text") need these extra properties (do NOT include `rawText`):
```json
{
  "text": "Sample text",
  "fontSize": 20,
  "fontFamily": 6,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": null,
  "originalText": "Sample text",
  "autoResize": true,
  "lineHeight": 1.25
}
```

### appState configuration
The grid is always visible (engineering diagrams):
```json
"appState": {
  "gridSize": 20,
  "gridStep": 5,
  "gridModeEnabled": true,
  "viewBackgroundColor": "#ffffff"
}
```

### files field
```json
"files": {}
```

## Common Mistakes to Avoid

- **Text offset**: a standalone text element's `x` is its left edge, not its center. Compute the centered `x` with the formula, or text drifts to one side.
- **Element overlap**: elements with similar `y` coordinates stack easily. Check for at least 20px of spacing before placing a new element.
- **Content touching the edges**: do not let content hug the page edge. Keep ~40px of inner margin.
- **Cramming one page**: if a page gets dense, start a new A4 page for the next part of the story instead of shrinking everything.
- **Overlapping pages**: when tiling pages, respect the 80px gutter so page guides and content do not collide.
- **Title not centered on the diagram**: the title should be centered over the full width of the diagram below it, not pinned at x=0.
- **Arrow label overflow**: long labels (e.g. "ATP + NADPH") spill past short arrows. Keep labels short or lengthen the arrow.
- **Insufficient contrast**: light text on white is almost invisible. Keep text no lighter than `#757575`; use dark variants for colored text.
- **Font too small**: below 16px is hard to read at normal zoom; body text is 20px (Nuno Medium).
- **Sloppy edges**: leaving `roughness` above 0 produces a sketchy look. Keep it at 0.

## Implementation Notes

### Auto-save & File Generation Workflow

When generating an Excalidraw diagram, **perform these steps automatically**:

#### 1. Choose the right diagram type
- Use the "Diagram Types & Selection Guide" table above, based on the content
- Analyze the core intent of the content and pick the clearest visualization

#### 2. Generate a meaningful filename

Choose the extension from the output mode:

| Mode | Filename format | Example |
|------|-----------------|---------|
| Obsidian | `[topic].[type].md` | `data-pipeline.flowchart.md` |
| Standard | `[topic].[type].excalidraw` | `auth-flow.relationship.excalidraw` |
| Animated | `[topic].[type].animate.excalidraw` | `auth-flow.relationship.animate.excalidraw` |

- Use concise, descriptive English filenames

#### 3. Save the file with the Write tool
- **Save location**: the current working directory (auto-detected)
- **Full path**: `{current_directory}/[filename].md`
- This keeps things portable, with no hardcoded paths

#### 4. Get the Markdown structure exactly right
**Generate in this format** (no modifications):

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw]
---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'

# Excalidraw Data

## Text Elements
%%
## Drawing
```json
{full JSON data}
```
%%
```

#### 5. JSON data requirements
- Include the full Excalidraw JSON structure
- Regular text uses `fontFamily: 6` (Nuno); code/monospace uses `fontFamily: 3` (Cascadia)
- Every element uses `roughness: 0`
- The JSON must be valid and pass a syntax check
- Every element has a unique `id`
- Include the grid-on `appState` and `files: {}` fields

#### 6. Report back to the user
Tell the user:
- The diagram has been generated
- The exact save location
- How to view it in Obsidian
- The design choice (which diagram type was used, and why)
- Whether any adjustments are needed

### Example Output Messages

**Obsidian mode:**
```
Excalidraw diagram generated.

Saved to: data-pipeline.flowchart.md

How to view:
1. Open this file in Obsidian
2. Click the MORE OPTIONS menu (top right)
3. Choose Switch to EXCALIDRAW VIEW
```

**Standard mode:**
```
Excalidraw diagram generated.

Saved to: auth-flow.relationship.excalidraw

How to view:
1. Open https://excalidraw.com
2. Menu (top left) → Open → select this file
3. Or drag the file onto the excalidraw.com page
```

**Animated mode:**
```
Excalidraw animated diagram generated.

Saved to: auth-flow.relationship.animate.excalidraw

Animation order: title(1) → main frame(2-4) → connectors(5-7) → labels(8-10)

How to render:
1. Open https://dai-shi.github.io/excalidraw-animate/
2. Click Load File and select this file
3. Preview the animation
4. Click Export to produce SVG or WebM
```
