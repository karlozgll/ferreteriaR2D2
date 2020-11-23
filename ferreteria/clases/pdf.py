from fpdf import FPDF
from flask import make_response
from datetime import datetime

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('ferreteria/static/images/Logo_v2.png', 10, 8, 15)
        # Arial bold 15
        self.set_font('Helvetica', 'B', 20)
        # Move to the right
        self.cell(105)
        # Title
        self.cell(50, 10, 'Clavo de Oro', 0, 0, 'C')
        fecha = datetime.now()
        self.set_font('Arial', 'B', 10)
        self.cell(130, 10, 'Fecha: ' + str(fecha.day) + '-' + str(fecha.month) + '-' + str(fecha.year), 0, 0, 'R')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 8, '2020', 0, 0, 'L')
        self.cell(0, 10, 'Pagina ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def pdfVentas(ventas):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page(orientation='L')
    page_width = pdf.w - 2 * pdf.l_margin
    pdf.cell(50, 10, 'Reportes de ploteos', 0, 0, 'C')
    pdf.ln(10)
    pdf.set_font('Courier', 'B', 8)
    col_width = page_width / 4
    pdf.ln(1)
    th = pdf.font_size
    pdf.cell(30)
    pdf.cell(15, th, "ID", 1, 0, 'C')
    pdf.cell(60, th, "Fecha", 1, 0, 'C')
    pdf.cell(40, th, "Descuento", 1, 0, 'C')
    pdf.cell(40, th, "Total", 1, 0, 'C')
    pdf.cell(60, th, "Cliente", 1, 0, 'C')
    pdf.ln(th)
    pdf.set_font('Courier', '', 8)

    for venta in ventas:
        pdf.cell(30)
        pdf.cell(15, th, str(venta.id), 1,0,'C')
        pdf.cell(60, th, str(venta.fecha), 1,0,'C')
        pdf.cell(40, th, str(venta.descuento), 1,0,'C')
        pdf.cell(40, th, str(venta.total), 1,0,'C')
        pdf.cell(60, th, str(venta.cliente_id), 1,0,'C')
        pdf.ln(th)

    pdf.ln(10)
    pdf.set_font('Times', '', 10.0)
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers.set('Content-Disposition', 'inline', filename="reportes.pdf")
    response.headers.set('Content-Type', 'application/pdf')
    return response

def pdfCompras(compras):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page(orientation='L')
    page_width = pdf.w - 2 * pdf.l_margin
    pdf.cell(50, 10, 'Reportes de ploteos', 0, 0, 'C')
    pdf.ln(10)
    pdf.set_font('Courier', 'B', 8)
    col_width = page_width / 4
    pdf.ln(1)
    th = pdf.font_size
    pdf.cell(30)
    pdf.cell(15, th, "ID", 1, 0, 'C')
    pdf.cell(60, th, "Fecha", 1, 0, 'C')
    pdf.cell(40, th, "Total", 1, 0, 'C')
    pdf.cell(60, th, "Proveedor", 1, 0, 'C')
    pdf.ln(th)
    pdf.set_font('Courier', '', 8)

    for compra in compras:
        pdf.cell(30)
        pdf.cell(15, th, str(compra.id), 1,0,'C')
        pdf.cell(60, th, str(compra.fecha), 1,0,'C')
        pdf.cell(40, th, str(compra.total), 1,0,'C')
        pdf.cell(60, th, str(compra.proveedor_id), 1,0,'C')
        pdf.ln(th)

    pdf.ln(10)
    pdf.set_font('Times', '', 10.0)
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers.set('Content-Disposition', 'inline', filename="reportes.pdf")
    response.headers.set('Content-Type', 'application/pdf')
    return response