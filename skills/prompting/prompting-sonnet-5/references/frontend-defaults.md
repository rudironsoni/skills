# Sonnet 5 design and frontend defaults

On open-ended frontend and design briefs, Sonnet 5 may settle into a consistent default visual style. A default house style can read well for some briefs and feel off for dashboards, dev tools, fintech, healthcare, and enterprise apps.

The default is persistent: generic instructions ("don't use that color", "make it clean and minimal") shift the model to a different fixed palette rather than producing variety. Two approaches work reliably.

## 1. Specify a concrete alternative

The model follows explicit specs precisely. An example brief at the right level of concreteness:

```text
Design a desktop landing page for a supplement brand called AEFRM.

The visual direction should come from a cold monochrome atmosphere using pale silver-gray tones that gradually deepen into blue-gray and near-black, similar to a misted metallic surface.

The page should feel sharp and controlled, with a strong sense of structure and restraint.

Use this tonal system across the full page instead of introducing bright accent colors.

Use the uploaded image on the hero design in black and white.

The layout should be built with clear horizontal sections and a centered max-width container. Use 4px corner radius consistently across cards, buttons, inputs, and media frames. Margins should feel generous, with enough empty space around each section so the page breathes.

Typography should use a square, angular sans-serif with wider letter spacing than usual, especially in headings and navigation, so the text feels more engineered and less compressed. Headline text can be large and uppercase, while supporting copy remains short and sparse. The sub texts should be written with Alumni Sans SC in 4-6px like tiny little texts on corners bottom centre like that.

For the structure, start with a hero section containing a strong product statement, one short supporting paragraph, and a clean product placeholder or packshot frame. Below that, add a benefit grid with three or four blocks, then a formulation or ingredients section, and finally a cta.

Buttons should be flat and precise, with subtle hover changes using transition: all 160ms ease out where brightness and border contrast shift slightly rather than using dramatic motion.

Color palette should stay within this range:
#E9ECEC, #C9D2D4, #8C9A9E, #44545B, #11171B.
```

## 2. Propose options before building

This breaks the default and gives users control. Because `temperature` is not accepted on Sonnet 5, this is the recommended way to produce meaningfully different design directions across runs:

```text
Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface, plus a one-line rationale). Ask the user to pick one, then implement only that direction.
```

## Anti-slop directive

To steer away from generic "AI slop" patterns, add a short directive to the system prompt. Anthropic's frontend-design skill (in the claude-code repo's plugins) gives the fuller treatment; this snippet works well alongside the variety approaches above:

```text
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```
