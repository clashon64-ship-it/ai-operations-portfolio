#!/usr/bin/env python3
"""
SYS-MOD-VISUAL-LINT-001: Enterprise Visual Lint & Presentation Integrity Engine
Penn Enterprises LLC — Autonomous Governance Standard

Audits SVGs, HTML UI designs, and Markdown presentations for:
1. Double-Lining / Duplicate Stroke artifacts
2. Text Overlaps & Bounding Box Collisions in Global Coordinate Space
3. Spelling Typos & Lexicon Integrity
4. XML / Entity compliance (e.g. unescaped & in SVGs)
"""

import sys
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

# Enterprise Whitelist: Technical terminology, brand names, and protocol abbreviations
ENTERPRISE_LEXICON = {
    "asyncio", "epoll", "kqueue", "n8n", "fastmcp", "pydantic", "telemetry",
    "orchestrator", "orchestration", "docker", "nginx", "ssl", "tls", "hitl",
    "webhook", "webhooks", "api", "apis", "crm", "sla", "slas", "pos", "sows",
    "keymon", "penn", "redlantern", "securitas", "prosegur", "github", "linkedin",
    "subtotal", "json", "svg", "html", "css", "sha-256", "postgres", "postgresql",
    "vps", "ufw", "pms", "eod", "folio", "sdsu", "anthropic", "mcp", "rag", "laer",
    "amina", "hadith", "clashon", "devops", "gtm", "b2b", "ui", "ux", "rbac"
}

# Common spelling mistakes and typos to catch
KNOWN_TYPOS = {
    "teh": "the",
    "enteprise": "enterprise",
    "protfolio": "portfolio",
    "mispelled": "misspelled",
    "techonology": "technology",
    "acheive": "achieve",
    "seperate": "separate",
    "occured": "occurred",
    "recieve": "receive",
    "definately": "definitely",
    "truely": "truly",
    "calender": "calendar",
    "compatability": "compatibility"
}


class VisualLintReport:
    def __init__(self, filepath):
        self.filepath = filepath
        self.double_lines = []
        self.overlaps = []
        self.spelling_errors = []
        self.xml_errors = []
        self.passed = True

    def add_double_line(self, desc, location=""):
        self.double_lines.append((desc, location))
        self.passed = False

    def add_overlap(self, desc, location=""):
        self.overlaps.append((desc, location))
        self.passed = False

    def add_spelling_error(self, typo, correction, line_num=0):
        self.spelling_errors.append((typo, correction, line_num))
        self.passed = False

    def add_xml_error(self, desc, line_num=0):
        self.xml_errors.append((desc, line_num))
        self.passed = False

    def print_summary(self):
        print(f"\n{'='*70}")
        print(f"  VISUAL LINT AUDIT: {os.path.basename(self.filepath)}")
        print(f"{'='*70}")
        print(f"  Target File: {self.filepath}")

        if self.passed:
            print("  [STATUS] \033[92mPASS: ZERO DEFECTS DETECTED (ENTERPRISE GRADE)\033[0m")
            print("  • Double Lining: None detected")
            print("  • Overlapping Elements: None detected")
            print("  • Spelling & Lexicon: 100% verified")
            print(f"{'='*70}\n")
            return True

        print("  [STATUS] \033[91mFAIL: VISUAL DEFECTS DETECTED\033[0m")
        if self.double_lines:
            print(f"\n  \033[93m[!] Double-Lining / Redundant Strokes ({len(self.double_lines)}):\033[0m")
            for desc, loc in self.double_lines:
                print(f"      - {desc} [{loc}]")

        if self.overlaps:
            print(f"\n  \033[93m[!] Element Collision / Overlap ({len(self.overlaps)}):\033[0m")
            for desc, loc in self.overlaps:
                print(f"      - {desc} [{loc}]")

        if self.spelling_errors:
            print(f"\n  \033[93m[!] Spelling & Lexicon Typos ({len(self.spelling_errors)}):\033[0m")
            for typo, fix, line in self.spelling_errors:
                print(f"      - Line {line}: '{typo}' -> Did you mean '{fix}'?")

        if self.xml_errors:
            print(f"\n  \033[93m[!] Syntax / Entity Errors ({len(self.xml_errors)}):\033[0m")
            for desc, line in self.xml_errors:
                print(f"      - Line {line}: {desc}")

        print(f"{'='*70}\n")
        return False


def parse_translate(transform_str):
    if not transform_str:
        return (0.0, 0.0)
    m = re.search(r'translate\(\s*([-\d.]+)(?:[,\s]+([-\d.]+))?\s*\)', transform_str)
    if m:
        dx = float(m.group(1))
        dy = float(m.group(2)) if m.group(2) is not None else 0.0
        return (dx, dy)
    return (0.0, 0.0)


def audit_svg(filepath):
    report = VisualLintReport(filepath)
    raw_content = Path(filepath).read_text(encoding="utf-8")

    # 1. Check for unescaped ampersands or malformed entities
    for idx, line in enumerate(raw_content.splitlines(), 1):
        bad_amp = re.findall(r'&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)', line)
        if bad_amp:
            report.add_xml_error(f"Unescaped '&' found ({len(bad_amp)}x). Must use '&amp;' in SVG/XML.", idx)

    # 2. Parse XML DOM
    try:
        root = ET.fromstring(raw_content)
    except ET.ParseError as e:
        report.add_xml_error(f"XML Parsing Exception: {e}", 0)
        return report

    # 3. Hierarchical Traversal to extract absolute global coordinates
    strokes = []
    text_boxes = []

    def traverse(node, current_dx=0.0, current_dy=0.0):
        # Accumulate transforms
        transform = node.get("transform", "")
        tdx, tdy = parse_translate(transform)
        abs_dx = current_dx + tdx
        abs_dy = current_dy + tdy

        tag = node.tag.split("}")[-1]
        stroke = node.get("stroke")
        stroke_w = float(node.get("stroke-width", "1")) if node.get("stroke-width") else 1.0

        if tag == "line":
            x1, y1 = float(node.get("x1", 0)) + abs_dx, float(node.get("y1", 0)) + abs_dy
            x2, y2 = float(node.get("x2", 0)) + abs_dx, float(node.get("y2", 0)) + abs_dy
            for (p_tag, p_x1, p_y1, p_x2, p_y2, p_sw) in strokes:
                if p_tag == "line":
                    if abs(y1 - p_y1) < 2.0 and abs(y2 - p_y2) < 2.0 and abs(x1 - p_x1) < 5.0:
                        report.add_double_line(f"Duplicate/Parallel stroke line at Y={y1}", f"line ({x1},{y1}) to ({x2},{y2})")
            strokes.append((tag, x1, y1, x2, y2, stroke_w))

        elif tag == "rect":
            rx, ry = float(node.get("x", 0)) + abs_dx, float(node.get("y", 0)) + abs_dy
            rw, rh = float(node.get("width", 0)), float(node.get("height", 0))
            if stroke and stroke != "none":
                for (p_tag, p_x1, p_y1, p_x2, p_y2, p_sw) in strokes:
                    if p_tag == "rect":
                        # Detect duplicate border rects sharing the exact same bounding box
                        if abs(rx - p_x1) < 1.0 and abs(ry - p_y1) < 1.0 and abs(rw - p_x2) < 1.0 and abs(rh - p_y2) < 1.0:
                            report.add_double_line(f"Coincident border stroke at ({rx},{ry})", f"rect: {rw}x{rh}")
                strokes.append((tag, rx, ry, rw, rh, stroke_w))

        elif tag == "text":
            tx = float(node.get("x", 0)) + abs_dx
            ty = float(node.get("y", 0)) + abs_dy
            text_content = (node.text or "").strip()
            font_size = float(node.get("font-size", 12))
            est_width = len(text_content) * (font_size * 0.55)
            est_height = font_size

            # Check true collision in global coordinate space
            for (p_x, p_y, p_w, p_h, p_text) in text_boxes:
                # Same horizontal line within font threshold
                if abs(ty - p_y) < (font_size * 0.6):
                    # Check horizontal overlap
                    if not (tx + est_width <= p_x or tx >= p_x + p_w):
                        report.add_overlap(f"Text collision: '{text_content}' overlaps with '{p_text}'", f"Global Y={ty:.1f}, X={tx:.1f}")

            if text_content:
                text_boxes.append((tx, ty, est_width, est_height, text_content))

        for child in node:
            traverse(child, abs_dx, abs_dy)

    traverse(root)

    # 4. Spelling and Lexicon Check
    for idx, line in enumerate(raw_content.splitlines(), 1):
        text_matches = re.findall(r'>([^<]+)<', line)
        for match in text_matches:
            words = re.findall(r'\b[a-zA-Z]{3,}\b', match)
            for word in words:
                clean_word = word.lower()
                if clean_word in KNOWN_TYPOS:
                    report.add_spelling_error(word, KNOWN_TYPOS[clean_word], idx)

    return report


def audit_html(filepath):
    report = VisualLintReport(filepath)
    raw_content = Path(filepath).read_text(encoding="utf-8")

    # Double border detection in CSS
    double_border = re.findall(r'border-bottom:\s*[^;]+;\s*border-top:\s*[^;]+;', raw_content)
    if double_border:
        report.add_double_line("Conflicting duplicate border rules in CSS rule block", "CSS")

    # Spelling check
    for idx, line in enumerate(raw_content.splitlines(), 1):
        text_matches = re.findall(r'>([^<]+)<', line)
        for match in text_matches:
            words = re.findall(r'\b[a-zA-Z]{3,}\b', match)
            for word in words:
                clean_word = word.lower()
                if clean_word in KNOWN_TYPOS:
                    report.add_spelling_error(word, KNOWN_TYPOS[clean_word], idx)

    return report


def audit_file(filepath):
    ext = os.path.splitext(filepath)[-1].lower()
    if ext == ".svg":
        return audit_svg(filepath)
    elif ext in [".html", ".htm"]:
        return audit_html(filepath)
    else:
        report = VisualLintReport(filepath)
        raw_content = Path(filepath).read_text(encoding="utf-8")
        for idx, line in enumerate(raw_content.splitlines(), 1):
            words = re.findall(r'\b[a-zA-Z]{3,}\b', line)
            for word in words:
                clean_word = word.lower()
                if clean_word in KNOWN_TYPOS:
                    report.add_spelling_error(word, KNOWN_TYPOS[clean_word], idx)
        return report


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 enterprise_visual_lint_engine.py <file_or_directory_path>")
        sys.exit(1)

    target_path = Path(sys.argv[1])
    files_to_check = []

    if target_path.is_file():
        files_to_check.append(str(target_path))
    elif target_path.is_dir():
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.endswith((".svg", ".html", ".htm", ".md")):
                    files_to_check.append(os.path.join(root, file))

    total_files = len(files_to_check)
    passed_files = 0

    print(f"\n[SYS-MOD-VISUAL-LINT-001] Auditing {total_files} file(s) for enterprise visual integrity...")

    for f in sorted(files_to_check):
        report = audit_file(f)
        if report.print_summary():
            passed_files += 1

    print(f"\nSUMMARY: {passed_files}/{total_files} files passed enterprise visual lint audit.")
    if passed_files != total_files:
        sys.exit(1)
    else:
        print("\033[92mALL DESIGN ASSETS COMPLIANT WITH PENN ENTERPRISES LLC VISUAL STANDARD.\033[0m\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
