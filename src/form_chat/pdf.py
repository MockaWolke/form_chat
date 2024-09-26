from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from form_chat.forms import FormFormat

def create_pdf_table(form: FormFormat, filename="ergebnisse.pdf"):
    # Create a SimpleDocTemplate object
    pdf = SimpleDocTemplate(filename, pagesize=letter)

    # Create a title with form name, description, and date
    styles = getSampleStyleSheet()
    title = Paragraph(f"<b>{form.name}</b>", styles['Title'])
    description = Paragraph(f"{form.description}", styles['Normal'])
    date = Paragraph(f"Datum: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}", styles['Normal'])

    # Initialize table data with header
    table_data = [["Kategorie", "Wert"]]

    # Add field data from form to the table
    for field_name, field_object in form.fields.items():
        table_data.append([field_name, str(field_object.value)])

    # Create the table with the data
    table = Table(table_data)

    # Define the style for the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background gray
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text white
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align text
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for header
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding at the bottom of header cells
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Beige background for table data
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Black grid for table
    ])

    table.setStyle(style)

    # Add title, description, date, and table to the PDF
    elements = [title, description, date, table]

    # Build the PDF document
    pdf.build(elements)
