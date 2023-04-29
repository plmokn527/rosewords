import os
from docx import Document
from docx.shared import Inches, Cm
from PIL import Image

def add_qrcode_to_table(table, row, col, img_path, img_size):
    cell = table.cell(row, col)
    paragraph = cell.paragraphs[0]
    run = paragraph.add_run()
    run.add_picture(img_path, width=img_size, height=img_size)
    paragraph.add_run().add_break()
    paragraph.add_run(os.path.splitext(os.path.basename(img_path))[0])

def create_word_with_qrcodes(qrcode_folder, output_file, rows=5, cols=3):
    qrcode_files = [f for f in os.listdir(qrcode_folder) if f.endswith('.png') or f.endswith('.jpg')]
    qrcode_files.sort()

    doc = Document()
    img_size = Cm(3) # 自定义图片大小，这里设置为3厘米

    i = 0
    while i < len(qrcode_files):
        table = doc.add_table(rows=rows, cols=cols)
        for row in range(rows):
            for col in range(cols):
                if i < len(qrcode_files):
                    add_qrcode_to_table(table, row, col, os.path.join(qrcode_folder, qrcode_files[i]), img_size)
                    i += 1
                else:
                    break
        if i < len(qrcode_files):
            doc.add_page_break()

    doc.save(output_file)

qrcode_folder = r'C:\Users\20139\PycharmProjects\pythonProject\qrcodes'
output_file = r'二维码文档.docx'

create_word_with_qrcodes(qrcode_folder, output_file)
