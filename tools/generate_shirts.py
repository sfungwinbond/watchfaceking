#!/usr/bin/env python3
"""Generate ten original VC/startup streetwear concepts with safe print areas."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "assets" / "shirts"

SHIRTS = [
    ("01_default_alive", "Default Alive", "DEFAULT ALIVE", "BURN LESS / BUILD MORE", 320, "#151513", "#f3efe4", "#ee503d", "headline"),
    ("02_series_a", "Series A Energy", "SERIES A", "PRE-REVENUE / POST-COOL", 340, "#ddd7ca", "#171612", "#ff4e30", "racing"),
    ("03_moat_mode", "Moat Mode", "MOAT MODE", "UNFAIR ADVANTAGE", 310, "#1b2234", "#f2eee3", "#c5ff3d", "crest"),
    ("04_pmf", "Product–Market Fit", "PMF", "PULL > PUSH", 360, "#b7b4ad", "#171612", "#3756ff", "diagram"),
    ("05_ai_native", "AI Native", "AI NATIVE", "SOFTWARE EATS SOFTWARE", 330, "#a83f35", "#f5ead8", "#171612", "warning"),
    ("06_hbm_hungry", "HBM Hungry", "HBM HUNGRY", "BANDWIDTH IS THE MOAT", 350, "#181817", "#eeeadd", "#f2d34f", "receipt"),
    ("07_gpu_rich", "GPU Rich", "GPU RICH", "FLOPS ONLY GO UP", 375, "#e7e1d5", "#161513", "#ee4938", "chart"),
    ("08_racks", "Racks on Racks", "RACKS", "POWER / COOLING / COMPUTE", 390, "#272a58", "#f0ebdf", "#f0a3da", "redacted"),
    ("09_founder_mode", "Founder Mode", "FOUNDER MODE", "PERMISSIONLESS", 370, "#101112", "#f1ede2", "#31d7c2", "gothic"),
    ("10_so_back", "We Are So Back", "WE ARE SO BACK", "BREAKING / STILL BUILDING", 395, "#d9d1c3", "#191614", "#e64739", "ticker"),
    ("11_silicon_saint", "Silicon Saint", "SILICON SAINT", "IN FLOPS WE TRUST", 420, "#111111", "#e7e3db", "#9b9b96", "silver_saint"),
    ("12_black_box", "Black Box", "BLACK BOX", "FAITH-BASED INFERENCE", 440, "#1a1918", "#eee9de", "#a6a39c", "thorn"),
    ("13_term_sheet", "Term Sheet", "TERM SHEET", "SIGNED IN SILVER", 410, "#ded9cf", "#191817", "#777773", "dagger"),
    ("14_compute_coven", "Compute Coven", "COMPUTE COVEN", "SUMMON MORE GPUs", 460, "#121416", "#eee9de", "#8c9298", "filigree"),
    ("15_latency_kills", "Latency Kills", "LATENCY KILLS", "MOVE FAST / NO CACHE", 430, "#25211f", "#f1ece0", "#9f8f84", "hardware"),
]


def esc(value: str) -> str:
    return value.replace("&", "&amp;").replace("–", "&#8211;")


def front_art(term: str, subline: str, ink: str, accent: str, style: str) -> str:
    term, subline = esc(term), esc(subline)
    if style in ("crest", "gothic", "silver_saint", "thorn", "dagger", "filigree", "hardware"):
        return f'''<g transform="translate(450 420)"><path d="M-118 -52 H118 V34 Q0 98 -118 34Z" fill="none" stroke="{ink}" stroke-width="4"/><text y="2" text-anchor="middle" font-family="Georgia" font-size="28" font-weight="700" fill="{ink}">{term}</text><circle cy="54" r="9" fill="{accent}"/></g>'''
    if style in ("receipt", "ticker"):
        return f'''<g transform="translate(450 418) rotate(-3)"><rect x="-142" y="-52" width="284" height="104" fill="{ink}"/><text y="-3" text-anchor="middle" font-family="Arial Black" font-size="25" fill="{accent}">{term}</text><text y="27" text-anchor="middle" font-family="monospace" font-size="11" fill="#fff" letter-spacing="2">{subline}</text></g>'''
    return f'''<g transform="translate(450 420)"><rect x="-144" y="-53" width="288" height="106" fill="none" stroke="{ink}" stroke-width="3"/><rect x="-144" y="-53" width="17" height="106" fill="{accent}"/><text x="8" y="-2" text-anchor="middle" font-family="Arial Black" font-size="29" fill="{ink}">{term}</text><text x="8" y="27" text-anchor="middle" font-family="monospace" font-size="10" fill="{ink}" letter-spacing="2">{subline}</text></g>'''


def back_art(term: str, subline: str, ink: str, accent: str, style: str) -> str:
    term, subline = esc(term), esc(subline)
    if style == "headline":
        return f'''<g transform="translate(450 505) rotate(-5)"><text x="-9" y="-66" text-anchor="middle" font-family="Arial Black" font-size="65" fill="{accent}">DEFAULT</text><text x="9" y="-49" text-anchor="middle" font-family="Arial Black" font-size="65" fill="{ink}">DEFAULT</text><text y="25" text-anchor="middle" font-family="Arial Black" font-size="78" fill="{ink}">ALIVE</text><path d="M-196 54 L-60 35 44 69 196 45" fill="none" stroke="{accent}" stroke-width="16"/><text y="114" text-anchor="middle" font-family="monospace" font-size="18" fill="{ink}" letter-spacing="4">{subline}</text></g>'''
    if style == "racing":
        return f'''<g transform="translate(450 506)"><path d="M-202 -182 L202 -182 142 -82 -202 -82Z" fill="{accent}"/><text x="-176" y="-112" font-family="Arial Black" font-size="68" font-style="italic" fill="{ink}">SERIES</text><text x="-184" y="15" font-family="Arial Black" font-size="146" font-style="italic" fill="{ink}">A</text><path d="M-54 -38 H205 M-54 2 H175 M-54 42 H205" stroke="{accent}" stroke-width="18"/><text y="105" text-anchor="middle" font-family="monospace" font-size="17" fill="{ink}" letter-spacing="3">{subline}</text><text y="151" text-anchor="middle" font-family="Arial Black" font-size="27" fill="{accent}">ACCELERATE / 01</text></g>'''
    if style == "crest":
        return f'''<g transform="translate(450 510)"><path d="M0 -205 L194 -132 169 102 Q100 184 0 221 Q-100 184 -169 102 L-194 -132Z" fill="none" stroke="{accent}" stroke-width="14"/><path d="M-140 -105 L140 135 M140 -105 L-140 135" stroke="{ink}" stroke-width="22"/><text y="-30" text-anchor="middle" font-family="Georgia" font-size="68" font-weight="700" fill="{ink}">MOAT</text><text y="42" text-anchor="middle" font-family="Georgia" font-size="68" font-weight="700" fill="{ink}">MODE</text><path d="M-150 94 H150" stroke="{accent}" stroke-width="8"/><text y="145" text-anchor="middle" font-family="monospace" font-size="17" fill="{ink}" letter-spacing="4">{subline}</text></g>'''
    if style == "diagram":
        return f'''<g transform="translate(450 510)"><circle cx="-150" cy="-95" r="55" fill="none" stroke="{ink}" stroke-width="7"/><circle cx="150" cy="-95" r="55" fill="none" stroke="{accent}" stroke-width="15"/><circle cy="115" r="73" fill="{accent}"/><path d="M-103 -64 L-43 47 M103 -64 L43 47" stroke="{ink}" stroke-width="7"/><text y="-46" text-anchor="middle" font-family="Arial Black" font-size="120" fill="{ink}">PMF</text><text y="124" text-anchor="middle" font-family="Arial Black" font-size="23" fill="#fff">FIT</text><rect x="-201" y="205" width="402" height="39" fill="{ink}"/><text y="231" text-anchor="middle" font-family="monospace" font-size="17" fill="#fff" letter-spacing="5">{subline}</text></g>'''
    if style == "warning":
        return f'''<g transform="translate(450 510)"><path d="M0 -220 L220 174 H-220Z" fill="none" stroke="{ink}" stroke-width="14"/><path d="M0 -175 V75" stroke="{accent}" stroke-width="34"/><circle cy="125" r="20" fill="{accent}"/><text y="-32" text-anchor="middle" font-family="Arial Black" font-size="68" fill="{ink}">AI</text><text y="44" text-anchor="middle" font-family="Arial Black" font-size="61" fill="{ink}">NATIVE</text><rect x="-192" y="198" width="384" height="42" fill="{ink}"/><text y="225" text-anchor="middle" font-family="monospace" font-size="14" fill="#fff" letter-spacing="3">{subline}</text></g>'''
    if style == "receipt":
        return f'''<g transform="translate(450 505) rotate(2)"><path d="M-188 -220 H188 V205 L166 224 144 205 122 224 100 205 78 224 56 205 34 224 12 205 -10 224 -32 205 -54 224 -76 205 -98 224 -120 205 -142 224 -164 205 -188 224Z" fill="#f4f0dd"/><text y="-157" text-anchor="middle" font-family="Arial Black" font-size="48" fill="#111">HBM</text><text y="-110" text-anchor="middle" font-family="Arial Black" font-size="42" fill="#111">HUNGRY</text><path d="M-150 -84 H150" stroke="#111" stroke-width="3" stroke-dasharray="8 8"/><text x="-145" y="-34" font-family="monospace" font-size="17" fill="#111">CAPACITY</text><text x="145" y="-34" text-anchor="end" font-family="monospace" font-size="17" fill="#111">192 GB</text><text x="-145" y="4" font-family="monospace" font-size="17" fill="#111">BANDWIDTH</text><text x="145" y="4" text-anchor="end" font-family="monospace" font-size="17" fill="#111">8 TB/s</text><path d="M-150 27 H150" stroke="#111" stroke-width="3"/><text y="72" text-anchor="middle" font-family="Arial Black" font-size="27" fill="{accent}">MEMORY BOUND</text><text y="123" text-anchor="middle" font-family="monospace" font-size="15" fill="#111" letter-spacing="3">{subline}</text><path d="M-86 158 h172" stroke="#111" stroke-width="16" stroke-dasharray="3 7"/></g>'''
    if style == "chart":
        return f'''<g transform="translate(450 510)"><path d="M-200 178 V-178 M-200 178 H210" stroke="{ink}" stroke-width="8"/><path d="M-182 140 L-93 84 -35 112 38 8 96 33 195 -158" fill="none" stroke="{accent}" stroke-width="22"/><path d="M154 -162 L205 -175 196 -124" fill="none" stroke="{accent}" stroke-width="22"/><text x="-175" y="-113" font-family="Arial Black" font-size="48" fill="{ink}">GPU</text><text x="-175" y="-61" font-family="Arial Black" font-size="48" fill="{ink}">RICH</text><text y="231" text-anchor="middle" font-family="monospace" font-size="15" fill="{ink}" letter-spacing="3">{subline}</text></g>'''
    if style == "redacted":
        return f'''<g transform="translate(450 510) rotate(3)"><rect x="-213" y="-220" width="426" height="440" fill="#eee9dc"/><text x="-180" y="-158" font-family="monospace" font-size="16" fill="#111">CONFIDENTIAL / CLUSTER MAP</text><text y="-70" text-anchor="middle" font-family="Arial Black" font-size="60" fill="#111">RACKS</text><g fill="#111"><rect x="-173" y="-33" width="105" height="140"/><rect x="-52" y="-33" width="105" height="140"/><rect x="69" y="-33" width="105" height="140"/></g><g fill="{accent}"><circle cx="-147" cy="-3" r="7"/><circle cx="-26" cy="-3" r="7"/><circle cx="95" cy="-3" r="7"/></g><path d="M-147 28 h53 M-147 48 h53 M-147 68 h53 M-26 28 h53 M-26 48 h53 M-26 68 h53 M95 28 h53 M95 48 h53 M95 68 h53" stroke="#eee9dc" stroke-width="6"/><rect x="-183" y="124" width="366" height="46" fill="{accent}"/><text y="154" text-anchor="middle" font-family="Arial Black" font-size="20" fill="#252b59">RACKS ON RACKS</text><text y="203" text-anchor="middle" font-family="monospace" font-size="14" fill="#111" letter-spacing="2">{subline}</text></g>'''
    if style == "gothic":
        return f'''<g transform="translate(450 510)"><path d="M0 -224 L48 -137 144 -153 116 -59 198 0 116 59 144 153 48 137 0 224 -48 137 -144 153 -116 59 -198 0 -116 -59 -144 -153 -48 -137Z" fill="none" stroke="{accent}" stroke-width="12"/><text y="-13" text-anchor="middle" font-family="Georgia" font-size="59" font-weight="700" fill="{ink}">FOUNDER</text><text y="56" text-anchor="middle" font-family="Georgia" font-size="67" font-weight="700" fill="{ink}">MODE</text><circle cy="-105" r="16" fill="{accent}"/><text y="184" text-anchor="middle" font-family="monospace" font-size="17" fill="{ink}" letter-spacing="5">{subline}</text></g>'''
    if style == "silver_saint":
        return f'''<g transform="translate(450 510)"><circle r="202" fill="none" stroke="{accent}" stroke-width="15" stroke-dasharray="4 13"/><path d="M0 -212 L30 -105 118 -155 78 -60 190 -48 92 5 180 78 67 62 92 174 15 89 -38 196 -48 78 -165 118 -82 26 -196 -20 -82 -48 -128 -148 -30 -92Z" fill="none" stroke="{ink}" stroke-width="8"/><text y="-20" text-anchor="middle" font-family="Georgia" font-size="54" font-weight="700" fill="{ink}">SILICON</text><text y="45" text-anchor="middle" font-family="Georgia" font-size="64" font-weight="700" fill="{ink}">SAINT</text><circle cy="-105" r="18" fill="{accent}"/><text y="160" text-anchor="middle" font-family="monospace" font-size="16" fill="{ink}" letter-spacing="4">{subline}</text></g>'''
    if style == "thorn":
        thorns="".join(f'<path d="M0 -210 l{-18 if i%2 else 18} 34 18 -8z" fill="{accent}" transform="rotate({i*30})"/>' for i in range(12))
        return f'''<g transform="translate(450 510)"><circle r="190" fill="none" stroke="{accent}" stroke-width="13"/>{thorns}<circle r="145" fill="none" stroke="{ink}" stroke-width="4"/><text y="-12" text-anchor="middle" font-family="Georgia" font-size="67" font-weight="700" fill="{ink}">BLACK</text><text y="60" text-anchor="middle" font-family="Georgia" font-size="72" font-weight="700" fill="{ink}">BOX</text><path d="M-92 92 H92" stroke="{accent}" stroke-width="10"/><text y="140" text-anchor="middle" font-family="monospace" font-size="14" fill="{ink}" letter-spacing="3">{subline}</text></g>'''
    if style == "dagger":
        return f'''<g transform="translate(450 510)"><path d="M0 -222 L35 -90 112 -40 35 0 20 159 0 219 -20 159 -35 0 -112 -40 -35 -90Z" fill="none" stroke="{accent}" stroke-width="14"/><path d="M-173 -155 Q0 -225 173 -155 M-173 155 Q0 225 173 155" fill="none" stroke="{ink}" stroke-width="7"/><text y="-54" text-anchor="middle" font-family="Georgia" font-size="52" font-weight="700" fill="{ink}">TERM</text><text y="12" text-anchor="middle" font-family="Georgia" font-size="56" font-weight="700" fill="{ink}">SHEET</text><text y="112" text-anchor="middle" font-family="monospace" font-size="15" fill="{ink}" letter-spacing="4">{subline}</text></g>'''
    if style == "filigree":
        return f'''<g transform="translate(450 510)"><path d="M0 -210 C48 -168 91 -185 111 -139 C132 -91 85 -70 112 -32 C142 10 196 -2 202 48 C207 93 156 112 118 94 C140 150 94 196 48 165 C28 151 17 128 0 102 C-17 128 -28 151 -48 165 C-94 196 -140 150 -118 94 C-156 112 -207 93 -202 48 C-196 -2 -142 10 -112 -32 C-85 -70 -132 -91 -111 -139 C-91 -185 -48 -168 0 -210Z" fill="none" stroke="{accent}" stroke-width="12"/><circle r="112" fill="none" stroke="{ink}" stroke-width="5"/><text y="-13" text-anchor="middle" font-family="Georgia" font-size="48" font-weight="700" fill="{ink}">COMPUTE</text><text y="48" text-anchor="middle" font-family="Georgia" font-size="55" font-weight="700" fill="{ink}">COVEN</text><text y="137" text-anchor="middle" font-family="monospace" font-size="15" fill="{ink}" letter-spacing="4">{subline}</text></g>'''
    if style == "hardware":
        return f'''<g transform="translate(450 510)"><rect x="-205" y="-205" width="410" height="410" rx="28" fill="none" stroke="{accent}" stroke-width="16"/><g fill="none" stroke="{ink}" stroke-width="8"><circle cx="-165" cy="-165" r="18"/><circle cx="165" cy="-165" r="18"/><circle cx="-165" cy="165" r="18"/><circle cx="165" cy="165" r="18"/></g><path d="M-145 -100 H145 M-145 100 H145" stroke="{ink}" stroke-width="5"/><text y="-15" text-anchor="middle" font-family="Georgia" font-size="55" font-weight="700" fill="{ink}">LATENCY</text><text y="53" text-anchor="middle" font-family="Georgia" font-size="66" font-weight="700" fill="{ink}">KILLS</text><path d="M-115 83 H115" stroke="{accent}" stroke-width="11"/><text y="137" text-anchor="middle" font-family="monospace" font-size="14" fill="{ink}" letter-spacing="3">{subline}</text></g>'''
    return f'''<g transform="translate(450 510)"><rect x="-215" y="-216" width="430" height="432" fill="none" stroke="{ink}" stroke-width="6"/><rect x="-215" y="-216" width="430" height="58" fill="{accent}"/><text y="-177" text-anchor="middle" font-family="monospace" font-size="18" fill="#fff" letter-spacing="3">BREAKING / 09:41</text><text y="-58" text-anchor="middle" font-family="Arial Black" font-size="57" fill="{ink}">WE ARE</text><text y="17" text-anchor="middle" font-family="Arial Black" font-size="76" fill="{ink}">SO BACK</text><path d="M-170 55 H170" stroke="{accent}" stroke-width="18"/><text y="113" text-anchor="middle" font-family="monospace" font-size="16" fill="{ink}" letter-spacing="3">{subline}</text><path d="M-174 155 h348" stroke="{ink}" stroke-width="3"/><text y="190" text-anchor="middle" font-family="monospace" font-size="13" fill="{ink}">SOURCE: PEOPLE FAMILIAR WITH THE MATTER</text></g>'''


def mockup(name: str, term: str, subline: str, cloth: str, ink: str, accent: str, style: str, side: str) -> str:
    shirt = "M236 156 L340 94 Q450 148 560 94 L664 156 L850 290 L734 420 L670 368 L700 1010 L200 1010 L230 368 L166 420 L50 290Z"
    artwork = front_art(term, subline, ink, accent, style) if side == "front" else back_art(term, subline, ink, accent, style)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="1100" viewBox="0 0 900 1100" role="img" aria-label="{esc(name)} T-shirt {side}">
    <defs>
      <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="24" stdDeviation="24" flood-color="#000" flood-opacity=".38"/></filter>
      <linearGradient id="cloth" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fff" stop-opacity=".12"/><stop offset=".3" stop-color="{cloth}"/><stop offset="1" stop-color="#000" stop-opacity=".16"/></linearGradient>
      <clipPath id="shirtClip"><path d="{shirt}"/></clipPath>
      <clipPath id="printSafe"><rect x="218" y="258" width="464" height="515" rx="8"/></clipPath>
    </defs>
    <path d="{shirt}" fill="{cloth}" filter="url(#shadow)"/><path d="{shirt}" fill="url(#cloth)" opacity=".55"/>
    <path d="M340 94 Q450 220 560 94 Q535 78 512 70 Q450 112 388 70 Q365 78 340 94Z" fill="#080808" opacity=".75"/>
    <path d="M236 156 Q272 235 230 368 M664 156 Q628 235 670 368" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="5"/>
    <g clip-path="url(#shirtClip)"><g clip-path="url(#printSafe)">{artwork}</g></g>
    </svg>\n'''


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    for old in ROOT.glob("*-front.svg"): old.unlink()
    for old in ROOT.glob("*-back.svg"): old.unlink()
    catalog=[]
    for slug,name,term,subline,price,cloth,ink,accent,style in SHIRTS:
        for side in ("front", "back"):
            (ROOT/f"{slug}-{side}.svg").write_text(mockup(name,term,subline,cloth,ink,accent,style,side),encoding="utf-8")
        catalog.append({"slug":slug,"name":name,"term":term,"subline":subline,"price":price,"sizes":["XS","S","M","L","XL","2XL","3XL"],"shirt_color":cloth,"ink":ink,"accent":accent,"description":"Original startup-culture streetwear study with a print-safe front and back composition."})
    (ROOT/"catalog.json").write_text(json.dumps(catalog,indent=2)+"\n",encoding="utf-8")
    print(f"generated {len(SHIRTS)} front/back shirt concepts")


if __name__ == "__main__": main()
