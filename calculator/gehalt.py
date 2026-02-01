"""
Bruttogehalt-Berechnung für Beamte NRW
"""

from data.besoldung import get_grundgehalt
from data.familienzuschlag import (
    get_familienzuschlag_stufe1,
    get_kinderzuschlag,
    get_familienzuschlag_gesamt,
    STANDARD_MIETENSTUFE
)
from data.zulagen import get_strukturzulage


def berechne_bruttogehalt(
    besoldungsgruppe: str,
    stufe: int,
    verheiratet: bool = False,
    anzahl_kinder: int = 0,
    mietenstufe: int = STANDARD_MIETENSTUFE,
    arbeitszeit_faktor: float = 1.0
) -> dict:
    """
    Berechnet das monatliche Bruttogehalt eines Beamten.

    Args:
        besoldungsgruppe: z.B. "A13"
        stufe: Erfahrungsstufe 1-8
        verheiratet: True wenn verheiratet
        anzahl_kinder: Anzahl der Kinder
        mietenstufe: Mietenstufe 1-7 (Standard: 2 für Datteln/Olfen)
        arbeitszeit_faktor: Anteil der Vollzeit (0.5 = 50%)

    Returns:
        Dictionary mit allen Gehaltsbestandteilen
    """
    # Grundgehalt
    grundgehalt = get_grundgehalt(besoldungsgruppe, stufe)

    # Strukturzulage
    strukturzulage = get_strukturzulage(besoldungsgruppe)

    # Familienzuschlag (neue Struktur mit Besoldungsgruppe)
    familienzuschlag_gesamt = get_familienzuschlag_gesamt(
        verheiratet, anzahl_kinder, mietenstufe, besoldungsgruppe
    )
    familienzuschlag_stufe1 = get_familienzuschlag_stufe1(besoldungsgruppe) if verheiratet else 0.0
    kinderzuschlag = get_kinderzuschlag(anzahl_kinder, mietenstufe, besoldungsgruppe)

    # Summe vor Arbeitszeit-Faktor
    brutto_vollzeit = grundgehalt + strukturzulage + familienzuschlag_gesamt

    # Mit Arbeitszeit-Faktor
    brutto_teilzeit = brutto_vollzeit * arbeitszeit_faktor

    return {
        "grundgehalt": round(grundgehalt, 2),
        "strukturzulage": round(strukturzulage, 2),
        "familienzuschlag_stufe1": round(familienzuschlag_stufe1, 2),
        "kinderzuschlag": round(kinderzuschlag, 2),
        "familienzuschlag_gesamt": round(familienzuschlag_gesamt, 2),
        "brutto_vollzeit": round(brutto_vollzeit, 2),
        "arbeitszeit_faktor": arbeitszeit_faktor,
        "brutto_teilzeit": round(brutto_teilzeit, 2),
        "brutto": round(brutto_teilzeit, 2),  # Alias für einfacheren Zugriff
    }


def berechne_ruhegehaltsfaehige_bezuege(
    besoldungsgruppe: str,
    stufe: int,
    verheiratet: bool = False,
    mietenstufe: int = STANDARD_MIETENSTUFE,
    arbeitszeit_faktor: float = 1.0
) -> float:
    """
    Berechnet die ruhegehaltsfähigen Bezüge.
    Diese bestehen aus Grundgehalt + Strukturzulage + Familienzuschlag Stufe 1
    (ohne Kinderzuschlag, da dieser separat weitergezahlt wird).

    Args:
        besoldungsgruppe: z.B. "A13"
        stufe: Erfahrungsstufe
        verheiratet: True wenn verheiratet
        mietenstufe: Mietenstufe 1-7
        arbeitszeit_faktor: Anteil der Vollzeit

    Returns:
        Ruhegehaltsfähige Bezüge in Euro
    """
    grundgehalt = get_grundgehalt(besoldungsgruppe, stufe)
    strukturzulage = get_strukturzulage(besoldungsgruppe)
    familienzuschlag = get_familienzuschlag_stufe1(besoldungsgruppe) if verheiratet else 0.0

    # Ruhegehaltsfähige Bezüge (Vollzeit)
    bezuege = grundgehalt + strukturzulage + familienzuschlag

    # Mit Arbeitszeit-Faktor
    return round(bezuege * arbeitszeit_faktor, 2)
