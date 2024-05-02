import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime

import base64

def decrypt(en):
    mv = 4
    de = {}
    for key, base in en.items():
        res = []
        decoded = base64.b64decode(base.encode()).decode()
        for i in decoded:
            if i.isalpha():
                start = ord('A') if i.isupper() else ord('a')
                temp = chr(start + (ord(i) - start - mv) % 26)  # Reverse the encryption logic
                res.append(temp)
            else:
                res.append(i)
        # Menambahkan '/' pada awal kunci
        de['/' + key] = ''.join(res)
    return de

def findmetadata(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    metadata = {}
    temp1 = {}

    metadata_keys = ['/Title', '/Author', '/Subject', '/Creator', '/Producer', '/CreationDate', '/ModDate', '/Keywords']

    for key in metadata_keys:
        if key in pdf_reader.metadata:
            value = pdf_reader.metadata[key]
            if "=" in value:
                # Jika nilai metadata mengandung "==", simpan ke dalam temp1
                metadata[key[1:]] = value

    result = decrypt(metadata)
    print(result)
    return result

def edit(input_pdf, output_pdf, new_metadata):
    # Open the input PDF file in read-binary mode
    with open(input_pdf, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        # Copy pages and metadata from the input PDF to the output PDF
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

    # Update metadata
    pdf_writer.add_metadata(new_metadata)

    # Write the updated metadata to the output PDF file
    with open(output_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)

def main(): 
    file = "output/output.pdf"
    output = "output/decrypt.pdf"
    decmetadata = findmetadata(file)
    edit(file, output, decmetadata)

main()
