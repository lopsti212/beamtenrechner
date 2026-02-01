# Beamtenpensions-Rechner NRW

## Projektübersicht
Web-App zur Berechnung von Beamtenpensionen und Dienstunfähigkeitsrenten in NRW für Kundenberatungen.

## Technologie-Stack
- **Framework**: Streamlit
- **Grafiken**: Plotly
- **PDF-Export**: ReportLab
- **Daten**: Python-Dictionaries

## Projektstruktur
```
beamtenrechner/
├── app.py                    # Hauptanwendung (Streamlit)
├── data/
│   ├── besoldung.py          # Besoldungstabellen A5-A16
│   ├── familienzuschlag.py   # Familienzuschläge nach Stufe/Mietenstufe
│   ├── zulagen.py            # Strukturzulagen
│   └── lohnsteuer.py         # Lohnsteuertabelle
├── calculator/
│   ├── gehalt.py             # Bruttogehalt-Berechnung
│   ├── steuer.py             # Netto-Berechnung
│   ├── pension.py            # Ruhegehalt-Berechnung
│   └── dienstunfaehigkeit.py # DU-Renten-Berechnung
├── export/
│   └── pdf_report.py         # PDF-Export mit Tabellen
├── requirements.txt
└── CLAUDE.md
```

## Starten der Anwendung
```bash
cd ~/projekte/beamtenrechner
pip install -r requirements.txt
streamlit run app.py
```

## Wichtige Regeln NRW

### Besoldungsgruppen
- Nur A5-A16 (keine B-Besoldung)
- Erfahrungsstufen 1-8

### Mietenstufe
- Fest auf Stufe II (Datteln/Olfen)

### Laufbahngruppen (Strukturzulage)
- Laufbahngruppe 1: A5-A8 → 90,89€
- Laufbahngruppe 2: A9-A16 → 114,06€

### Altersgrenzen
| Beamtentyp | Regelaltersgrenze |
|------------|-------------------|
| Allgemein  | 67 Jahre          |
| Polizei/FW | 60 Jahre          |

### Ruhegehaltssatz
- 1,79375% pro Dienstjahr
- Minimum: 35% (bei ≥5 Jahren)
- Maximum: 71,75%

### Versorgungsabschlag
- 3,6% pro Jahr vor Regelaltersgrenze
- Maximum: 14,4%

### Dienstunfähigkeit
- Zurechnungszeit bis 62 Jahre (ab 2019)
- Faktor: 2/3
- Abschlag bei DU vor 63: 3,6% pro Jahr
- Mindestversorgung: A4 Stufe 8 × 65%

## Berechnungsformeln

### Bruttogehalt
```
Grundgehalt + Strukturzulage + Familienzuschlag + Kinderzuschlag
× Arbeitszeit-Faktor
```

### Ruhegehaltsfähige Bezüge
```
Grundgehalt + Strukturzulage + Familienzuschlag Stufe 1
× Arbeitszeit-Faktor
```

### Ruhegehalt
```
Ruhegehaltsfähige Bezüge × Ruhegehaltssatz × (1 - Abschlag)
```

### DU-Rente
```
Dienstjahre + Zurechnungszeit = Gesamt-Dienstjahre
Ruhegehaltsfähige Bezüge × DU-Satz × (1 - Abschlag)
Minimum: Mindestversorgung
```

## Testfall
- Besoldungsgruppe: A13
- Stufe: 5
- Geburtsjahr: 1988
- Verbeamtung: 2006
- Verheiratet: Ja
- 2 Kinder
- Steuerklasse: 3
