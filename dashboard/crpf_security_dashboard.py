import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
from datetime import datetime, timedelta, timezone
import time
from collections import defaultdict
import numpy as np

# Page configuration
st.set_page_config(
    page_title="CRPF Security Operations Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 3px solid #1f4e79;
        padding-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f4e79;
    }
    .alert-critical {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .alert-high {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class CRPFSecurityDashboard:
    def __init__(self):
        self.opensearch_url = "http://localhost:9200"
        self.index_pattern = "crpf-logs-*"
        
    def query_opensearch(self, query_body, size=1000):
        """Query OpenSearch for security data"""
        try:
            url = f"{self.opensearch_url}/{self.index_pattern}/_search"
            response = requests.post(
                url, 
                json=query_body, 
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"OpenSearch query failed: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Error querying OpenSearch: {e}")
            return None

    def get_security_metrics(self, time_range_minutes=15):
        """Get key security metrics"""
        query = {
            "size": 0,
            "query": {
                "range": {
                    "@timestamp": {
                        "gte": f"now-{time_range_minutes}m"
                    }
                }
            },
            "aggs": {
                "total_events": {"value_count": {"field": "@timestamp"}},
                "severity_breakdown": {
                    "terms": {"field": "severity.keyword", "size": 10}
                },
                "threat_levels": {
                    "terms": {"field": "threat_level.keyword", "size": 10}
                },
                "event_categories": {
                    "terms": {"field": "event_category.keyword", "size": 10}
                },
                "top_locations": {
                    "terms": {"field": "location_id.keyword", "size": 10}
                },
                "critical_events": {
                    "filter": {"term": {"severity.keyword": "CRITICAL"}},
                    "aggs": {
                        "count": {"value_count": {"field": "@timestamp"}}
                    }
                },
                "high_risk_events": {
                    "filter": {"range": {"risk_score": {"gte": 70}}},
                    "aggs": {
                        "count": {"value_count": {"field": "@timestamp"}}
                    }
                }
            }
        }
        
        return self.query_opensearch(query)

    def get_timeline_data(self, time_range_minutes=60):
        """Get events timeline for visualization"""
        query = {
            "size": 0,
            "query": {
                "range": {
                    "@timestamp": {
                        "gte": f"now-{time_range_minutes}m"
                    }
                }
            },
            "aggs": {
                "events_over_time": {
                    "date_histogram": {
                        "field": "@timestamp",
                        "fixed_interval": "2m",
                        "min_doc_count": 0
                    },
                    "aggs": {
                        "severity_breakdown": {
                            "terms": {"field": "severity.keyword"}
                        }
                    }
                }
            }
        }
        
        return self.query_opensearch(query)

    def get_threat_analysis(self, time_range_minutes=30):
        """Get detailed threat analysis"""
        query = {
            "size": 100,
            "query": {
                "bool": {
                    "must": [
                        {"range": {"@timestamp": {"gte": f"now-{time_range_minutes}m"}}},
                        {"exists": {"field": "threat_indicators"}}
                    ]
                }
            },
            "sort": [{"risk_score": {"order": "desc"}}]
        }
        
        return self.query_opensearch(query)

    def get_alerts(self, time_range_minutes=30):
        """Get security alerts based on patterns"""
        alerts = []
        
        # Query for suspicious patterns
        patterns = [
            {
                "name": "Multiple Failed Logins",
                "query": {
                    "size": 0,
                    "query": {
                        "bool": {
                            "must": [
                                {"range": {"@timestamp": {"gte": f"now-{time_range_minutes}m"}}},
                                {"term": {"event_type.keyword": "login_failed"}}
                            ]
                        }
                    },
                    "aggs": {
                        "users": {
                            "terms": {"field": "user.keyword", "min_doc_count": 5}
                        }
                    }
                }
            },
            {
                "name": "Malware Detections",
                "query": {
                    "size": 0,
                    "query": {
                        "bool": {
                            "must": [
                                {"range": {"@timestamp": {"gte": f"now-{time_range_minutes}m"}}},
                                {"term": {"event_type.keyword": "malware_detected"}}
                            ]
                        }
                    }
                }
            },
            {
                "name": "High Risk Events",
                "query": {
                    "size": 0,
                    "query": {
                        "bool": {
                            "must": [
                                {"range": {"@timestamp": {"gte": f"now-{time_range_minutes}m"}}},
                                {"range": {"risk_score": {"gte": 80}}}
                            ]
                        }
                    }
                }
            }
        ]
        
        for pattern in patterns:
            result = self.query_opensearch(pattern["query"])
            if result and result.get("hits", {}).get("total", {}).get("value", 0) > 0:
                count = result["hits"]["total"]["value"]
                severity = "CRITICAL" if count > 10 else "HIGH" if count > 5 else "MEDIUM"
                alerts.append({
                    "name": pattern["name"],
                    "count": count,
                    "severity": severity,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
        
        return alerts

def main():
    dashboard = CRPFSecurityDashboard()
    
    # Header
    st.markdown('<h1 class="main-header">🛡️ CRPF Security Operations Center</h1>', unsafe_allow_html=True)
    
    # Sidebar controls
    st.sidebar.header("⚙️ Dashboard Controls")
    
    # Time range selector
    time_options = {
        "Last 15 minutes": 15,
        "Last 30 minutes": 30,
        "Last 1 hour": 60,
        "Last 2 hours": 120,
        "Last 4 hours": 240
    }
    
    selected_time = st.sidebar.selectbox(
        "Time Range",
        options=list(time_options.keys()),
        index=1
    )
    time_range = time_options[selected_time]
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("Auto Refresh (10s)", value=True)
    
    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Now"):
        st.rerun()
    
    # Main dashboard content
    try:
        # Get security metrics
        metrics_data = dashboard.get_security_metrics(time_range)
        
        if metrics_data:
            aggs = metrics_data.get("aggregations", {})
            
            # Key metrics row
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                total_events = aggs.get("total_events", {}).get("value", 0)
                st.metric("📊 Total Events", f"{total_events:,}")
            
            with col2:
                critical_events = aggs.get("critical_events", {}).get("count", {}).get("value", 0)
                st.metric("🚨 Critical Events", critical_events)
            
            with col3:
                high_risk = aggs.get("high_risk_events", {}).get("count", {}).get("value", 0)
                st.metric("⚠️ High Risk Events", high_risk)
            
            with col4:
                locations = len(aggs.get("top_locations", {}).get("buckets", []))
                st.metric("📍 Active Locations", locations)
            
            with col5:
                # Calculate threat ratio
                threat_buckets = aggs.get("threat_levels", {}).get("buckets", [])
                malicious = sum(b["doc_count"] for b in threat_buckets if b["key"] in ["malicious", "critical_threat"])
                threat_ratio = round((malicious / max(total_events, 1)) * 100, 1)
                st.metric("🎯 Threat Ratio", f"{threat_ratio}%")
            
            # Alerts section
            st.markdown("## 🚨 Active Security Alerts")
            alerts = dashboard.get_alerts(time_range)
            
            if alerts:
                for alert in alerts:
                    severity_class = "alert-critical" if alert["severity"] == "CRITICAL" else "alert-high"
                    st.markdown(f"""
                    <div class="{severity_class}">
                        <strong>{alert["name"]}</strong><br>
                        Count: {alert["count"]} | Severity: {alert["severity"]} | Time: {alert["timestamp"]}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ No active alerts in the selected time range")
            
            # Charts row
            col1, col2 = st.columns(2)
            
            with col1:
                # Severity distribution
                st.markdown("### 📊 Event Severity Distribution")
                severity_data = aggs.get("severity_breakdown", {}).get("buckets", [])
                
                if severity_data:
                    severity_df = pd.DataFrame([
                        {"Severity": bucket["key"], "Count": bucket["doc_count"]}
                        for bucket in severity_data
                    ])
                    
                    colors = {
                        'INFO': '#2196F3',
                        'WARN': '#FF9800', 
                        'ERROR': '#F44336',
                        'CRITICAL': '#9C27B0'
                    }
                    
                    fig_severity = px.pie(
                        severity_df,
                        values='Count',
                        names='Severity',
                        color='Severity',
                        color_discrete_map=colors,
                        title="Security Event Severity"
                    )
                    fig_severity.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_severity, use_container_width=True)
            
            with col2:
                # Event categories
                st.markdown("### 🔍 Event Categories")
                category_data = aggs.get("event_categories", {}).get("buckets", [])
                
                if category_data:
                    category_df = pd.DataFrame([
                        {"Category": bucket["key"], "Count": bucket["doc_count"]}
                        for bucket in category_data
                    ])
                    
                    fig_category = px.bar(
                        category_df,
                        x='Category',
                        y='Count',
                        color='Count',
                        color_continuous_scale='Reds',
                        title="Events by Category"
                    )
                    fig_category.update_layout(showlegend=False)
                    st.plotly_chart(fig_category, use_container_width=True)
            
            # Timeline chart
            st.markdown("### ⏰ Security Events Timeline")
            timeline_data = dashboard.get_timeline_data(time_range)
            
            if timeline_data:
                timeline_buckets = timeline_data.get("aggregations", {}).get("events_over_time", {}).get("buckets", [])
                
                if timeline_buckets:
                    timeline_records = []
                    for bucket in timeline_buckets:
                        timestamp = pd.to_datetime(bucket["key_as_string"] if "key_as_string" in bucket else bucket["key"])
                        
                        severity_breakdown = bucket.get("severity_breakdown", {}).get("buckets", [])
                        if severity_breakdown:
                            for sev_bucket in severity_breakdown:
                                timeline_records.append({
                                    "timestamp": timestamp,
                                    "severity": sev_bucket["key"],
                                    "count": sev_bucket["doc_count"]
                                })
                        else:
                            timeline_records.append({
                                "timestamp": timestamp,
                                "severity": "Unknown",
                                "count": bucket["doc_count"]
                            })
                    
                    if timeline_records:
                        timeline_df = pd.DataFrame(timeline_records)
                        
                        fig_timeline = px.line(
                            timeline_df,
                            x='timestamp',
                            y='count',
                            color='severity',
                            title="Security Events Over Time",
                            color_discrete_map={
                                'INFO': '#2196F3',
                                'WARN': '#FF9800',
                                'ERROR': '#F44336', 
                                'CRITICAL': '#9C27B0'
                            }
                        )
                        fig_timeline.update_layout(
                            xaxis_title="Time",
                            yaxis_title="Event Count",
                            hovermode='x unified'
                        )
                        st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Location analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📍 Top Active Locations")
                location_data = aggs.get("top_locations", {}).get("buckets", [])
                
                if location_data:
                    location_df = pd.DataFrame([
                        {"Location": bucket["key"], "Events": bucket["doc_count"]}
                        for bucket in location_data[:10]
                    ])
                    
                    fig_locations = px.bar(
                        location_df,
                        x='Events',
                        y='Location',
                        orientation='h',
                        color='Events',
                        color_continuous_scale='Blues',
                        title="Events by Location"
                    )
                    st.plotly_chart(fig_locations, use_container_width=True)
            
            with col2:
                # Threat analysis
                st.markdown("### 🎯 Threat Analysis")
                threat_data = dashboard.get_threat_analysis(time_range)
                
                if threat_data and threat_data.get("hits", {}).get("hits"):
                    threats = []
                    for hit in threat_data["hits"]["hits"][:10]:
                        source = hit["_source"]
                        threats.append({
                            "Event Type": source.get("event_type", "Unknown"),
                            "Risk Score": source.get("risk_score", 0),
                            "Location": source.get("location_id", "Unknown"),
                            "Indicators": ", ".join(source.get("threat_indicators", []))[:50]
                        })
                    
                    if threats:
                        threats_df = pd.DataFrame(threats)
                        st.dataframe(threats_df, use_container_width=True, height=300)
                else:
                    st.info("No threat indicators found in the selected time range")
        
        else:
            st.error("❌ Unable to fetch security metrics. Check OpenSearch connection.")
    
    except Exception as e:
        st.error(f"❌ Dashboard error: {e}")
    
    # Footer with system info
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.caption(f"🕒 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    with col2:
        st.caption(f"⏱️ Time Range: {selected_time}")
    
    with col3:
        st.caption("🔒 CRPF Classified - Internal Use Only")
    
    # Auto-refresh
    if auto_refresh:
        time.sleep(10)
        st.rerun()

if __name__ == "__main__":
    main()
