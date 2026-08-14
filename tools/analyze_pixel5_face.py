#!/usr/bin/env python3
"""Rectify and measure the angled watch face in pixel5.tiff with OpenCV.

This is a deterministic reference-analysis tool, not a shipped image generator.
It fits the dark glass boundary as an ellipse, maps its principal axes back to a
circle, extracts the coral telemetry marks, and writes a geometry/palette report.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import cv2
import numpy as np


def find_face_ellipse(image: np.ndarray) -> tuple[tuple[float, float], tuple[float, float], float, np.ndarray]:
    height, width = image.shape[:2]
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    dark = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([179, 255, 78]))

    # The supplied product shot places the tilted glass inside this convex hull.
    # It deliberately excludes the woven strap, crown, button, and lower lug;
    # a rectangular ROI joins those dark regions to the face and over-fits it.
    spatial = np.zeros_like(dark)
    hull = np.array([
        [2, 260], [112, 125], [326, 74], [488, 126], [535, 282],
        [505, 500], [390, 675], [208, 733], [58, 644], [2, 485],
    ], dtype=np.int32)
    cv2.fillConvexPoly(spatial, hull, 255)
    dark = cv2.bitwise_and(dark, spatial)
    dark = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((11, 11), np.uint8), iterations=2)
    dark = cv2.morphologyEx(dark, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8), iterations=1)

    contours, _ = cv2.findContours(dark, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    candidates = [c for c in contours if len(c) >= 5 and cv2.contourArea(c) > width * height * .04]
    if not candidates:
        raise RuntimeError("No watch-face contour found")

    contour = max(candidates, key=cv2.contourArea)
    center, axes, angle = cv2.fitEllipse(contour)
    return center, axes, angle, contour


def rectify(image: np.ndarray, center: tuple[float, float], axes: tuple[float, float], angle: float, size: int = 1024) -> tuple[np.ndarray, np.ndarray]:
    cx, cy = center
    axis_x, axis_y = axes[0] / 2, axes[1] / 2
    theta = math.radians(angle)
    ux = np.array([math.cos(theta), math.sin(theta)], dtype=np.float32)
    uy = np.array([-math.sin(theta), math.cos(theta)], dtype=np.float32)

    src = np.float32([
        [cx, cy],
        np.array([cx, cy], dtype=np.float32) + ux * axis_x,
        np.array([cx, cy], dtype=np.float32) + uy * axis_y,
    ])
    radius = size * .43
    dst = np.float32([[size / 2, size / 2], [size / 2 + radius, size / 2], [size / 2, size / 2 + radius]])
    matrix = cv2.getAffineTransform(src, dst)
    rectified = cv2.warpAffine(image, matrix, (size, size), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))

    yy, xx = np.ogrid[:size, :size]
    circle = ((xx - size / 2) ** 2 + (yy - size / 2) ** 2 <= radius ** 2).astype(np.uint8) * 255
    rectified[circle == 0] = (245, 241, 234)
    return rectified, matrix


def extract_coral_geometry(rectified: np.ndarray) -> tuple[list[dict], str]:
    hsv = cv2.cvtColor(rectified, cv2.COLOR_BGR2HSV)
    mask_a = cv2.inRange(hsv, np.array([0, 95, 95]), np.array([13, 255, 255]))
    mask_b = cv2.inRange(hsv, np.array([174, 95, 95]), np.array([179, 255, 255]))
    coral = cv2.bitwise_or(mask_a, mask_b)
    coral = cv2.morphologyEx(coral, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

    contours, _ = cv2.findContours(coral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    marks = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 28:
            continue
        moments = cv2.moments(contour)
        if not moments["m00"]:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cx = moments["m10"] / moments["m00"]
        cy = moments["m01"] / moments["m00"]
        radius = math.hypot(cx - 512, cy - 512)
        clock_angle = (math.degrees(math.atan2(cy - 512, cx - 512)) + 90) % 360
        marks.append({
            "area": round(area, 1),
            "bbox": [x, y, w, h],
            "center": [round(cx, 1), round(cy, 1)],
            "radius": round(radius, 1),
            "clock_angle": round(clock_angle, 1),
        })
    marks.sort(key=lambda item: (-item["area"], item["clock_angle"]))

    pixels = rectified[coral > 0]
    median_bgr = np.median(pixels, axis=0).astype(int) if len(pixels) else np.array([79, 104, 255])
    color = f"#{median_bgr[2]:02x}{median_bgr[1]:02x}{median_bgr[0]:02x}"
    return marks, color


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path("/private/tmp/pixel5-cv"))
    args = parser.parse_args()

    image = cv2.imread(str(args.source), cv2.IMREAD_COLOR)
    if image is None:
        raise SystemExit(f"Could not read {args.source}")

    center, axes, angle, contour = find_face_ellipse(image)
    rectified, matrix = rectify(image, center, axes, angle)
    coral_marks, coral_color = extract_coral_geometry(rectified)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    overlay = image.copy()
    cv2.ellipse(overlay, (center, axes, angle), (74, 255, 80), 4, cv2.LINE_AA)
    cv2.drawContours(overlay, [contour], -1, (255, 160, 45), 2, cv2.LINE_AA)
    cv2.imwrite(str(args.out_dir / "ellipse-fit.png"), overlay)
    cv2.imwrite(str(args.out_dir / "rectified-face.png"), rectified)
    cv2.imwrite(str(args.out_dir / "source-exact.png"), image, [cv2.IMWRITE_PNG_COMPRESSION, 9])

    report = {
        "source": str(args.source),
        "source_size": [int(image.shape[1]), int(image.shape[0])],
        "ellipse": {
            "center": [round(center[0], 2), round(center[1], 2)],
            "axes": [round(axes[0], 2), round(axes[1], 2)],
            "angle_degrees": round(angle, 3),
        },
        "affine_matrix": np.round(matrix, 6).tolist(),
        "coral_median": coral_color,
        "coral_marks": coral_marks,
    }
    (args.out_dir / "measurements.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
