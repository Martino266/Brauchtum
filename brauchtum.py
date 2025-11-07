import streamlit as st
import json
import datetime
from dateutil.easter import easter

st.set_page_config(page_title="Online Brauchtumskalender", page_icon="📅")

st.title("📅 Online-Brauchtumskalender")
st.write("Ein interaktiver Kalender mit traditionellen Festen und Bräuchen.")

# Jahr wählen
jahr = st.number_input("Wähle ein Jahr:", min_value=1900, max_value=2100, value=datetime.date.today().year)

# Bräuche laden
with open("braeuche.json", encoding="utf-8") as f:
    braeuche = json.load(f)


def berechne_datum(brauch, jahr):
    if "rule" in brauch:
        base, op, offset = brauch["rule"].split()
        datum = None
        if base == "ostern":
            datum = easter(jahr)
        if datum:
            if op == "-":
                datum -= datetime.timedelta(days=int(offset))
            elif op == "+":
                datum += datetime.timedelta(days=int(offset))
        return datum
    elif "date" in brauch:
        return datetime.date.fromisoformat(brauch["date"])
    return None


# Ergebnisse berechnen
resultate = []
for b in braeuche:
    datum = berechne_datum(b, jahr)
    if datum:
        resultate.append({
            "Datum": datum.strftime("%d.%m.%Y"),
            "Name": b["name"],
            "Region": b["region"],
            "Beschreibung": b.get("beschreibung", "")
        })

# Sortieren nach Datum
resultate = sorted(resultate, key=lambda x: datetime.datetime.strptime(x["Datum"], "%d.%m.%Y"))

st.table(resultate)
