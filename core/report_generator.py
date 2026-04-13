"""
Report Generator für Black Ops Framework
"""

import json
import yaml
import csv
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class ReportGenerator:
    def __init__(self):
        self.templates_dir = Path("data/templates/report_templates")
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_pentest_report(self, data: Dict, format: str = "pdf") -> str:
        """Generiert Pentest-Report"""
        report_id = f"pentest_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if format == "pdf":
            return self._generate_pdf_pentest_report(report_id, data)
        elif format == "html":
            return self._generate_html_pentest_report(report_id, data)
        elif format == "json":
            return self._generate_json_pentest_report(report_id, data)
        else:
            return self._generate_markdown_pentest_report(report_id, data)
    
    def _generate_pdf_pentest_report(self, report_id: str, data: Dict) -> str:
        """Generiert PDF Report"""
        filename = f"{report_id}.pdf"
        filepath = self.reports_dir / "pentest" / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        doc = SimpleDocTemplate(str(filepath), pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30
        )
        story.append(Paragraph("Penetration Test Report", title_style))
        
        # Metadata
        meta_data = [
            ["Report ID:", report_id],
            ["Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ["Target:", data.get('target', 'N/A')],
            ["Tester:", data.get('tester', 'N/A')],
            ["Scope:", data.get('scope', 'N/A')]
        ]
        
        meta_table = Table(meta_data, colWidths=[1.5*inch, 4*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(meta_table)
        story.append(Spacer(1, 20))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", styles['Heading2']))
        story.append(Paragraph(
            data.get('executive_summary', 'No summary provided.'),
            styles['Normal']
        ))
        story.append(Spacer(1, 12))
        
        # Findings
        story.append(Paragraph("Findings", styles['Heading2']))
        
        findings = data.get('findings', [])
        if findings:
            findings_data = [["Severity", "Vulnerability", "Description", "Risk"]]
            
            for finding in findings:
                findings_data.append([
                    finding.get('severity', 'N/A'),
                    finding.get('vulnerability', 'N/A'),
                    finding.get('description', 'N/A'),
                    finding.get('risk', 'N/A')
                ])
            
            findings_table = Table(findings_data, colWidths=[0.8*inch, 1.5*inch, 2.5*inch, 0.8*inch])
            findings_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(findings_table)
        
        story.append(Spacer(1, 12))
        
        # Recommendations
        story.append(Paragraph("Recommendations", styles['Heading2']))
        
        recommendations = data.get('recommendations', [])
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                story.append(Paragraph(f"{i}. {rec}", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        return str(filepath)
    
    def _generate_html_pentest_report(self, report_id: str, data: Dict) -> str:
        """Generiert HTML Report"""
        filename = f"{report_id}.html"
        filepath = self.reports_dir / "pentest" / filename
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Penetration Test Report - {report_id}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background-color: #333; color: white; padding: 20px; }}
                .metadata {{ margin: 20px 0; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .critical {{ color: red; font-weight: bold; }}
                .high {{ color: orange; }}
                .medium {{ color: yellow; }}
                .low {{ color: green; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Penetration Test Report</h1>
                <p>Report ID: {report_id}</p>
                <p>Date: {date}</p>
            </div>
            
            <div class="metadata">
                <h2>Test Information</h2>
                <p><strong>Target:</strong> {target}</p>
                <p><strong>Tester:</strong> {tester}</p>
                <p><strong>Scope:</strong> {scope}</p>
            </div>
            
            <div class="summary">
                <h2>Executive Summary</h2>
                <p>{executive_summary}</p>
            </div>
            
            <div class="findings">
                <h2>Findings</h2>
                <table>
                    <tr>
                        <th>Severity</th>
                        <th>Vulnerability</th>
                        <th>Description</th>
                        <th>Risk</th>
                        <th>Remediation</th>
                    </tr>
                    {findings_rows}
                </table>
            </div>
            
            <div class="recommendations">
                <h2>Recommendations</h2>
                <ol>
                    {recommendations_list}
                </ol>
            </div>
            
            <div class="footer">
                <hr>
                <p>Generated by Black Ops Framework v2.2</p>
                <p>This report is confidential and intended for authorized personnel only.</p>
            </div>
        </body>
        </html>
        """
        
        # Prepare findings rows
        findings_rows = ""
        for finding in data.get('findings', []):
            severity_class = finding.get('severity', '').lower()
            findings_rows += f"""
            <tr>
                <td class="{severity_class}">{finding.get('severity', 'N/A')}</td>
                <td>{finding.get('vulnerability', 'N/A')}</td>
                <td>{finding.get('description', 'N/A')}</td>
                <td>{finding.get('risk', 'N/A')}</td>
                <td>{finding.get('remediation', 'N/A')}</td>
            </tr>
            """
        
        # Prepare recommendations list
        recommendations_list = ""
        for rec in data.get('recommendations', []):
            recommendations_list += f"<li>{rec}</li>"
        
        html_content = html_template.format(
            report_id=report_id,
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            target=data.get('target', 'N/A'),
            tester=data.get('tester', 'N/A'),
            scope=data.get('scope', 'N/A'),
            executive_summary=data.get('executive_summary', 'No summary provided.'),
            findings_rows=findings_rows,
            recommendations_list=recommendations_list
        )
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        return str(filepath)
    
    def _generate_json_pentest_report(self, report_id: str, data: Dict) -> str:
        """Generiert JSON Report"""
        filename = f"{report_id}.json"
        filepath = self.reports_dir / "pentest" / filename
        
        report_data = {
            'report_id': report_id,
            'generated': datetime.now().isoformat(),
            'metadata': {
                'target': data.get('target'),
                'tester': data.get('tester'),
                'scope': data.get('scope'),
                'tools_used': data.get('tools_used', [])
            },
            'executive_summary': data.get('executive_summary'),
            'findings': data.get('findings', []),
            'recommendations': data.get('recommendations', []),
            'technical_details': data.get('technical_details', {}),
            'evidence': data.get('evidence', [])
        }
        
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        return str(filepath)
    
    def _generate_markdown_pentest_report(self, report_id: str, data: Dict) -> str:
        """Generiert Markdown Report"""
        filename = f"{report_id}.md"
        filepath = self.reports_dir / "pentest" / filename
        
        md_content = f"""# Penetration Test Report

## Report ID: {report_id}
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Target:** {data.get('target', 'N/A')}
**Tester:** {data.get('tester', 'N/A')}
**Scope:** {data.get('scope', 'N/A')}

## Executive Summary

{data.get('executive_summary', 'No summary provided.')}

## Findings

| Severity | Vulnerability | Description | Risk | Remediation |
|----------|---------------|-------------|------|-------------|
"""
        
        for finding in data.get('findings', []):
            severity = finding.get('severity', 'N/A')
            md_content += f"| {severity} | {finding.get('vulnerability', 'N/A')} | {finding.get('description', 'N/A')} | {finding.get('risk', 'N/A')} | {finding.get('remediation', 'N/A')} |\n"
        
        md_content += "\n## Recommendations\n\n"
        
        for i, rec in enumerate(data.get('recommendations', []), 1):
            md_content += f"{i}. {rec}\n"
        
        md_content += "\n---\n*Generated by Black Ops Framework v2.2*"
        
        with open(filepath, 'w') as f:
            f.write(md_content)
        
        return str(filepath)
    
    def generate_vulnerability_report(self, scan_data: Dict) -> str:
        """Generiert Vulnerability Report"""
        report_id = f"vuln_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        filepath = self.reports_dir / "scans" / f"{report_id}.json"
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        report_data = {
            'report_id': report_id,
            'scan_date': datetime.now().isoformat(),
            'target': scan_data.get('target'),
            'scan_type': scan_data.get('scan_type'),
            'vulnerabilities': scan_data.get('vulnerabilities', []),
            'statistics': {
                'total': len(scan_data.get('vulnerabilities', [])),
                'critical': sum(1 for v in scan_data.get('vulnerabilities', []) 
                              if v.get('severity') == 'critical'),
                'high': sum(1 for v in scan_data.get('vulnerabilities', []) 
                           if v.get('severity') == 'high'),
                'medium': sum(1 for v in scan_data.get('vulnerabilities', []) 
                             if v.get('severity') == 'medium'),
                'low': sum(1 for v in scan_data.get('vulnerabilities', []) 
                          if v.get('severity') == 'low')
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        return str(filepath)