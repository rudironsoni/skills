# Excalidraw JSON Schema Reference

## Color Palette

### Primary Colors
| Purpose | Color | Hex |
|---------|-------|-----|
| Main Title | Deep Blue | `#1e40af` |
| Subtitle | Medium Blue | `#3b82f6` |
| Body Text | Dark Gray | `#374151` |
| Emphasis | Orange | `#f59e0b` |
| Success | Green | `#10b981` |
| Warning | Red | `#ef4444` |

### Background Colors
| Purpose | Color | Hex |
|---------|-------|-----|
| Light Blue | Background | `#dbeafe` |
| Light Gray | Neutral | `#f3f4f6` |
| Light Orange | Highlight | `#fef3c7` |
| Light Green | Success | `#d1fae5` |
| Light Purple | Accent | `#ede9fe` |

## Element Types

### Rectangle
```json
{
  "type": "rectangle",
  "id": "unique-id",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 80,
  "strokeColor": "#1e40af",
  "backgroundColor": "#dbeafe",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roughness": 0,
  "opacity": 100,
  "roundness": { "type": 3 }
}
```

### Text
```json
{
  "type": "text",
  "id": "unique-id",
  "x": 150,
  "y": 130,
  "text": "Content here",
  "fontSize": 20,
  "fontFamily": 6,
  "textAlign": "center",
  "verticalAlign": "middle",
  "strokeColor": "#1e40af",
  "backgroundColor": "transparent"
}
```

### Arrow
```json
{
  "type": "arrow",
  "id": "unique-id",
  "x": 300,
  "y": 140,
  "width": 100,
  "height": 0,
  "points": [[0, 0], [100, 0]],
  "strokeColor": "#374151",
  "strokeWidth": 2,
  "startArrowhead": null,
  "endArrowhead": "arrow"
}
```

### Ellipse
```json
{
  "type": "ellipse",
  "id": "unique-id",
  "x": 100,
  "y": 100,
  "width": 120,
  "height": 120,
  "strokeColor": "#10b981",
  "backgroundColor": "#d1fae5",
  "fillStyle": "solid"
}
```

### Diamond
```json
{
  "type": "diamond",
  "id": "unique-id",
  "x": 100,
  "y": 100,
  "width": 150,
  "height": 100,
  "strokeColor": "#f59e0b",
  "backgroundColor": "#fef3c7",
  "fillStyle": "solid"
}
```

### Line
```json
{
  "type": "line",
  "id": "unique-id",
  "x": 100,
  "y": 100,
  "points": [[0, 0], [200, 100]],
  "strokeColor": "#374151",
  "strokeWidth": 2
}
```

### Page guide (A4 page boundary)
A light, locked rectangle marking one A4 page. Use one per page and tile it with the page origin (`originX = k * (pageW + 80)`).
```json
{
  "type": "rectangle",
  "id": "page-1-guide",
  "x": 0,
  "y": 0,
  "width": 1123,
  "height": 794,
  "strokeColor": "#ced4da",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "roughness": 0,
  "opacity": 100,
  "roundness": null,
  "locked": true
}
```

## Full JSON Structure

The grid is always on (engineering diagrams). Lay elements out across one or more A4 pages at 96 DPI (`1123 x 794` landscape default, or `794 x 1123` portrait), tiled left to right with an 80px gutter: page `k` starts at `originX = k * (pageW + 80)`. See the Page Layout section in SKILL.md.

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    // Array of elements
  ],
  "appState": {
    "gridSize": 20,
    "gridStep": 5,
    "gridModeEnabled": true,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## Font Family Values

| Value | Font Name | Usage |
|-------|-----------|-------|
| 3 | Cascadia | Code / monospaced text |
| 6 | Nunito ("Nuno") | Regular text (default), size 20 (Medium) |
| 4 | Local Font (4th font) | Optional; JetBrains Mono in this vault. Obsidian only - does not render on excalidraw.com |
| 5 | Excalifont | Legacy hand-drawn; not used in engineering diagrams |
| 1 | Virgil | Legacy hand-drawn |
| 2 | Helvetica | Legacy sans |

## Fill Styles

- `solid` - Solid fill
- `hachure` - Hatched lines
- `cross-hatch` - Cross-hatched
- `dots` - Dotted pattern

## Roundness Types

- `{ "type": 1 }` - Sharp corners
- `{ "type": 2 }` - Slight rounding
- `{ "type": 3 }` - Full rounding (recommended)

## Element Binding

To connect text to a container:

```json
{
  "type": "rectangle",
  "id": "container-id",
  "boundElements": [{ "id": "text-id", "type": "text" }]
}
```

```json
{
  "type": "text",
  "id": "text-id",
  "containerId": "container-id"
}
```

## Arrow Binding

To connect arrows to shapes:

```json
{
  "type": "arrow",
  "startBinding": {
    "elementId": "source-shape-id",
    "focus": 0,
    "gap": 5
  },
  "endBinding": {
    "elementId": "target-shape-id",
    "focus": 0,
    "gap": 5
  }
}
```
