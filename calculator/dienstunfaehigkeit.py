"""
Dienstunfähigkeits-Renten-Berechnung für Beamte NRW
"""

from calculator.gehalt import berechne_ruhegehaltsfaehige_bezuege
from calculator.pension import (
    berechne_dienstjahre,
    RUHEGEHALTSSATZ_PRO_JAHR,
    MAX_RUHEGEHALTSSATZ,
    MIN_RUHEGEHALTSSATZ,
    ABSCHLAG_PRO_JAHR,
    MAX_ABSCHLAG  # Max. 10,8% Abschlag in NRW
)
from data.besoldung import MINDESTVERSORGUNG_GRUNDGEHALT
from data.familienzuschlag import STANDARD_MIETENSTUFE


# Zurechnungszeit-Grenzen
# Vor 2019: Zurechnungszeit bis 60 Jahre
# Ab 2019: Zurechnungszeit bis 62 Jahre
ZURECHNUNGSZEIT_GRENZE_ALT = 60  # vor 2019
ZURECHNUNGSZEIT_GRENZE_NEU = 62  # ab 2019
ZURECHNUNGSZEIT_UEBERGANGSJAHR = 2019

# Faktor für Zurechnungszeit (2/3)
ZURECHNUNGSZEIT_FAKTOR = 2 / 3

# DU-Abschlag ab Alter unter 63
DU_ABSCHLAG_ALTERSGRENZE = 63

# Mindestversorgungssatz
MINDESTVERSORGUNGSSATZ = 65.0  # Prozent

# Wartezeit für Versorgungsanspruch
WARTEZEIT_JAHRE = 5  # Mindestens 5 Jahre Dienstzeit für Anspruch


def berechne_zurechnungszeit(
    alter_bei_du: int,
    jahr_du: int
) -> float:
    """
    Berechnet die Zurechnungszeit bei Dienstunfähigkeit.

    Args:
        alter_bei_du: Alter bei Eintritt der Dienstunfähigkeit
        jahr_du: Jahr der Dienstunfähigkeit

    Returns:
        Zurechnungszeit in Jahren
    """
    # Grenze abhängig vom Jahr der DU
    if jahr_du < ZURECHNUNGSZEIT_UEBERGANGSJAHR:
        grenze = ZURECHNUNGSZEIT_GRENZE_ALT
    else:
        grenze = ZURECHNUNGSZEIT_GRENZE_NEU

    # Zeit bis zur Grenze
    zeit_bis_grenze = grenze - alter_bei_du

    if zeit_bis_grenze <= 0:
        return 0.0

    # Zurechnungszeit = 2/3 der Zeit bis zur Grenze
    return zeit_bis_grenze * ZURECHNUNGSZEIT_FAKTOR


def berechne_du_abschlag(alter_bei_du: int) -> float:
    """
    Berechnet den Versorgungsabschlag bei Dienstunfähigkeit vor 63.

    Args:
        alter_bei_du: Alter bei Eintritt der Dienstunfähigkeit

    Returns:
        Abschlag in Prozent
    """
    if alter_bei_du >= DU_ABSCHLAG_ALTERSGRENZE:
        return 0.0

    jahre_vor_63 = DU_ABSCHLAG_ALTERSGRENZE - alter_bei_du
    abschlag = jahre_vor_63 * ABSCHLAG_PRO_JAHR

    # Max. 10,8% Abschlag in NRW
    return min(abschlag, MAX_ABSCHLAG)


def berechne_mindestversorgung() -> float:
    """
    Berechnet die Mindestversorgung (A4 Stufe 8 × 65%).

    Returns:
        Mindestversorgung in Euro
    """
    return round(MINDESTVERSORGUNG_GRUNDGEHALT * (MINDESTVERSORGUNGSSATZ / 100), 2)


def berechne_du_rente(
    besoldungsgruppe: str,
    stufe: int,
    geburtsjahr: int,
    jahr_verbeamtung: int,
    jahr_du: int,
    verheiratet: bool = False,
    mietenstufe: int = STANDARD_MIETENSTUFE,
    teilzeitjahre: float = 0,
    teilzeitanteil: float = 1.0,
    arbeitszeit_faktor: float = 1.0,
    ist_polizei_feuerwehr: bool = False
) -> dict:
    """
    Berechnet die Dienstunfähigkeitsrente.

    Args:
        besoldungsgruppe: z.B. "A13"
        stufe: Erfahrungsstufe
        geburtsjahr: Geburtsjahr
        jahr_verbeamtung: Jahr der Verbeamtung
        jahr_du: Jahr der Dienstunfähigkeit
        verheiratet: True wenn verheiratet
        mietenstufe: Mietenstufe
        teilzeitjahre: Jahre in Teilzeit
        teilzeitanteil: Anteil der Teilzeit
        arbeitszeit_faktor: Aktueller Arbeitszeit-Faktor
        ist_polizei_feuerwehr: True für Polizei/Feuerwehr

    Returns:
        Dictionary mit allen Berechnungsergebnissen
    """
    # Alter bei DU
    alter_bei_du = jahr_du - geburtsjahr

    # Tatsächliche Dienstjahre
    ist_dienstjahre = berechne_dienstjahre(
        jahr_verbeamtung,
        jahr_du,
        teilzeitjahre,
        teilzeitanteil
    )

    # Mindestversorgung berechnen
    mindestversorgung = berechne_mindestversorgung()

    # Prüfung: Wartezeit erfüllt (mindestens 5 Jahre Dienstzeit)?
    hat_anspruch = ist_dienstjahre >= WARTEZEIT_JAHRE

    if not hat_anspruch:
        # Kein Anspruch auf DU-Rente bei weniger als 5 Dienstjahren
        return {
            "alter_bei_du": alter_bei_du,
            "ist_dienstjahre": round(ist_dienstjahre, 2),
            "zurechnungszeit": 0.0,
            "gesamt_dienstjahre": round(ist_dienstjahre, 2),
            "ruhegehaltssatz_roh": 0.0,
            "ruhegehaltssatz": 0.0,
            "du_abschlag_prozent": 0.0,
            "effektiver_ruhegehaltssatz": 0.0,
            "ruhegehaltsfaehige_bezuege": 0.0,
            "du_rente_brutto": 0.0,
            "mindestversorgung": mindestversorgung,
            "wird_mindestversorgung": False,
            "hat_anspruch": False,
            "fehlende_dienstjahre": round(WARTEZEIT_JAHRE - ist_dienstjahre, 2),
        }

    # Ab hier: Anspruch vorhanden (>= 5 Jahre)

    # Zurechnungszeit
    zurechnungszeit = berechne_zurechnungszeit(alter_bei_du, jahr_du)

    # Gesamtdienstjahre für Ruhegehaltssatz
    gesamt_dienstjahre = ist_dienstjahre + zurechnungszeit

    # Ruhegehaltssatz (vor Abschlag)
    ruhegehaltssatz_roh = gesamt_dienstjahre * RUHEGEHALTSSATZ_PRO_JAHR
    ruhegehaltssatz = max(MIN_RUHEGEHALTSSATZ, min(MAX_RUHEGEHALTSSATZ, ruhegehaltssatz_roh))

    # DU-Abschlag
    du_abschlag = berechne_du_abschlag(alter_bei_du)

    # Effektiver Ruhegehaltssatz
    effektiver_satz = ruhegehaltssatz * (1 - du_abschlag / 100)

    # Ruhegehaltsfähige Bezüge
    ruhegehaltsfaehige_bezuege = berechne_ruhegehaltsfaehige_bezuege(
        besoldungsgruppe,
        stufe,
        verheiratet,
        mietenstufe,
        arbeitszeit_faktor
    )

    # DU-Rente brutto
    du_rente_brutto = ruhegehaltsfaehige_bezuege * (effektiver_satz / 100)

    # Mindestversorgung prüfen - gilt ab 5 Jahren Dienstzeit
    wird_mindestversorgung = du_rente_brutto < mindestversorgung

    if wird_mindestversorgung:
        du_rente_brutto = mindestversorgung

    return {
        "alter_bei_du": alter_bei_du,
        "ist_dienstjahre": round(ist_dienstjahre, 2),
        "zurechnungszeit": round(zurechnungszeit, 2),
        "gesamt_dienstjahre": round(gesamt_dienstjahre, 2),
        "ruhegehaltssatz_roh": round(ruhegehaltssatz_roh, 2),
        "ruhegehaltssatz": round(ruhegehaltssatz, 2),
        "du_abschlag_prozent": round(du_abschlag, 2),
        "effektiver_ruhegehaltssatz": round(effektiver_satz, 2),
        "ruhegehaltsfaehige_bezuege": ruhegehaltsfaehige_bezuege,
        "du_rente_brutto": round(du_rente_brutto, 2),
        "mindestversorgung": mindestversorgung,
        "wird_mindestversorgung": wird_mindestversorgung,
        "hat_anspruch": True,
        "fehlende_dienstjahre": 0.0,
    }


def berechne_du_entwicklung(
    besoldungsgruppe: str,
    stufe: int,
    geburtsjahr: int,
    jahr_verbeamtung: int,
    verheiratet: bool = False,
    mietenstufe: int = STANDARD_MIETENSTUFE,
    teilzeitjahre: float = 0,
    teilzeitanteil: float = 1.0,
    arbeitszeit_faktor: float = 1.0,
    ist_polizei_feuerwehr: bool = False,
    jahre_voraus: int = 30
) -> list:
    """
    Berechnet die DU-Rente für die nächsten Jahre.

    Args:
        jahre_voraus: Anzahl Jahre in die Zukunft

    Returns:
        Liste von Dictionaries mit DU-Rente pro Jahr
    """
    import datetime
    aktuelles_jahr = datetime.datetime.now().year

    ergebnisse = []

    for i in range(jahre_voraus + 1):
        jahr_du = aktuelles_jahr + i
        ergebnis = berechne_du_rente(
            besoldungsgruppe=besoldungsgruppe,
            stufe=stufe,
            geburtsjahr=geburtsjahr,
            jahr_verbeamtung=jahr_verbeamtung,
            jahr_du=jahr_du,
            verheiratet=verheiratet,
            mietenstufe=mietenstufe,
            teilzeitjahre=teilzeitjahre,
            teilzeitanteil=teilzeitanteil,
            arbeitszeit_faktor=arbeitszeit_faktor,
            ist_polizei_feuerwehr=ist_polizei_feuerwehr
        )
        ergebnis["jahr_du"] = jahr_du
        ergebnisse.append(ergebnis)

    return ergebnisse
