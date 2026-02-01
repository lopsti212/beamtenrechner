"""
Ruhegehalt-Berechnung (Altersrente) für Beamte NRW
"""

from calculator.gehalt import berechne_ruhegehaltsfaehige_bezuege
from data.familienzuschlag import STANDARD_MIETENSTUFE
from data.besoldung import berechne_stufe_nach_dienstjahren, get_max_stufe


# Konstanten
RUHEGEHALTSSATZ_PRO_JAHR = 1.79375  # Prozent pro Dienstjahr
MAX_RUHEGEHALTSSATZ = 71.75  # Maximum in Prozent
MIN_RUHEGEHALTSSATZ = 35.0  # Minimum bei mindestens 5 Jahren Dienstzeit
MIN_DIENSTJAHRE = 5  # Mindestens 5 Jahre für Pensionsanspruch

# Altersgrenzen
REGELALTERSGRENZE_NORMAL = 67
REGELALTERSGRENZE_POLIZEI = 60
ANTRAGSALTERSGRENZE_NORMAL = 63
ANTRAGSALTERSGRENZE_POLIZEI = 60

# Versorgungsabschlag
ABSCHLAG_PRO_JAHR = 3.6  # Prozent pro Jahr vor Altersgrenze
MAX_ABSCHLAG = 10.8  # Maximum Versorgungsabschlag NRW (§16 LBeamtVG NRW)


def berechne_dienstjahre(
    jahr_verbeamtung: int,
    jahr_pension: int,
    teilzeitjahre: float = 0,
    teilzeitanteil: float = 1.0
) -> float:
    """
    Berechnet die ruhegehaltsfähigen Dienstjahre.

    Args:
        jahr_verbeamtung: Jahr der Verbeamtung
        jahr_pension: Jahr des Pensionsantritts
        teilzeitjahre: Anzahl der Jahre in Teilzeit
        teilzeitanteil: Anteil der Teilzeit (z.B. 0.5 für 50%)

    Returns:
        Ruhegehaltsfähige Dienstjahre
    """
    gesamtjahre = jahr_pension - jahr_verbeamtung
    vollzeitjahre = gesamtjahre - teilzeitjahre

    # Teilzeitjahre werden anteilig gerechnet
    anrechenbare_teilzeit = teilzeitjahre * teilzeitanteil

    return vollzeitjahre + anrechenbare_teilzeit


def berechne_ruhegehaltssatz(dienstjahre: float) -> float:
    """
    Berechnet den Ruhegehaltssatz aus den Dienstjahren.

    Args:
        dienstjahre: Ruhegehaltsfähige Dienstjahre

    Returns:
        Ruhegehaltssatz in Prozent
    """
    if dienstjahre < MIN_DIENSTJAHRE:
        return 0.0

    ruhegehaltssatz = dienstjahre * RUHEGEHALTSSATZ_PRO_JAHR

    # Minimum und Maximum beachten
    ruhegehaltssatz = max(MIN_RUHEGEHALTSSATZ, ruhegehaltssatz)
    ruhegehaltssatz = min(MAX_RUHEGEHALTSSATZ, ruhegehaltssatz)

    return round(ruhegehaltssatz, 2)


def berechne_versorgungsabschlag(
    geburtsjahr: int,
    jahr_pension: int,
    ist_polizei_feuerwehr: bool = False
) -> float:
    """
    Berechnet den Versorgungsabschlag bei vorzeitiger Pensionierung.

    Args:
        geburtsjahr: Geburtsjahr des Beamten
        jahr_pension: Jahr des Pensionsantritts
        ist_polizei_feuerwehr: True für Polizei/Feuerwehr

    Returns:
        Versorgungsabschlag in Prozent
    """
    # Alter bei Pensionierung
    alter_pension = jahr_pension - geburtsjahr

    # Regelaltersgrenze
    if ist_polizei_feuerwehr:
        regelaltersgrenze = REGELALTERSGRENZE_POLIZEI
    else:
        regelaltersgrenze = REGELALTERSGRENZE_NORMAL

    # Jahre vor Regelaltersgrenze
    jahre_vor_grenze = regelaltersgrenze - alter_pension

    if jahre_vor_grenze <= 0:
        return 0.0

    # Abschlag berechnen
    abschlag = jahre_vor_grenze * ABSCHLAG_PRO_JAHR

    # Maximum beachten (10,8% in NRW)
    return min(abschlag, MAX_ABSCHLAG)


def berechne_ruhegehalt(
    besoldungsgruppe: str,
    stufe: int,
    geburtsjahr: int,
    jahr_verbeamtung: int,
    jahr_pension: int,
    verheiratet: bool = False,
    mietenstufe: int = STANDARD_MIETENSTUFE,
    teilzeitjahre: float = 0,
    teilzeitanteil: float = 1.0,
    arbeitszeit_faktor: float = 1.0,
    ist_polizei_feuerwehr: bool = False
) -> dict:
    """
    Berechnet das vollständige Ruhegehalt.

    Args:
        besoldungsgruppe: z.B. "A13"
        stufe: Aktuelle Erfahrungsstufe
        geburtsjahr: Geburtsjahr
        jahr_verbeamtung: Jahr der Verbeamtung
        jahr_pension: Gewünschtes Jahr der Pensionierung
        verheiratet: True wenn verheiratet
        mietenstufe: Mietenstufe
        teilzeitjahre: Jahre in Teilzeit
        teilzeitanteil: Anteil der Teilzeit
        arbeitszeit_faktor: Aktueller Arbeitszeit-Faktor
        ist_polizei_feuerwehr: True für Polizei/Feuerwehr

    Returns:
        Dictionary mit allen Berechnungsergebnissen
    """
    import datetime
    aktuelles_jahr = datetime.datetime.now().year

    # Alter bei Pensionierung
    alter_pension = jahr_pension - geburtsjahr

    # Regelaltersgrenze
    if ist_polizei_feuerwehr:
        regelaltersgrenze = REGELALTERSGRENZE_POLIZEI
    else:
        regelaltersgrenze = REGELALTERSGRENZE_NORMAL

    # Dienstjahre berechnen
    dienstjahre = berechne_dienstjahre(
        jahr_verbeamtung,
        jahr_pension,
        teilzeitjahre,
        teilzeitanteil
    )

    # Erfahrungsstufe bei Pensionierung berechnen
    jahre_bis_pension = max(0, jahr_pension - aktuelles_jahr)
    stufe_bei_pension = berechne_stufe_nach_dienstjahren(
        besoldungsgruppe,
        stufe,
        jahre_bis_pension
    )
    max_stufe = get_max_stufe(besoldungsgruppe)

    # Ruhegehaltssatz
    ruhegehaltssatz = berechne_ruhegehaltssatz(dienstjahre)

    # Versorgungsabschlag
    versorgungsabschlag = berechne_versorgungsabschlag(
        geburtsjahr,
        jahr_pension,
        ist_polizei_feuerwehr
    )

    # Effektiver Ruhegehaltssatz nach Abschlag
    effektiver_satz = ruhegehaltssatz * (1 - versorgungsabschlag / 100)

    # Ruhegehaltsfähige Bezüge mit projizierter Stufe
    ruhegehaltsfaehige_bezuege = berechne_ruhegehaltsfaehige_bezuege(
        besoldungsgruppe,
        stufe_bei_pension,
        verheiratet,
        mietenstufe,
        arbeitszeit_faktor
    )

    # Ruhegehalt brutto
    ruhegehalt_brutto = ruhegehaltsfaehige_bezuege * (effektiver_satz / 100)

    return {
        "alter_pension": alter_pension,
        "regelaltersgrenze": regelaltersgrenze,
        "dienstjahre": round(dienstjahre, 2),
        "ruhegehaltssatz": ruhegehaltssatz,
        "versorgungsabschlag_prozent": round(versorgungsabschlag, 2),
        "effektiver_ruhegehaltssatz": round(effektiver_satz, 2),
        "ruhegehaltsfaehige_bezuege": ruhegehaltsfaehige_bezuege,
        "ruhegehalt_brutto": round(ruhegehalt_brutto, 2),
        "ist_vorzeitig": alter_pension < regelaltersgrenze,
        "jahre_vor_grenze": max(0, regelaltersgrenze - alter_pension),
        "stufe_bei_pension": stufe_bei_pension,
        "max_stufe": max_stufe,
    }


def berechne_pension_nach_alter(
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
    von_alter: int = 60,
    bis_alter: int = 67
) -> list:
    """
    Berechnet die Pension für verschiedene Pensionsalter.

    Returns:
        Liste von Dictionaries mit Pension pro Alter
    """
    ergebnisse = []

    for alter in range(von_alter, bis_alter + 1):
        jahr_pension = geburtsjahr + alter
        ergebnis = berechne_ruhegehalt(
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
        ergebnis["pensionsalter"] = alter
        ergebnisse.append(ergebnis)

    return ergebnisse
