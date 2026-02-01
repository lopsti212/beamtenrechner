"""
Lohnsteuertabelle 2024 - vereinfachte Berechnung
Für Beamte (keine Sozialversicherung)
"""

# Grundfreibetrag 2024
GRUNDFREIBETRAG = 11604

# Steuersätze nach Zonen (vereinfacht für 2024)
# Zone 1: 0 bis Grundfreibetrag: 0%
# Zone 2: Grundfreibetrag bis 17005€: 14% bis 24%
# Zone 3: 17006€ bis 66760€: 24% bis 42%
# Zone 4: 66761€ bis 277825€: 42%
# Zone 5: ab 277826€: 45%


def berechne_einkommensteuer(zu_versteuerndes_einkommen: float) -> float:
    """
    Berechnet die Einkommensteuer nach dem Einkommensteuertarif 2024.

    Args:
        zu_versteuerndes_einkommen: Jahreseinkommen in Euro

    Returns:
        Einkommensteuer in Euro (Jahresbetrag)
    """
    zve = zu_versteuerndes_einkommen

    if zve <= GRUNDFREIBETRAG:
        return 0.0

    # Progressionszonen nach § 32a EStG 2024
    if zve <= 17005:
        # Zone 2: Progressionszone 1
        y = (zve - GRUNDFREIBETRAG) / 10000
        steuer = (979.18 * y + 1400) * y
    elif zve <= 66760:
        # Zone 3: Progressionszone 2
        z = (zve - 17005) / 10000
        steuer = (192.59 * z + 2397) * z + 966.53
    elif zve <= 277825:
        # Zone 4: Proportionalzone 1
        steuer = 0.42 * zve - 10636.31
    else:
        # Zone 5: Proportionalzone 2 (Reichensteuer)
        steuer = 0.45 * zve - 18971.06

    return max(0, round(steuer, 2))


def get_steuerklassen_faktor(steuerklasse: int) -> float:
    """
    Gibt den Faktor für die Steuerberechnung nach Steuerklasse zurück.

    Args:
        steuerklasse: Steuerklasse 1-6

    Returns:
        Faktor für Steuerberechnung
    """
    # Vereinfachte Faktoren für die Steuerberechnung
    # Bei Steuerklasse 3/5 wird das Einkommen des Partners berücksichtigt
    faktoren = {
        1: 1.0,    # Ledig
        2: 1.0,    # Alleinerziehend (leicht günstiger, hier vereinfacht)
        3: 0.75,   # Verheiratet, Alleinverdiener
        4: 1.0,    # Verheiratet, beide verdienen ähnlich
        5: 1.35,   # Verheiratet, Partner verdient mehr
        6: 1.15,   # Zweitjob
    }
    return faktoren.get(steuerklasse, 1.0)


def berechne_lohnsteuer_monatlich(
    brutto_monatlich: float,
    steuerklasse: int,
    kirchensteuer: bool = False,
    bundesland: str = "NRW"
) -> dict:
    """
    Berechnet die monatliche Lohnsteuer für einen Beamten.

    Args:
        brutto_monatlich: Monatliches Bruttogehalt
        steuerklasse: Steuerklasse 1-6
        kirchensteuer: True wenn Kirchensteuer zu zahlen ist
        bundesland: Bundesland für Kirchensteuersatz

    Returns:
        Dictionary mit Steuerbeträgen
    """
    # Jahresbrutto berechnen (12 Monate, kein 13. Gehalt bei Beamten)
    # Aber: Sonderzahlung im November (ca. 30% eines Monatsgehalts)
    # Vereinfacht: 12.3 Monate
    jahresbrutto = brutto_monatlich * 12.3

    # Werbungskostenpauschale (1230€ für 2024)
    werbungskosten = 1230

    # Sonderausgabenpauschale
    sonderausgaben = 36

    # Zu versteuerndes Einkommen
    # Bei Beamten: keine Sozialversicherung, aber Vorsorgeaufwendungen
    # Vereinfacht: Krankenversicherung ca. 4% des Bruttos
    krankenversicherung_jahres = jahresbrutto * 0.04

    # Zu versteuerndes Einkommen
    zve = jahresbrutto - werbungskosten - sonderausgaben - krankenversicherung_jahres

    # Steuerklassen-Anpassung
    faktor = get_steuerklassen_faktor(steuerklasse)
    steuer_basis = berechne_einkommensteuer(zve)
    einkommensteuer_jahr = steuer_basis * faktor

    # Solidaritätszuschlag (nur wenn Steuer > 18130€ für Steuerklasse 1)
    # Seit 2021 stark eingeschränkt, für die meisten Beamten nicht relevant
    if steuerklasse in [3, 4]:
        soli_grenze = 36260
    else:
        soli_grenze = 18130

    if einkommensteuer_jahr > soli_grenze:
        # Gleitzone bis 1,5-fache der Grenze
        if einkommensteuer_jahr < soli_grenze * 1.5:
            soli_prozent = ((einkommensteuer_jahr / soli_grenze) - 1) * 11.9
        else:
            soli_prozent = 5.5
        soli_jahr = einkommensteuer_jahr * (soli_prozent / 100)
    else:
        soli_jahr = 0

    # Kirchensteuer (9% in NRW)
    if kirchensteuer:
        kirche_jahr = einkommensteuer_jahr * 0.09
    else:
        kirche_jahr = 0

    # Auf Monat umrechnen
    lohnsteuer_monat = einkommensteuer_jahr / 12
    soli_monat = soli_jahr / 12
    kirche_monat = kirche_jahr / 12

    return {
        "lohnsteuer": round(lohnsteuer_monat, 2),
        "solidaritaetszuschlag": round(soli_monat, 2),
        "kirchensteuer": round(kirche_monat, 2),
        "gesamt": round(lohnsteuer_monat + soli_monat + kirche_monat, 2),
        "jahresbrutto": round(jahresbrutto, 2),
        "zve": round(zve, 2),
    }
