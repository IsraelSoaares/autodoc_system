from fpdf import FPDF 
import os
from jinja2 import Environment, FileSystemLoader
from datetime import date

template_dir = 'templates'
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template('contrato_servico.html')

data = date.today()


dados = {
    'Cliente' : "Levi Ricardo Ferreira Nunes",
    'Empresa' : 'VascoDaGama',
    'servico' : 'Programador FullStack',
    'Valor' : '2.000,00',
    'Data' : data,


}

html_content = template.render(dados)

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

pdf.multi_cell(0,10, html_content)

pdf_output_path = os.path.join('docs', 'contrato_levi.pdf')
pdf.output(pdf_output_path)



