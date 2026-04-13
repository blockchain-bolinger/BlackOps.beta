#!/usr/bin/env python3
"""
Integration Tests für Tool-Integration
"""

import unittest
import tempfile
import os
from pathlib import Path

from tools.recon.social_hunter_v7 import SocialHunterV7
from tools.offensive.airstrike import AirStrike
from core.session_manager import SessionManager
from core.report_generator import ReportGenerator

class TestToolIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        
        # Setup test environment
        os.environ['BLACKOPS_TEST'] = '1'
        
        # Create test configs
        config_dir = Path(self.temp_dir) / "data/configs"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        # Create test social sites config
        test_social_config = {
            "social_media": {
                "test_site": {
                    "url": "https://test.com/{}",
                    "api_endpoint": "https://api.test.com/{}"
                }
            }
        }
        
        with open(config_dir / "social_sites.json", 'w') as f:
            import json
            json.dump(test_social_config, f)
    
    def test_session_tool_integration(self):
        """Testet Session-Management mit Tools"""
        session_manager = SessionManager()
        
        # Create session for tool
        session_id = session_manager.create_session(
            user="test_user",
            tool="SocialHunterV7",
            target="test_target",
            description="Integration test"
        )
        
        self.assertIsNotNone(session_id)
        
        # Add tool logs to session
        success = session_manager.add_log(
            session_id,
            "tool_execution",
            "SocialHunterV7 executed successfully"
        )
        
        self.assertTrue(success)
        
        # End session
        success = session_manager.end_session(session_id)
        self.assertTrue(success)
        
        # Verify session data
        session = session_manager.get_session(session_id)
        self.assertEqual(session['status'], 'completed')
        self.assertEqual(len(session['logs']), 1)
    
    def test_report_tool_integration(self):
        """Testet Report-Generierung mit Tool-Daten"""
        report_generator = ReportGenerator()
        
        # Create test tool data
        tool_data = {
            'target': 'test.example.com',
            'tester': 'integration_test',
            'scope': 'Full scope test',
            'executive_summary': 'Test summary',
            'findings': [
                {
                    'severity': 'high',
                    'vulnerability': 'SQL Injection',
                    'description': 'Test vulnerability',
                    'risk': 'High risk',
                    'remediation': 'Fix query parameters'
                }
            ],
            'recommendations': [
                'Implement input validation',
                'Use prepared statements'
            ]
        }
        
        # Generate report
        report_path = report_generator.generate_pentest_report(
            tool_data,
            format="json"
        )
        
        self.assertTrue(os.path.exists(report_path))
        
        # Verify report content
        import json
        with open(report_path, 'r') as f:
            report_data = json.load(f)
        
        self.assertEqual(report_data['metadata']['target'], 'test.example.com')
        self.assertEqual(len(report_data['findings']), 1)
    
    def test_ethics_tool_integration(self):
        """Testet Ethics-Enforcement mit Tools"""
        from core.ethics_enforcer import EthicsEnforcer
        
        ethics = EthicsEnforcer()
        
        # Create test ethics config
        test_config = {
            "rules": {
                "no_illegal_activities": True
            },
            "restrictions": {
                "forbidden_targets": ["*.gov"],
                "allowed_actions": ["security_testing"]
            }
        }
        
        config_path = Path(self.temp_dir) / "ethics_config.json"
        with open(config_path, 'w') as f:
            import json
            json.dump(test_config, f)
        
        # Test target validation
        self.assertTrue(ethics.check_target("example.com"))
        
        # Tool should respect ethics
        social_hunter = SocialHunterV7()
        
        # Mock approval for testing
        import builtins
        original_input = builtins.input
        
        def mock_input(prompt):
            return "yes"
        
        builtins.input = mock_input
        
        try:
            # Test with valid target
            results = social_hunter.search_username("testuser")
            self.assertIsInstance(results, dict)
        finally:
            builtins.input = original_input

if __name__ == '__main__':
    unittest.main()