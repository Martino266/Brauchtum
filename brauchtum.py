import streamlit as st
import json
from datetime import datetime
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Interaktiver Brauchtumskalender", layout="wide")
st.title("📅 Interaktiver Brauchtumskalender")
st.write("Klicke auf ein Datum, um alle Bräuche an diesem Tag zu sehen.")

# JSON-Datei laden
with open("braeuche.json", encoding="utf-8") as f:
    braeuche = json.load(f)

# Datumsauswahl
selected_date = st.date_input("Wähle ein Datum:")

# Filter nach Region
regions = sorted(list(set([b["region"] for b in braeuche])))
selected_region = st.selectbox("Region wählen", ["Alle"] + regions)

# Bräuche für das Datum filtern
events_today = [
    b for b in braeuche
    if datetime.fromisoformat(b["date"]).date() == selected_date and
    (selected_region == "Alle" or b["region"] == selected_region)
]

# Ergebnisse anzeigen
if events_today:
    st.subheader(f"Bräuche am {selected_date.strftime('%d.%m.%Y')}:")
    for event in events_today:
        st.markdown(f"### {event['name']} – {event['region']} um {event['zeit']}")
        st.markdown(f"{event['beschreibung']}")
        if event.get("bild_url"):
            st.image(event["bild_url"], caption=event["name"])
        st.markdown("---")

    # Karte anzeigen, wenn Koordinaten vorhanden
    if any("lat" in e and "lon" in e for e in events_today):
        m = folium.Map(location=[47.3769, 8.5417], zoom_start=6)
        for event in events_today:
            if "lat" in event and "lon" in event:
                folium.Marker(
                    [event["lat"], event["lon"]],
                    popup=f"{event['name']} – {event['zeit']}"
                ).add_to(m)
        st.subheader("📍 Karte der Bräuche")
        st_data = st_folium(m, width=700, height=450)

else:
    st.info("An diesem Tag finden keine Bräuche statt.")
