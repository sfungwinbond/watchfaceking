const FACES = [
  { slug: "pixel-01-ember-atlas", name: "Reference Replica", mode: "HYBRID", description: "A CV-measured redraw of the supplied face: rounded hours, health icons, inner seconds, and coral telemetry arcs.", metrics: ["heart", "steps", "temperature"] },
  { slug: "pixel-02-pulse-orbit", name: "Pulse Orbit", mode: "CARDIO", description: "Heart rate becomes the clock: one vivid orbit, one calm central readout.", metrics: ["heart", "activity", "recovery"] },
  { slug: "pixel-03-stride-grid", name: "Stride Grid", mode: "MOVE", description: "A bold typographic step counter with pace, distance, and daily progress.", metrics: ["steps", "distance", "activity"] },
  { slug: "pixel-04-recovery-field", name: "Recovery Field", mode: "RECOVER", description: "Recovery, sleep, and resting pulse arranged as a quiet readiness dashboard.", metrics: ["recovery", "sleep", "resting"] },
  { slug: "pixel-05-oxygen-bloom", name: "Oxygen Bloom", mode: "VITALS", description: "A radial oxygen study that turns a vital reading into a soft kinetic bloom.", metrics: ["oxygen", "heart", "temperature"] },
  { slug: "pixel-06-night-shift", name: "Night Shift", mode: "SLEEP", description: "A nocturnal face for sleep duration, recovery rhythm, and tomorrow's alarm.", metrics: ["sleep", "recovery", "resting"] },
  { slug: "pixel-07-summit-line", name: "Summit Line", mode: "OUTDOOR", description: "Elevation, temperature, and sunrise live inside a compact topographic dial.", metrics: ["elevation", "temperature", "steps"] },
  { slug: "pixel-08-tempo-zones", name: "Tempo Zones", mode: "TRAIN", description: "Training load and heart zones animate around a fast, legible time display.", metrics: ["heart", "activity", "calories"] },
  { slug: "pixel-09-vital-stack", name: "Vital Stack", mode: "OVERVIEW", description: "A dense but calm stack of the metrics that matter most right now.", metrics: ["heart", "steps", "oxygen", "recovery"] },
  { slug: "pixel-10-quiet-signal", name: "Quiet Signal", mode: "MINIMAL", description: "A restrained analog face with health signals tucked into four precise capsules.", metrics: ["heart", "steps", "oxygen", "sleep"] }
];

const METRIC_LABELS = {
  heart: "Heart rate", steps: "Steps", calories: "Calories", activity: "Active minutes",
  recovery: "Recovery", distance: "Distance", sleep: "Sleep", resting: "Resting heart",
  oxygen: "Blood oxygen", temperature: "Temperature", elevation: "Elevation"
};

const ASSET_VERSION = "cv-replica-3";

const faceGrid = document.querySelector("#faceGrid");
const template = document.querySelector("#faceTemplate");
const liveDocuments = new Set();

function createFace(face, index) {
  const fragment = template.content.cloneNode(true);
  const card = fragment.querySelector(".face-card");
  const object = fragment.querySelector(".watch-face");
  const metricList = fragment.querySelector(".metric-list");

  card.dataset.mode = face.mode;
  card.style.transitionDelay = `${Math.min(index * 55, 330)}ms`;
  card.querySelector(".face-number").textContent = String(index + 1).padStart(2, "0");
  card.querySelector(".face-mode").textContent = face.mode;
  card.querySelector("h3").textContent = face.name;
  card.querySelector(".face-description").textContent = face.description;
  object.data = `assets/watchfaces/${face.slug}/face.svg?v=${ASSET_VERSION}`;
  object.setAttribute("aria-label", `${face.name}, live demo watch face`);

  face.metrics.forEach(metric => {
    const item = document.createElement("li");
    item.textContent = METRIC_LABELS[metric];
    metricList.append(item);
  });

  object.addEventListener("load", () => {
    try {
      liveDocuments.add(object.contentDocument);
      updateLiveDemo();
    } catch (error) {
      console.warn(`Unable to activate ${face.name}`, error);
    }
  });

  return fragment;
}

FACES.forEach((face, index) => faceGrid.append(createFace(face, index)));

const heroFace = document.querySelector(".hero-live-face");
heroFace.addEventListener("load", () => {
  try {
    liveDocuments.add(heroFace.contentDocument);
    updateLiveDemo();
  } catch (error) {
    console.warn("Unable to activate hero replica", error);
  }
});

function getDemoValues(now = new Date()) {
  const elapsed = now.getTime() / 1000;
  const heart = Math.round(76 + Math.sin(elapsed / 7) * 4 + Math.sin(elapsed / 2.7) * 2);
  const steps = 8742 + Math.floor((elapsed % 3600) / 18);
  const recovery = Math.round(82 + Math.sin(elapsed / 29) * 2);
  const oxygen = Math.round(98 + Math.sin(elapsed / 17) * .55);
  const activity = 54 + Math.floor((elapsed % 300) / 60);
  const calories = 612 + Math.floor((elapsed % 600) / 75);
  const elevation = 1842 + Math.round(Math.sin(elapsed / 11) * 3);
  const outsideTemp = 80 + Math.round(Math.sin(elapsed / 19));
  const elevationGain = 15 + Math.round(Math.sin(elapsed / 8) * 2);
  const stress = 74 + Math.round(Math.sin(elapsed / 13) * 4);
  const ringSteps = 972 + Math.floor((elapsed % 900) / 3);
  const heartLow = heart + 6;
  const heartHigh = heart + 27;
  const date = now.toLocaleDateString(undefined, { month: "short", day: "numeric" }).toUpperCase();
  const day = now.toLocaleDateString(undefined, { weekday: "short" }).toUpperCase();
  const time = now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", hour12: false });
  const timeSeconds = now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false });
  const timeSeconds12 = now.toLocaleTimeString([], { hour: "numeric", minute: "2-digit", second: "2-digit", hour12: true }).toUpperCase();

  return {
    heart: String(heart), steps: steps.toLocaleString(), recovery: String(recovery), oxygen: `${oxygen}%`,
    activity: `${activity} MIN`, calories: String(calories), distance: "6.4 KM", sleep: "7H 42M",
    resting: "54 BPM", temperature: "+0.2°", elevation: elevation.toLocaleString(), date, day, time,
    time_seconds: timeSeconds, time_seconds_12: timeSeconds12,
    ring_heart: String(heart),
    outside_temp: `${outsideTemp}°`, outside_temp_value: String(outsideTemp),
    elevation_gain: `${elevationGain >= 0 ? "+" : ""}${elevationGain}`, elevation_gain_value: String(elevationGain),
    stress: String(stress), stress_value: String(stress),
    heart_range: `${heartLow}–${heartHigh}`, heart_range_value: String(heartHigh),
    ring_steps: ringSteps.toLocaleString(), temperature_face: "77°"
  };
}

function progressFor(metric, values) {
  const number = parseFloat(String(values[metric]).replace(/[^0-9.]/g, ""));
  const scales = {
    heart: [45, 150], steps: [0, 12000], recovery: [0, 100], oxygen: [90, 100], activity: [0, 90],
    outside_temp_value: [40, 110], elevation_gain_value: [0, 25],
    stress_value: [0, 100], heart_range_value: [40, 200], ring_heart: [40, 120], ring_steps: [0, 10000]
  };
  const [min, max] = scales[metric] || [0, 100];
  return Math.max(.04, Math.min(1, (number - min) / (max - min)));
}

function updateSvg(documentNode, now, values) {
  documentNode.querySelectorAll("[data-live]").forEach(node => {
    const metric = node.dataset.live;
    if (values[metric] !== undefined) node.textContent = values[metric];
  });

  const seconds = now.getSeconds() + now.getMilliseconds() / 1000;
  const minutes = now.getMinutes() + seconds / 60;
  const hours = (now.getHours() % 12) + minutes / 60;
  const rotations = { hour: hours * 30, minute: minutes * 6, second: seconds * 6 };
  documentNode.querySelectorAll("[data-hand]").forEach(node => {
    node.setAttribute("transform", `rotate(${rotations[node.dataset.hand]} 512 512)`);
  });

  documentNode.querySelectorAll("[data-progress]").forEach(node => {
    const circumference = Number(node.dataset.circumference);
    node.style.strokeDashoffset = String(circumference * (1 - progressFor(node.dataset.progress, values)));
    node.style.transition = "stroke-dashoffset 900ms cubic-bezier(.2,.8,.2,1)";
  });

  documentNode.querySelectorAll("[data-gauge]").forEach(node => {
    const fill = progressFor(node.dataset.gauge, values) * 100;
    node.style.strokeDasharray = `${fill.toFixed(1)} 100`;
    node.style.transition = "stroke-dasharray 900ms cubic-bezier(.2,.8,.2,1)";
  });
}

function updateLiveDemo() {
  const now = new Date();
  const values = getDemoValues(now);
  document.querySelectorAll("[data-demo]").forEach(node => {
    const value = values[node.dataset.demo];
    if (value !== undefined) node.textContent = value;
  });
  liveDocuments.forEach(documentNode => updateSvg(documentNode, now, values));
}

updateLiveDemo();
setInterval(updateLiveDemo, 1000);

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("is-visible");
      observer.unobserve(entry.target);
    }
  });
}, { rootMargin: "0px 0px -8%", threshold: .08 });

document.querySelectorAll(".face-card").forEach(card => observer.observe(card));

document.querySelectorAll(".filter").forEach(button => {
  button.addEventListener("click", () => {
    const selected = button.dataset.filter;
    document.querySelectorAll(".filter").forEach(item => {
      const active = item === button;
      item.classList.toggle("is-active", active);
      item.setAttribute("aria-pressed", String(active));
    });
    document.querySelectorAll(".face-card").forEach(card => {
      const visible = selected === "all" || card.dataset.mode === selected;
      card.classList.toggle("is-filtered", !visible);
    });
  });
});
