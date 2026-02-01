# Beamtenpensions-Rechner NRW

## Projektübersicht
Web-App zur Berechnung von Beamtenpensionen und Dienstunfähigkeitsrenten in NRW für Kundenberatungen.
Entwickelt für Vertrieb/Verkaufsgespräche mit Versorgungslücken-Fokus.

## Technologie-Stack
- **Framework**: Streamlit
- **Grafiken**: Plotly
- **PDF-Export**: ReportLab
- **Deployment**: Streamlit Cloud (https://github.com/lopsti212/beamtenrechner)

## Starten der Anwendung
```bash
cd ~/projekte/beamtenrechner
streamlit run app.py
```

## Wichtige Datenquellen (im Ordner ~/projekte/)
- `familienzuschlaege-01.02.2025.pdf` - Offizielle Familienzuschlag-Tabelle
- `besoldungstabellen-a-b-r-und-w-01.02.2025.pdf` - Besoldungstabellen
- `Kindergeld2026.xlsx` - Kindergeld 259€/Kind
- `Mappe.xlsx` - Besoldungswerte

## Berechnungsregeln NRW (Stand Februar 2025)

### Besoldungsgruppen & Einstiegsstufen
| Gruppe | Einstiegsstufe | Max. Stufe |
|--------|----------------|------------|
| A5-A11 | 3 | 10-12 |
| A12 | 4 | 12 |
| A13-A14 | 5 | 12 |
| A15-A16 | 6 | 12 |

### Stufenlaufzeiten (§27 LBesG NRW)
- Stufe 3→4, 4→5: je 2 Jahre
- Stufe 5→6, 6→7, 7→8: je 3 Jahre
- Ab Stufe 8: je 4 Jahre

### Ruhegehalt
- Ruhegehaltssatz: 1,79375% pro Dienstjahr
- Minimum: 35% (bei ≥5 Jahren)
- Maximum: 71,75%
- **Versorgungsabschlag: max. 10,8%** (für alle Beamten in NRW!)

### Altersgrenzen
| Beamtentyp | Regelaltersgrenze | Antragsaltersgrenze |
|------------|-------------------|---------------------|
| Allgemein | 67 Jahre | 63 Jahre |
| Polizei/FW | 60 Jahre | 55 Jahre |

### Dienstunfähigkeit (DU)
- **Wartezeit: 5 Jahre** (vorher kein Anspruch!)
- Zurechnungszeit: (62 - Alter bei DU) × 2/3
- DU-Abschlag bei Alter < 63: max. 10,8%
- Mindestversorgung: A4 Stufe 8 × 65% = 2.052,54€

### Familienzuschlag
- Abhängig von: Besoldungsgruppe-Kategorie (A5-A6, A7-A8, A9+) + Mietenstufe (I-VII)
- Standard-Mietenstufe: II (Datteln/Olfen)
- Stufe 1 (verheiratet): ~168,76€ (A9+)
- Mit Kindern: Stufe 2-5 aus Tabelle (enthält bereits Stufe 1)

### Strukturzulage
- A5-A8: 90,89€
- A9-A16: 114,06€

## Features für Vertrieb
1. Versorgungslücke (monatlich + Gesamtlaufzeit)
2. Absicherungsbedarf-Rechner (% vom Netto einstellbar)
3. Szenarien-Vergleich (DU in 0/5/10/15/20 Jahren)
4. Timeline-Chart (DU-Rente vs. Lücke)
5. Inflationsrechner
6. Kindergeld-Info (nicht im Netto)
7. PKV-Beitrag optional eingebbar

## Git-Workflow
```bash
git add -A
git commit -m "Beschreibung"
git push --force-with-lease  # Bei Token-Abfrage: GitHub PAT verwenden
```

## Bekannte Besonderheiten
- Zurechnungszeit kann junge Beamte mit wenig Dienstjahren auf hohe DU-Renten bringen (gewollt!)
- Beispiel: 24-Jähriger mit 5 Jahren → 30,33 Gesamt-Dienstjahre → 2.589€ DU-Rente
