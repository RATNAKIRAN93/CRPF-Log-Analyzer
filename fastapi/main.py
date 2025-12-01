import os
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from opensearchpy import OpenSearch

from agent import log_agent

app = FastAPI(
    title="CRPF Log Analyzer API",
    description="Centralized log analysis system with AI-powered threat detection and anomaly analysis for CRPF IT systems",
    version="2.0.0"
)

OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "http://opensearch:9200")
INDEX = os.getenv("OPENSEARCH_INDEX", "system-logs")
client = OpenSearch([OPENSEARCH_HOST])


# ============== Pydantic Models ==============

class AnalysisRequest(BaseModel):
    """Request model for log analysis"""
    query: Optional[str] = "*"
    time_range_hours: Optional[int] = 24
    max_logs: Optional[int] = 1000


class ThreatSummaryRequest(BaseModel):
    """Request model for threat summary"""
    query: Optional[str] = "*"
    max_logs: Optional[int] = 500


# ============== Helper Functions ==============

def fetch_logs(query: str = "*", size: int = 100, time_range_hours: Optional[int] = None) -> List[dict]:
    """Fetch logs from OpenSearch with optional time range filter."""
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "query": query
                        }
                    }
                ]
            }
        },
        "size": size,
        "sort": [{"timestamp": {"order": "desc"}}]
    }

    # Add time range filter if specified
    if time_range_hours:
        time_filter = {
            "range": {
                "timestamp": {
                    "gte": f"now-{time_range_hours}h",
                    "lte": "now"
                }
            }
        }
        body["query"]["bool"]["must"].append(time_filter)

    try:
        res = client.search(index=INDEX, body=body)
        return [h["_source"] for h in res["hits"]["hits"]]
    except Exception as e:
        # Return empty list if index doesn't exist or other errors
        return []


# ============== Original Endpoints ==============

@app.get("/search")
def search(q: str = Query(..., description="Query string")):
    """Search logs using query string syntax."""
    body = {
        "query": {
            "query_string": {
                "query": q
            }
        },
        "size": 100
    }
    res = client.search(index=INDEX, body=body)
    hits = [h["_source"] for h in res["hits"]["hits"]]
    return {"count": res["hits"]["total"]["value"], "results": hits}


# ============== Agent Endpoints ==============

@app.get("/agent/status")
def agent_status():
    """Get the current status of the log analysis agent."""
    return {
        "status": "active",
        "agent_type": "LogAnalysisAgent",
        "version": "1.0.0",
        "capabilities": [
            "threat_detection",
            "anomaly_detection",
            "log_summarization",
            "risk_scoring",
            "recommendation_generation"
        ],
        "analysis_history_count": len(log_agent.analysis_history)
    }


@app.post("/agent/analyze")
def analyze_logs(request: AnalysisRequest):
    """
    Perform comprehensive AI-powered analysis on logs.

    This endpoint fetches logs based on the query and time range,
    then runs them through the log analysis agent to detect:
    - Security threats
    - Anomalies
    - Risk levels
    - Actionable recommendations
    """
    logs = fetch_logs(
        query=request.query,
        size=request.max_logs,
        time_range_hours=request.time_range_hours
    )

    if not logs:
        return {
            "status": "no_data",
            "message": "No logs found matching the criteria",
            "query": request.query,
            "time_range_hours": request.time_range_hours
        }

    analysis = log_agent.analyze_logs(logs)
    return analysis


@app.get("/agent/analyze/quick")
def quick_analyze(
    q: str = Query("*", description="Query string"),
    hours: int = Query(24, description="Time range in hours"),
    limit: int = Query(500, description="Maximum logs to analyze")
):
    """
    Quick analysis endpoint using GET parameters.
    Useful for simple queries and dashboard integrations.
    """
    logs = fetch_logs(query=q, size=limit, time_range_hours=hours)

    if not logs:
        return {
            "status": "no_data",
            "message": "No logs found"
        }

    analysis = log_agent.analyze_logs(logs)
    return analysis


@app.post("/agent/threats")
def get_threats(request: ThreatSummaryRequest):
    """
    Get a quick threat summary from recent logs.
    Faster than full analysis, focuses only on threat detection.
    """
    logs = fetch_logs(query=request.query, size=request.max_logs)

    if not logs:
        return {
            "status": "no_data",
            "total_threats": 0,
            "message": "No logs found"
        }

    summary = log_agent.get_threat_summary(logs)
    summary["logs_analyzed"] = len(logs)
    return summary


@app.get("/agent/threats/quick")
def quick_threats(
    q: str = Query("*", description="Query string"),
    limit: int = Query(500, description="Maximum logs to analyze")
):
    """Quick threat summary using GET parameters."""
    logs = fetch_logs(query=q, size=limit)

    if not logs:
        return {
            "status": "no_data",
            "total_threats": 0
        }

    summary = log_agent.get_threat_summary(logs)
    summary["logs_analyzed"] = len(logs)
    return summary


@app.get("/agent/report", response_class=PlainTextResponse)
def generate_report(
    q: str = Query("*", description="Query string"),
    hours: int = Query(24, description="Time range in hours"),
    limit: int = Query(1000, description="Maximum logs to analyze")
):
    """
    Generate a human-readable text report of log analysis.
    Suitable for email alerts or text-based reporting systems.
    """
    logs = fetch_logs(query=q, size=limit, time_range_hours=hours)

    if not logs:
        return "No logs found for the specified criteria."

    report = log_agent.summarize_for_report(logs)
    return report


@app.get("/agent/endpoints")
def analyze_by_endpoint(
    hours: int = Query(24, description="Time range in hours"),
    limit: int = Query(1000, description="Maximum logs to analyze")
):
    """
    Get analysis broken down by endpoint.
    Useful for identifying problematic endpoints.
    """
    logs = fetch_logs(query="*", size=limit, time_range_hours=hours)

    if not logs:
        return {"status": "no_data", "endpoints": {}}

    analysis = log_agent.analyze_logs(logs)
    return {
        "total_logs": len(logs),
        "endpoints": analysis.get("endpoint_analysis", {}),
        "timestamp": analysis.get("timestamp")
    }


@app.get("/agent/users")
def analyze_by_user(
    hours: int = Query(24, description="Time range in hours"),
    limit: int = Query(1000, description="Maximum logs to analyze")
):
    """
    Get user activity analysis.
    Useful for identifying suspicious user behavior.
    """
    logs = fetch_logs(query="*", size=limit, time_range_hours=hours)

    if not logs:
        return {"status": "no_data", "users": {}}

    analysis = log_agent.analyze_logs(logs)
    return {
        "total_logs": len(logs),
        "users": analysis.get("user_activity", {}),
        "timestamp": analysis.get("timestamp")
    }


@app.get("/agent/anomalies")
def get_anomalies(
    hours: int = Query(24, description="Time range in hours"),
    limit: int = Query(1000, description="Maximum logs to analyze")
):
    """
    Get detected anomalies from recent logs.
    """
    logs = fetch_logs(query="*", size=limit, time_range_hours=hours)

    if not logs:
        return {"status": "no_data", "anomalies": []}

    analysis = log_agent.analyze_logs(logs)
    return {
        "total_logs": len(logs),
        "anomalies": analysis.get("anomalies", []),
        "risk_score": analysis.get("risk_score", 0),
        "timestamp": analysis.get("timestamp")
    }


@app.get("/agent/recommendations")
def get_recommendations(
    hours: int = Query(24, description="Time range in hours"),
    limit: int = Query(1000, description="Maximum logs to analyze")
):
    """
    Get AI-generated security recommendations based on log analysis.
    """
    logs = fetch_logs(query="*", size=limit, time_range_hours=hours)

    if not logs:
        return {
            "status": "no_data",
            "recommendations": [{
                "priority": "low",
                "action": "No data available",
                "description": "No logs found for analysis. Ensure log producers are running."
            }]
        }

    analysis = log_agent.analyze_logs(logs)
    return {
        "total_logs": len(logs),
        "risk_score": analysis.get("risk_score", 0),
        "recommendations": analysis.get("recommendations", []),
        "timestamp": analysis.get("timestamp")
    }


@app.get("/agent/history")
def get_analysis_history():
    """
    Get the history of recent analyses performed by the agent.
    """
    return {
        "total_analyses": len(log_agent.analysis_history),
        "history": log_agent.analysis_history[-20:]  # Last 20 analyses
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Check OpenSearch connection
        client.cluster.health()
        opensearch_status = "healthy"
    except Exception:
        opensearch_status = "unhealthy"

    return {
        "status": "healthy" if opensearch_status == "healthy" else "degraded",
        "components": {
            "api": "healthy",
            "agent": "healthy",
            "opensearch": opensearch_status
        }
    }
