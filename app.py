import streamlit as st
import psycopg2
import time

st.set_page_config(page_title="CDC Real-Time Dashboard", layout="wide")
st.title("🚀 Real-Time Event-Driven CDC Dashboard")

if "events" not in st.session_state:
    st.session_state.events = []
    st.session_state.last_id = 0

# Direct PostgreSQL connection
# Direct PostgreSQL connection via Streamlit Secrets
db_connected = False
try:
    conn = psycopg2.connect(st.secrets["url"])
    conn.autocommit = True
    cursor = conn.cursor()
    db_connected = True
except Exception as e:
    db_connected = False
    st.error(f"DB Connection Error: {e}")

# Fetch new records FIRST so metrics and feed sync instantly
if db_connected:
    try:
        cursor.execute("SELECT id, first_name, last_name, email FROM customers WHERE id > %s ORDER BY id ASC LIMIT 50", (st.session_state.last_id,))
        rows = cursor.fetchall()
        for row in rows:
            r_id, fname, lname, email = row
            st.session_state.events.insert(0, {
                "type": "INSERT",
                "data": {"id": r_id, "first_name": fname, "last_name": lname, "email": email}
            })
            st.session_state.last_id = max(st.session_state.last_id, r_id)
            if len(st.session_state.events) > 30:
                st.session_state.events.pop()
        cursor.close()
        conn.close()
    except Exception:
        pass

# Metrics layout
col1, col2, col3 = st.columns(3)
col1.metric("Total Events", len(st.session_state.events))
col2.metric("Status", "Connected (DB)" if db_connected else "Waiting DB")
col3.metric("Table", "public.customers")

st.markdown("---")
st.subheader("Live Feed")

if st.session_state.events:
    for ev in st.session_state.events:
        st.markdown(
            f"<div style='background-color: #f8f9fa; border-left: 4px solid #ff4b4b; padding: 10px 14px; border-radius: 4px; margin-bottom: 8px; color: #111; font-family: monospace; font-size: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>"
            f"<b style='color: #d32f2f;'>[{ev['type']}]</b> <span style='color: #333;'>Data: {ev['data']}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
else:
    st.info("Awaiting live stream records... Run `python producer.py` to push data.")

time.sleep(1)
st.rerun()
