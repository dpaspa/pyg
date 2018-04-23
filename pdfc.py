from pyPdf import PdfFileReader, PdfFileWriter

def pdfCreate():
    output = PdfFileWriter()
    pdfOne = PdfFileReader(file( "out.pdf", "rb"))
    pdfTwo = PdfFileReader(file("out1.pdf", "rb"))

    output.addPage(pdfOne.getPage(0))
    output.addPage(pdfTwo.getPage(0))

    outputStream = file(r"output.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

pdfCreate()




#    def paragraph_replace(self, search, replace):
#        searchre = re.compile(search)
#        for paragraph in self.paragraphs:
#            paragraph_text = paragraph.text
#            if paragraph_text:
#                if searchre.search(paragraph_text):
#                    self.clear_paragraph(paragraph)
#                    paragraph.add_run(re.sub(search, replace, paragraph_text))
#        return paragraph

#    def clear_paragraph(self, paragraph):
#        p_element = paragraph._p
#        p_child_elements = [elm for elm in p_element.iterchildren()]
#        for child_element in p_child_elements:
#            p_element.remove(child_element)


#        document = Document()
#        paragraph = document.add_paragraph('Lorem ipsum dolor sit amet.')
#        prior_paragraph = paragraph.insert_paragraph_before('Lorem ipsum')
#        document.add_heading('The REAL meaning of the universe')
#        document.add_heading('The role of dolphins', level=2)
#        table = document.add_table(rows=2, cols=2)
#        paragraph = document.add_paragraph('Lorem ipsum dolor sit amet.')
#        paragraph.style = 'Normal'
#        document.save('./test.odt')

#table = document.add_table(1, 3)
