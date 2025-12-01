"""
AI Agent Module for CRPF Log Analyzer
Provides intelligent log analysis, anomaly detection, and summarization capabilities.
"""
import os
import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone
from collections import Counter


class LogAnalysisAgent:
    """
    An AI agent for analyzing system logs with intelligent pattern detection,
    anomaly identification, and automated summarization.
    """

    # Severity weights for scoring
    SEVERITY_WEIGHTS = {
        "ERROR": 10,
        "WARN": 5,
        "WARNING": 5,
        "INFO": 1,
        "DEBUG": 0
    }

    # Known threat patterns
    THREAT_PATTERNS = [
        {"pattern": r"failed\s+password", "threat_type": "brute_force", "severity": "high"},
        {"pattern": r"unauthorized\s+access", "threat_type": "unauthorized_access", "severity": "critical"},
        {"pattern": r"unusual\s+network", "threat_type": "network_anomaly", "severity": "medium"},
        {"pattern": r"service\s+crash", "threat_type": "service_failure", "severity": "high"},
        {"pattern": r"configuration\s+changed", "threat_type": "config_change", "severity": "medium"},
        {"pattern": r"file\s+deleted", "threat_type": "data_modification", "severity": "medium"},
        {"pattern": r"root\s+login", "threat_type": "privilege_escalation", "severity": "high"},
        {"pattern": r"malware|virus|trojan", "threat_type": "malware", "severity": "critical"},
        {"pattern": r"sql\s+injection|xss|csrf", "threat_type": "attack", "severity": "critical"},
    ]

    # Anomaly thresholds
    ANOMALY_THRESHOLDS = {
        "error_rate_percent": 20,  # Alert if error rate exceeds 20%
        "events_per_minute": 100,  # Alert if events exceed this rate
        "failed_logins_threshold": 5,  # Alert if failed logins exceed this count
    }

    def __init__(self):
        self.analysis_history: List[Dict[str, Any]] = []

    def analyze_logs(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform comprehensive analysis on a set of logs.

        Args:
            logs: List of log entries to analyze

        Returns:
            Dictionary containing analysis results
        """
        if not logs:
            return {
                "status": "no_data",
                "message": "No logs provided for analysis",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        analysis_result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_logs_analyzed": len(logs),
            "summary": self._generate_summary(logs),
            "severity_distribution": self._analyze_severity(logs),
            "threats_detected": self._detect_threats(logs),
            "anomalies": self._detect_anomalies(logs),
            "endpoint_analysis": self._analyze_endpoints(logs),
            "user_activity": self._analyze_user_activity(logs),
            "recommendations": [],
            "risk_score": 0
        }

        # Calculate overall risk score and generate recommendations
        analysis_result["risk_score"] = self._calculate_risk_score(analysis_result)
        analysis_result["recommendations"] = self._generate_recommendations(analysis_result)

        # Store in history
        self.analysis_history.append({
            "timestamp": analysis_result["timestamp"],
            "logs_count": len(logs),
            "risk_score": analysis_result["risk_score"]
        })

        return analysis_result

    def _generate_summary(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a human-readable summary of the logs."""
        if not logs:
            return {"status": "no_data"}

        messages = [log.get("message", "") for log in logs]
        message_counts = Counter(messages)

        # Get time range
        timestamps = [log.get("timestamp", "") for log in logs if log.get("timestamp")]
        time_range = {
            "earliest": min(timestamps) if timestamps else None,
            "latest": max(timestamps) if timestamps else None
        }

        return {
            "total_events": len(logs),
            "unique_message_types": len(message_counts),
            "most_common_events": message_counts.most_common(5),
            "time_range": time_range
        }

    def _analyze_severity(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the severity distribution of logs."""
        severity_counts = Counter(log.get("level", "UNKNOWN").upper() for log in logs)
        total = len(logs)

        distribution = {
            level: {
                "count": count,
                "percentage": round((count / total) * 100, 2) if total > 0 else 0
            }
            for level, count in severity_counts.items()
        }

        # Calculate weighted severity score
        weighted_score = sum(
            self.SEVERITY_WEIGHTS.get(level, 0) * count
            for level, count in severity_counts.items()
        )

        return {
            "distribution": distribution,
            "weighted_score": weighted_score,
            "average_severity": round(weighted_score / total, 2) if total > 0 else 0
        }

    def _detect_threats(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect potential security threats in logs."""
        threats = []

        for log in logs:
            message = log.get("message", "").lower()
            for threat_pattern in self.THREAT_PATTERNS:
                if re.search(threat_pattern["pattern"], message, re.IGNORECASE):
                    threats.append({
                        "log": log,
                        "threat_type": threat_pattern["threat_type"],
                        "severity": threat_pattern["severity"],
                        "pattern_matched": threat_pattern["pattern"],
                        "timestamp": log.get("timestamp"),
                        "endpoint": log.get("endpoint"),
                        "user": log.get("user")
                    })

        return threats

    def _detect_anomalies(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect anomalies in log patterns."""
        anomalies = []
        total_logs = len(logs)

        if total_logs == 0:
            return anomalies

        # Check error rate
        error_count = sum(1 for log in logs if log.get("level", "").upper() in ["ERROR", "WARN", "WARNING"])
        error_rate = (error_count / total_logs) * 100

        if error_rate > self.ANOMALY_THRESHOLDS["error_rate_percent"]:
            anomalies.append({
                "type": "high_error_rate",
                "description": f"Error rate ({error_rate:.1f}%) exceeds threshold ({self.ANOMALY_THRESHOLDS['error_rate_percent']}%)",
                "severity": "high",
                "value": error_rate,
                "threshold": self.ANOMALY_THRESHOLDS["error_rate_percent"]
            })

        # Check for failed login attempts by user
        failed_logins = [log for log in logs if "failed password" in log.get("message", "").lower()]
        user_failed_logins = Counter(log.get("user") for log in failed_logins)

        for user, count in user_failed_logins.items():
            if count >= self.ANOMALY_THRESHOLDS["failed_logins_threshold"]:
                anomalies.append({
                    "type": "brute_force_attempt",
                    "description": f"User '{user}' has {count} failed login attempts",
                    "severity": "critical",
                    "user": user,
                    "count": count,
                    "threshold": self.ANOMALY_THRESHOLDS["failed_logins_threshold"]
                })

        # Check for unusual source IPs (too many unique IPs from one user)
        user_ips = {}
        for log in logs:
            user = log.get("user")
            src_ip = log.get("src_ip")
            if user and src_ip:
                if user not in user_ips:
                    user_ips[user] = set()
                user_ips[user].add(src_ip)

        for user, ips in user_ips.items():
            if len(ips) > 5:  # User accessing from many different IPs
                anomalies.append({
                    "type": "multiple_source_ips",
                    "description": f"User '{user}' is accessing from {len(ips)} different source IPs",
                    "severity": "medium",
                    "user": user,
                    "ip_count": len(ips),
                    "ips": list(ips)[:10]  # Only show first 10 IPs
                })

        return anomalies

    def _analyze_endpoints(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze activity by endpoint."""
        endpoint_data = {}

        for log in logs:
            endpoint = log.get("endpoint", "unknown")
            if endpoint not in endpoint_data:
                endpoint_data[endpoint] = {
                    "total_events": 0,
                    "error_count": 0,
                    "warn_count": 0,
                    "users": set()
                }

            endpoint_data[endpoint]["total_events"] += 1
            level = log.get("level", "").upper()
            if level == "ERROR":
                endpoint_data[endpoint]["error_count"] += 1
            elif level in ["WARN", "WARNING"]:
                endpoint_data[endpoint]["warn_count"] += 1

            user = log.get("user")
            if user:
                endpoint_data[endpoint]["users"].add(user)

        # Convert sets to lists for JSON serialization
        for endpoint in endpoint_data:
            endpoint_data[endpoint]["users"] = list(endpoint_data[endpoint]["users"])
            endpoint_data[endpoint]["unique_users"] = len(endpoint_data[endpoint]["users"])

        return endpoint_data

    def _analyze_user_activity(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze user activity patterns."""
        user_data = {}

        for log in logs:
            user = log.get("user", "unknown")
            if user not in user_data:
                user_data[user] = {
                    "total_events": 0,
                    "error_count": 0,
                    "endpoints_accessed": set(),
                    "actions": Counter()
                }

            user_data[user]["total_events"] += 1
            level = log.get("level", "").upper()
            if level == "ERROR":
                user_data[user]["error_count"] += 1

            endpoint = log.get("endpoint")
            if endpoint:
                user_data[user]["endpoints_accessed"].add(endpoint)

            message = log.get("message", "")
            if message:
                user_data[user]["actions"][message] += 1

        # Convert for JSON serialization
        for user in user_data:
            user_data[user]["endpoints_accessed"] = list(user_data[user]["endpoints_accessed"])
            user_data[user]["actions"] = dict(user_data[user]["actions"].most_common(5))

        return user_data

    def _calculate_risk_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate an overall risk score (0-100) based on analysis results."""
        score = 0

        # Add points for threats
        threats = analysis.get("threats_detected", [])
        for threat in threats:
            if threat.get("severity") == "critical":
                score += 20
            elif threat.get("severity") == "high":
                score += 10
            elif threat.get("severity") == "medium":
                score += 5

        # Add points for anomalies
        anomalies = analysis.get("anomalies", [])
        for anomaly in anomalies:
            if anomaly.get("severity") == "critical":
                score += 15
            elif anomaly.get("severity") == "high":
                score += 8
            elif anomaly.get("severity") == "medium":
                score += 3

        # Add points based on severity distribution
        severity = analysis.get("severity_distribution", {})
        avg_severity = severity.get("average_severity", 0)
        score += int(avg_severity * 2)

        # Cap at 100
        return min(score, 100)

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []
        risk_score = analysis.get("risk_score", 0)

        # Risk level based recommendations
        if risk_score >= 70:
            recommendations.append({
                "priority": "critical",
                "action": "Immediate investigation required",
                "description": f"Risk score of {risk_score} indicates critical security concerns. Engage incident response team immediately."
            })

        # Threat-based recommendations
        threats = analysis.get("threats_detected", [])
        threat_types = set(t.get("threat_type") for t in threats)

        if "brute_force" in threat_types:
            recommendations.append({
                "priority": "high",
                "action": "Review authentication security",
                "description": "Multiple failed password attempts detected. Consider implementing account lockout policies and multi-factor authentication."
            })

        if "unauthorized_access" in threat_types:
            recommendations.append({
                "priority": "critical",
                "action": "Audit access controls",
                "description": "Unauthorized access attempts detected. Review and strengthen access control policies."
            })

        if "network_anomaly" in threat_types:
            recommendations.append({
                "priority": "medium",
                "action": "Network traffic analysis",
                "description": "Unusual network connections detected. Review firewall rules and monitor network traffic."
            })

        if "service_failure" in threat_types:
            recommendations.append({
                "priority": "high",
                "action": "Service health check",
                "description": "Service crashes detected. Review service logs and implement proper error handling and monitoring."
            })

        # Anomaly-based recommendations
        anomalies = analysis.get("anomalies", [])
        for anomaly in anomalies:
            if anomaly.get("type") == "high_error_rate":
                recommendations.append({
                    "priority": "high",
                    "action": "Error rate investigation",
                    "description": "High error rate detected. Review application logs and identify root cause of errors."
                })
            elif anomaly.get("type") == "multiple_source_ips":
                recommendations.append({
                    "priority": "medium",
                    "action": "User session review",
                    "description": f"User '{anomaly.get('user')}' accessing from multiple IPs. Verify if this is expected behavior or potential credential compromise."
                })

        # If no specific recommendations, provide general ones
        if not recommendations:
            recommendations.append({
                "priority": "low",
                "action": "Continue monitoring",
                "description": "No significant threats or anomalies detected. Continue routine monitoring."
            })

        return recommendations

    def get_threat_summary(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get a quick threat summary without full analysis."""
        threats = self._detect_threats(logs)

        threat_summary = {
            "total_threats": len(threats),
            "critical": len([t for t in threats if t.get("severity") == "critical"]),
            "high": len([t for t in threats if t.get("severity") == "high"]),
            "medium": len([t for t in threats if t.get("severity") == "medium"]),
            "threat_types": list(set(t.get("threat_type") for t in threats))
        }

        return threat_summary

    def summarize_for_report(self, logs: List[Dict[str, Any]]) -> str:
        """Generate a human-readable text summary for reporting."""
        analysis = self.analyze_logs(logs)

        summary_lines = [
            "=" * 60,
            "CRPF LOG ANALYSIS REPORT",
            "=" * 60,
            f"Generated: {analysis['timestamp']}",
            f"Logs Analyzed: {analysis['total_logs_analyzed']}",
            f"Risk Score: {analysis['risk_score']}/100",
            "",
            "SEVERITY DISTRIBUTION:",
            "-" * 40
        ]

        severity = analysis.get("severity_distribution", {}).get("distribution", {})
        for level, data in severity.items():
            summary_lines.append(f"  {level}: {data['count']} ({data['percentage']}%)")

        summary_lines.extend([
            "",
            "THREATS DETECTED:",
            "-" * 40
        ])

        threats = analysis.get("threats_detected", [])
        if threats:
            for threat in threats[:10]:  # Show top 10 threats
                summary_lines.append(
                    f"  [{threat['severity'].upper()}] {threat['threat_type']}: {threat.get('log', {}).get('message', 'N/A')}"
                )
        else:
            summary_lines.append("  No threats detected")

        summary_lines.extend([
            "",
            "ANOMALIES:",
            "-" * 40
        ])

        anomalies = analysis.get("anomalies", [])
        if anomalies:
            for anomaly in anomalies:
                summary_lines.append(f"  [{anomaly['severity'].upper()}] {anomaly['description']}")
        else:
            summary_lines.append("  No anomalies detected")

        summary_lines.extend([
            "",
            "RECOMMENDATIONS:",
            "-" * 40
        ])

        for rec in analysis.get("recommendations", []):
            summary_lines.append(f"  [{rec['priority'].upper()}] {rec['action']}")
            summary_lines.append(f"    {rec['description']}")

        summary_lines.append("=" * 60)

        return "\n".join(summary_lines)


# Create a singleton instance for use across the application
log_agent = LogAnalysisAgent()
