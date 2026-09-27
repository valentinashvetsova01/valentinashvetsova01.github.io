# Image prompts (Gemini)

Model: `gemini-3.1-flash-image` (Nano Banana 2) for everything; `gemini-3-pro-image` only if a key image
needs more realism after review.

**One visual language for every image:** realistic editorial still-life photography, soft natural
window light from the left, early morning, milky cream and powder-pink palette, gentle film softness,
low contrast, shallow depth of field, no harsh shadows, no saturated colours, no illustration.
The same peony, the same glass bottle, the same linen table in every scene, so the four stills read
as one flower opening over time.

Technique:
- **Scenes** (full-bleed interludes) are generated whole, 16:9, subject in the right third so text fits
  on the left. Stages 2–4 are generated **from stage 1 as a reference image** to keep the flower,
  bottle, table and light identical.
- **Cut-outs** (loader and the falling petal) are generated on flat chroma green `#00FF00` and keyed to
  transparent WebP.
- Everything is compressed to WebP (scenes ≤ 2400px wide, cut-outs ≤ 900px).

---

## Scenes: the peony interludes

### 1. `still-1-bud.webp` · chapter "the bud" (childhood, Berdsk)
Realistic editorial still-life photograph. A single pale pink peony with a tight, closed round bud,
on a long green stem with two leaves, standing in a small clear antique glass bottle on a table covered
with creamy natural linen. Soft early-morning window light from the left, a sheer white curtain
casting very faint diffused shadows across the linen. Milky cream and powder palette, low contrast,
gentle film softness, shallow depth of field, the background a softly blurred warm off-white wall.
The bottle and flower stand in the right third of the frame; the left two thirds are calm empty linen
and wall. Wide 16:9 landscape. No people, no text, no other objects.

### 2. `still-2-colour.webp` · chapter "the first crack" (olympiads, SUNC)
*(reference: image 1)* The exact same scene, camera, bottle, table and light. The peony bud is now
slightly looser: the green sepals have opened and soft pink colour is showing at the top of the bud,
the first petal edges just beginning to separate. Everything else identical.

### 3. `still-3-open.webp` · chapter "the decision" (leaving)
*(reference: image 2)* The exact same scene. The peony is now half open: the outer petals have
unfurled into a soft cup, the centre still tightly ruffled. The morning light is a little warmer
and brighter. Everything else identical.

### 4. `still-4-bloom.webp` · finale "And now?"
*(reference: image 3)* The exact same scene. The peony is in full, generous bloom, a lush ruffled
pale-pink head, the light now warm golden late-morning. One single petal has fallen and lies on the
linen beside the bottle. Everything else identical.

### 5. `still-suitcase.webp` · chapter "the decision" (alternative / second image)
Realistic editorial still-life photograph in the same light and palette as the peony series: a
half-packed vintage tan leather suitcase lying open on creamy linen, a folded cream cashmere scarf,
a small stack of papers with a passport-sized booklet on top (no readable text, no emblems), and one
half-open pale-pink peony laid across the scarf. Soft early-morning window light from the left,
sheer curtain, low contrast, film softness, shallow depth of field. Suitcase in the right half of the
frame, calm empty space on the left. Wide 16:9. No people, no text, no logos.

### 6. `linen.webp` · background texture (finale, Professional header)
Top-down realistic photograph of creamy natural linen fabric with soft, loose folds, lit by diffused
morning window light, faint shadow of a sheer curtain. Very bright, low contrast, milky off-white
with a hint of warm powder pink. Seamless-looking, no objects, no text. Wide 16:9.

---

## Cut-outs: on chroma green

### 7. `peony-bud.webp` · loader, frame 1
Realistic macro product photograph of a single pale pink peony bud, tightly closed, with a short piece
of stem and one small leaf, three-quarter view, soft diffused studio light from the upper left, fine
natural texture, the whole flower in frame with generous margin. Background: completely flat pure
chroma green (#00FF00), evenly lit, no gradient, no shadow on the background, no green reflections
or spill on the petals. No text.

### 8. `peony-half.webp` · loader, frame 2
*(reference: image 7)* The same peony, same angle, same stem and leaf, same light, now half open,
outer petals unfurled into a soft cup. Same flat chroma green background, no spill.

### 9. `peony-full.webp` · loader, frame 3 + small accent
*(reference: image 8)* The same peony, same angle, now in full ruffled bloom. Same flat chroma green
background, no spill.

### 10. `petals.webp` · the falling petal in the finale (cut into 3 files)
Three single loose pale-pink peony petals, realistic macro photograph, each petal curled slightly
differently and shown at a different angle, spaced far apart in a row with lots of empty space
between them, soft diffused light, delicate translucent texture. Background: completely flat pure
chroma green (#00FF00), evenly lit, no shadows on the background, no green spill. Wide landscape.
No text.

---

## Not generated
- Photos of Valentina: her own photos, only resized, gently colour-matched (a touch warmer, slightly
  lower saturation) and converted to WebP.
- Travels: her own photos later; the prototype uses Wikimedia Commons placeholders.
- Video (Veo): not needed; the loader and the falling petal are CSS animations over the images above.

Estimated cost: 10 images + ~10–15 retries ≈ 25 × ~$0.07 ≈ **$1.5–2**.

---

# v2 · Me tab redesign: stylised 3D objects (style test)

The realistic still life read as a "good morning" postcard. New direction: small stylised 3D objects
that float around the page like the keycaps on the Iris site, plus a looping animated flower.
Three style candidates, each shows the same three objects so they can be compared.

### 11. `style-clay.webp` · style A: soft matte clay
A stylish 3D render of three separate small objects floating in a row with lots of empty space between
them: a single peony flower, a six-pointed snowflake, and a single white piano key. Soft matte clay
material like a premium Blender claymation render, smooth rounded forms, subtle subsurface scattering,
palette of powder pink, milky cream and a touch of warm terracotta, soft diffused studio light from the
upper left, gentle soft shadows on the objects themselves, each object tilted at a different playful
angle, editorial and elegant, not childish, not cartoon. Background: completely flat pure chroma green
(#00FF00), evenly lit, no gradient, no shadows on the background, no green reflections. No text.

### 12. `style-glass.webp` · style B: frosted glass and chrome
A stylish 3D render of three separate small objects floating in a row with lots of empty space between
them: a single peony flower, a six-pointed snowflake, and a single piano key. Frosted translucent glass
with a soft pearlescent pink and cream iridescence, fine polished chrome details, luxurious and airy,
soft diffused studio light from the upper left, each object tilted at a different playful angle, high-end
fashion-campaign 3D, elegant, not childish. Background: completely flat pure chroma green (#00FF00),
evenly lit, no gradient, no shadows on the background, no green reflections or tint in the glass. No text.

### 13. `style-porcelain.webp` · style C: glossy porcelain with gold
A stylish 3D render of three separate small objects floating in a row with lots of empty space between
them: a single peony flower, a six-pointed snowflake, and a single piano key. Glossy white and blush-pink
porcelain with thin warm gold edges, smooth and refined like luxury ceramics, soft diffused studio light
from the upper left, delicate reflections, each object tilted at a different playful angle, elegant
editorial 3D, not childish, not cartoon. Background: completely flat pure chroma green (#00FF00), evenly
lit, no gradient, no shadows on the background, no green reflections. No text.


# v2 · the glass set (chosen style B)

All sheets share this style text:

> Stylish 3D render in one consistent style: frosted translucent glass with a soft pearlescent pink and cream iridescence and fine polished chrome details, luxurious and airy, soft diffused studio light from the upper left, high-end fashion-campaign 3D, elegant, not childish, not cartoon. Each object is tilted at a different playful angle. Background: completely flat pure chroma green (#00FF00), evenly lit, no gradient, no shadows on the background, no green reflections or green tint inside the glass.

### 14. `glass-a.webp` · cut into 3 files
A row of 3 separate small objects floating with lots of empty space between them: a treble clef, a ballroom dance shoe with a small heel, and a round olympiad medal on a short ribbon. Stylish 3D render in one consistent style: frosted translucent glass with a soft pearlescent pink and cream iridescence and fine polished chrome details, luxurious and airy, soft diffused studio light from the upper left, high-end fashion-campaign 3D, elegant, not childish, not cartoon. Each object is tilted at a different playful angle. Background: completely flat pure chroma green (#00FF00), evenly lit, no gradient, no shadows on the background, no green reflections or green tint inside the glass. No text other than what is printed on the keycaps.

### 15. `glass-b.webp` · cut into 3 files
A row of 3 separate small objects floating with lots of empty space between them: a chemistry flask with a little liquid inside, the mathematical symbol pi, and an integral sign. Stylish 3D render in one consistent style: frosted translucent glass with a soft pearlescent pink and cream iridescence and fine polished chrome details, luxurious and airy, soft diffused studio light from the upper left, high-end fashion-campaign 3D, elegant, not childish, not cartoon. Each object is tilted at a different playful angle. Background: completely flat pure chroma green (#00FF00), evenly lit, no gradient, no shadows on the background, no green reflections or green tint inside the glass. No text other than what is printed on the keycaps.

### 16. `glass-c.webp` · cut into 3 files
A row of 3 separate small objects floating with lots of empty space between them: a computer keycap printed with curly braces { }, a computer keycap printed with >_ , and a capital sigma symbol. Stylish 3D render in one consistent style: frosted translucent glass with a soft pearlescent pink and cream iridescence and fine polished chrome details, luxurious and airy, soft diffused studio light from the upper left, high-end fashion-campaign 3D, elegant, not childish, not cartoon. Each object is tilted at a different playful angle. Background: completely flat pure chroma green (#00FF00), evenly lit, no gradient, no shadows on the background, no green reflections or green tint inside the glass. No text other than what is printed on the keycaps.

### 17. `glass-d.webp` · cut into 3 files
A row of 3 separate small objects floating with lots of empty space between them: a small vintage suitcase, a paper airplane, and a closed umbrella. Stylish 3D render in one consistent style: frosted translucent glass with a soft pearlescent pink and cream iridescence and fine polished chrome details, luxurious and airy, soft diffused studio light from the upper left, high-end fashion-campaign 3D, elegant, not childish, not cartoon. Each object is tilted at a different playful angle. Background: completely flat pure chroma green (#00FF00), evenly lit, no gradient, no shadows on the background, no green reflections or green tint inside the glass. No text other than what is printed on the keycaps.

### 18. `glass-e.webp` · cut into 3 files
A row of 3 separate small objects floating with lots of empty space between them: an Italian moka coffee pot, a small espresso cup on a saucer, and a sun shape with soft rays. Stylish 3D render in one consistent style: frosted translucent glass with a soft pearlescent pink and cream iridescence and fine polished chrome details, luxurious and airy, soft diffused studio light from the upper left, high-end fashion-campaign 3D, elegant, not childish, not cartoon. Each object is tilted at a different playful angle. Background: completely flat pure chroma green (#00FF00), evenly lit, no gradient, no shadows on the background, no green reflections or green tint inside the glass. No text other than what is printed on the keycaps.

### 19. `glass-f.webp` · cut into 3 files
A row of 3 separate small objects floating with lots of empty space between them: a trophy cup, a laurel wreath, and a graduation cap with a tassel. Stylish 3D render in one consistent style: frosted translucent glass with a soft pearlescent pink and cream iridescence and fine polished chrome details, luxurious and airy, soft diffused studio light from the upper left, high-end fashion-campaign 3D, elegant, not childish, not cartoon. Each object is tilted at a different playful angle. Background: completely flat pure chroma green (#00FF00), evenly lit, no gradient, no shadows on the background, no green reflections or green tint inside the glass. No text other than what is printed on the keycaps.

### 20. `glass-g.webp` · cut into 3 files
A row of 3 separate small objects floating with lots of empty space between them: a small neural network made of glass spheres connected by thin chrome rods, a lightbulb, and a small open laptop. Stylish 3D render in one consistent style: frosted translucent glass with a soft pearlescent pink and cream iridescence and fine polished chrome details, luxurious and airy, soft diffused studio light from the upper left, high-end fashion-campaign 3D, elegant, not childish, not cartoon. Each object is tilted at a different playful angle. Background: completely flat pure chroma green (#00FF00), evenly lit, no gradient, no shadows on the background, no green reflections or green tint inside the glass. No text other than what is printed on the keycaps.

### 21. `glass-h.webp` · cut into 2 files
A row of 2 separate small objects floating with lots of empty space between them: the same pale pink peony shown at two stages: a tightly closed round bud, and a half-open flower. Stylish 3D render in one consistent style: frosted translucent glass with a soft pearlescent pink and cream iridescence and fine polished chrome details, luxurious and airy, soft diffused studio light from the upper left, high-end fashion-campaign 3D, elegant, not childish, not cartoon. Each object is tilted at a different playful angle. Background: completely flat pure chroma green (#00FF00), evenly lit, no gradient, no shadows on the background, no green reflections or green tint inside the glass. No text other than what is printed on the keycaps.

### 22. `glass-i.webp` · cut into 2 files (replaces the medal and the sigma)
A row of 2 separate small objects floating with lots of empty space between them: a round academic medal on a short ribbon engraved with a simple laurel branch and a small star (no rings, no logos, no letters), and a clean, correctly shaped capital Greek letter sigma, Σ, facing the viewer. Stylish 3D render in one consistent style: frosted translucent glass with a soft pearlescent pink and cream iridescence and fine polished chrome details, luxurious and airy, soft diffused studio light from the upper left, high-end fashion-campaign 3D, elegant, not childish, not cartoon. Each object is tilted at a different playful angle. Background: completely flat pure chroma green (#00FF00), evenly lit, no gradient, no shadows on the background, no green reflections or green tint inside the glass. No text.
