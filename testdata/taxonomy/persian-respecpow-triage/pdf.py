from weasyprint import HTML
HTML(string='<p>Hello</p>').write_pdf('out.pdf')
