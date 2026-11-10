import streamlit as st
import requests
import pandas as pd
from datetime import date
from typing import Any

# ============================================================
# INDIAN RAILWAY EXPLORER - GLASSMORPHISM UI
# ============================================================

st.set_page_config(
    page_title="Indian Railway Explorer",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_URL = "https://api.railradar.in/v1"
API_KEY = st.secrets.get("RAILRADAR_API_KEY", "")

# -------------------------- STYLE ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Outfit:wght@500;600;700;800&display=swap');

:root { --glass: rgba(255,255,255,.085); --line: rgba(255,255,255,.17); }
.stApp {
  background:
    radial-gradient(ellipse at 12% 8%, rgba(22,135,211,.38), transparent 38%),
    radial-gradient(ellipse at 88% 25%, rgba(131,75,210,.27), transparent 38%),
    radial-gradient(ellipse at 55% 100%, rgba(15,178,174,.17), transparent 42%),
    linear-gradient(135deg,#061323 0%,#0c1d35 48%,#17152e 100%);
  background-attachment: fixed;
  color:#f4f7ff;
  font-family:'DM Sans',sans-serif;
}
.block-container { max-width:1320px; padding-top:1.5rem; padding-bottom:3rem; }
h1,h2,h3,h4,p,label,span { font-family:'DM Sans',sans-serif; }
h1,h2,h3 { color:#f7f9ff; }
.hero {
  position:relative; overflow:hidden; text-align:center;
  padding:38px 18px 32px; margin:4px 0 22px;
  border:1px solid rgba(255,255,255,.22); border-radius:28px;
  background:linear-gradient(115deg,rgba(255,255,255,.14),rgba(255,255,255,.045));
  backdrop-filter:blur(22px); -webkit-backdrop-filter:blur(22px);
  box-shadow:0 18px 55px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.15);
}
.hero:before {
  content:""; position:absolute; width:320px;height:320px;top:-220px;left:10%;
  background:rgba(60,174,255,.22);filter:blur(35px);border-radius:50%;
}
.hero:after {
  content:""; position:absolute; width:260px;height:260px;bottom:-210px;right:8%;
  background:rgba(164,91,255,.22);filter:blur(35px);border-radius:50%;
}
.hero h1 { position:relative; font-family:'Outfit',sans-serif; font-size:clamp(29px,4vw,45px);font-weight:800;letter-spacing:.7px;margin:0; }
.hero p { position:relative;color:#c6d8f4;font-size:15px;margin:10px 0 0; }
.eyebrow { color:#8fdcff;font-size:11px;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;margin-bottom:8px; }
.glass-card {
  background:var(--glass);border:1px solid var(--line);border-radius:22px;
  padding:22px 24px;margin:12px 0 18px;
  backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  box-shadow:0 12px 36px rgba(0,0,0,.20),inset 0 1px 0 rgba(255,255,255,.10);
}
.section-title {font-family:'Outfit',sans-serif;font-size:21px;font-weight:700;margin:4px 0 14px;}
.stCaption, [data-testid="stCaptionContainer"] {color:#b8cbe8!important;}
div[data-baseweb="select"]>div, div[data-baseweb="input"]>div,
div[data-baseweb="textarea"]>div {
  background:rgba(255,255,255,.09)!important;
  border:1px solid rgba(255,255,255,.20)!important;border-radius:12px!important;
}
input,textarea {color:#fff!important;}
.stButton>button,.stFormSubmitButton>button,.stDownloadButton>button {
  color:white!important;background:linear-gradient(100deg,#168eea,#7857e8)!important;
  border:1px solid rgba(255,255,255,.20)!important;border-radius:13px!important;
  min-height:46px;font-weight:800;box-shadow:0 8px 22px rgba(47,113,225,.22);
  transition:transform .18s ease,box-shadow .18s ease;
}
.stButton>button:hover,.stFormSubmitButton>button:hover,.stDownloadButton>button:hover {
  transform:translateY(-2px);box-shadow:0 12px 28px rgba(47,113,225,.36);
}
div[data-testid="stMetric"] {
  background:rgba(255,255,255,.075);border:1px solid rgba(255,255,255,.15);
  border-radius:17px;padding:15px 17px;backdrop-filter:blur(14px);
}
div[data-testid="stMetricLabel"] {color:#bcd0ee!important;}
div[data-testid="stMetricValue"] {color:#fff!important;font-weight:800;}
div[data-testid="stDataFrame"] {
  border:1px solid rgba(255,255,255,.14);border-radius:16px;overflow:hidden;
}
div[role="tablist"] {gap:10px;}
button[data-baseweb="tab"] {border-radius:12px 12px 0 0;color:#cbd9f0;}
button[data-baseweb="tab"][aria-selected="true"] {color:#fff;border-bottom:3px solid #55c8ff;}
.status-pill {
  display:inline-block;padding:6px 12px;border-radius:99px;
  background:rgba(34,197,140,.15);border:1px solid rgba(75,230,175,.35);
  color:#8cf2c9;font-size:12px;font-weight:800;letter-spacing:.4px;
}
.live-grid {display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:14px 0;}
.live-item {
  background:rgba(255,255,255,.075);border:1px solid rgba(255,255,255,.15);
  border-radius:16px;padding:14px 16px;min-height:78px;
}
.live-label {color:#a9c2e4;font-size:11px;text-transform:uppercase;letter-spacing:1px;font-weight:800;}
.live-value {color:#fff;font-size:18px;font-weight:800;margin-top:7px;overflow-wrap:anywhere;}
.route-stop {
  display:flex;gap:14px;align-items:flex-start;padding:12px 8px;
  border-bottom:1px solid rgba(255,255,255,.10);
}
.route-dot {width:11px;height:11px;border-radius:50%;background:#55d7ff;margin-top:6px;box-shadow:0 0 12px #55d7ff;flex-shrink:0;}
.route-name {font-weight:800;color:#fff;}
.route-meta {font-size:12px;color:#b6c9e5;margin-top:4px;}
.footer {text-align:center;color:#91a9ca;padding:20px 0 8px;font-size:12px;}
hr {border-color:rgba(255,255,255,.14)!important;}
</style>
""", unsafe_allow_html=True)

HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# ----------------------- API HELPERS -------------------------
def api_get(path: str, params: dict | None = None) -> dict:
    if not API_KEY:
        raise RuntimeError("RailRadar API key is missing. Configure .streamlit/secrets.toml.")
    response = requests.get(
        f"{BASE_URL}{path}", headers=HEADERS, params=params or {}, timeout=30
    )
    try:
        payload = response.json()
    except ValueError:
        payload = {}
    if not response.ok:
        message = payload.get("error", payload) if isinstance(payload, dict) else payload
        raise RuntimeError(f"API returned HTTP {response.status_code}: {message}")
    if isinstance(payload, dict) and payload.get("success") is False:
        raise RuntimeError(str(payload.get("error", "API request failed")))
    return payload

@st.cache_data(ttl=86400, show_spinner=False)
def load_stations(_key: str) -> dict:
    payload = api_get("/lookup/stations", {"lang": "en"})
    data = payload.get("data", {})
    if isinstance(data, dict):
        return {str(k): str(v) for k, v in data.items()}
    if isinstance(data, list):
        result = {}
        for item in data:
            if isinstance(item, dict):
                code = item.get("code") or item.get("stationCode")
                name = item.get("name") or item.get("stationName")
                if code and name:
                    result[str(code)] = str(name)
        return result
    return {}

def station_label(stations: dict, code: str) -> str:
    return f"{stations.get(code, code)} ({code})"

def show_live_cards(value: Any):
    """Render live status as readable cards instead of dumping raw JSON."""
    if value is None:
        st.info("Live running information was not supplied for this request.")
        return

    if isinstance(value, dict):
        # Common fields first, then any additional scalar values.
        preferred = [
            ("status", "Running status"),
            ("currentStation", "Current station"),
            ("currentStationName", "Current station"),
            ("currentStationCode", "Station code"),
            ("lastStation", "Last station"),
            ("nextStation", "Next station"),
            ("nextStationName", "Next station"),
            ("delayMinutes", "Delay (minutes)"),
            ("delay", "Delay"),
            ("platform", "Platform"),
            ("updatedAt", "Last updated"),
            ("lastUpdated", "Last updated"),
            ("speed", "Speed"),
        ]
        used = set()
        cards = []
        for key, label in preferred:
            if key in value and value[key] not in (None, "", [], {}):
                cards.append((label, value[key]))
                used.add(key)
        for key, item in value.items():
            if key not in used and isinstance(item, (str, int, float, bool)) and item not in ("", None):
                label = key.replace("_", " ").replace("-", " ").title()
                cards.append((label, item))
        if cards:
            html = '<div class="live-grid">'
            for label, item in cards[:12]:
                display = str(item)
                if isinstance(item, bool):
                    display = "Yes" if item else "No"
                html += (
                    '<div class="live-item">'
                    f'<div class="live-label">{label}</div>'
                    f'<div class="live-value">{display}</div>'
                    '</div>'
                )
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)

        # Render nested station/position details in readable expandable sections.
        nested = [(k, v) for k, v in value.items() if isinstance(v, (dict, list)) and v]
        for key, item in nested:
            title = key.replace("_", " ").replace("-", " ").title()
            with st.expander(title):
                if isinstance(item, list) and item and all(isinstance(x, dict) for x in item):
                    st.dataframe(pd.DataFrame(item), use_container_width=True, hide_index=True)
                elif isinstance(item, dict):
                    pairs = [(str(k).replace("_", " ").title(), str(v)) for k, v in item.items() if not isinstance(v, (dict, list))]
                    if pairs:
                        for label, val in pairs:
                            st.write(f"**{label}:** {val}")
                    else:
                        st.caption("No simple details available in this section.")
                else:
                    st.write(item)
    elif isinstance(value, list):
        if value and all(isinstance(x, dict) for x in value):
            st.dataframe(pd.DataFrame(value), use_container_width=True, hide_index=True)
        else:
            st.write(", ".join(map(str, value)))
    else:
        st.write(str(value))

def render_route_search(stations: dict):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧭 Find trains between stations</div>', unsafe_allow_html=True)
    codes = sorted(stations)
    c1, c2 = st.columns([1, 1])
    with c1:
        source = st.selectbox(
            "FROM · Departure station", codes, index=None,
            placeholder="Search station name or code",
            format_func=lambda x: station_label(stations, x), key="route_from"
        )
    with c2:
        destination = st.selectbox(
            "TO · Arrival station", codes, index=None,
            placeholder="Search station name or code",
            format_func=lambda x: station_label(stations, x), key="route_to"
        )
    journey_date = st.date_input("Journey date", value=date.today(), min_value=date.today(), key="route_journey_date")
    submit = st.button("✦ SEARCH TRAINS", use_container_width=True, key="route_submit")
    st.markdown("</div>", unsafe_allow_html=True)

    if submit:
        if not source or not destination:
            st.warning("Please select both stations.")
        elif source == destination:
            st.warning("Choose two different stations.")
        else:
            try:
                with st.spinner("Searching schedules..."):
                    payload = api_get(
                        f"/trains/between/{source}/{destination}",
                        {"date": journey_date.isoformat(), "lang": "en"}
                    )
                data = payload.get("data", {})
                trains = data.get("trains", []) if isinstance(data, dict) else []
                if not trains:
                    st.info("No trains were returned for this route and date.")
                    return
                rows = []
                for item in trains:
                    train = item.get("train", {}) or {}
                    start = item.get("from", {}) or {}
                    end = item.get("to", {}) or {}
                    rows.append({
                        "Train number": train.get("number", ""),
                        "Train name": train.get("name", ""),
                        "Type": train.get("type", ""),
                        "Departure": start.get("departure") or "-",
                        "Arrival": end.get("arrival") or "-",
                        "Duration (min)": item.get("duration", "-"),
                        "Distance (km)": item.get("distance", "-"),
                        "Running days": ", ".join(train.get("runDays", []) or []),
                    })
                df = pd.DataFrame(rows)
                a, b, c = st.columns(3)
                a.metric("Trains found", len(df))
                b.metric("From", source)
                c.metric("To", destination)
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.download_button("⬇ Download CSV", df.to_csv(index=False), "train_search_results.csv", "text/csv")
            except Exception as exc:
                st.error(str(exc))

def render_number_search():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🚆 Search by train number</div>', unsafe_allow_html=True)
    with st.form("number_search_form"):
        number = st.text_input("Train number", placeholder="Example: 12919")
        journey_date = st.date_input("Journey date", value=date.today(), min_value=date.today(), key="number_journey_date")
        submit = st.form_submit_button("✦ FIND TRAIN", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if not submit:
        return
    if not number.strip().isdigit():
        st.warning("Enter a valid numeric train number.")
        return

    try:
        with st.spinner("Loading train details..."):
            payload = api_get(
                f"/legacy/trains/{number.strip()}",
                {"journeyDate": journey_date.isoformat(), "dataType": "full"}
            )
        data = payload.get("data", {}) if isinstance(payload, dict) else {}
        train = data.get("train", {}) or {}
        route = data.get("route", []) or []
        if not train and not route:
            st.info("No train details were returned. Check the number and API access.")
            return

        train_name = train.get("trainName", "Train details")
        train_no = train.get("trainNumber", number.strip())
        st.markdown(
            f'<div class="glass-card"><div class="eyebrow">TRAIN PROFILE</div>'
            f'<h2 style="margin:0;font-family:Outfit,sans-serif">{train_name}</h2>'
            f'<div style="color:#a9dfff;font-size:15px;margin-top:5px">Train No. {train_no}</div>'
            f'<div style="margin-top:12px"><span class="status-pill">✓ API details received</span></div></div>',
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Train type", train.get("type") or "N/A")
        c2.metric("Distance", f"{train.get('distanceKm', 'N/A')} km")
        c3.metric("Total halts", train.get("totalHalts", "N/A"))

        left, right = st.columns(2)
        with left:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("**Origin station**")
            st.markdown(f"### {train.get('sourceStationName', 'N/A')}")
            st.caption(train.get("sourceStationCode", ""))
            st.markdown("</div>", unsafe_allow_html=True)
        with right:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("**Destination station**")
            st.markdown(f"### {train.get('destinationStationName', 'N/A')}")
            st.caption(train.get("destinationStationCode", ""))
            st.markdown("</div>", unsafe_allow_html=True)

        days = train.get("runningDays", {})
        if isinstance(days, dict) and days.get("days"):
            st.caption("Runs on: " + " · ".join(days["days"]))

        live_data = data.get("liveData")
        st.markdown('<div class="section-title">📍 Live running information</div>', unsafe_allow_html=True)
        if live_data:
            show_live_cards(live_data)
        else:
            st.info("Live running information is not available in this API response. The timetable can still be shown below.")

        st.markdown('<div class="section-title">🗺️ Complete route timetable</div>', unsafe_allow_html=True)
        if route:
            route_rows = []
            for stop in route:
                route_rows.append({
                    "Stop": stop.get("sequence", ""),
                    "Station": stop.get("stationName", ""),
                    "Code": stop.get("stationCode", ""),
                    "Arrival": stop.get("scheduledArrival", "-"),
                    "Departure": stop.get("scheduledDeparture", "-"),
                    "Day": stop.get("day", ""),
                    "Distance (km)": stop.get("distanceFromSourceKm", ""),
                    "Halt": "Yes" if stop.get("isHalt") else "No",
                })
            route_df = pd.DataFrame(route_rows)
            st.dataframe(route_df, use_container_width=True, hide_index=True)
            st.download_button("⬇ Download route CSV", route_df.to_csv(index=False), f"train_{number.strip()}_route.csv", "text/csv")
        else:
            st.info("No route timetable was included in the API response.")

    except Exception as exc:
        st.error(str(exc))

# --------------------------- PAGE ----------------------------
st.markdown("""
<div class="hero">
  <div class="eyebrow">SMART JOURNEY PLANNING</div>
  <h1>🚆 INDIAN RAILWAY EXPLORER</h1>
  <p>Explore stations · Discover trains · Follow your journey</p>
</div>
""", unsafe_allow_html=True)

if not API_KEY:
    st.error("API key not configured. Add RAILRADAR_API_KEY to .streamlit/secrets.toml.")
    st.stop()

try:
    with st.spinner("Loading station directory..."):
        stations = load_stations(API_KEY)
    if not stations:
        st.error("No stations were returned by the station directory.")
        st.stop()
except Exception as exc:
    st.error(f"Unable to load stations: {exc}")
    st.stop()

st.caption(f"✦ Station directory ready · {len(stations):,} stations")
tab_route, tab_number = st.tabs(["🛤️  ROUTE SEARCH", "🔢  TRAIN NUMBER SEARCH"])
with tab_route:
    render_route_search(stations)
with tab_number:
    render_number_search()

st.markdown('<div class="footer">INDIAN RAILWAY EXPLORER · A SMART RAIL JOURNEY INTERFACE</div>', unsafe_allow_html=True)
