const WATCHES = [
  ["01_obsidian_chrono", "Obsidian Chronograph", "A dark instrument dial with three crisp timing registers and a signal-orange sweep."],
  ["02_alpine_explorer", "Alpine Explorer", "Field-watch clarity, compass cues, and contour lines drawn for the long way home."],
  ["03_solar_flare", "Solar Flare", "Radiant geometry in ember red and molten gold, centered on a miniature sun."],
  ["04_ocean_depth", "Ocean Depth", "A luminous dive face with strong minute marks, a date aperture, and deep-sea color."],
  ["05_ivory_sector", "Ivory Sector", "Warm paper tones and precise railway tracks give this sector dial a quiet authority."],
  ["06_cyber_grid", "Cyber Grid", "Electric cyan, a technical grid, and a digital complication meet analog motion."],
  ["07_lunar_phase", "Lunar Phase", "Roman numerals orbit a midnight dial and a golden crescent phase display."],
  ["08_copper_skeleton", "Copper Skeleton", "Open gear forms, copper structure, and a small-seconds register reveal the machine."],
  ["09_minimal_mono", "Minimal Mono", "Pure contrast and exact proportions reduce time to its most legible elements."],
  ["10_aurora_sport", "Aurora Sport", "Twin performance registers and an aurora arc give the collection its kinetic finale."]
];

const collection = document.querySelector("#collection");
const template = document.querySelector("#watchTemplate");
const liveHands = new Set();
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)");

function createWatch([slug, name, description], index) {
  const fragment = template.content.cloneNode(true);
  const card = fragment.querySelector(".watch-card");
  const base = `assets/watchfaces/${slug}`;
  const dial = fragment.querySelector(".dial");
  const complications = fragment.querySelector(".complications");
  const hands = fragment.querySelector(".hands");

  card.dataset.slug = slug;
  card.style.setProperty("--accent", "#ffffff");
  card.querySelector(".watch").setAttribute("aria-label", `${name}, animated live watchface`);
  card.querySelector(".index").textContent = String(index + 1).padStart(2, "0");
  card.querySelector("h2").textContent = name;
  card.querySelector(".description").textContent = description;
  dial.src = `${base}/dial.svg`;
  complications.src = `${base}/complications.svg`;
  hands.data = `${base}/hands.svg`;

  hands.addEventListener("load", () => {
    try {
      const groups = hands.contentDocument.querySelectorAll("svg > g > g[transform]");
      if (groups.length >= 3) {
        liveHands.add({ hour: groups[0], minute: groups[1], second: groups[2] });
        updateClocks();
      }
    } catch (error) {
      console.warn(`Could not animate ${name}`, error);
    }
  });

  fetch(`${base}/metadata.json`)
    .then(response => response.ok ? response.json() : Promise.reject(response.status))
    .then(meta => {
      card.style.setProperty("--accent", meta.palette.accent);
      const palette = card.querySelector(".palette");
      Object.values(meta.palette).slice(0, 5).forEach(color => {
        const swatch = document.createElement("span");
        swatch.className = "swatch";
        swatch.style.background = color;
        swatch.title = color;
        palette.append(swatch);
      });
    })
    .catch(() => {});

  return fragment;
}

WATCHES.forEach((watch, index) => collection.append(createWatch(watch, index)));

function updateClocks() {
  const now = new Date();
  const milliseconds = reduceMotion.matches ? 0 : now.getMilliseconds();
  const seconds = now.getSeconds() + milliseconds / 1000;
  const minutes = now.getMinutes() + seconds / 60;
  const hours = (now.getHours() % 12) + minutes / 60;
  const angles = {
    hour: hours * 30,
    minute: minutes * 6,
    second: seconds * 6
  };

  for (const hands of liveHands) {
    hands.hour.setAttribute("transform", `rotate(${angles.hour} 512 512)`);
    hands.minute.setAttribute("transform", `rotate(${angles.minute} 512 512)`);
    hands.second.setAttribute("transform", `rotate(${angles.second} 512 512)`);
  }

  document.querySelector("#digitalTime").textContent = now.toLocaleTimeString([], {
    hour12: false,
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit"
  });
  document.querySelector("#timeZone").textContent = Intl.DateTimeFormat().resolvedOptions().timeZone.replaceAll("_", " ");
}

function tick() {
  updateClocks();
  requestAnimationFrame(tick);
}

tick();
