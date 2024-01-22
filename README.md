# Show Angle and Distance and Italic Width
Glyphs app plugin that shows on the info panel the angle and distance between currently selected notes.
The angle and distance are simply calculated between the bottom left and top right corners of the selection rectangle. Upright is 0°, horizontal is 90°, and everything else falls in between (‘Italic angle’ kind of logic).

<img width="332" alt="image" src="https://github.com/slobzheninov/ShowAngle/assets/60325634/e8ef927b-efe2-4774-a1b9-4bd707b16070">


Jan 22, 2024 update:

Added an option to show Italic Width (𝑖↔︎) — horizontal distance between selected nodes adjusted for the italic angle of the layer. In other words, nodes located exactly above each other at the italic angle will show 0 Italic Width, which makes it easy to measure slanted stems and similar stuff.
You can switch between Italic Width and Distance by clicking on the panel when layer has an italic angle.

<img width="252" alt="image" src="https://github.com/slobzheninov/ShowAngle/assets/60325634/447ca851-8029-44b1-b5c8-60f04e2391ad">

Also, added an option to show Angle, Distance and Italic Width between the offcurve and the oncurve point, if you select 1 offcurve (“handle”). This shows the same as the above:

<img width="227" alt="image" src="https://github.com/slobzheninov/ShowAngle/assets/60325634/25e766a6-b333-4683-9fcd-5a64534a5f58">

Measuring italic stems now makes sense:

<img width="328" alt="image" src="https://github.com/slobzheninov/ShowAngle/assets/60325634/ee235345-09b2-4d89-83ea-8c1c86fca312">
