"""Render report/report.html to PDF with Chromium (Playwright). Run: python calcs/make_report.py"""
import os
from playwright.sync_api import sync_playwright
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(root, "report", "report.html")
out = os.path.join(root, "report", "5MWp_solar_design_report_DRAFT.pdf")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto("file://" + src); pg.wait_for_load_state("networkidle")
    pg.pdf(path=out, format="A4", print_background=True, prefer_css_page_size=True)
    b.close()
print(out)
