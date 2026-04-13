#!/usr/bin/env python3
import json
import csv
import os
from datetime import datetime
from jinja2 import Template

class ReportGenerator:
    """Erzeugt Reports aus Scan-Daten in verschiedenen Formaten."""

    def __init__(self, scan_data, tool_name, output_dir="reports/exports"):
        self.data = scan_data
        self.tool = tool_name
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.base_name = f"{self.tool}_{self.timestamp}"
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def to_json(self):
        """Export als JSON"""
        path = os.path.join(self.output_dir, f"{self.base_name}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        return path

    def to_csv(self, key="results"):
        """Export flacher Daten als CSV (erwartet Liste von Dicts unter 'key')"""
        items = self.data.get(key, [])
        if not items:
            return None
        path = os.path.join(self.output_dir, f"{self.base_name}.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=items[0].keys())
            writer.writeheader()
            writer.writerows(items)
        return path

    def to_html(self):
        """Export als HTML mit Jinja2-Template"""
        template_str = """<!DOCTYPE html>
<html>
<head><title>Report: {{ tool }}</title></head>
<body>
    <h1>BlackOps Report: {{ tool }}</h1>
    <p>Erstellt am: {{ timestamp }}</p>
    <pre>{{ data | tojson(indent=2) }}</pre>
</body>
</html>"""
        template = Template(template_str)
        html = template.render(data=self.data, tool=self.tool, timestamp=self.timestamp)
        path = os.path.join(self.output_dir, f"{self.base_name}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return path

    def to_pdf(self):
        """Export als PDF via weasyprint (HTML → PDF)"""
        try:
            from weasyprint import HTML
            html_file = self.to_html()
            pdf_file = os.path.join(self.output_dir, f"{self.base_name}.pdf")
            HTML(filename=html_file).write_pdf(pdf_file)
            return pdf_file
        except ImportError:
            print("[-] weasyprint nicht installiert. PDF-Export nicht verfügbar.")
            return None

if __name__ == "__main__":
    # Beispielnutzung
    sample_data = {
        "host": "192.168.1.1",
        "results": [
            {"port": 80, "service": "http", "banner": "Apache"},
            {"port": 22, "service": "ssh", "banner": "OpenSSH"}
        ]
    }
    rg = ReportGenerator(sample_data, "portscan")
    print("JSON:", rg.to_json())
    print("CSV:", rg.to_csv())
    print("HTML:", rg.to_html())
    print("PDF:", rg.to_pdf())