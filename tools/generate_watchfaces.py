#!/usr/bin/env python3
"""Generate ten original luxury-inspired layered SVG watchfaces.

The collection references broad Swiss watchmaking design languages without
using brand names, logos, signatures, or exact model geometry.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "assets" / "watchfaces"
S = 1024
C = 512

WATCHES = [
    dict(slug="01_regency_date", name="Regency Date", family="Crown Sport", note="Fluted elegance, a jade sunburst dial, and a magnified date aperture.", bg="#12352b", bg2="#071914", fg="#f7f1dc", metal="#d9c997", accent="#d6b85a", lume="#eefbd3", shape="round", pattern="sunburst", markers="baton", comp="date", hands="faceted", second="needle"),
    dict(slug="02_meridian_gmt", name="Meridian GMT", family="Crown Sport", note="A split 24-hour ring and independent travel pointer built for changing horizons.", bg="#111419", bg2="#030405", fg="#f5f2e9", metal="#b9c1c8", accent="#e7463c", lume="#bfffd7", shape="round", pattern="matte", markers="round", comp="gmt", hands="orb", second="bolt"),
    dict(slug="03_veloce_chronograph", name="Veloce Chronograph", family="Crown Sport", note="A crisp panda layout with three distinct registers and a scarlet timing hand.", bg="#e8e4d9", bg2="#faf8f1", fg="#181b20", metal="#c6c9ca", accent="#e0453a", lume="#fffbd7", shape="round", pattern="rings", markers="baton", comp="chrono", hands="faceted", second="diamond"),
    dict(slug="04_monolith_tapisserie", name="Monolith Tapisserie", family="Octagonal Atelier", note="Steel architecture frames a deep blue geometric dial with exposed fasteners.", bg="#142b4a", bg2="#071425", fg="#edf4f7", metal="#aeb9c4", accent="#66b7d7", lume="#d9fff2", shape="octagon", pattern="tapisserie", markers="baton", comp="date", hands="architect", second="open"),
    dict(slug="05_carbon_offshore", name="Carbon Offshore", family="Octagonal Atelier", note="Forged-carbon texture, oversized registers, and an electric yellow sweep.", bg="#111315", bg2="#050607", fg="#f5f5ef", metal="#4e5358", accent="#e9ff3f", lume="#f6ffd2", shape="octagon", pattern="carbon", markers="block", comp="offshore", hands="paddle", second="counter"),
    dict(slug="06_openwork_bridges", name="Openwork Bridges", family="Octagonal Atelier", note="Rose-gold bridges cross an open mechanical field of wheels and jewel points.", bg="#251713", bg2="#080706", fg="#f4d5b7", metal="#ba714c", accent="#ef9b68", lume="#ffe7c6", shape="octagon", pattern="openwork", markers="minimal", comp="tourbillon", hands="skeleton", second="crescent"),
    dict(slug="07_geneva_96", name="Geneva 96", family="Genevan Classics", note="A warm ivory dress dial with applied indices and discreet small seconds.", bg="#eee6d2", bg2="#fffdf6", fg="#2a2926", metal="#cdb77d", accent="#8f2e38", lume="#fff8df", shape="round", pattern="silk", markers="applied", comp="small_seconds", hands="dauphine", second="leaf"),
    dict(slug="08_horizon_sport", name="Horizon Sport", family="Genevan Classics", note="A porthole silhouette, horizontal dial relief, and an integrated-sport attitude.", bg="#29485b", bg2="#0e2533", fg="#eff8f7", metal="#aebbc2", accent="#65d3c9", lume="#ddfff5", shape="porthole", pattern="horizon", markers="applied", comp="date", hands="baton", second="spear"),
    dict(slug="09_celestial_perpetual", name="Celestial Perpetual", family="Genevan Classics", note="A midnight calendar composition orbiting a hand-finished moon display.", bg="#111d3b", bg2="#050a18", fg="#f3e8c5", metal="#d1bc78", accent="#e0bd58", lume="#fff5c9", shape="round", pattern="stars", markers="roman", comp="perpetual", hands="leaf", second="star"),
    dict(slug="10_salmon_repeater", name="Salmon Repeater", family="Genevan Classics", note="A salmon sector dial with minute-track precision and a musical, old-world calm.", bg="#c88970", bg2="#f1baa0", fg="#28211e", metal="#c8bfae", accent="#723a36", lume="#fff0d2", shape="round", pattern="sector", markers="arabic", comp="reserve", hands="breguet", second="drop"),
]


def polar(r: float, deg: float) -> tuple[float, float]:
    a = math.radians(deg - 90)
    return C + r * math.cos(a), C + r * math.sin(a)


def line(deg: float, r1: float, r2: float, color: str, width: float, opacity: float = 1) -> str:
    x1, y1 = polar(r1, deg); x2, y2 = polar(r2, deg)
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{width}" opacity="{opacity}" stroke-linecap="round"/>'


def txt(value: str, r: float, deg: float, size: int, color: str, family: str = "Arial", weight: int = 600) -> str:
    x, y = polar(r, deg)
    return f'<text x="{x:.1f}" y="{y + size*.34:.1f}" text-anchor="middle" font-family="{family},sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{value}</text>'


def defs(t: dict) -> str:
    return f'''<defs>
      <radialGradient id="dial" cx="38%" cy="31%" r="74%"><stop stop-color="{t['bg2']}"/><stop offset=".55" stop-color="{t['bg']}"/><stop offset="1" stop-color="{t['bg2']}"/></radialGradient>
      <linearGradient id="steel" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f8fafb"/><stop offset=".25" stop-color="{t['metal']}"/><stop offset=".52" stop-color="#535961"/><stop offset=".75" stop-color="{t['metal']}"/><stop offset="1" stop-color="#f7f8f6"/></linearGradient>
      <linearGradient id="hand" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{t['fg']}"/><stop offset=".48" stop-color="{t['metal']}"/><stop offset=".52" stop-color="#fff"/><stop offset="1" stop-color="{t['fg']}"/></linearGradient>
      <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#000" flood-opacity=".5"/></filter>
      <filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5"/></filter>
    </defs>'''


def doc(t: dict, body: str, label: str) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024" role="img" aria-label="{label}">{defs(t)}{body}</svg>\n'


def case(t: dict) -> str:
    if t["shape"] == "octagon":
        points = "512,34 844,172 982,512 844,852 512,990 180,852 42,512 180,172"
        inner = "512,75 814,200 939,512 814,824 512,949 210,824 85,512 210,200"
        screws = "".join(f'<circle cx="{polar(430,d)[0]:.1f}" cy="{polar(430,d)[1]:.1f}" r="14" fill="{t["bg2"]}" stroke="#e8ecee" stroke-width="5"/><line x1="{polar(430,d)[0]-7:.1f}" y1="{polar(430,d)[1]:.1f}" x2="{polar(430,d)[0]+7:.1f}" y2="{polar(430,d)[1]:.1f}" stroke="#aab1b5" stroke-width="3"/>' for d in range(0,360,45))
        return f'<polygon points="{points}" fill="url(#steel)" filter="url(#shadow)"/><polygon points="{inner}" fill="url(#dial)" stroke="{t["metal"]}" stroke-width="8"/>{screws}'
    if t["shape"] == "porthole":
        return f'<rect x="54" y="126" width="916" height="772" rx="286" fill="url(#steel)" filter="url(#shadow)"/><rect x="92" y="158" width="840" height="708" rx="250" fill="url(#dial)" stroke="{t["metal"]}" stroke-width="9"/>'
    flutes = "".join(line(d, 438, 477, "#f2f1eb", 8, .68) for d in range(0, 360, 6)) if t["family"] == "Crown Sport" else ""
    return f'<circle cx="512" cy="512" r="482" fill="url(#steel)" filter="url(#shadow)"/>{flutes}<circle cx="512" cy="512" r="438" fill="url(#dial)" stroke="{t["metal"]}" stroke-width="8"/>'


def texture(t: dict) -> str:
    p = t["pattern"]
    if p == "sunburst": return "".join(line(d, 70, 418, t["accent"], 3, .16) for d in range(0,360,6))
    if p == "rings": return "".join(f'<circle cx="512" cy="512" r="{r}" fill="none" stroke="{t["fg"]}" stroke-width="1" opacity=".12"/>' for r in range(100,420,14))
    if p == "tapisserie": return "".join(f'<rect x="{x}" y="{y}" width="34" height="34" rx="3" fill="none" stroke="{t["accent"]}" stroke-width="2" opacity=".22"/>' for x in range(220,805,42) for y in range(220,805,42) if (x-C)**2+(y-C)**2 < 345**2)
    if p == "carbon": return "".join(f'<path d="M{x} {y} l34 -18 34 18 -34 18z" fill="{t["metal"]}" opacity="{.10 if (x+y)//60%2 else .18}"/>' for x in range(190,820,70) for y in range(190,820,40) if (x-C)**2+(y-C)**2 < 360**2)
    if p == "openwork":
        gears = "".join(f'<g><circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{t["metal"]}" stroke-width="15" stroke-dasharray="13 11" opacity=".65"/><circle cx="{x}" cy="{y}" r="{r*.52}" fill="none" stroke="{t["fg"]}" stroke-width="5" opacity=".4"/><circle cx="{x}" cy="{y}" r="12" fill="{t["accent"]}"/></g>' for x,y,r in [(330,340,105),(685,350,125),(315,675,135),(710,680,98)])
        return gears + f'<path d="M205 525 Q375 385 512 512 T820 485" fill="none" stroke="{t["metal"]}" stroke-width="38" opacity=".48"/><path d="M252 780 Q500 590 772 250" fill="none" stroke="{t["metal"]}" stroke-width="30" opacity=".45"/>'
    if p == "silk": return "".join(f'<line x1="180" y1="{y}" x2="844" y2="{y}" stroke="#8d826b" opacity=".06"/>' for y in range(180,845,5))
    if p == "horizon": return "".join(f'<path d="M160 {y} Q512 {y+10} 864 {y}" fill="none" stroke="{t["accent"]}" stroke-width="6" opacity=".18"/>' for y in range(240,805,42))
    if p == "stars":
        return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t["fg"]}" opacity=".55"/>' for x,y,r in [(245,312,3),(322,205,4),(706,235,3),(792,342,5),(242,686,4),(735,746,3),(625,808,4),(358,786,2)])
    if p == "sector": return f'<circle cx="512" cy="512" r="330" fill="none" stroke="{t["fg"]}" stroke-width="3"/><circle cx="512" cy="512" r="382" fill="none" stroke="{t["fg"]}" stroke-width="3"/>'
    return ""


def markers(t: dict) -> str:
    out = []
    for i in range(60):
        d = i * 6; major = i % 5 == 0
        if major:
            if t["markers"] == "round":
                x,y=polar(366,d); out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{19 if i else 24}" fill="{t["lume"]}" stroke="{t["metal"]}" stroke-width="6"/>')
            elif t["markers"] in ("roman", "arabic"):
                vals = (["XII","I","II","III","IV","V","VI","VII","VIII","IX","X","XI"] if t["markers"]=="roman" else ["12","1","2","3","4","5","6","7","8","9","10","11"])
                out.append(txt(vals[i//5], 350, d, 35, t["fg"], "Georgia", 500))
            elif t["markers"] == "minimal": out.append(line(d, 365, 398, t["fg"], 5))
            else: out.append(line(d, 345 if t["markers"]=="block" else 358, 405, t["lume"], 22 if t["markers"]=="block" else 13))
        else: out.append(line(d, 394, 409, t["fg"], 2.5, .65))
    return "".join(out)


def dial_svg(t: dict) -> str:
    body = case(t) + texture(t) + markers(t)
    body += f'<circle cx="512" cy="512" r="418" fill="none" stroke="{t["fg"]}" stroke-width="2" opacity=".32"/>'
    return doc(t, body, f"{t['name']} dial")


def subdial(x: int, y: int, r: int, t: dict, label: str, style: int = 0) -> str:
    face = t["bg2"] if style % 2 == 0 else t["bg"]
    ticks = "".join(f'<line x1="{x+(r-18)*math.cos(math.radians(d-90)):.1f}" y1="{y+(r-18)*math.sin(math.radians(d-90)):.1f}" x2="{x+(r-5)*math.cos(math.radians(d-90)):.1f}" y2="{y+(r-5)*math.sin(math.radians(d-90)):.1f}" stroke="{t["fg"]}" stroke-width="3"/>' for d in range(0,360,30))
    hand_angle = [42,118,224,306][style%4]; a=math.radians(hand_angle-90)
    return f'<g><circle cx="{x}" cy="{y}" r="{r}" fill="{face}" stroke="{t["metal"]}" stroke-width="5"/>{ticks}<line x1="{x}" y1="{y}" x2="{x+r*.57*math.cos(a):.1f}" y2="{y+r*.57*math.sin(a):.1f}" stroke="{t["accent"]}" stroke-width="7"/><circle cx="{x}" cy="{y}" r="8" fill="{t["fg"]}"/><text x="{x}" y="{y+r*.54}" text-anchor="middle" font-family="Arial" font-size="17" fill="{t["fg"]}" opacity=".75">{label}</text></g>'


def complications_svg(t: dict) -> str:
    c=t["comp"]; body=""
    if c == "date":
        body=f'<g><rect x="666" y="470" width="120" height="84" rx="10" fill="{t["bg2"]}" stroke="{t["metal"]}" stroke-width="6"/><text x="726" y="529" text-anchor="middle" font-family="Georgia" font-size="46" fill="{t["fg"]}">28</text>'
        if t["family"]=="Crown Sport": body += '<ellipse cx="726" cy="512" rx="78" ry="59" fill="none" stroke="#fff" stroke-width="10" opacity=".22"/>'
        body += '</g>'
    elif c == "gmt":
        body=''.join(txt(str(24 if i==0 else i*2), 292, i*30, 22, t["accent"], "Arial", 700) for i in range(12))
        body += f'<g transform="rotate(92 512 512)"><path d="M512 562 L495 232 L472 260 L512 186 L552 260 L529 232 Z" fill="{t["accent"]}" opacity=".9"/></g>'
    elif c == "chrono": body=subdial(336,512,106,t,"MIN",0)+subdial(688,512,106,t,"SEC",1)+subdial(512,704,88,t,"HOUR",2)
    elif c == "offshore": body=subdial(340,512,118,t,"30",1)+subdial(684,512,118,t,"60",2)+subdial(512,708,92,t,"12",3)
    elif c == "tourbillon":
        body=f'<g><circle cx="512" cy="698" r="112" fill="#070605" stroke="{t["metal"]}" stroke-width="8"/><circle cx="512" cy="698" r="74" fill="none" stroke="{t["accent"]}" stroke-width="10" stroke-dasharray="9 9"/><path d="M438 698 H586 M512 624 V772" stroke="{t["metal"]}" stroke-width="12"/><circle cx="512" cy="698" r="22" fill="{t["accent"]}"/></g>'
    elif c == "small_seconds": body=subdial(512,700,92,t,"60",0)
    elif c == "perpetual":
        body=subdial(324,510,88,t,"DAY",0)+subdial(700,510,88,t,"MON",1)
        body+=f'<g><circle cx="512" cy="704" r="116" fill="#030714" stroke="{t["metal"]}" stroke-width="6"/><circle cx="482" cy="685" r="54" fill="{t["accent"]}"/><circle cx="510" cy="664" r="54" fill="#030714"/><path d="M418 735 Q512 666 606 735" fill="none" stroke="{t["metal"]}" stroke-width="4"/></g>'
    elif c == "reserve":
        body=f'<g><path d="M348 712 A178 178 0 0 1 676 712" fill="none" stroke="{t["fg"]}" stroke-width="5"/><path d="M372 705 A154 154 0 0 1 634 644" fill="none" stroke="{t["accent"]}" stroke-width="15" stroke-linecap="round"/><text x="512" y="748" text-anchor="middle" font-family="Georgia" font-size="22" fill="{t["fg"]}">POWER</text></g>'
    return doc(t, body, f"{t['name']} complications")


def hand_shapes(t: dict) -> tuple[str,str]:
    h=t["hands"]
    if h=="faceted": return (f'<path d="M512 555 L484 512 L502 292 L512 255 L522 292 L540 512 Z" fill="url(#hand)" stroke="{t["fg"]}" stroke-width="4"/>', f'<path d="M512 557 L491 512 L505 154 L512 122 L519 154 L533 512 Z" fill="url(#hand)" stroke="{t["fg"]}" stroke-width="4"/>')
    if h=="orb": return (f'<path d="M512 552 L477 498 L490 354 A43 43 0 1 1 534 354 L547 498 Z M512 314 A20 20 0 1 0 512 354 A20 20 0 1 0 512 314" fill="{t["lume"]}" fill-rule="evenodd" stroke="{t["metal"]}" stroke-width="7"/>', f'<path d="M512 552 L490 503 L503 158 L512 128 L521 158 L534 503 Z" fill="{t["lume"]}" stroke="{t["metal"]}" stroke-width="7"/>')
    if h=="architect": return (f'<path d="M512 553 L476 501 L491 298 L512 262 L533 298 L548 501 Z" fill="none" stroke="{t["metal"]}" stroke-width="13"/>', f'<path d="M512 556 L486 504 L500 146 L512 112 L524 146 L538 504 Z" fill="none" stroke="{t["metal"]}" stroke-width="11"/>')
    if h=="paddle": return (f'<path d="M512 558 L468 496 L484 496 L484 310 Q512 270 540 310 L540 496 L556 496 Z" fill="{t["lume"]}" stroke="{t["metal"]}" stroke-width="8"/>', f'<path d="M512 558 L480 500 L494 500 L494 170 Q512 132 530 170 L530 500 L544 500 Z" fill="{t["lume"]}" stroke="{t["metal"]}" stroke-width="8"/>')
    if h=="skeleton": return (f'<path d="M512 555 L482 510 L500 273 L512 238 L524 273 L542 510 Z" fill="none" stroke="{t["metal"]}" stroke-width="12"/>', f'<path d="M512 557 L490 510 L502 145 L512 112 L522 145 L534 510 Z" fill="none" stroke="{t["metal"]}" stroke-width="10"/>')
    if h in ("dauphine","leaf"): return (f'<path d="M512 552 Q470 414 512 262 Q554 414 512 552Z" fill="url(#hand)" stroke="{t["fg"]}" stroke-width="3"/>', f'<path d="M512 554 Q480 342 512 128 Q544 342 512 554Z" fill="url(#hand)" stroke="{t["fg"]}" stroke-width="3"/>')
    if h=="breguet": return (f'<path d="M507 550 L506 344 A27 27 0 1 1 518 344 L517 550Z M512 307 A13 13 0 1 0 512 333 A13 13 0 1 0 512 307" fill="{t["fg"]}" fill-rule="evenodd"/>', f'<path d="M508 552 L507 191 A24 24 0 1 1 517 191 L516 552Z M512 158 A12 12 0 1 0 512 182 A12 12 0 1 0 512 158" fill="{t["fg"]}" fill-rule="evenodd"/>')
    return (f'<rect x="494" y="285" width="36" height="270" rx="12" fill="{t["lume"]}" stroke="{t["metal"]}" stroke-width="6"/>', f'<rect x="499" y="132" width="26" height="423" rx="10" fill="{t["lume"]}" stroke="{t["metal"]}" stroke-width="6"/>')


def second_shape(t: dict) -> str:
    a=t["accent"]; s=t["second"]
    base=f'<line x1="512" y1="602" x2="512" y2="118" stroke="{a}" stroke-width="7" stroke-linecap="round"/>'
    forms={
        "needle": '<path d="M512 105 l-11 45 h22z" fill="%s"/><circle cx="512" cy="570" r="12" fill="%s"/>'%(a,a),
        "bolt": '<path d="M512 104 l-18 62 17-8 -9 46 30-76-18 9z" fill="%s"/>'%a,
        "diamond": '<path d="M512 98 l17 35-17 35-17-35z" fill="%s"/><rect x="504" y="558" width="16" height="52" rx="8" fill="%s"/>'%(a,a),
        "open": '<circle cx="512" cy="160" r="24" fill="none" stroke="%s" stroke-width="8"/><path d="M512 586 l-22 24 h44z" fill="%s"/>'%(a,a),
        "counter": '<rect x="495" y="558" width="34" height="58" rx="17" fill="%s"/><circle cx="512" cy="142" r="11" fill="%s"/>'%(a,a),
        "crescent": '<path d="M500 145 A28 28 0 1 0 530 178 A22 22 0 1 1 500 145" fill="%s"/><circle cx="512" cy="585" r="16" fill="none" stroke="%s" stroke-width="6"/>'%(a,a),
        "leaf": '<path d="M512 120 Q478 160 512 202 Q546 160 512 120Z" fill="%s"/><path d="M512 575 q-20 18 0 39 q20-21 0-39" fill="%s"/>'%(a,a),
        "spear": '<path d="M512 95 l25 58-25 34-25-34z" fill="%s"/>'%a,
        "star": '<path d="M512 102 l9 22 24 2-18 16 6 24-21-13-21 13 6-24-18-16 24-2z" fill="%s"/>'%a,
        "drop": '<path d="M512 105 C548 156 540 184 512 184 C484 184 476 156 512 105Z" fill="none" stroke="%s" stroke-width="7"/>'%a,
    }
    return base+forms[s]


def hands_svg(t: dict) -> str:
    hour,minute=hand_shapes(t)
    body=f'<g filter="url(#shadow)"><g transform="rotate(304 512 512)">{hour}</g><g transform="rotate(54 512 512)">{minute}</g><g transform="rotate(216 512 512)">{second_shape(t)}</g><circle cx="512" cy="512" r="31" fill="url(#steel)" stroke="{t["bg2"]}" stroke-width="7"/><circle cx="512" cy="512" r="10" fill="{t["accent"]}"/></g>'
    return doc(t, body, f"{t['name']} hands")


def inner(svg: str) -> str:
    return svg.split("</defs>",1)[1].rsplit("</svg>",1)[0]


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    catalog=[]
    for t in WATCHES:
        folder=ROOT/t["slug"]; folder.mkdir(parents=True,exist_ok=True)
        dial=dial_svg(t); comps=complications_svg(t); hands=hands_svg(t)
        preview=doc(t,inner(dial)+inner(comps)+inner(hands),f"{t['name']} preview")
        for name,data in (("dial.svg",dial),("complications.svg",comps),("hands.svg",hands),("preview.svg",preview)):
            (folder/name).write_text(data,encoding="utf-8")
        meta={"slug":t["slug"],"name":t["name"],"family":t["family"],"description":t["note"],"canvas":[1024,1024],"layers":["dial","complications","hands"],"palette":{k:t[k] for k in ("bg","bg2","fg","metal","accent","lume")},"originality":"Unbranded original artwork informed by broad luxury-watch design traditions; no logos or exact replicas."}
        (folder/"metadata.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
        catalog.append(meta)
    (ROOT/"catalog.json").write_text(json.dumps(catalog,indent=2)+"\n",encoding="utf-8")
    print(f"generated {len(WATCHES)} layered watchfaces")


if __name__ == "__main__": main()
