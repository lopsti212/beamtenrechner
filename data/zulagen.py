"""
Struktur- und Amtszulagen NRW (Stand 2024)
"""

# Strukturzulagen nach Laufbahngruppe
STRUKTURZULAGE = {
    1: 90.89,   # Laufbahngruppe 1: A5-A8
    2: 114.06,  # Laufbahngruppe 2: A9-A16
}

# Zuordnung Besoldungsgruppe -> Laufbahngruppe
LAUFBAHNGRUPPE = {
    "A5": 1,
    "A6": 1,
    "A7": 1,
    "A8": 1,
    "A9": 2,
    "A10": 2,
    "A11": 2,
    "A12": 2,
    "A13": 2,
    "A14": 2,
    "A15": 2,
    "A16": 2,
}


def get_strukturzulage(besoldungsgruppe: str) -> float:
    """
    Gibt die Strukturzulage für eine Besoldungsgruppe zurück.

    Args:
        besoldungsgruppe: z.B. "A13"

    Returns:
        Strukturzulage in Euro
    """
    if besoldungsgruppe not in LAUFBAHNGRUPPE:
        raise ValueError(f"Besoldungsgruppe {besoldungsgruppe} nicht gefunden")

    laufbahngruppe = LAUFBAHNGRUPPE[besoldungsgruppe]
    return STRUKTURZULAGE[laufbahngruppe]


def get_laufbahngruppe(besoldungsgruppe: str) -> int:
    """
    Gibt die Laufbahngruppe für eine Besoldungsgruppe zurück.

    Args:
        besoldungsgruppe: z.B. "A13"

    Returns:
        Laufbahngruppe (1 oder 2)
    """
    return LAUFBAHNGRUPPE.get(besoldungsgruppe, 2)
