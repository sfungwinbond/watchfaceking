#!/usr/bin/env python3
"""Generate ten original, Pixel-inspired live health watch faces.

The artwork borrows the supplied reference's broad visual language—round black
glass, warm metal, compact white telemetry, and ember accents—without copying
logos or exact interface geometry. Every SVG exposes data-live, data-hand, and
data-progress hooks for the gallery demo.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "assets" / "watchfaces"
S = 1024
C = 512
STATUS = "#ff684f"

FACES = [
    dict(slug="pixel-01-ember-atlas", name="Reference Replica", mode="HYBRID", accent="#ff7358", bg="#050505", description="A CV-measured redraw with rounded hours, an open inner scale, and one glowing bright-orange telemetry band.", metrics=["heart", "steps", "temperature", "stress"]),
    dict(slug="pixel-02-pulse-orbit", name="Pulse Orbit", mode="CARDIO", accent="#ff4f6d", bg="#070507", description="Heart rate becomes the clock: one vivid orbit, one calm central readout.", metrics=["heart", "activity", "recovery"]),
    dict(slug="pixel-03-stride-grid", name="Stride Grid", mode="MOVE", accent="#ffb23f", bg="#080706", description="A bold typographic step counter with pace, distance, and daily progress.", metrics=["steps", "distance", "activity"]),
    dict(slug="pixel-04-recovery-field", name="Recovery Field", mode="RECOVER", accent="#b6f06b", bg="#060806", description="Recovery, sleep, and resting pulse arranged as a quiet readiness dashboard.", metrics=["recovery", "sleep", "resting"]),
    dict(slug="pixel-05-oxygen-bloom", name="Oxygen Bloom", mode="VITALS", accent="#63d9ff", bg="#040708", description="A radial oxygen study that turns a vital reading into a soft kinetic bloom.", metrics=["oxygen", "heart", "temperature"]),
    dict(slug="pixel-06-night-shift", name="Night Shift", mode="SLEEP", accent="#a88cff", bg="#050508", description="A nocturnal face for sleep duration, recovery rhythm, and tomorrow's alarm.", metrics=["sleep", "recovery", "resting"]),
    dict(slug="pixel-07-summit-line", name="Summit Line", mode="OUTDOOR", accent="#f18a52", bg="#080706", description="Elevation, temperature, and sunrise live inside a compact topographic dial.", metrics=["elevation", "temperature", "steps"]),
    dict(slug="pixel-08-tempo-zones", name="Tempo Zones", mode="TRAIN", accent="#ff5c48", bg="#070505", description="Training load and heart zones animate around a fast, legible time display.", metrics=["heart", "activity", "calories"]),
    dict(slug="pixel-09-vital-stack", name="Vital Stack", mode="OVERVIEW", accent="#f2eadf", bg="#060606", description="A dense but calm stack of the metrics that matter most right now.", metrics=["heart", "steps", "oxygen", "recovery"]),
    dict(slug="pixel-10-quiet-signal", name="Quiet Signal", mode="MINIMAL", accent="#ff765e", bg="#050505", description="A restrained analog face with health signals tucked into four precise capsules.", metrics=["heart", "steps", "oxygen", "sleep"]),
]


def polar(r: float, deg: float) -> tuple[float, float]:
    angle = math.radians(deg - 90)
    return C + r * math.cos(angle), C + r * math.sin(angle)


def dial_rotation(deg: float) -> float:
    """Return an upright tangent rotation for any position on the dial."""
    normalized = deg % 360
    if normalized <= 90:
        return normalized
    if normalized <= 270:
        return normalized - 180
    return normalized - 360


def svg_text(x: float, y: float, value: str, size: int, fill: str = "#f7f4ed", *,
             anchor: str = "middle", weight: int = 650, tracking: float = 0,
             live: str | None = None, opacity: float = 1) -> str:
    hook = f' data-live="{live}"' if live else ""
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" '
            f'font-family="Arial Rounded MT Bold,Nunito,Inter,Arial,sans-serif" font-size="{size}" font-weight="{weight}" '
            f'letter-spacing="{tracking}" opacity="{opacity}"{hook}>{value}</text>')


def line_markers(color: str = "#f7f4ed", every: int = 5, r1: int = 355, r2: int = 382) -> str:
    marks = []
    for i in range(60):
        deg = i * 6
        x1, y1 = polar(r1 if i % every == 0 else r2 - 10, deg)
        x2, y2 = polar(r2, deg)
        marks.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{8 if i % every == 0 else 3}" stroke-linecap="round" opacity="{1 if i % every == 0 else .55}"/>')
    return "".join(marks)


def progress_ring(metric: str, r: int, color: str, width: int = 18, dash: str = "") -> str:
    circumference = 2 * math.pi * r
    dash_attr = f' stroke-dasharray="{dash}"' if dash else f' stroke-dasharray="{circumference:.2f}"'
    return (f'<circle cx="512" cy="512" r="{r}" fill="none" stroke="{STATUS}" stroke-width="{width}" '
            f'stroke-linecap="round" transform="rotate(-90 512 512)"{dash_attr} '
            f'data-progress="{metric}" data-circumference="{circumference:.2f}"/>')


def pill(x: int, y: int, w: int, label: str, value: str, metric: str, accent: str) -> str:
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="92" rx="46" fill="#171513" opacity=".98"/>'
            f'{svg_text(x + 34, y + 37, label, 18, "#a7a39b", anchor="start", weight=700, tracking=1.4)}'
            f'{svg_text(x + w - 32, y + 62, value, 35, STATUS, anchor="end", weight=750, live=metric)}</g>')


def round_numerals(r: int = 336, color: str = "#f7f4ed", size: int = 28) -> str:
    return "".join(
        svg_text(*polar(r, deg), str(12 if deg == 0 else deg // 30), size, color, weight=700)
        for deg in range(0, 360, 30)
    )


def analog_hands(accent: str) -> str:
    return f'''<g>
      <g data-hand="hour" transform="rotate(300 512 512)"><path d="M492 534 L500 325 Q512 298 524 325 L532 534Z" fill="#f7f4ed"/></g>
      <g data-hand="minute" transform="rotate(55 512 512)"><path d="M500 538 L504 192 Q512 166 520 192 L524 538Z" fill="#f7f4ed"/></g>
      <g data-hand="second" transform="rotate(210 512 512)"><line x1="512" y1="584" x2="512" y2="155" stroke="{accent}" stroke-width="6" stroke-linecap="round"/></g>
      <circle cx="512" cy="512" r="24" fill="{accent}"/><circle cx="512" cy="512" r="8" fill="#111"/>
    </g>'''


def status_gauge(start: float, end: float, metric: str, fill: float, color: str, width: int = 22, radius: int = 400) -> str:
    x1, y1 = polar(radius, start)
    x2, y2 = polar(radius, end)
    large = 1 if (end - start) % 360 > 180 else 0
    path = f'M{x1:.1f} {y1:.1f} A{radius} {radius} 0 {large} 1 {x2:.1f} {y2:.1f}'
    return (
        f'<path d="{path}" fill="none" stroke="#3a302b" stroke-width="{width}" stroke-linecap="round" opacity=".78"/>'
        f'<path d="{path}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" pathLength="100" '
        f'stroke-dasharray="{fill:.1f} 100" data-gauge="{metric}" filter="url(#meter-glow)"/>'
    )


def band_text(value: str, radius: int, deg: float, size: int, color: str, live: str | None = None) -> str:
    x, y = polar(radius, deg)
    rotation = dial_rotation(deg)
    hook = f' data-live="{live}"' if live else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" dominant-baseline="middle" fill="{color}" '
        f'font-family="Arial Rounded MT Bold,Nunito,Arial,sans-serif" font-size="{size}" font-weight="800" '
        f'transform="rotate({rotation:.1f} {x:.1f} {y:.1f})"{hook}>{value}</text>'
    )


def arc_text(identifier: str, value: str, radius: int, start: float, end: float, size: int, color: str) -> str:
    """Set a short label on the dial curve while keeping the lower half upright."""
    midpoint = (start + end) / 2 % 360
    if 90 < midpoint < 270:
        x1, y1 = polar(radius, end)
        x2, y2 = polar(radius, start)
        sweep = 0
    else:
        x1, y1 = polar(radius, start)
        x2, y2 = polar(radius, end)
        sweep = 1
    path = f'M{x1:.1f} {y1:.1f} A{radius} {radius} 0 0 {sweep} {x2:.1f} {y2:.1f}'
    return (
        f'<defs><path id="{identifier}" d="{path}"/></defs>'
        f'<text fill="{color}" font-family="Arial Rounded MT Bold,Nunito,Arial,sans-serif" '
        f'font-size="{size}" font-weight="800" letter-spacing="1.1">'
        f'<textPath href="#{identifier}" startOffset="50%" text-anchor="middle">{value}</textPath></text>'
    )


def heart_icon(x: int, y: int, scale: float = 1, color: str = STATUS) -> str:
    return f'<path d="M0 8 C-15-6-31 8-24 24 C-18 36 0 46 0 46 C0 46 18 36 24 24 C31 8 15-6 0 8Z" fill="{color}" transform="translate({x} {y}) scale({scale})"/>'


def step_icon(x: int, y: int, scale: float = 1, color: str = STATUS) -> str:
    return f'<g transform="translate({x} {y}) rotate(-32) scale({scale})" fill="{color}"><ellipse cx="-7" cy="-7" rx="9" ry="18"/><ellipse cx="9" cy="10" rx="8" ry="16"/></g>'


def thermometer_icon(x: float, y: float, scale: float = 1, color: str = STATUS) -> str:
    return f'<g transform="translate({x:.1f} {y:.1f}) scale({scale})" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round"><path d="M0-25 V12"/><circle cy="22" r="12" fill="{color}"/><path d="M0-25 A8 8 0 0 1 8-17 V12"/></g>'


def bolt_icon(x: float, y: float, scale: float = 1, color: str = STATUS) -> str:
    return f'<path d="M6-27 L-18 6 H-3 L-9 29 L19-8 H4Z" transform="translate({x:.1f} {y:.1f}) scale({scale})" fill="{color}"/>'


def ring_icon_badge(markup: str, x: float, y: float, deg: float, color: str) -> str:
    """Seat an upright icon directly into the outer gauge track."""
    rotation = dial_rotation(deg)
    delay = -((deg % 360) / 360) * .84
    return (
        f'<g data-ring-icon="true" filter="url(#icon-glow)" style="animation-delay:{delay:.2f}s">'
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="34" fill="#070606" stroke="#241b18" stroke-width="6"/>'
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="29" fill="#070606" stroke="{color}" stroke-width="4" opacity=".98"/>'
        f'<g transform="rotate({rotation:.1f} {x:.1f} {y:.1f})">{markup}</g>'
        '</g>'
    )


def face_ember(t: dict) -> str:
    accent = t["accent"]
    pale, rust, bright = "#f4e8df", "#e24624", "#ff5a36"
    telemetry_band = (
        '<defs>'
        '<filter id="meter-glow" x="-25%" y="-25%" width="150%" height="150%">'
        '<feGaussianBlur stdDeviation="4.5" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>'
        '</filter>'
        '<filter id="icon-glow" x="-80%" y="-80%" width="260%" height="260%">'
        '<feGaussianBlur stdDeviation="8" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>'
        '</filter>'
        '</defs>'
        '<style>'
        '[data-ring-icon]{animation:icon-flash .84s ease-in-out infinite;transform-box:fill-box;transform-origin:center}'
        '[data-gauge]{animation:meter-flash .84s steps(2,end) infinite}'
        '@keyframes icon-flash{0%,38%,100%{opacity:.58;transform:scale(.96)}50%,62%{opacity:1;transform:scale(1.12)}}'
        '@keyframes meter-flash{0%,100%{stroke-opacity:.72}50%{stroke-opacity:1}}'
        '</style>'
        '<circle cx="512" cy="512" r="382" fill="none" stroke="#120f0e" stroke-width="120"/>'
        '<circle cx="512" cy="512" r="321" fill="none" stroke="#332722" stroke-width="3" opacity=".9"/>'
        '<circle cx="512" cy="512" r="443" fill="none" stroke="#332722" stroke-width="3" opacity=".9"/>'
    )
    gauges = "".join([
        status_gauge(230, 310, "outside_temp_value", 57, bright, width=112, radius=382),
        status_gauge(320, 400, "ring_heart", 48, accent, width=112, radius=382),
        status_gauge(50, 130, "stress_value", 74, rust, width=112, radius=382),
        status_gauge(140, 220, "ring_steps", 86, bright, width=112, radius=382),
    ])

    inner_ticks_parts = []
    for d in range(0, 360, 6):
        # Keep a clean 108° window at twelve o'clock for the three-line readout.
        if d <= 54 or d >= 306:
            continue
        x1, y1 = polar(164 if d % 30 == 0 else 174, d)
        x2, y2 = polar(190, d)
        inner_ticks_parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="#797671" stroke-width="{6 if d % 30 == 0 else 4}" stroke-linecap="round" '
            f'opacity="{.92 if d % 30 == 0 else .72}" data-inner-tick="true"/>'
        )
    inner_ticks = "".join(inner_ticks_parts)
    inner_values = "".join(
        svg_text(*polar(142, deg), value, 21, "#d8d4cd", weight=700)
        for deg, value in [(90, "20"), (135, "25"), (180, "30"), (225, "35"), (270, "40")]
    )

    temp_icon_xy = polar(406, 255)
    heart_xy = polar(406, 345)
    stress_xy = polar(406, 75)
    steps_xy = polar(406, 165)
    complications = (
        arc_text("label-temp", "TEMP · 60–85°F", 365, 238, 302, 18, pale)
        + ring_icon_badge(thermometer_icon(*temp_icon_xy, .62, bright), *temp_icon_xy, 255, bright)
        + band_text("80°", 408, 285, 34, pale, "outside_temp")
        + arc_text("label-heart", "HEART · 60–100", 365, 328, 392, 18, pale)
        + ring_icon_badge(heart_icon(int(heart_xy[0]), int(heart_xy[1] - 10), .52, accent), *heart_xy, 345, accent)
        + band_text("78", 408, 15, 34, pale, "heart")
        + arc_text("label-stress", "STRESS · 0–40", 365, 58, 122, 18, pale)
        + ring_icon_badge(bolt_icon(*stress_xy, .60, bright), *stress_xy, 75, bright)
        + band_text("74", 408, 105, 34, pale, "stress")
        + arc_text("label-steps", "STEPS · 8–10K", 365, 148, 212, 18, pale)
        + ring_icon_badge(step_icon(int(steps_xy[0]), int(steps_xy[1]), .54, bright), *steps_xy, 165, bright)
        + band_text("8,600", 408, 195, 28, pale, "ring_steps")
    )

    center_readout = (
        svg_text(512, 331, "AUG 20", 34, bright, live="date", tracking=2)
        + svg_text(512, 380, "10:10:30 PM", 32, bright, live="time_seconds_12", tracking=.8)
        + svg_text(512, 425, "77°", 32, bright, live="temperature_face")
    )
    return telemetry_band + gauges + complications + line_markers(r1=294, r2=320) + round_numerals(258, pale, 28) + inner_ticks + inner_values + center_readout + analog_hands(bright)


def face_pulse(t: dict) -> str:
    a = t["accent"]
    bars = "".join(f'<rect x="{255+i*26}" y="{705-(i%5)*12}" width="12" height="{38+(i%5)*12}" rx="6" fill="{a}" opacity="{.25+i*.025}"/>' for i in range(20))
    return progress_ring("heart", 345, a, 28) + progress_ring("activity", 300, "#ffb447", 10) + svg_text(512, 307, "LIVE HEART", 22, "#aaa59d", tracking=4) + svg_text(512, 510, "78", 190, "#fff", live="heart", weight=500) + svg_text(512, 572, "BPM", 28, a, tracking=5) + svg_text(512, 653, "10:09", 48, "#fff", live="time") + bars


def face_stride(t: dict) -> str:
    a = t["accent"]
    grid = "".join(f'<line x1="{x}" y1="210" x2="{x}" y2="790" stroke="#fff" opacity=".035"/>' for x in range(250, 801, 50)) + "".join(f'<line x1="210" y1="{y}" x2="814" y2="{y}" stroke="#fff" opacity=".035"/>' for y in range(250, 801, 50))
    return grid + svg_text(226, 270, "TODAY / MOVE", 20, a, anchor="start", tracking=3) + svg_text(226, 420, "8,742", 126, live="steps", anchor="start", weight=600) + svg_text(226, 468, "STEPS", 24, "#99958e", anchor="start", tracking=5) + progress_ring("activity", 350, a, 18, "48 18") + pill(222, 595, 580, "DISTANCE", "6.4 KM", "distance", a) + pill(222, 704, 580, "ACTIVE", "54 MIN", "activity", a) + svg_text(798, 270, "10:09", 28, "#fff", anchor="end", live="time")


def face_recovery(t: dict) -> str:
    a = t["accent"]
    waves = "".join(f'<path d="M220 {660+i*20} Q340 {615+i*14} 455 {660+i*8} T805 {635+i*12}" fill="none" stroke="{a}" stroke-width="3" opacity="{.18+i*.06}"/>' for i in range(6))
    return progress_ring("recovery", 342, a, 24) + svg_text(512, 282, "RECOVERY", 22, "#9da097", tracking=5) + svg_text(512, 505, "82", 182, a, live="recovery", weight=520) + svg_text(512, 555, "READY", 26, "#fff", tracking=6) + waves + pill(245, 690, 250, "SLEEP", "7H 42M", "sleep", a) + pill(529, 690, 250, "REST", "54 BPM", "resting", a)


def face_oxygen(t: dict) -> str:
    a = t["accent"]
    petals = []
    for i in range(36):
        x, y = polar(320 + 22 * math.sin(i * .8), i * 10)
        petals.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{7 + i % 4}" fill="{a}" opacity="{.25 + (i % 6)*.1}"/>')
    return "".join(petals) + progress_ring("oxygen", 278, a, 10) + svg_text(512, 325, "BLOOD OXYGEN", 20, "#989da0", tracking=4) + svg_text(512, 508, "98%", 150, "#fff", live="oxygen", weight=520) + svg_text(512, 570, "STEADY", 24, a, tracking=5) + pill(252, 680, 240, "PULSE", "78", "heart", a) + pill(532, 680, 240, "SKIN", "+0.2°", "temperature", a) + svg_text(512, 800, "10:09", 32, "#fff", live="time")


def face_sleep(t: dict) -> str:
    a = t["accent"]
    timeline = "".join(f'<rect x="{220+i*24}" y="{620-(i%4)*18}" width="16" height="{45+(i%4)*18}" rx="8" fill="{a}" opacity="{.22+(i%5)*.12}"/>' for i in range(25))
    stars = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".4"/>' for x, y, r in [(230,270,3),(740,255,4),(790,390,2),(286,430,3),(685,480,3)])
    return stars + svg_text(512, 315, "10:09", 122, "#fff", live="time", weight=450) + svg_text(512, 365, "THU / NIGHT MODE", 20, a, live="day", tracking=3) + svg_text(230, 520, "7H 42M", 64, a, live="sleep", anchor="start") + svg_text(230, 558, "LAST NIGHT", 18, "#96919e", anchor="start", tracking=4) + timeline + pill(252, 724, 240, "RECOVERY", "82", "recovery", a) + pill(532, 724, 240, "REST", "54", "resting", a)


def face_summit(t: dict) -> str:
    a = t["accent"]
    contours = "".join(f'<ellipse cx="512" cy="565" rx="{110+i*38}" ry="{55+i*22}" fill="none" stroke="{a}" stroke-width="3" opacity="{.1+i*.055}" transform="rotate({i*7-18} 512 565)"/>' for i in range(7))
    return contours + svg_text(218, 274, "SUMMIT LINE", 20, a, anchor="start", tracking=4) + svg_text(806, 274, "10:09", 28, "#fff", anchor="end", live="time") + svg_text(512, 440, "1,842", 118, "#fff", live="elevation", weight=550) + svg_text(512, 485, "METERS", 21, "#aaa39d", tracking=6) + pill(220, 680, 275, "TEMP", "18°", "temperature", a) + pill(529, 680, 275, "STEPS", "8,742", "steps", a) + svg_text(512, 820, "SUNSET 7:48 PM", 18, "#b4aca5", tracking=3)


def face_tempo(t: dict) -> str:
    a = t["accent"]
    zone_colors = ["#5b9cff", "#63d9a4", "#f5d55c", "#ff9a4c", a]
    zones = "".join(f'<path d="M {polar(350-i*27, 215)[0]:.1f} {polar(350-i*27, 215)[1]:.1f} A {350-i*27} {350-i*27} 0 0 1 {polar(350-i*27, 505)[0]:.1f} {polar(350-i*27, 505)[1]:.1f}" fill="none" stroke="{c}" stroke-width="18" stroke-linecap="round" opacity="{.38+i*.12}"/>' for i, c in enumerate(zone_colors))
    return zones + svg_text(512, 300, "TEMPO / ZONE 3", 21, a, tracking=4) + svg_text(512, 490, "142", 166, "#fff", live="heart", weight=520) + svg_text(512, 540, "BPM", 24, a, tracking=5) + svg_text(512, 624, "10:09", 48, "#fff", live="time") + pill(250, 700, 252, "LOAD", "54 MIN", "activity", a) + pill(522, 700, 252, "BURN", "612", "calories", a)


def face_stack(t: dict) -> str:
    a = t["accent"]
    rows = [("HEART", "78", "heart", "BPM"), ("STEPS", "8,742", "steps", "TODAY"), ("OXYGEN", "98%", "oxygen", "SPO₂"), ("READY", "82", "recovery", "SCORE")]
    body = svg_text(216, 244, "10:09", 76, "#fff", anchor="start", live="time", weight=520) + svg_text(808, 230, "THU", 20, "#aaa6a0", anchor="end", live="day", tracking=3)
    for i, (label, value, metric, unit) in enumerate(rows):
        y = 330 + i * 125
        body += f'<line x1="216" y1="{y+86}" x2="808" y2="{y+86}" stroke="#fff" opacity=".09"/>' + svg_text(216, y+35, label, 18, "#8f8c87", anchor="start", tracking=3) + svg_text(808, y+54, value, 60, a if i == 0 else "#f4f1eb", anchor="end", live=metric, weight=560) + svg_text(216, y+70, unit, 16, "#625f5b", anchor="start", tracking=2)
    return body


def face_quiet(t: dict) -> str:
    a = t["accent"]
    numerals = round_numerals(332, "#e8e4dd", 28)
    return line_markers("#d9d5ce", r1=370, r2=385) + numerals + analog_hands(a) + svg_text(512, 328, "THU 20", 18, a, live="date", tracking=3) + pill(235, 706, 255, "HEART", "78", "heart", a) + pill(534, 706, 255, "STEPS", "8,742", "steps", a) + svg_text(280, 843, "98% O₂", 18, "#aaa6a0", live="oxygen") + svg_text(744, 843, "7H 42M", 18, "#aaa6a0", live="sleep")


DRAWERS = [face_ember, face_pulse, face_stride, face_recovery, face_oxygen, face_sleep, face_summit, face_tempo, face_stack, face_quiet]


def document(t: dict, content: str) -> str:
    a, bg = t["accent"], t["bg"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024" role="img" aria-label="{t['name']} live health watch face">
  <defs>
    <radialGradient id="case" cx="36%" cy="27%" r="78%"><stop stop-color="#ece5db"/><stop offset=".24" stop-color="#8e877f"/><stop offset=".55" stop-color="#302e2c"/><stop offset=".82" stop-color="#a59e94"/><stop offset="1" stop-color="#2b2927"/></radialGradient>
    <radialGradient id="glass" cx="36%" cy="24%" r="78%"><stop stop-color="#24211f"/><stop offset=".34" stop-color="{bg}"/><stop offset="1" stop-color="#000"/></radialGradient>
    <linearGradient id="glint" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fff" stop-opacity=".18"/><stop offset=".32" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="{a}" stop-opacity=".04"/></linearGradient>
    <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="24" stdDeviation="28" flood-color="#000" flood-opacity=".62"/></filter>
    <clipPath id="dialClip"><circle cx="512" cy="512" r="420"/></clipPath>
  </defs>
  <circle cx="512" cy="512" r="482" fill="url(#case)" filter="url(#shadow)"/>
  <circle cx="512" cy="512" r="435" fill="#080706" stroke="#181716" stroke-width="8"/>
  <circle cx="512" cy="512" r="420" fill="url(#glass)"/>
  <g clip-path="url(#dialClip)">{content}</g>
  <circle cx="512" cy="512" r="420" fill="url(#glint)" pointer-events="none"/>
  <path d="M207 329 A350 350 0 0 1 418 174" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".12"/>
</svg>\n'''


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    catalog = []
    for t, drawer in zip(FACES, DRAWERS):
        folder = ROOT / t["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        face = document(t, drawer(t))
        (folder / "face.svg").write_text(face, encoding="utf-8")
        originality = (
            "Faithful unbranded redraw of the user-supplied reference face, measured after CV ellipse rectification."
            if t["slug"] == "pixel-01-ember-atlas"
            else "Original unbranded artwork informed by the supplied round-watch reference; no logos or exact UI replicas."
        )
        metadata = {**t, "canvas": [S, S], "liveDemo": True, "originality": originality}
        (folder / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        catalog.append(metadata)
    (ROOT / "pixel-catalog.json").write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(catalog)} Pixel-inspired live health faces")


if __name__ == "__main__":
    main()
