"""
Tests for the CRPF Log Analyzer FastAPI Endpoints
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import the app
from main import app

client = TestClient(app)


class TestAgentEndpoints:
    """Tests for the agent API endpoints."""

    def test_agent_status(self):
        """Test the agent status endpoint."""
        response = client.get("/agent/status")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "active"
        assert data["agent_type"] == "LogAnalysisAgent"
        assert "capabilities" in data
        assert "threat_detection" in data["capabilities"]
        assert "anomaly_detection" in data["capabilities"]

    def test_health_check(self):
        """Test the health check endpoint."""
        # Mock the OpenSearch client to avoid connection issues
        with patch("main.client.cluster") as mock_cluster:
            mock_cluster.health.return_value = {"status": "green"}
            response = client.get("/health")
            assert response.status_code == 200

            data = response.json()
            assert "status" in data
            assert "components" in data
            assert data["components"]["api"] == "healthy"
            assert data["components"]["agent"] == "healthy"

    def test_analyze_quick_no_data(self):
        """Test quick analysis with no data."""
        with patch("main.fetch_logs") as mock_fetch:
            mock_fetch.return_value = []
            response = client.get("/agent/analyze/quick?q=*&hours=24")
            assert response.status_code == 200

            data = response.json()
            assert data["status"] == "no_data"

    def test_analyze_quick_with_data(self):
        """Test quick analysis with sample data."""
        sample_logs = [
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
            }
        ]

        with patch("main.fetch_logs") as mock_fetch:
            mock_fetch.return_value = sample_logs
            response = client.get("/agent/analyze/quick")
            assert response.status_code == 200

            data = response.json()
            assert "total_logs_analyzed" in data
            assert "severity_distribution" in data
            assert "threats_detected" in data
            assert "risk_score" in data

    def test_threats_quick_endpoint(self):
        """Test quick threats endpoint."""
        sample_logs = [
            {
                "timestamp": "2024-01-15T10:00:00Z",
                "level": "ERROR",
                "message": "Failed password attempt",
                "user": "attacker",
                "endpoint": "endpoint-1"
            }
        ]

        with patch("main.fetch_logs") as mock_fetch:
            mock_fetch.return_value = sample_logs
            response = client.get("/agent/threats/quick")
            assert response.status_code == 200

            data = response.json()
            assert "total_threats" in data
            assert "logs_analyzed" in data

    def test_report_endpoint(self):
        """Test report generation endpoint."""
        sample_logs = [
            {
                "timestamp": "2024-01-15T10:00:00Z",
                "level": "INFO",
                "message": "User logged in",
                "user": "alice",
                "endpoint": "endpoint-1"
            }
        ]

        with patch("main.fetch_logs") as mock_fetch:
            mock_fetch.return_value = sample_logs
            response = client.get("/agent/report")
            assert response.status_code == 200
            assert "CRPF LOG ANALYSIS REPORT" in response.text

    def test_endpoints_analysis(self):
        """Test endpoints analysis."""
        sample_logs = [
            {
                "timestamp": "2024-01-15T10:00:00Z",
                "level": "INFO",
                "message": "Event",
                "user": "alice",
                "endpoint": "endpoint-1"
            },
            {
                "timestamp": "2024-01-15T10:01:00Z",
                "level": "ERROR",
                "message": "Error",
                "user": "bob",
                "endpoint": "endpoint-2"
            }
        ]

        with patch("main.fetch_logs") as mock_fetch:
            mock_fetch.return_value = sample_logs
            response = client.get("/agent/endpoints")
            assert response.status_code == 200

            data = response.json()
            assert "endpoints" in data
            assert "total_logs" in data

    def test_users_analysis(self):
        """Test user activity analysis."""
        sample_logs = [
            {
                "timestamp": "2024-01-15T10:00:00Z",
                "level": "INFO",
                "message": "Event",
                "user": "alice",
                "endpoint": "endpoint-1"
            }
        ]

        with patch("main.fetch_logs") as mock_fetch:
            mock_fetch.return_value = sample_logs
            response = client.get("/agent/users")
            assert response.status_code == 200

            data = response.json()
            assert "users" in data

    def test_anomalies_endpoint(self):
        """Test anomalies detection endpoint."""
        sample_logs = [
            {"timestamp": "2024-01-15T10:00:00Z", "level": "ERROR", "message": "Error", "user": "test", "endpoint": "e1"}
            for _ in range(10)
        ]

        with patch("main.fetch_logs") as mock_fetch:
            mock_fetch.return_value = sample_logs
            response = client.get("/agent/anomalies")
            assert response.status_code == 200

            data = response.json()
            assert "anomalies" in data
            assert "risk_score" in data

    def test_recommendations_endpoint(self):
        """Test recommendations endpoint."""
        sample_logs = [
            {
                "timestamp": "2024-01-15T10:00:00Z",
                "level": "ERROR",
                "message": "Failed password attempt",
                "user": "attacker",
                "endpoint": "endpoint-1"
            }
        ]

        with patch("main.fetch_logs") as mock_fetch:
            mock_fetch.return_value = sample_logs
            response = client.get("/agent/recommendations")
            assert response.status_code == 200

            data = response.json()
            assert "recommendations" in data
            assert len(data["recommendations"]) > 0

    def test_history_endpoint(self):
        """Test analysis history endpoint."""
        response = client.get("/agent/history")
        assert response.status_code == 200

        data = response.json()
        assert "total_analyses" in data
        assert "history" in data

    def test_analyze_post_endpoint(self):
        """Test POST analysis endpoint."""
        sample_logs = [
            {
                "timestamp": "2024-01-15T10:00:00Z",
                "level": "INFO",
                "message": "User logged in",
                "user": "alice",
                "endpoint": "endpoint-1"
            }
        ]

        with patch("main.fetch_logs") as mock_fetch:
            mock_fetch.return_value = sample_logs
            response = client.post(
                "/agent/analyze",
                json={"query": "*", "time_range_hours": 24, "max_logs": 100}
            )
            assert response.status_code == 200

            data = response.json()
            assert "total_logs_analyzed" in data

    def test_threats_post_endpoint(self):
        """Test POST threats endpoint."""
        sample_logs = [
            {
                "timestamp": "2024-01-15T10:00:00Z",
                "level": "ERROR",
                "message": "Unauthorized access attempt",
                "user": "attacker",
                "endpoint": "endpoint-1"
            }
        ]

        with patch("main.fetch_logs") as mock_fetch:
            mock_fetch.return_value = sample_logs
            response = client.post(
                "/agent/threats",
                json={"query": "*", "max_logs": 100}
            )
            assert response.status_code == 200

            data = response.json()
            assert "total_threats" in data


class TestSearchEndpoint:
    """Tests for the original search endpoint."""

    def test_search_endpoint(self):
        """Test the search endpoint."""
        with patch("main.client.search") as mock_search:
            mock_search.return_value = {
                "hits": {
                    "total": {"value": 1},
                    "hits": [{"_source": {"message": "test"}}]
                }
            }
            response = client.get("/search?q=test")
            assert response.status_code == 200

            data = response.json()
            assert "count" in data
            assert "results" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
