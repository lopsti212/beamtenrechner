"""
Besoldungstabellen NRW (Stand Februar 2025)
Landesbesoldungsordnung A - Grundgehaltssätze
Quelle: finanzverwaltung.nrw.de - Anlage 6, gültig ab 1. Februar 2025

Einstiegsstufen:
- A5-A11: ab Stufe 3
- A12: ab Stufe 4
- A13-A14: ab Stufe 5
- A15-A16: ab Stufe 6
"""

# Besoldungstabelle A5-A16 NRW (gültig ab 01.02.2025)
# Werte in Euro, monatlich
BESOLDUNG_A = {
    "A5": {
        3: 2976.36,
        4: 3042.97,
        5: 3109.57,
        6: 3176.18,
        7: 3242.79,
        8: 3309.40,
        9: 3376.03,
        10: 3442.65,
    },
    "A6": {
        3: 3026.58,
        4: 3099.71,
        5: 3172.85,
        6: 3246.00,
        7: 3319.15,
        8: 3392.27,
        9: 3465.40,
        10: 3538.51,
    },
    "A7": {
        3: 3111.11,
        4: 3202.07,
        5: 3293.01,
        6: 3383.90,
        7: 3474.86,
        8: 3539.78,
        9: 3604.75,
        10: 3669.72,
    },
    "A8": {
        3: 3190.15,
        4: 3306.68,
        5: 3423.20,
        6: 3539.74,
        7: 3656.29,
        8: 3733.96,
        9: 3811.65,
        10: 3889.36,
        11: 3967.02,
    },
    "A9": {
        3: 3326.45,
        4: 3449.33,
        5: 3572.19,
        6: 3695.07,
        7: 3817.95,
        8: 3902.37,
        9: 3986.91,
        10: 4071.36,
        11: 4155.81,
    },
    "A10": {
        3: 3573.44,
        4: 3730.84,
        5: 3888.29,
        6: 4045.70,
        7: 4203.15,
        8: 4308.10,
        9: 4413.56,
        10: 4520.90,
        11: 4628.26,
    },
    "A11": {
        3: 3916.14,
        4: 4072.76,
        5: 4229.42,
        6: 4386.08,
        7: 4546.22,
        8: 4653.01,
        9: 4759.85,
        10: 4868.15,
        11: 4977.10,
        12: 5086.10,
    },
    "A12": {
        4: 4358.34,
        5: 4548.64,
        6: 4739.70,
        7: 4933.46,
        8: 5063.39,
        9: 5193.30,
        10: 5323.26,
        11: 5453.20,
        12: 5583.06,
    },
    "A13": {
        5: 5051.74,
        6: 5262.14,
        7: 5472.56,
        8: 5612.86,
        9: 5753.14,
        10: 5893.45,
        11: 6033.77,
        12: 6174.04,
    },
    "A14": {
        5: 5350.96,
        6: 5623.86,
        7: 5896.70,
        8: 6078.64,
        9: 6260.54,
        10: 6442.48,
        11: 6624.41,
        12: 6806.34,
    },
    "A15": {
        6: 6149.10,
        7: 6449.11,
        8: 6689.11,
        9: 6929.13,
        10: 7169.18,
        11: 7409.21,
        12: 7649.22,
    },
    "A16": {
        6: 6754.48,
        7: 7101.42,
        8: 7379.04,
        9: 7656.65,
        10: 7934.20,
        11: 8211.82,
        12: 8489.42,
    },
}

# Maximale und minimale Erfahrungsstufen pro Besoldungsgruppe
MAX_STUFEN = {
    "A5": 10,
    "A6": 10,
    "A7": 10,
    "A8": 11,
    "A9": 11,
    "A10": 11,
    "A11": 12,
    "A12": 12,
    "A13": 12,
    "A14": 12,
    "A15": 12,
    "A16": 12,
}

MIN_STUFEN = {
    "A5": 3,
    "A6": 3,
    "A7": 3,
    "A8": 3,
    "A9": 3,
    "A10": 3,
    "A11": 3,
    "A12": 4,
    "A13": 5,
    "A14": 5,
    "A15": 6,
    "A16": 6,
}

# Mindestversorgung: A4 Stufe 8 (für DU-Berechnung)
MINDESTVERSORGUNG_GRUNDGEHALT = 3157.75  # A4 Stufe 8


def get_grundgehalt(besoldungsgruppe: str, stufe: int) -> float:
    """
    Gibt das Grundgehalt für eine Besoldungsgruppe und Stufe zurück.
    """
    if besoldungsgruppe not in BESOLDUNG_A:
        raise ValueError(f"Besoldungsgruppe {besoldungsgruppe} nicht gefunden")

    max_stufe = MAX_STUFEN[besoldungsgruppe]
    min_stufe = MIN_STUFEN[besoldungsgruppe]

    # Stufe auf gültigen Bereich begrenzen
    stufe = max(min_stufe, min(stufe, max_stufe))

    return BESOLDUNG_A[besoldungsgruppe][stufe]


def get_besoldungsgruppen() -> list:
    """Gibt alle verfügbaren Besoldungsgruppen zurück."""
    return list(BESOLDUNG_A.keys())


def get_max_stufe(besoldungsgruppe: str) -> int:
    """Gibt die maximale Stufe für eine Besoldungsgruppe zurück."""
    return MAX_STUFEN.get(besoldungsgruppe, 12)


def get_min_stufe(besoldungsgruppe: str) -> int:
    """Gibt die minimale Stufe für eine Besoldungsgruppe zurück."""
    return MIN_STUFEN.get(besoldungsgruppe, 3)
