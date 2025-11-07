import streamlit as st
import json
from datetime import datetime, date
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Interaktiver Brauchtumskalender", layout="wide")
st.title("📅 Interaktiver Brauchtumskalender – erweiterte Version")
st.write("Klicke ein Datum an oder nutze die Suche, um Bräuche zu entdecken.")

# JSON-Datei laden
with open("braeuche.json", encoding="utf-8") as f:
    braeuche = json.load(f)

# Filter: Region und Stichwortsuche
regions = sorted(list(set([b["region"] for b in braeuche])))
selected_region = st.selectbox("Region wählen", ["Alle"] + regions)
search_term = st.text_input("Suche nach Stichworten:")

# Monatsübersicht
st.subheader("Monatsübersicht")
months = {1:"Januar",2:"Februar",3:"März",4:"April",5:"Mai",6:"Juni",
          7:"Juli",8:"August",9:"September",10:"Oktober",11:"November",12:"Dezember"}
selected_month = st.selectbox("Monat wählen", list(months.values()))

# Bräuche für gewählten Monat filtern
month_events = [
    b for b in braeuche
    if datetime.fromisoformat(b["date"]).month == list(months.keys())[list(months.values()).index(selected_month)]
    and (selected_region == "Alle" or b["region"] == selected_region)
    and (search_term.lower() in b["name"].lower() or search_term.lower() in b["beschreibung"].lower())
]

# Kalenderansicht: zeige alle Tage mit Bräuchen
st.subheader(f"Bräuche im {selected_month}")
if month_events:
    # Gruppieren nach Datum
    grouped_events = {}
    for b in month_events:
        grouped_events.setdefault(b["date"], []).append(b)

    for day, events in sorted(grouped_events.items()):
        st.markdown(f"### {datetime.fromisoformat(day).strftime('%d.%m.%Y')}")
        for event in events:
            st.markdown(f"**{event['name']}** – {event['region']} um {event['zeit']}")
            st.markdown(f"{event['beschreibung']}")
            if event.get("bild_url"):
                st.image(event["bild_url"], caption=event["name"])
        st.markdown("---")

    # Karte mit allen Events des Monats
    if any("lat" in e and "lon" in e for e in month_events):
        m = folium.Map(location=[47.3769, 8.5417], zoom_start=6)
        for event in month_events:
            if "lat" in event and "lon" in event:
                folium.Marker(
                    [event["lat"], event["lon"]],
                    popup=f"{event['name']} – {event['zeit']} ({event['region']})"
                ).add_to(m)
        st.subheader("📍 Karte der Bräuche im Monat")
        st_data = st_folium(m, width=700, height=450)

else:
    st.info("Keine Bräuche in diesem Monat mit den gewählten Filtern.")
