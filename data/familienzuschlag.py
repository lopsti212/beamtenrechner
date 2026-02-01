"""
Familienzuschläge NRW (Stand 1. Februar 2025)
Quelle: Landtag NRW Drucksache 18/9514, Anlage 13

Stufe 1 = verheiratet, keine Kinder
Stufe 2 = verheiratet + 1 Kind (oder ledig mit 1 Kind)
Stufe 3 = verheiratet + 2 Kinder
Stufe 4 = verheiratet + 3 Kinder
Stufe 5 = verheiratet + 4 Kinder
Ab 5. Kind: Erhöhungsbetrag pro Kind
"""

# Standard-Mietenstufe für Datteln/Olfen
STANDARD_MIETENSTUFE = 2

# Stufe 1 (§ 43 Absatz 1) - Verheiratet, keine Kinder
# Kein Mietenstufen-Unterschied
FAMILIENZUSCHLAG_STUFE1 = {
    "A5_A6": 164.64,
    "A7_A8": 162.70,
    "uebrige": 168.76,  # A9-A16
}

# Stufe 2 (§ 43 Absatz 2) - 1 Kind
# Format: {Mietenstufe: Betrag}
FAMILIENZUSCHLAG_STUFE2 = {
    "A5_A6": {1: 315.07, 2: 315.07, 3: 363.01, 4: 504.03, 5: 633.21, 6: 772.13, 7: 928.44},
    "A7_A8": {1: 311.35, 2: 311.35, 3: 359.30, 4: 500.31, 5: 629.50, 6: 768.42, 7: 924.73},
    "uebrige": {1: 315.68, 2: 315.68, 3: 363.63, 4: 504.63, 5: 633.82, 6: 772.75, 7: 929.04},
}

# Stufe 3 (§ 43 Absatz 2) - 2 Kinder
FAMILIENZUSCHLAG_STUFE3 = {
    "A5_A6": {1: 717.01, 2: 856.32, 3: 999.88, 4: 1166.69, 5: 1324.84, 6: 1487.43, 7: 1677.53},
    "A7_A8": {1: 711.52, 2: 850.84, 3: 994.40, 4: 1161.21, 5: 1319.35, 6: 1481.96, 7: 1672.05},
    "uebrige": {1: 714.09, 2: 853.40, 3: 996.96, 4: 1163.77, 5: 1321.92, 6: 1484.52, 7: 1674.61},
}

# Stufe 4 (§ 43 Absatz 2) - 3 Kinder
FAMILIENZUSCHLAG_STUFE4 = {
    "A5_A6": {1: 1410.99, 2: 1571.84, 3: 1740.64, 4: 1937.16, 5: 2117.59, 6: 2308.49, 7: 2529.94},
    "A7_A8": {1: 1400.01, 2: 1560.85, 3: 1729.65, 4: 1926.18, 5: 2106.60, 6: 2297.51, 7: 2518.96},
    "uebrige": {1: 1397.12, 2: 1557.97, 3: 1726.77, 4: 1923.29, 5: 2103.71, 6: 2294.63, 7: 2516.07},
}

# Stufe 5 (§ 43 Absatz 2) - 4 Kinder
FAMILIENZUSCHLAG_STUFE5 = {
    "A5_A6": {1: 2110.07, 2: 2294.95, 3: 2490.12, 4: 2713.91, 5: 2917.52, 6: 3149.72, 7: 3403.65},
    "A7_A8": {1: 2093.58, 2: 2278.46, 3: 2473.62, 4: 2697.42, 5: 2901.03, 6: 3133.23, 7: 3387.16},
    "uebrige": {1: 2085.25, 2: 2270.13, 3: 2465.29, 4: 2689.10, 5: 2892.69, 6: 3124.90, 7: 3378.83},
}

# Erhöhungsbetrag für 5. und jedes weitere Kind
FAMILIENZUSCHLAG_ERHOEHUNG = {
    "A5_A6": {1: 740.17, 2: 767.33, 3: 797.36, 4: 828.69, 5: 855.57, 6: 903.68, 7: 942.04},
    "A7_A8": {1: 734.66, 2: 761.83, 3: 791.85, 4: 823.18, 5: 850.07, 6: 898.17, 7: 936.54},
    "uebrige": {1: 729.22, 2: 756.38, 3: 786.41, 4: 817.74, 5: 844.62, 6: 892.73, 7: 931.09},
}


def get_besoldungsgruppe_kategorie(besoldungsgruppe: str) -> str:
    """
    Ermittelt die Kategorie für den Familienzuschlag.

    Args:
        besoldungsgruppe: z.B. "A13"

    Returns:
        "A5_A6", "A7_A8" oder "uebrige"
    """
    if besoldungsgruppe in ["A5", "A6"]:
        return "A5_A6"
    elif besoldungsgruppe in ["A7", "A8"]:
        return "A7_A8"
    else:
        return "uebrige"


def get_familienzuschlag_stufe1(besoldungsgruppe: str) -> float:
    """
    Gibt den Familienzuschlag Stufe 1 (verheiratet, keine Kinder) zurück.
    """
    kategorie = get_besoldungsgruppe_kategorie(besoldungsgruppe)
    return FAMILIENZUSCHLAG_STUFE1[kategorie]


def get_familienzuschlag_gesamt(
    verheiratet: bool,
    anzahl_kinder: int,
    mietenstufe: int = STANDARD_MIETENSTUFE,
    besoldungsgruppe: str = "A13"
) -> float:
    """
    Berechnet den gesamten Familienzuschlag.

    Args:
        verheiratet: True wenn verheiratet
        anzahl_kinder: Anzahl der Kinder
        mietenstufe: Mietenstufe 1-7 (Standard: 2 für Datteln/Olfen)
        besoldungsgruppe: Besoldungsgruppe (für Kategorie-Zuordnung)

    Returns:
        Gesamter Familienzuschlag in Euro
    """
    mietenstufe = max(1, min(7, mietenstufe))
    kategorie = get_besoldungsgruppe_kategorie(besoldungsgruppe)

    # Nicht verheiratet und keine Kinder = kein Zuschlag
    if not verheiratet and anzahl_kinder == 0:
        return 0.0

    # Verheiratet ohne Kinder = Stufe 1
    if verheiratet and anzahl_kinder == 0:
        return FAMILIENZUSCHLAG_STUFE1[kategorie]

    # Mit Kindern: Stufe 2-5 + ggf. Erhöhung
    if anzahl_kinder == 1:
        basis = FAMILIENZUSCHLAG_STUFE2[kategorie][mietenstufe]
    elif anzahl_kinder == 2:
        basis = FAMILIENZUSCHLAG_STUFE3[kategorie][mietenstufe]
    elif anzahl_kinder == 3:
        basis = FAMILIENZUSCHLAG_STUFE4[kategorie][mietenstufe]
    elif anzahl_kinder >= 4:
        basis = FAMILIENZUSCHLAG_STUFE5[kategorie][mietenstufe]
        # Ab dem 5. Kind: Erhöhungsbetrag pro Kind
        if anzahl_kinder > 4:
            erhoehung = FAMILIENZUSCHLAG_ERHOEHUNG[kategorie][mietenstufe]
            basis += erhoehung * (anzahl_kinder - 4)
    else:
        basis = 0.0

    # Nicht verheiratet mit Kindern: Nur Kinderzuschlag (ohne Ehegattenzuschlag)
    if not verheiratet:
        basis -= FAMILIENZUSCHLAG_STUFE1[kategorie]

    return round(basis, 2)


def get_kinderzuschlag(
    anzahl_kinder: int,
    mietenstufe: int = STANDARD_MIETENSTUFE,
    besoldungsgruppe: str = "A13"
) -> float:
    """
    Berechnet nur den Kinderzuschlag (ohne Ehegattenzuschlag).
    Für die Ruhegehaltsfähigen Bezüge wird nur der Kinderzuschlag berücksichtigt.

    Args:
        anzahl_kinder: Anzahl der Kinder
        mietenstufe: Mietenstufe 1-7
        besoldungsgruppe: Besoldungsgruppe

    Returns:
        Kinderzuschlag in Euro
    """
    if anzahl_kinder == 0:
        return 0.0

    # Familienzuschlag mit Kindern minus Stufe 1 = reiner Kinderzuschlag
    kategorie = get_besoldungsgruppe_kategorie(besoldungsgruppe)
    mietenstufe = max(1, min(7, mietenstufe))

    if anzahl_kinder == 1:
        gesamt = FAMILIENZUSCHLAG_STUFE2[kategorie][mietenstufe]
    elif anzahl_kinder == 2:
        gesamt = FAMILIENZUSCHLAG_STUFE3[kategorie][mietenstufe]
    elif anzahl_kinder == 3:
        gesamt = FAMILIENZUSCHLAG_STUFE4[kategorie][mietenstufe]
    elif anzahl_kinder >= 4:
        gesamt = FAMILIENZUSCHLAG_STUFE5[kategorie][mietenstufe]
        if anzahl_kinder > 4:
            erhoehung = FAMILIENZUSCHLAG_ERHOEHUNG[kategorie][mietenstufe]
            gesamt += erhoehung * (anzahl_kinder - 4)
    else:
        gesamt = 0.0

    kinderzuschlag = gesamt - FAMILIENZUSCHLAG_STUFE1[kategorie]
    return round(kinderzuschlag, 2)
