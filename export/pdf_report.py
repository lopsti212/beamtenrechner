"""
PDF-Report Generator für Beamtenpensions-Rechner NRW
Erstellt professionelle PDF-Reports mit Grafiken
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
import datetime


def erstelle_pdf_report(daten: dict) -> bytes:
    """
    Erstellt einen PDF-Report mit allen Berechnungsergebnissen.

    Args:
        daten: Dictionary mit allen Berechnungsdaten

    Returns:
        PDF als Bytes
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    # Styles
    styles = getSampleStyleSheet()

    # Custom Styles
    styles.add(ParagraphStyle(
        name='TitleCustom',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor("#2c3e50")
    ))

    styles.add(ParagraphStyle(
        name='Heading1Custom',
        parent=styles['Heading1'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.HexColor("#34495e")
    ))

    styles.add(ParagraphStyle(
        name='Heading2Custom',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=8,
        textColor=colors.HexColor("#34495e")
    ))

    styles.add(ParagraphStyle(
        name='WarningBox',
        parent=styles['Normal'],
        fontSize=14,
        spaceBefore=10,
        spaceAfter=10,
        textColor=colors.white,
        backColor=colors.HexColor("#e74c3c"),
        borderPadding=10,
        alignment=TA_CENTER
    ))

    styles.add(ParagraphStyle(
        name='Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.gray,
        alignment=TA_CENTER
    ))

    # Elemente sammeln
    elements = []

    # Titel
    elements.append(Paragraph("Beamtenpensions-Rechner NRW", styles['TitleCustom']))
    elements.append(Paragraph(
        f"Berechnungsbericht vom {datetime.datetime.now().strftime('%d.%m.%Y')}",
        styles['Normal']
    ))
    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#3498db")))
    elements.append(Spacer(1, 20))

    # 1. Eingabedaten
    elements.append(Paragraph("1. Eingabedaten", styles['Heading1Custom']))

    eingabe_daten = [
        ["Parameter", "Wert"],
        ["Geburtsjahr", str(daten['geburtsjahr'])],
        ["Jahr der Verbeamtung", str(daten['jahr_verbeamtung'])],
        ["Besoldungsgruppe", daten['besoldungsgruppe']],
        ["Erfahrungsstufe", str(daten['stufe'])],
        ["Verheiratet", "Ja" if daten['verheiratet'] else "Nein"],
        ["Anzahl Kinder", str(daten['anzahl_kinder'])],
        ["Steuerklasse", str(daten['steuerklasse'])],
        ["Polizei/Feuerwehr", "Ja" if daten['ist_polizei_feuerwehr'] else "Nein"],
        ["Arbeitszeit-Faktor", f"{daten['arbeitszeit_faktor'] * 100:.0f}%"],
        ["Teilzeitjahre", f"{daten['teilzeitjahre']:.1f} Jahre"],
        ["Gewünschtes Pensionsalter", str(daten['gewuenschtes_pensionsalter'])],
        ["DU-Szenario Jahr", str(daten['du_szenario_jahr'])],
    ]

    table_eingabe = Table(eingabe_daten, colWidths=[8 * cm, 6 * cm])
    table_eingabe.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#3498db")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#ecf0f1")),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ecf0f1"), colors.white]),
    ]))
    elements.append(table_eingabe)
    elements.append(Spacer(1, 20))

    # 2. Aktuelles Gehalt
    elements.append(Paragraph("2. Aktuelles Gehalt", styles['Heading1Custom']))

    gehalt = daten['gehalt']
    netto = daten['netto_daten']

    gehalt_daten = [
        ["Bestandteil", "Betrag"],
        ["Grundgehalt", format_euro(gehalt['grundgehalt'])],
        ["Strukturzulage", format_euro(gehalt['strukturzulage'])],
        ["Familienzuschlag Stufe 1", format_euro(gehalt['familienzuschlag_stufe1'])],
        ["Kinderzuschlag", format_euro(gehalt['kinderzuschlag'])],
        ["Brutto (Vollzeit)", format_euro(gehalt['brutto_vollzeit'])],
        ["Brutto (aktuell)", format_euro(gehalt['brutto'])],
    ]

    table_gehalt = Table(gehalt_daten, colWidths=[8 * cm, 6 * cm])
    table_gehalt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#27ae60")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ecf0f1"), colors.white]),
    ]))
    elements.append(table_gehalt)
    elements.append(Spacer(1, 10))

    # Netto
    netto_daten = [
        ["Abzug", "Betrag"],
        ["Lohnsteuer", format_euro(netto['lohnsteuer'])],
        ["Solidaritätszuschlag", format_euro(netto['solidaritaetszuschlag'])],
        ["Kirchensteuer", format_euro(netto['kirchensteuer'])],
        ["PKV-Beitrag (geschätzt)", format_euro(netto['pkv_beitrag'])],
        ["Abzüge gesamt", format_euro(netto['abzuege_gesamt'])],
        ["Netto", format_euro(netto['netto'])],
    ]

    table_netto = Table(netto_daten, colWidths=[8 * cm, 6 * cm])
    table_netto.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#9b59b6")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ecf0f1"), colors.white]),
    ]))
    elements.append(table_netto)
    elements.append(Spacer(1, 20))

    # 3. Altersrente
    elements.append(Paragraph("3. Altersrente", styles['Heading1Custom']))

    pension = daten['pension']

    pension_daten = [
        ["Parameter", "Wert"],
        ["Pensionsalter", f"{daten['gewuenschtes_pensionsalter']} Jahre"],
        ["Regelaltersgrenze", f"{pension['regelaltersgrenze']} Jahre"],
        ["Dienstjahre", f"{pension['dienstjahre']:.2f} Jahre"],
        ["Ruhegehaltssatz (vor Abschlag)", f"{pension['ruhegehaltssatz']:.2f}%"],
        ["Versorgungsabschlag", f"{pension['versorgungsabschlag_prozent']:.2f}%"],
        ["Effektiver Ruhegehaltssatz", f"{pension['effektiver_ruhegehaltssatz']:.2f}%"],
        ["Ruhegehaltsfähige Bezüge", format_euro(pension['ruhegehaltsfaehige_bezuege'])],
        ["Ruhegehalt brutto", format_euro(pension['ruhegehalt_brutto'])],
    ]

    table_pension = Table(pension_daten, colWidths=[8 * cm, 6 * cm])
    table_pension.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f39c12")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ecf0f1"), colors.white]),
    ]))
    elements.append(table_pension)
    elements.append(Spacer(1, 20))

    # 4. DU-Rente
    elements.append(Paragraph("4. Dienstunfähigkeitsrente", styles['Heading1Custom']))

    du = daten['du_rente']

    du_daten = [
        ["Parameter", "Wert"],
        ["DU-Szenario Jahr", str(daten['du_szenario_jahr'])],
        ["Alter bei DU", f"{du['alter_bei_du']} Jahre"],
        ["Ist-Dienstjahre", f"{du['ist_dienstjahre']:.2f} Jahre"],
        ["Zurechnungszeit", f"{du['zurechnungszeit']:.2f} Jahre"],
        ["Gesamt-Dienstjahre", f"{du['gesamt_dienstjahre']:.2f} Jahre"],
        ["Ruhegehaltssatz (vor Abschlag)", f"{du['ruhegehaltssatz']:.2f}%"],
        ["DU-Abschlag", f"{du['du_abschlag_prozent']:.2f}%"],
        ["Effektiver Ruhegehaltssatz", f"{du['effektiver_ruhegehaltssatz']:.2f}%"],
        ["Ruhegehaltsfähige Bezüge", format_euro(du['ruhegehaltsfaehige_bezuege'])],
        ["DU-Rente brutto", format_euro(du['du_rente_brutto'])],
        ["Mindestversorgung", format_euro(du['mindestversorgung'])],
    ]

    table_du = Table(du_daten, colWidths=[8 * cm, 6 * cm])
    table_du.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e74c3c")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -2), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ecf0f1"), colors.white]),
    ]))
    elements.append(table_du)
    elements.append(Spacer(1, 30))

    # 5. VERSORGUNGSLÜCKE - WICHTIG!
    elements.append(Paragraph("5. Versorgungslücke", styles['Heading1Custom']))

    versorgungsluecke = daten['versorgungsluecke']

    if versorgungsluecke > 0:
        # Warnung Box
        luecke_text = f"""
        <b>ACHTUNG: Versorgungslücke!</b><br/><br/>
        Bei Dienstunfähigkeit im Jahr {daten['du_szenario_jahr']} fehlen monatlich<br/>
        <font size="18"><b>{format_euro(versorgungsluecke)}</b></font><br/>
        gegenüber dem aktuellen Nettoeinkommen.<br/><br/>
        Das sind <b>{format_euro(versorgungsluecke * 12)}</b> pro Jahr!
        """

        luecke_daten = [[Paragraph(luecke_text, ParagraphStyle(
            name='LueckeText',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.white,
            alignment=TA_CENTER,
            leading=18
        ))]]

        table_luecke = Table(luecke_daten, colWidths=[14 * cm])
        table_luecke.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#c0392b")),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
            ('BOX', (0, 0), (-1, -1), 3, colors.HexColor("#922b21")),
        ]))
        elements.append(table_luecke)
    else:
        elements.append(Paragraph(
            "Keine Versorgungslücke - DU-Rente deckt das aktuelle Netto.",
            styles['Normal']
        ))

    elements.append(Spacer(1, 20))

    # 6. Vergleichstabelle
    elements.append(Paragraph("6. Übersicht", styles['Heading1Custom']))

    vergleich_daten = [
        ["Bezugsart", "Brutto", "Info"],
        ["Aktuelles Gehalt", format_euro(gehalt['brutto']), f"Netto: {format_euro(netto['netto'])}"],
        ["Altersrente", format_euro(pension['ruhegehalt_brutto']),
         f"Mit {daten['gewuenschtes_pensionsalter']} Jahren"],
        ["DU-Rente", format_euro(du['du_rente_brutto']), f"Szenario {daten['du_szenario_jahr']}"],
    ]

    table_vergleich = Table(vergleich_daten, colWidths=[5 * cm, 4 * cm, 5 * cm])
    table_vergleich.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ecf0f1"), colors.white]),
    ]))
    elements.append(table_vergleich)
    elements.append(Spacer(1, 30))

    # Footer
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.gray))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "Erstellt mit Beamtenrechner NRW | Alle Angaben ohne Gewähr | "
        f"Stand: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}",
        styles['Footer']
    ))

    # PDF erstellen
    doc.build(elements)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes


def format_euro(betrag: float) -> str:
    """Formatiert einen Betrag als Euro-String im deutschen Format."""
    return f"{betrag:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
