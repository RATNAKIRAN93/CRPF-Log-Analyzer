"""
Tests for the CRPF Log Analyzer Agent Module
"""
import pytest
from datetime import datetime
from agent import LogAnalysisAgent, log_agent


class TestLogAnalysisAgent:
    """Tests for the LogAnalysisAgent class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.agent = LogAnalysisAgent()
        self.sample_logs = [
            {
                "timestamp": "2024-01-15T10:00:00Z",
                "endpoint": "endpoint-1",
                "level": "INFO",
                "message": "User logged in",
                "user": "alice",
                "src_ip": "10.0.1.100",
                "dest_ip": "192.168.1.50",
                "pid": 1234
            },
            {
                "timestamp": "2024-01-15T10:01:00Z",
                "endpoint": "endpoint-1",
                "level": "ERROR",
                "message": "Failed password attempt",
                "user": "bob",
                "src_ip": "10.0.2.100",
                "dest_ip": "192.168.1.50",
                "pid": 1235
            },
            {
                "timestamp": "2024-01-15T10:02:00Z",
                "endpoint": "endpoint-2",
                "level": "WARN",
                "message": "Unusual network connection",
                "user": "system",
                "src_ip": "10.0.3.100",
                "dest_ip": "192.168.2.50",
                "pid": 1236
            },
            {
                "timestamp": "2024-01-15T10:03:00Z",
                "endpoint": "endpoint-1",
                "level": "ERROR",
                "message": "Service crashed",
                "user": "admin",
                "src_ip": "10.0.1.101",
                "dest_ip": "192.168.1.51",
                "pid": 1237
            },
            {
                "timestamp": "2024-01-15T10:04:00Z",
                "endpoint": "endpoint-2",
                "level": "INFO",
                "message": "Configuration changed",
                "user": "admin",
                "src_ip": "10.0.1.102",
                "dest_ip": "192.168.1.52",
                "pid": 1238
            }
        ]

    def test_analyze_empty_logs(self):
        """Test analysis with empty log list."""
        result = self.agent.analyze_logs([])
        assert result["status"] == "no_data"
        assert "timestamp" in result

    def test_analyze_logs_basic(self):
        """Test basic log analysis."""
        result = self.agent.analyze_logs(self.sample_logs)

        assert result["total_logs_analyzed"] == 5
        assert "summary" in result
        assert "severity_distribution" in result
        assert "threats_detected" in result
        assert "anomalies" in result
        assert "endpoint_analysis" in result
        assert "user_activity" in result
        assert "recommendations" in result
        assert "risk_score" in result
        assert 0 <= result["risk_score"] <= 100

    def test_severity_distribution(self):
        """Test severity distribution calculation."""
        result = self.agent.analyze_logs(self.sample_logs)
        severity = result["severity_distribution"]

        assert "distribution" in severity
        assert "weighted_score" in severity
        assert "average_severity" in severity

        # Check that distribution contains expected levels
        distribution = severity["distribution"]
        assert "INFO" in distribution
        assert "ERROR" in distribution
        assert "WARN" in distribution

    def test_threat_detection(self):
        """Test threat detection capabilities."""
        result = self.agent.analyze_logs(self.sample_logs)
        threats = result["threats_detected"]

        # Should detect failed password attempt
        threat_types = [t["threat_type"] for t in threats]
        assert "brute_force" in threat_types  # "Failed password attempt"
        assert "network_anomaly" in threat_types  # "Unusual network connection"
        assert "service_failure" in threat_types  # "Service crashed"
        assert "config_change" in threat_types  # "Configuration changed"

    def test_endpoint_analysis(self):
        """Test endpoint analysis."""
        result = self.agent.analyze_logs(self.sample_logs)
        endpoints = result["endpoint_analysis"]

        assert "endpoint-1" in endpoints
        assert "endpoint-2" in endpoints
        assert endpoints["endpoint-1"]["total_events"] == 3
        assert endpoints["endpoint-2"]["total_events"] == 2

    def test_user_activity_analysis(self):
        """Test user activity analysis."""
        result = self.agent.analyze_logs(self.sample_logs)
        users = result["user_activity"]

        assert "alice" in users
        assert "bob" in users
        assert "admin" in users
        assert users["admin"]["total_events"] == 2

    def test_recommendations_generated(self):
        """Test that recommendations are generated."""
        result = self.agent.analyze_logs(self.sample_logs)
        recommendations = result["recommendations"]

        assert len(recommendations) > 0
        for rec in recommendations:
            assert "priority" in rec
            assert "action" in rec
            assert "description" in rec

    def test_threat_summary(self):
        """Test quick threat summary."""
        summary = self.agent.get_threat_summary(self.sample_logs)

        assert "total_threats" in summary
        assert "critical" in summary
        assert "high" in summary
        assert "medium" in summary
        assert "threat_types" in summary
        assert summary["total_threats"] >= 0

    def test_summarize_for_report(self):
        """Test report generation."""
        report = self.agent.summarize_for_report(self.sample_logs)

        assert isinstance(report, str)
        assert "CRPF LOG ANALYSIS REPORT" in report
        assert "Risk Score:" in report
        assert "SEVERITY DISTRIBUTION:" in report
        assert "THREATS DETECTED:" in report
        assert "RECOMMENDATIONS:" in report

    def test_risk_score_calculation(self):
        """Test risk score calculation."""
        # Create logs with high-risk events
        high_risk_logs = [
            {
                "timestamp": "2024-01-15T10:00:00Z",
                "endpoint": "endpoint-1",
                "level": "ERROR",
                "message": "Failed password attempt",
                "user": "attacker",
                "src_ip": "10.0.1.100",
                "dest_ip": "192.168.1.50",
                "pid": 1234
            }
        ] * 10  # Multiple failed attempts

        result = self.agent.analyze_logs(high_risk_logs)
        # Risk score should be higher due to multiple threats
        assert result["risk_score"] > 0

    def test_anomaly_detection_high_error_rate(self):
        """Test anomaly detection for high error rate."""
        # Create logs with high error rate (>20%)
        error_logs = [
            {"timestamp": "2024-01-15T10:00:00Z", "level": "ERROR", "message": "Error", "user": "test", "endpoint": "e1"}
            for _ in range(5)
        ] + [
            {"timestamp": "2024-01-15T10:00:00Z", "level": "INFO", "message": "Info", "user": "test", "endpoint": "e1"}
            for _ in range(5)
        ]

        result = self.agent.analyze_logs(error_logs)
        anomalies = result["anomalies"]

        # Should detect high error rate (50%)
        anomaly_types = [a["type"] for a in anomalies]
        assert "high_error_rate" in anomaly_types

    def test_anomaly_detection_brute_force(self):
        """Test anomaly detection for brute force attempts."""
        # Create logs with multiple failed login attempts from same user
        brute_force_logs = [
            {
                "timestamp": "2024-01-15T10:00:00Z",
                "level": "ERROR",
                "message": "Failed password attempt",
                "user": "victim",
                "src_ip": f"10.0.1.{i}",
                "endpoint": "endpoint-1"
            }
            for i in range(10)
        ]

        result = self.agent.analyze_logs(brute_force_logs)
        anomalies = result["anomalies"]

        # Should detect brute force attempt
        anomaly_types = [a["type"] for a in anomalies]
        assert "brute_force_attempt" in anomaly_types

    def test_analysis_history(self):
        """Test that analysis history is tracked."""
        initial_count = len(self.agent.analysis_history)
        self.agent.analyze_logs(self.sample_logs)
        assert len(self.agent.analysis_history) == initial_count + 1

    def test_singleton_instance(self):
        """Test that log_agent singleton is available."""
        assert log_agent is not None
        assert isinstance(log_agent, LogAnalysisAgent)


class TestThreatPatterns:
    """Tests for threat pattern matching."""

    def setup_method(self):
        """Set up test fixtures."""
        self.agent = LogAnalysisAgent()

    def test_detect_sql_injection(self):
        """Test SQL injection pattern detection."""
        logs = [
            {
                "timestamp": "2024-01-15T10:00:00Z",
                "level": "ERROR",
                "message": "SQL injection attempt detected",
                "user": "attacker",
                "endpoint": "endpoint-1"
            }
        ]
        threats = self.agent._detect_threats(logs)
        threat_types = [t["threat_type"] for t in threats]
        assert "attack" in threat_types

    def test_detect_malware(self):
        """Test malware pattern detection."""
        logs = [
            {
                "timestamp": "2024-01-15T10:00:00Z",
                "level": "ERROR",
                "message": "Malware detected in file",
                "user": "scanner",
                "endpoint": "endpoint-1"
            }
        ]
        threats = self.agent._detect_threats(logs)
        threat_types = [t["threat_type"] for t in threats]
        assert "malware" in threat_types


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
