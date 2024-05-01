import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import base64

def encrypt(string):
    en = {}
    mv = 4
    for key, char in string.items():
        res = []  # Initialize res as a list
        for i in char:
            if i.isalpha():
                start = ord('A') if i.isupper() else ord('a')
                temp = chr(start + (ord(i) - start + mv) % 26)
                res.append(temp)
            else:
                res.append(i)
                
        base = base64.b64encode(''.join(res).encode()).decode()        
        en[key] = base
    return en

def addlastpage(output_buffer):
    c = canvas.Canvas(output_buffer, pagesize=letter)
    c.showPage()
    c.save()

def addfirstpage(image_path, output_buffer):
    c = canvas.Canvas(output_buffer, pagesize=letter)
    # Add image
    c.drawImage(image_path, 0, 0, width=letter[0], height=letter[1])
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
    c.showPage()
    c.save()

def edit(input_pdf, output_pdf, new_metadata, img):
    output_buffer = io.BytesIO()

    # Create a blank page with the first page image
    addfirstpage(img, output_buffer)
    output_buffer.seek(0)

    pdf_writer = PdfWriter()

    # Add page 
    pagefirst = PdfReader(output_buffer).pages[0]
    pdf_writer.add_page(pagefirst)

    # Open the input PDF file in read-binary mode
    with open(input_pdf, 'rb') as file:
        pdf_reader = PdfReader(file)

        # Copy pages from the input PDF to the output PDF
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

    # Create a buffer for the last page
    output_buffer = io.BytesIO()
    addlastpage(output_buffer)
    output_buffer.seek(0)

    # Add last page
    lastpage = PdfReader(output_buffer).pages[0]
    pdf_writer.add_page(lastpage)

    # Update metadata
    pdf_writer.add_metadata(new_metadata)
    with open(output_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)


def main():
    input_pdf = 'output/1-4-PB.pdf'
    output_pdf = 'output/output.pdf'    
    new_metadata = {'/Title': 'why??', '/Author': 'Tejo', '/Subject': 't'}
    message = encrypt(new_metadata)
    print(message)
    img = 'foto.png'

    edit(input_pdf, output_pdf, message, img)

main()
