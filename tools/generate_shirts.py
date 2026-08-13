#!/usr/bin/env python3
"""Generate ten original streetwear T-shirt mockups as editable SVG assets."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "assets" / "shirts"

SHIRTS = [
    ("01_midtraining", "Midtraining", "MIDTRAINING", "BASE → CAPABILITY", 320, "#141414", "#f2f0e9", "#f05245", "fracture"),
    ("02_lora", "LoRA", "LoRA", "LOW-RANK ADAPTATION", 290, "#ece9df", "#111111", "#ff5a36", "signal"),
    ("03_rag", "RAG", "RAG", "RETRIEVE / AUGMENT / GENERATE", 300, "#11151c", "#f6f2e8", "#a9ff3f", "orbit"),
    ("04_inference", "Inference", "INFERENCE", "SERVE / SAMPLE / REPEAT", 340, "#c8c6bf", "#171717", "#3757ff", "glitch"),
    ("05_context", "Context", "CONTEXT", "WINDOW 128K", 310, "#d94e43", "#f8eddd", "#1b1b1b", "curve"),
    ("06_agentic", "Agentic", "AGENTIC", "PLAN / ACT / OBSERVE", 360, "#171717", "#e8e6dd", "#d8ff37", "utility"),
    ("07_rlhf", "RLHF", "RLHF", "HUMAN IN THE LOOP", 295, "#f1eee5", "#121212", "#ff4b28", "rebuild"),
    ("08_quantized", "Quantized", "QUANTIZED", "INT8 / INT4", 330, "#252b59", "#eee9dc", "#f0a6db", "label"),
    ("09_distilled", "Distilled", "DISTILLED", "TEACHER → STUDENT", 350, "#0c0d0f", "#f5f0e8", "#35d9c5", "frame"),
    ("10_synthetic", "Synthetic", "SYNTHETIC", "DATA / GENERATED", 380, "#e7dfd2", "#181514", "#e3453c", "spiral"),
]


def esc(text: str) -> str:
    return text.replace("&", "&amp;")


def art(kind: str, phrase: str, ink: str, accent: str) -> str:
    p = esc(phrase)
    if kind == "fracture":
        return f'''<g transform="translate(450 505) rotate(-7)"><text x="0" y="-95" text-anchor="middle" font-family="Arial Black,Arial" font-size="60" fill="{ink}">PROMPT</text><text x="0" y="-25" text-anchor="middle" font-family="Arial Black,Arial" font-size="58" fill="{ink}">LIKE YOU</text><text x="0" y="48" text-anchor="middle" font-family="Arial Black,Arial" font-size="58" fill="{accent}">MEAN IT</text><path d="M-245 -2 L-75 -26 22 8 244 -14" fill="none" stroke="{accent}" stroke-width="14"/><rect x="-218" y="88" width="436" height="38" fill="none" stroke="{ink}" stroke-width="3"/><text y="115" text-anchor="middle" font-family="monospace" font-size="18" fill="{ink}" letter-spacing="7">REVISION 01 / OPEN</text></g>'''
    if kind == "signal":
        return f'''<g transform="translate(450 495)"><circle r="205" fill="none" stroke="{ink}" stroke-width="3"/><circle r="164" fill="none" stroke="{accent}" stroke-width="18" stroke-dasharray="190 35"/><path d="M-250 178 L250 -178" stroke="{accent}" stroke-width="32"/><text x="0" y="-18" text-anchor="middle" font-family="Arial Black" font-size="48" fill="{ink}" letter-spacing="3">I DREAM</text><text x="0" y="48" text-anchor="middle" font-family="Arial Black" font-size="48" fill="{ink}" letter-spacing="3">IN TOKENS</text><text x="0" y="88" text-anchor="middle" font-family="monospace" font-size="17" fill="{ink}">NEXT TOKEN / NEXT THOUGHT</text></g>'''
    if kind == "orbit":
        return f'''<g transform="translate(450 505)"><ellipse rx="230" ry="118" fill="none" stroke="{accent}" stroke-width="12" transform="rotate(-22)"/><ellipse rx="230" ry="118" fill="none" stroke="{ink}" stroke-width="3" transform="rotate(30)"/><circle r="42" fill="{accent}"/><text x="0" y="-178" text-anchor="middle" font-family="Arial Black" font-size="42" fill="{ink}">HALLUCINATE</text><text x="0" y="207" text-anchor="middle" font-family="Arial Black" font-size="38" fill="{ink}">RESPONSIBLY</text><text x="0" y="7" text-anchor="middle" font-family="monospace" font-size="16" fill="#101010">0.7 TEMP</text></g>'''
    if kind == "glitch":
        return f'''<g transform="translate(450 500)"><text x="-12" y="-35" text-anchor="middle" font-family="Arial Black" font-size="61" fill="{accent}">CONTEXT</text><text x="12" y="-20" text-anchor="middle" font-family="Arial Black" font-size="61" fill="{ink}" opacity=".88">CONTEXT</text><rect x="-240" y="10" width="480" height="18" fill="{accent}"/><rect x="-205" y="46" width="350" height="10" fill="{ink}"/><text y="112" text-anchor="middle" font-family="monospace" font-size="24" fill="{ink}" letter-spacing="4">WINDOW CLOSING</text><path d="M-230 142 h95 l22 -18 h92 l16 35 h106 l20 -26 h115" fill="none" stroke="{ink}" stroke-width="5"/></g>'''
    if kind == "curve":
        letters = "ALIGNMENT AFTER HOURS • ALIGNMENT AFTER HOURS • "
        return f'''<defs><path id="curve" d="M210 545 A240 240 0 1 1 690 545"/></defs><g><text font-family="Arial Black" font-size="38" fill="{ink}" letter-spacing="4"><textPath href="#curve" startOffset="2%">{letters}</textPath></text><circle cx="450" cy="545" r="145" fill="none" stroke="{ink}" stroke-width="4"/><circle cx="450" cy="545" r="103" fill="{accent}"/><text x="450" y="537" text-anchor="middle" font-family="Arial Black" font-size="42" fill="{ink}">OPEN</text><text x="450" y="582" text-anchor="middle" font-family="monospace" font-size="22" fill="{ink}">WHEN CLOSED</text></g>'''
    if kind == "utility":
        return f'''<g transform="translate(450 500)"><rect x="-240" y="-190" width="480" height="380" fill="none" stroke="{ink}" stroke-width="5"/><path d="M-240 -110 H240 M-240 115 H240 M-120 -190 V190" stroke="{ink}" stroke-width="3"/><rect x="-100" y="-92" width="320" height="185" fill="{accent}"/><text x="60" y="-25" text-anchor="middle" font-family="Arial Black" font-size="37" fill="#111">ARTIFICIAL</text><text x="60" y="27" text-anchor="middle" font-family="Arial Black" font-size="37" fill="#111">FEELINGS</text><text x="60" y="70" text-anchor="middle" font-family="monospace" font-size="15" fill="#111">REAL CONSEQUENCES</text><text x="-180" y="-142" text-anchor="middle" font-family="monospace" font-size="17" fill="{ink}" transform="rotate(-90 -180 -142)">HANDLE WITH CARE</text><text x="0" y="158" text-anchor="middle" font-family="monospace" font-size="16" fill="{ink}" letter-spacing="4">SYNTHETIC / SINCERE</text></g>'''
    if kind == "rebuild":
        return f'''<g transform="translate(450 505)"><text x="-220" y="-102" font-family="Arial Black" font-size="54" fill="{ink}">RE</text><text x="-142" y="-102" font-family="Arial Black" font-size="54" fill="{accent}">GENERATE</text><text x="-220" y="-38" font-family="Arial Black" font-size="54" fill="{ink}">TOMORROW</text><path d="M-220 6 h440 v190 h-440z" fill="none" stroke="{ink}" stroke-width="4"/><path d="M-215 190 l80-150 80 150 80-150 80 150 80-150" fill="none" stroke="{accent}" stroke-width="18"/><text x="0" y="235" text-anchor="middle" font-family="monospace" font-size="17" fill="{ink}" letter-spacing="5">NEW SEED / NEW WORLD</text></g>'''
    if kind == "label":
        return f'''<g transform="translate(450 510) rotate(4)"><rect x="-250" y="-165" width="500" height="330" rx="6" fill="{ink}"/><rect x="-226" y="-141" width="452" height="282" fill="none" stroke="{accent}" stroke-width="7" stroke-dasharray="22 12"/><text x="0" y="-58" text-anchor="middle" font-family="Arial Black" font-size="45" fill="{accent}">PLEASE DO NOT</text><text x="0" y="6" text-anchor="middle" font-family="Arial Black" font-size="49" fill="#252b59">FINE-TUNE ME</text><text x="0" y="64" text-anchor="middle" font-family="monospace" font-size="17" fill="#252b59">BASE MODEL / FRAGILE EGO</text><path d="M-175 96 h350" stroke="#252b59" stroke-width="12" stroke-dasharray="4 8"/></g>'''
    if kind == "frame":
        return f'''<g transform="translate(450 500)"><path d="M-245 -180 H120 V-130 H-190 V155 H120 V205 H-245Z" fill="{ink}"/><path d="M180 -180 H245 V205 H-110 V155 H180Z" fill="{accent}"/><text x="5" y="-49" text-anchor="middle" font-family="Arial Black" font-size="53" fill="{ink}">OUTSIDE</text><text x="5" y="18" text-anchor="middle" font-family="Arial Black" font-size="48" fill="{ink}">THE TRAINING</text><text x="5" y="78" text-anchor="middle" font-family="Arial Black" font-size="53" fill="{ink}">SET</text><text x="5" y="116" text-anchor="middle" font-family="monospace" font-size="15" fill="{ink}" letter-spacing="3">UNSEEN / UNBOTHERED</text></g>'''
    return f'''<g transform="translate(450 505)"><path d="M0 -220 C220 -220 260 -20 86 45 C-70 102 -125 230 0 238 C145 248 244 115 206 -20 C163 -172 -54 -184 -146 -73 C-226 25 -166 175 -52 169" fill="none" stroke="{accent}" stroke-width="23"/><text x="0" y="-22" text-anchor="middle" font-family="Arial Black" font-size="48" fill="{ink}">SLOW TOKEN</text><text x="0" y="42" text-anchor="middle" font-family="Arial Black" font-size="48" fill="{ink}">FAST WORLD</text><text x="0" y="89" text-anchor="middle" font-family="monospace" font-size="17" fill="{ink}" letter-spacing="4">STREAMING THOUGHTS</text></g>'''


def technical_art(kind: str, term: str, subline: str, ink: str, accent: str) -> str:
    term = esc(term); subline = esc(subline)
    if kind in ("fracture", "glitch"):
        return f'''<g transform="translate(450 510) rotate(-6)"><text x="-12" y="-25" text-anchor="middle" font-family="Arial Black" font-size="68" fill="{accent}">{term}</text><text x="12" y="-7" text-anchor="middle" font-family="Arial Black" font-size="68" fill="{ink}">{term}</text><path d="M-240 28 L-80 4 34 42 238 15" fill="none" stroke="{accent}" stroke-width="17"/><text x="0" y="91" text-anchor="middle" font-family="monospace" font-size="20" fill="{ink}" letter-spacing="5">{subline}</text><rect x="-220" y="118" width="440" height="42" fill="none" stroke="{ink}" stroke-width="3"/></g>'''
    if kind in ("signal", "orbit", "spiral"):
        return f'''<g transform="translate(450 515)"><ellipse rx="238" ry="126" fill="none" stroke="{accent}" stroke-width="17" transform="rotate(-24)"/><ellipse rx="238" ry="126" fill="none" stroke="{ink}" stroke-width="4" transform="rotate(31)"/><circle r="48" fill="{accent}"/><text x="0" y="-178" text-anchor="middle" font-family="Arial Black" font-size="72" fill="{ink}">{term}</text><text x="0" y="211" text-anchor="middle" font-family="monospace" font-size="18" fill="{ink}" letter-spacing="4">{subline}</text></g>'''
    if kind in ("curve", "frame"):
        return f'''<g transform="translate(450 510)"><rect x="-248" y="-192" width="496" height="384" fill="none" stroke="{ink}" stroke-width="5"/><path d="M-248 -192 H92 V-142 H-192 V142 H110 V192 H-248Z" fill="{accent}" opacity=".9"/><text x="20" y="-10" text-anchor="middle" font-family="Arial Black" font-size="70" fill="{ink}">{term}</text><text x="20" y="54" text-anchor="middle" font-family="monospace" font-size="18" fill="{ink}" letter-spacing="4">{subline}</text><path d="M-190 88 h380" stroke="{ink}" stroke-width="13" stroke-dasharray="5 9"/></g>'''
    if kind in ("utility", "label"):
        return f'''<g transform="translate(450 510) rotate(3)"><rect x="-252" y="-180" width="504" height="360" rx="5" fill="{ink}"/><rect x="-226" y="-154" width="452" height="308" fill="none" stroke="{accent}" stroke-width="8" stroke-dasharray="24 12"/><text x="0" y="-20" text-anchor="middle" font-family="Arial Black" font-size="65" fill="{accent}">{term}</text><text x="0" y="49" text-anchor="middle" font-family="monospace" font-size="18" fill="#111" letter-spacing="3">{subline}</text><path d="M-174 90 h348" stroke="#111" stroke-width="14" stroke-dasharray="4 8"/></g>'''
    return f'''<g transform="translate(450 510)"><text x="0" y="-88" text-anchor="middle" font-family="Arial Black" font-size="76" fill="{ink}">{term}</text><path d="M-230 -30 h460 v205 h-460z" fill="none" stroke="{ink}" stroke-width="5"/><path d="M-218 163 l82-174 82 174 82-174 82 174 82-174" fill="none" stroke="{accent}" stroke-width="20"/><text x="0" y="222" text-anchor="middle" font-family="monospace" font-size="18" fill="{ink}" letter-spacing="4">{subline}</text></g>'''


def front_art(term: str, subline: str, ink: str, accent: str) -> str:
    return f'''<g transform="translate(450 438)"><rect x="-135" y="-54" width="270" height="108" fill="none" stroke="{ink}" stroke-width="3"/><rect x="-135" y="-54" width="18" height="108" fill="{accent}"/><text x="10" y="-2" text-anchor="middle" font-family="Arial Black" font-size="31" fill="{ink}">{esc(term)}</text><text x="10" y="27" text-anchor="middle" font-family="monospace" font-size="11" fill="{ink}" letter-spacing="2">{esc(subline)}</text></g>'''


def mockup(slug: str, name: str, term: str, subline: str, cloth: str, ink: str, accent: str, kind: str, side: str) -> str:
    shirt = "M236 156 L340 94 Q450 148 560 94 L664 156 L850 290 L734 420 L670 368 L700 1010 L200 1010 L230 368 L166 420 L50 290Z"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="1100" viewBox="0 0 900 1100" role="img" aria-label="{name} T-shirt concept">
    <defs><filter id="shadow" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="24" stdDeviation="24" flood-color="#000" flood-opacity=".38"/></filter><linearGradient id="cloth" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fff" stop-opacity=".12"/><stop offset=".3" stop-color="{cloth}"/><stop offset="1" stop-color="#000" stop-opacity=".16"/></linearGradient></defs>
    <path d="{shirt}" fill="{cloth}" filter="url(#shadow)"/><path d="{shirt}" fill="url(#cloth)" opacity=".55"/>
    <path d="M340 94 Q450 220 560 94 Q535 78 512 70 Q450 112 388 70 Q365 78 340 94Z" fill="#080808" opacity=".75"/>
    <path d="M236 156 Q272 235 230 368 M664 156 Q628 235 670 368" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="5"/>
    {front_art(term, subline, ink, accent) if side == 'front' else technical_art(kind, term, subline, ink, accent)}
    </svg>\n'''


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    catalog=[]
    for slug,name,term,subline,price,cloth,ink,accent,kind in SHIRTS:
        for side in ("front", "back"):
            (ROOT/f"{slug}-{side}.svg").write_text(mockup(slug,name,term,subline,cloth,ink,accent,kind,side),encoding="utf-8")
        catalog.append(dict(slug=slug,name=name,term=term,subline=subline,price=price,sizes=["XS","S","M","L","XL","2XL","3XL"],shirt_color=cloth,ink=ink,accent=accent,description="Original technical streetwear study with deconstructed luxury, industrial graphics, and concise machine-learning language."))
    (ROOT/"catalog.json").write_text(json.dumps(catalog,indent=2)+"\n",encoding="utf-8")
    print(f"generated {len(SHIRTS)} shirt concepts")


if __name__ == "__main__": main()
