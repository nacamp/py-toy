'''
https://stackoverflow.com/questions/6011115/doc-to-pdf-using-python
https://github.com/AlJohri/docx2pdf
https://pypi.org/project/comtypes/
python \\tsclient\rdp_share\doc2pdf.py
4장워드 12초
'''
import sys
import os
import time
import comtypes.client
start = time.time()

wdFormatPDF = 17

# in_file = os.path.abspath(sys.argv[1])
# out_file = os.path.abspath(sys.argv[2])
in_file = os.path.abspath('\\\\tsclient\\rdp_share\\doc.doc')
out_file = os.path.abspath('\\\\tsclient\\rdp_share\\doc.pdf')

word = comtypes.client.CreateObject('Word.Application')
doc = word.Documents.Open(in_file)
doc.SaveAs(out_file, FileFormat=wdFormatPDF)
doc.Close()
word.Quit()
print("time :", time.time() - start)