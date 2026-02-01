"""
Beamtenpensions-Rechner NRW
Streamlit-Hauptanwendung für die Berechnung von Beamtenpensionen und Dienstunfähigkeitsrenten
"""

import streamlit as st
import plotly.graph_objects as go
import datetime
import sys
import os

# Projektpfad hinzufügen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.besoldung import get_besoldungsgruppen, get_max_stufe, get_min_stufe
from data.familienzuschlag import STANDARD_MIETENSTUFE
from calculator.gehalt import berechne_bruttogehalt
from calculator.steuer import berechne_netto
from calculator.pension import berechne_ruhegehalt, berechne_pension_nach_alter
from calculator.dienstunfaehigkeit import berechne_du_rente

# Pfad zum Favicon
FAVICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "favicon.png")

# Seitenkonfiguration
st.set_page_config(
    page_title="Beamtenpensions-Rechner NRW",
    page_icon=FAVICON_PATH if os.path.exists(FAVICON_PATH) else "JG",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS für professionelles dunkles Design
st.markdown("""
<style>
    /* Basis-Schriftgröße reduzieren */
    html, body, [class*="css"] {
        font-size: 13px;
    }

    /* Haupthintergrund */
    .stApp {
        background-color: #1a1a1a;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #252525;
        border-right: 1px solid #3a3a3a;
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: #e0e0e0;
    }

    /* Header-Styling */
    h1 {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #4a4a4a;
        padding-bottom: 10px;
        margin-bottom: 20px !important;
    }

    h2 {
        color: #e0e0e0 !important;
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        margin-top: 15px !important;
        margin-bottom: 10px !important;
    }

    h3 {
        color: #d0d0d0 !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
    }

    /* Metric-Styling */
    [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
        color: #ffffff !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
        color: #a0a0a0 !important;
    }

    /* Cards/Container */
    .result-card {
        background-color: #2a2a2a;
        border: 1px solid #3a3a3a;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
    }

    .result-card-header {
        color: #b0b0b0;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
        padding-bottom: 8px;
        border-bottom: 1px solid #3a3a3a;
    }

    .result-value {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 600;
    }

    .result-subvalue {
        color: #808080;
        font-size: 0.8rem;
    }

    /* Versorgungslücke-Box */
    .warning-box {
        background-color: #3d1f1f;
        border: 1px solid #6b2b2b;
        border-left: 4px solid #c0392b;
        border-radius: 4px;
        padding: 15px;
        margin: 15px 0;
    }

    .warning-box-title {
        color: #e74c3c;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 5px;
    }

    .warning-box-value {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
    }

    .warning-box-detail {
        color: #b0b0b0;
        font-size: 0.85rem;
        margin-top: 8px;
    }

    /* Tabellen */
    .stTable {
        font-size: 0.85rem !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #252525;
        border-radius: 4px;
        padding: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        color: #a0a0a0;
        font-size: 0.85rem;
    }

    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        background-color: #3a3a3a;
    }

    /* Input-Felder in Sidebar */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] select {
        font-size: 0.85rem !important;
    }

    [data-testid="stSidebar"] label {
        font-size: 0.8rem !important;
        color: #b0b0b0 !important;
    }

    /* Sidebar Subheader */
    [data-testid="stSidebar"] h2 {
        font-size: 0.9rem !important;
        color: #808080 !important;
        border-bottom: 1px solid #3a3a3a;
        padding-bottom: 5px;
        margin-top: 20px !important;
    }

    /* Divider */
    hr {
        border-color: #3a3a3a !important;
    }

    /* Button */
    .stButton > button {
        background-color: #3a3a3a;
        color: #ffffff;
        border: 1px solid #4a4a4a;
        font-size: 0.85rem;
    }

    .stButton > button:hover {
        background-color: #4a4a4a;
        border-color: #5a5a5a;
    }

    /* Download Button */
    .stDownloadButton > button {
        background-color: #2d5a2d;
        border-color: #3d7a3d;
    }

    /* Info Box in Sidebar */
    [data-testid="stSidebar"] .stAlert {
        background-color: #2a2a2a;
        border: 1px solid #3a3a3a;
        font-size: 0.75rem;
        padding: 8px;
    }

    /* Caption */
    .stCaption {
        color: #707070 !important;
        font-size: 0.75rem !important;
    }

    /* Markdown Tabellen */
    table {
        font-size: 0.85rem !important;
    }

    th {
        background-color: #2a2a2a !important;
        color: #b0b0b0 !important;
    }

    td {
        background-color: #1f1f1f !important;
        color: #e0e0e0 !important;
    }

    /* Section Divider */
    .section-divider {
        border-top: 1px solid #3a3a3a;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Titel
st.title("Beamtenpensions-Rechner NRW")

# Sidebar für Eingaben
st.sidebar.markdown("### Eingabedaten")

# 1. Persönliche Daten
st.sidebar.markdown("## Persönliche Daten")
aktuelles_jahr = datetime.datetime.now().year

geburtsjahr = st.sidebar.number_input(
    "Geburtsjahr",
    min_value=1950,
    max_value=2005,
    value=1988,
    step=1
)

jahr_verbeamtung = st.sidebar.number_input(
    "Jahr der Verbeamtung",
    min_value=1970,
    max_value=aktuelles_jahr,
    value=2006,
    step=1
)

besoldungsgruppe = st.sidebar.selectbox(
    "Besoldungsgruppe",
    options=get_besoldungsgruppen(),
    index=8
)

max_stufe = get_max_stufe(besoldungsgruppe)
min_stufe = get_min_stufe(besoldungsgruppe)
stufe = st.sidebar.number_input(
    "Erfahrungsstufe",
    min_value=min_stufe,
    max_value=max_stufe,
    value=max(5, min_stufe),  # Standard: 5 oder Mindeststufe
    step=1
)

# 2. Familiensituation
st.sidebar.markdown("## Familiensituation")

verheiratet = st.sidebar.checkbox("Verheiratet", value=True)

anzahl_kinder = st.sidebar.number_input(
    "Anzahl Kinder",
    min_value=0,
    max_value=10,
    value=2,
    step=1
)

mietenstufe = STANDARD_MIETENSTUFE
st.sidebar.caption("Mietenstufe: II (Datteln/Olfen)")

steuerklasse = st.sidebar.selectbox(
    "Steuerklasse",
    options=[1, 2, 3, 4, 5, 6],
    index=2
)

kirchensteuer = st.sidebar.checkbox("Kirchensteuer", value=False)

pkv_beitrag = st.sidebar.number_input(
    "PKV-Beitrag (€/Monat)",
    min_value=0.0,
    max_value=2000.0,
    value=0.0,
    step=10.0,
    help="Optionaler monatlicher PKV-Beitrag. Bei 0 wird kein Beitrag abgezogen."
)

# 3. Dienstzeiten
st.sidebar.markdown("## Dienstzeiten")

teilzeitjahre = st.sidebar.number_input(
    "Teilzeitjahre",
    min_value=0.0,
    max_value=40.0,
    value=0.0,
    step=0.5
)

teilzeitanteil = st.sidebar.slider(
    "Teilzeitanteil (%)",
    min_value=10,
    max_value=100,
    value=50,
    step=5
) / 100

arbeitszeit_faktor = st.sidebar.slider(
    "Aktueller Arbeitszeit-Faktor (%)",
    min_value=10,
    max_value=100,
    value=100,
    step=5
) / 100

# 4. Beamtentyp & Szenarien
st.sidebar.markdown("## Szenarien")

ist_polizei_feuerwehr = st.sidebar.checkbox("Polizei/Feuerwehr", value=False)

if ist_polizei_feuerwehr:
    regelaltersgrenze = 60
else:
    regelaltersgrenze = 67

gewuenschtes_pensionsalter = st.sidebar.number_input(
    "Gewünschtes Pensionsalter",
    min_value=60,
    max_value=70,
    value=min(67, regelaltersgrenze),
    step=1
)

aktuelles_alter = aktuelles_jahr - geburtsjahr
du_szenario_jahr = st.sidebar.number_input(
    "DU-Szenario Jahr",
    min_value=aktuelles_jahr,
    max_value=aktuelles_jahr + 40,
    value=aktuelles_jahr + 1,
    step=1
)

# Berechnungen durchführen
gehalt = berechne_bruttogehalt(
    besoldungsgruppe=besoldungsgruppe,
    stufe=stufe,
    verheiratet=verheiratet,
    anzahl_kinder=anzahl_kinder,
    mietenstufe=mietenstufe,
    arbeitszeit_faktor=arbeitszeit_faktor
)

netto_daten = berechne_netto(
    brutto_monatlich=gehalt["brutto"],
    steuerklasse=steuerklasse,
    kirchensteuer=kirchensteuer,
    pkv_beitrag=pkv_beitrag
)

jahr_pension = geburtsjahr + gewuenschtes_pensionsalter
pension = berechne_ruhegehalt(
    besoldungsgruppe=besoldungsgruppe,
    stufe=stufe,
    geburtsjahr=geburtsjahr,
    jahr_verbeamtung=jahr_verbeamtung,
    jahr_pension=jahr_pension,
    verheiratet=verheiratet,
    mietenstufe=mietenstufe,
    teilzeitjahre=teilzeitjahre,
    teilzeitanteil=teilzeitanteil,
    arbeitszeit_faktor=arbeitszeit_faktor,
    ist_polizei_feuerwehr=ist_polizei_feuerwehr
)

du_rente = berechne_du_rente(
    besoldungsgruppe=besoldungsgruppe,
    stufe=stufe,
    geburtsjahr=geburtsjahr,
    jahr_verbeamtung=jahr_verbeamtung,
    jahr_du=du_szenario_jahr,
    verheiratet=verheiratet,
    mietenstufe=mietenstufe,
    teilzeitjahre=teilzeitjahre,
    teilzeitanteil=teilzeitanteil,
    arbeitszeit_faktor=arbeitszeit_faktor,
    ist_polizei_feuerwehr=ist_polizei_feuerwehr
)

versorgungsluecke = netto_daten["netto"] - du_rente["du_rente_brutto"]

# Kindergeld berechnen (nur zur Info, nicht im Netto enthalten)
KINDERGELD_PRO_KIND = 259.0  # Stand 2026
kindergeld_gesamt = anzahl_kinder * KINDERGELD_PRO_KIND

# Hilfsfunktion für Euro-Formatierung
def fmt_euro(betrag):
    return f"{betrag:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

# Hauptbereich - Ergebnisse
st.markdown("## Übersicht")

# Vier Spalten für kompakte Darstellung
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="result-card">
        <div class="result-card-header">Aktuelles Brutto</div>
        <div class="result-value">""" + fmt_euro(gehalt['brutto']) + """</div>
        <div class="result-subvalue">""" + besoldungsgruppe + " Stufe " + str(stufe) + """</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="result-card">
        <div class="result-card-header">Aktuelles Netto</div>
        <div class="result-value">""" + fmt_euro(netto_daten['netto']) + """</div>
        <div class="result-subvalue">Steuerklasse """ + str(steuerklasse) + """</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    abschlag_text = f"inkl. {pension['versorgungsabschlag_prozent']:.2f}% Abschlag" if pension['versorgungsabschlag_prozent'] > 0 else f"{pension['effektiver_ruhegehaltssatz']:.2f}% Ruhegehaltssatz"
    stufe_pension_text = f"Stufe {pension.get('stufe_bei_pension', stufe)}"
    st.markdown("""
    <div class="result-card">
        <div class="result-card-header">Altersrente (""" + str(gewuenschtes_pensionsalter) + """ J.)</div>
        <div class="result-value">""" + fmt_euro(pension['ruhegehalt_brutto']) + """</div>
        <div class="result-subvalue">""" + stufe_pension_text + """, """ + abschlag_text + """</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    if du_rente.get('hat_anspruch', True):
        du_abschlag_text = f"inkl. {du_rente['du_abschlag_prozent']:.2f}% Abschlag" if du_rente['du_abschlag_prozent'] > 0 else f"{du_rente['effektiver_ruhegehaltssatz']:.2f}% Ruhegehaltssatz"
        if du_rente.get('wird_mindestversorgung', False):
            du_abschlag_text = "Mindestversorgung"
        st.markdown("""
        <div class="result-card">
            <div class="result-card-header">DU-Rente (""" + str(du_szenario_jahr) + """)</div>
            <div class="result-value">""" + fmt_euro(du_rente['du_rente_brutto']) + """</div>
            <div class="result-subvalue">Alter """ + str(du_rente['alter_bei_du']) + """, """ + du_abschlag_text + """</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-card" style="border-color: #6b2b2b;">
            <div class="result-card-header">DU-Rente (""" + str(du_szenario_jahr) + """)</div>
            <div class="result-value" style="color: #e74c3c;">KEIN ANSPRUCH</div>
            <div class="result-subvalue">Noch """ + str(du_rente['fehlende_dienstjahre']) + """ Jahre bis Anspruch (5 J. Wartezeit)</div>
        </div>
        """, unsafe_allow_html=True)

# Versorgungslücke
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("## Versorgungslücke bei Dienstunfähigkeit")

col_vl1, col_vl2 = st.columns([3, 2])

with col_vl1:
    if not du_rente.get('hat_anspruch', True):
        # Kein Anspruch - volle Versorgungslücke
        st.markdown("""
        <div class="warning-box" style="border-left-color: #8e44ad;">
            <div class="warning-box-title" style="color: #9b59b6;">KEIN ANSPRUCH AUF DU-RENTE</div>
            <div class="warning-box-value">""" + fmt_euro(netto_daten['netto']) + """ / Monat</div>
            <div class="warning-box-detail">
                Bei Dienstunfähigkeit im Jahr """ + str(du_szenario_jahr) + """ besteht <strong>kein Anspruch</strong> auf eine DU-Rente.<br>
                Die 5-jährige Wartezeit ist noch nicht erfüllt (noch """ + str(du_rente['fehlende_dienstjahre']) + """ Jahre).<br>
                <strong>Das gesamte Nettoeinkommen von """ + fmt_euro(netto_daten['netto'] * 12) + """ pro Jahr wäre nicht abgesichert.</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif versorgungsluecke > 0:
        st.markdown("""
        <div class="warning-box">
            <div class="warning-box-title">VERSORGUNGSLÜCKE</div>
            <div class="warning-box-value">""" + fmt_euro(versorgungsluecke) + """ / Monat</div>
            <div class="warning-box-detail">
                Bei Dienstunfähigkeit im Jahr """ + str(du_szenario_jahr) + """ fehlen monatlich """ + fmt_euro(versorgungsluecke) + """
                gegenüber dem aktuellen Nettoeinkommen.<br>
                <strong>Das sind """ + fmt_euro(versorgungsluecke * 12) + """ pro Jahr.</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("Keine Versorgungslücke - DU-Rente deckt das aktuelle Netto.")

with col_vl2:
    fig_luecke = go.Figure()

    fig_luecke.add_trace(go.Bar(
        x=["Netto", "DU-Rente"],
        y=[netto_daten["netto"], du_rente["du_rente_brutto"]],
        marker_color=["#4a7c4a", "#7c4a4a"],
        text=[fmt_euro(netto_daten["netto"]), fmt_euro(du_rente["du_rente_brutto"])],
        textposition="inside",
        textfont=dict(color="#e0e0e0", size=11)
    ))

    fig_luecke.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#a0a0a0', size=10),
        margin=dict(l=20, r=20, t=30, b=20),
        height=200,
        yaxis=dict(gridcolor='#3a3a3a', showgrid=True),
        xaxis=dict(showgrid=False),
        showlegend=False
    )

    st.plotly_chart(fig_luecke, use_container_width=True)

# Detailierte Berechnungen
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("## Details")

tab1, tab2, tab3, tab4 = st.tabs(["Gehalt", "Altersrente", "DU-Rente", "Vergleich"])

with tab1:
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("**Gehaltsbestandteile**")
        st.markdown(f"""
| Bestandteil | Betrag |
|-------------|-------:|
| Grundgehalt ({besoldungsgruppe}, Stufe {stufe}) | {fmt_euro(gehalt['grundgehalt'])} |
| Strukturzulage | {fmt_euro(gehalt['strukturzulage'])} |
| Familienzuschlag Stufe 1 | {fmt_euro(gehalt['familienzuschlag_stufe1'])} |
| Kinderzuschlag ({anzahl_kinder} Kinder) | {fmt_euro(gehalt['kinderzuschlag'])} |
| **Brutto (Vollzeit)** | **{fmt_euro(gehalt['brutto_vollzeit'])}** |
| Arbeitszeit-Faktor | {arbeitszeit_faktor * 100:.0f}% |
| **Brutto (aktuell)** | **{fmt_euro(gehalt['brutto'])}** |
        """)

    with col_g2:
        st.markdown("**Abzüge**")
        pkv_label = "PKV-Beitrag" if pkv_beitrag > 0 else "PKV-Beitrag (nicht angegeben)"
        st.markdown(f"""
| Abzug | Betrag |
|-------|-------:|
| Lohnsteuer | {fmt_euro(netto_daten['lohnsteuer'])} |
| Solidaritätszuschlag | {fmt_euro(netto_daten['solidaritaetszuschlag'])} |
| Kirchensteuer | {fmt_euro(netto_daten['kirchensteuer'])} |
| {pkv_label} | {fmt_euro(netto_daten['pkv_beitrag'])} |
| **Abzüge gesamt** | **{fmt_euro(netto_daten['abzuege_gesamt'])}** |
| **Netto** | **{fmt_euro(netto_daten['netto'])}** |
        """)

        # Kindergeld Info
        if anzahl_kinder > 0:
            st.markdown("---")
            st.markdown("**Kindergeld (Info)**")
            st.markdown(f"""
| Info | Betrag |
|------|-------:|
| Kindergeld pro Kind | {fmt_euro(KINDERGELD_PRO_KIND)} |
| Kindergeld gesamt ({anzahl_kinder} Kinder) | {fmt_euro(kindergeld_gesamt)} |
            """)
            st.caption("Kindergeld wird separat ausgezahlt und ist nicht im Netto enthalten.")

with tab2:
    col_p1, col_p2 = st.columns([1, 2])

    with col_p1:
        st.markdown("**Parameter**")
        stufe_info = f"Stufe {pension.get('stufe_bei_pension', stufe)}"
        if pension.get('stufe_bei_pension', stufe) == pension.get('max_stufe', 12):
            stufe_info += " (max)"
        st.markdown(f"""
| Parameter | Wert |
|-----------|-----:|
| Pensionsalter | {gewuenschtes_pensionsalter} Jahre |
| Jahr | {jahr_pension} |
| **Erfahrungsstufe bei Pension** | **{stufe_info}** |
| Regelaltersgrenze | {pension['regelaltersgrenze']} Jahre |
| Dienstjahre | {pension['dienstjahre']:.1f} Jahre |
| Ruhegehaltssatz | {pension['ruhegehaltssatz']:.2f}% |
| Versorgungsabschlag | {pension['versorgungsabschlag_prozent']:.2f}% |
| **Eff. Satz** | **{pension['effektiver_ruhegehaltssatz']:.2f}%** |
| Ruhegehaltsfähige Bezüge | {fmt_euro(pension['ruhegehaltsfaehige_bezuege'])} |
| **Ruhegehalt brutto** | **{fmt_euro(pension['ruhegehalt_brutto'])}** |
        """)
        st.caption(f"Aktuelle Stufe: {stufe} → Bei Pension: {pension.get('stufe_bei_pension', stufe)}")

    with col_p2:
        st.markdown("**Pensionsentwicklung nach Alter**")

        # Antragsaltersgrenze: 63 für normale Beamte, 55 für Polizei/FW (Übersicht)
        von_alter_vergleich = 55 if ist_polizei_feuerwehr else 63

        pension_verlauf = berechne_pension_nach_alter(
            besoldungsgruppe=besoldungsgruppe,
            stufe=stufe,
            geburtsjahr=geburtsjahr,
            jahr_verbeamtung=jahr_verbeamtung,
            verheiratet=verheiratet,
            mietenstufe=mietenstufe,
            teilzeitjahre=teilzeitjahre,
            teilzeitanteil=teilzeitanteil,
            arbeitszeit_faktor=arbeitszeit_faktor,
            ist_polizei_feuerwehr=ist_polizei_feuerwehr,
            von_alter=von_alter_vergleich,
            bis_alter=67
        )

        alter_liste = [p["pensionsalter"] for p in pension_verlauf]
        pension_liste = [p["ruhegehalt_brutto"] for p in pension_verlauf]
        abschlag_liste = [p["versorgungsabschlag_prozent"] for p in pension_verlauf]

        fig_pension = go.Figure()

        fig_pension.add_trace(go.Bar(
            x=alter_liste,
            y=pension_liste,
            marker_color=["#7c4a4a" if a > 0 else "#4a7c4a" for a in abschlag_liste],
            text=[fmt_euro(p) for p in pension_liste],
            textposition="inside",
            textfont=dict(color="#e0e0e0", size=9)
        ))

        fig_pension.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#a0a0a0', size=10),
            margin=dict(l=20, r=20, t=10, b=30),
            height=250,
            yaxis=dict(gridcolor='#3a3a3a', showgrid=True),
            xaxis=dict(showgrid=False, title="Pensionsalter"),
            showlegend=False
        )

        st.plotly_chart(fig_pension, use_container_width=True)
        st.caption("Rot = mit Abschlag, Grün = ohne Abschlag")

with tab3:
    st.markdown("**DU-Renten-Berechnung**")
    if not du_rente.get('hat_anspruch', True):
        st.error(f"**Kein Anspruch auf DU-Rente** - Die 5-jährige Wartezeit ist nicht erfüllt.")
        st.markdown(f"""
| Parameter | Wert |
|-----------|-----:|
| DU-Szenario Jahr | {du_szenario_jahr} |
| Alter bei DU | {du_rente['alter_bei_du']} Jahre |
| Ist-Dienstjahre | {du_rente['ist_dienstjahre']:.2f} Jahre |
| **Wartezeit erforderlich** | **5,00 Jahre** |
| **Fehlende Dienstjahre** | **{du_rente['fehlende_dienstjahre']:.2f} Jahre** |
| DU-Rente | **0,00 €** |
        """)
        st.info("Nach Erfüllung der 5-jährigen Wartezeit besteht Anspruch auf mindestens die Mindestversorgung.")
    else:
        st.markdown(f"""
| Parameter | Wert |
|-----------|-----:|
| DU-Szenario Jahr | {du_szenario_jahr} |
| Alter bei DU | {du_rente['alter_bei_du']} Jahre |
| Ist-Dienstjahre | {du_rente['ist_dienstjahre']:.2f} Jahre |
| Zurechnungszeit | {du_rente['zurechnungszeit']:.2f} Jahre |
| **Gesamt-Dienstjahre** | **{du_rente['gesamt_dienstjahre']:.2f} Jahre** |
| Ruhegehaltssatz (vor Abschlag) | {du_rente['ruhegehaltssatz']:.2f}% |
| DU-Abschlag | {du_rente['du_abschlag_prozent']:.2f}% |
| **Effektiver Ruhegehaltssatz** | **{du_rente['effektiver_ruhegehaltssatz']:.2f}%** |
| Ruhegehaltsfähige Bezüge | {fmt_euro(du_rente['ruhegehaltsfaehige_bezuege'])} |
| **DU-Rente brutto** | **{fmt_euro(du_rente['du_rente_brutto'])}** |
| Mindestversorgung | {fmt_euro(du_rente['mindestversorgung'])} |
| Mindestversorgung aktiv? | {'Ja' if du_rente['wird_mindestversorgung'] else 'Nein'} |
        """)

with tab4:
    col_v1, col_v2 = st.columns([2, 1])

    with col_v1:
        fig_vergleich = go.Figure()

        kategorien = ["Brutto", "Netto", "DU-Rente", "Altersrente"]
        werte = [gehalt["brutto"], netto_daten["netto"], du_rente["du_rente_brutto"], pension["ruhegehalt_brutto"]]
        farben = ["#5a5a5a", "#4a7c4a", "#7c4a4a", "#7c6a4a"]

        fig_vergleich.add_trace(go.Bar(
            x=kategorien,
            y=werte,
            marker_color=farben,
            text=[fmt_euro(w) for w in werte],
            textposition="inside",
            textfont=dict(color="#e0e0e0", size=11)
        ))

        fig_vergleich.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#a0a0a0', size=10),
            margin=dict(l=20, r=20, t=20, b=30),
            height=280,
            yaxis=dict(gridcolor='#3a3a3a', showgrid=True),
            xaxis=dict(showgrid=False),
            showlegend=False
        )

        st.plotly_chart(fig_vergleich, use_container_width=True)

    with col_v2:
        st.markdown("**Pensionsalter-Vergleich**")

        vergleich_text = "| Alter | Stufe | Pension | Abschlag |\n|------:|------:|--------:|---------:|\n"
        for p in pension_verlauf:
            stufe_p = p.get('stufe_bei_pension', stufe)
            vergleich_text += f"| {p['pensionsalter']} | {stufe_p} | {fmt_euro(p['ruhegehalt_brutto'])} | {p['versorgungsabschlag_prozent']:.2f}% |\n"

        st.markdown(vergleich_text)

# PDF-Export
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("## Export")

if "export_data" not in st.session_state:
    st.session_state.export_data = {}

st.session_state.export_data = {
    "geburtsjahr": geburtsjahr,
    "jahr_verbeamtung": jahr_verbeamtung,
    "besoldungsgruppe": besoldungsgruppe,
    "stufe": stufe,
    "verheiratet": verheiratet,
    "anzahl_kinder": anzahl_kinder,
    "steuerklasse": steuerklasse,
    "teilzeitjahre": teilzeitjahre,
    "teilzeitanteil": teilzeitanteil,
    "arbeitszeit_faktor": arbeitszeit_faktor,
    "ist_polizei_feuerwehr": ist_polizei_feuerwehr,
    "gewuenschtes_pensionsalter": gewuenschtes_pensionsalter,
    "du_szenario_jahr": du_szenario_jahr,
    "gehalt": gehalt,
    "netto_daten": netto_daten,
    "pension": pension,
    "du_rente": du_rente,
    "versorgungsluecke": versorgungsluecke,
}

try:
    from export.pdf_report import erstelle_pdf_report

    if st.button("PDF-Report erstellen"):
        with st.spinner("PDF wird erstellt..."):
            pdf_bytes = erstelle_pdf_report(st.session_state.export_data)

            st.download_button(
                label="PDF herunterladen",
                data=pdf_bytes,
                file_name=f"Beamtenpension_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
except ImportError:
    st.warning("PDF-Export-Modul nicht verfügbar.")

# Footer
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.caption("Beamtenrechner NRW | Alle Angaben ohne Gewähr | Stand Februar 2025")
