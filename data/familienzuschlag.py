"""
Familienzuschläge NRW (Stand 2024)
Nach Stufen und Mietenstufen
"""

# Familienzuschlag Stufe 1 (verheiratet, ohne Kinder) nach Mietenstufe
# Mietenstufen I-VII
FAMILIENZUSCHLAG_STUFE1 = {
    1: 155.48,  # Mietenstufe I
    2: 163.80,  # Mietenstufe II (Datteln/Olfen - Standard)
    3: 172.12,  # Mietenstufe III
    4: 180.44,  # Mietenstufe IV
    5: 188.76,  # Mietenstufe V
    6: 197.08,  # Mietenstufe VI
    7: 205.40,  # Mietenstufe VII
}

# Kinderzuschlag pro Kind (unabhängig von Mietenstufe)
# Ab dem 3. Kind erhöht sich der Zuschlag
KINDERZUSCHLAG = {
    1: 132.55,  # 1. Kind
    2: 132.55,  # 2. Kind
    3: 412.15,  # 3. Kind
    4: 412.15,  # 4. Kind
    5: 412.15,  # 5. und weitere Kinder
}

# Standard-Mietenstufe für Datteln/Olfen
STANDARD_MIETENSTUFE = 2


def get_familienzuschlag_stufe1(mietenstufe: int = STANDARD_MIETENSTUFE) -> float:
    """
    Gibt den Familienzuschlag Stufe 1 (verheiratet) zurück.

    Args:
        mietenstufe: Mietenstufe 1-7 (Standard: 2 für Datteln/Olfen)

    Returns:
        Familienzuschlag in Euro
    """
    mietenstufe = max(1, min(7, mietenstufe))
    return FAMILIENZUSCHLAG_STUFE1[mietenstufe]


def get_kinderzuschlag(anzahl_kinder: int) -> float:
    """
    Berechnet den gesamten Kinderzuschlag.

    Args:
        anzahl_kinder: Anzahl der Kinder

    Returns:
        Gesamter Kinderzuschlag in Euro
    """
    if anzahl_kinder <= 0:
        return 0.0

    total = 0.0
    for i in range(1, anzahl_kinder + 1):
        if i <= 5:
            total += KINDERZUSCHLAG[i]
        else:
            # Ab dem 6. Kind: wie 5. Kind
            total += KINDERZUSCHLAG[5]
    return total


def get_familienzuschlag_gesamt(
    verheiratet: bool,
    anzahl_kinder: int,
    mietenstufe: int = STANDARD_MIETENSTUFE
) -> float:
    """
    Berechnet den gesamten Familienzuschlag.

    Args:
        verheiratet: True wenn verheiratet
        anzahl_kinder: Anzahl der Kinder
        mietenstufe: Mietenstufe 1-7

    Returns:
        Gesamter Familienzuschlag in Euro
    """
    total = 0.0

    if verheiratet:
        total += get_familienzuschlag_stufe1(mietenstufe)

    total += get_kinderzuschlag(anzahl_kinder)

    return total
