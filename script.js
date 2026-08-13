const WATCHES = [
  ["01_regency_date", "Regency Date", "Fluted elegance, a jade sunburst dial, and a magnified date aperture."],
  ["02_meridian_gmt", "Meridian GMT", "A split 24-hour ring and independent travel pointer built for changing horizons."],
  ["03_veloce_chronograph", "Veloce Chronograph", "A crisp panda layout with three distinct registers and a scarlet timing hand."],
  ["04_monolith_tapisserie", "Monolith Tapisserie", "Steel architecture frames a deep blue geometric dial with exposed fasteners."],
  ["05_carbon_offshore", "Carbon Offshore", "Forged-carbon texture, oversized registers, and an electric yellow sweep."],
  ["06_openwork_bridges", "Openwork Bridges", "Rose-gold bridges cross an open mechanical field of wheels and jewel points."],
  ["07_geneva_96", "Geneva 96", "A warm ivory dress dial with applied indices and discreet small seconds."],
  ["08_horizon_sport", "Horizon Sport", "A porthole silhouette, horizontal dial relief, and an integrated-sport attitude."],
  ["09_celestial_perpetual", "Celestial Perpetual", "A midnight calendar composition orbiting a hand-finished moon display."],
  ["10_salmon_repeater", "Salmon Repeater", "A salmon sector dial with minute-track precision and a musical, old-world calm."]
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
