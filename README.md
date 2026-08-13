# Watchface King

A single-page gallery of ten original, animated watchface concepts. All ten
faces display the viewer's current local time and move together in real time.

The site is plain HTML, CSS, and JavaScript. It has no dependencies and no build
step. Dial artwork is stored as editable SVG layers under `assets/watchfaces/`.

## Run locally

Browsers restrict scripting inside SVG files opened directly from `file://`, so
serve the directory over HTTP:

```sh
python3 -m http.server 4173
```

Then open <http://localhost:4173>.

## Deploy to Vercel

Import the GitHub repository into Vercel and deploy with the default static-site
settings. Leave the build command empty and set the output directory to `.` if
Vercel asks for one.
