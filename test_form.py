from form_chat.hunde_form import DOG_FORM
from form_chat.pdf import create_pdf_table
from datetime import date

for i,a in DOG_FORM.fields.items():
    a.value = i[::-1]
    
DOG_FORM.fields["birthday"].value = date(1966,4,20)

create_pdf_table(DOG_FORM, "pdfs/test.pdf")