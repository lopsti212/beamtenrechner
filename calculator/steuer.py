"""
Netto-Berechnung für Beamte NRW
Beamte zahlen keine Sozialversicherungsbeiträge!
"""

from data.lohnsteuer import berechne_lohnsteuer_monatlich


def berechne_netto(
    brutto_monatlich: float,
    steuerklasse: int,
    kirchensteuer: bool = False
) -> dict:
    """
    Berechnet das Nettogehalt eines Beamten.
    Beamte zahlen keine Sozialversicherung (Renten-, Kranken-, Pflege-, Arbeitslosenversicherung).

    Args:
        brutto_monatlich: Monatliches Bruttogehalt
        steuerklasse: Steuerklasse 1-6
        kirchensteuer: True wenn Kirchensteuer zu zahlen ist

    Returns:
        Dictionary mit Brutto, Abzügen und Netto
    """
    # Steuern berechnen
    steuern = berechne_lohnsteuer_monatlich(
        brutto_monatlich=brutto_monatlich,
        steuerklasse=steuerklasse,
        kirchensteuer=kirchensteuer
    )

    # Private Krankenversicherung (PKV) - geschätzt ca. 4% des Bruttos
    # Beihilfe deckt 50-80%, Rest privat versichert
    # Vereinfacht: 4% des Bruttos als PKV-Beitrag
    pkv_beitrag = brutto_monatlich * 0.04

    # Gesamtabzüge
    abzuege_gesamt = steuern["gesamt"] + pkv_beitrag

    # Netto
    netto = brutto_monatlich - abzuege_gesamt

    return {
        "brutto": round(brutto_monatlich, 2),
        "lohnsteuer": steuern["lohnsteuer"],
        "solidaritaetszuschlag": steuern["solidaritaetszuschlag"],
        "kirchensteuer": steuern["kirchensteuer"],
        "steuern_gesamt": steuern["gesamt"],
        "pkv_beitrag": round(pkv_beitrag, 2),
        "abzuege_gesamt": round(abzuege_gesamt, 2),
        "netto": round(netto, 2),
    }


def berechne_netto_einfach(
    brutto_monatlich: float,
    steuerklasse: int,
    kirchensteuer: bool = False
) -> float:
    """
    Vereinfachte Netto-Berechnung, gibt nur den Nettobetrag zurück.

    Args:
        brutto_monatlich: Monatliches Bruttogehalt
        steuerklasse: Steuerklasse 1-6
        kirchensteuer: True wenn Kirchensteuer zu zahlen ist

    Returns:
        Monatliches Nettogehalt in Euro
    """
    ergebnis = berechne_netto(brutto_monatlich, steuerklasse, kirchensteuer)
    return ergebnis["netto"]
