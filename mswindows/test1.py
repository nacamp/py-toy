'''
https://stackoverflow.com/questions/6011115/doc-to-pdf-using-python
https://github.com/AlJohri/docx2pdf
https://pypi.org/project/comtypes/
python \\tsclient\rdp_share\doc2pdf.py
t2-medium : 2cpu-4G
4장워드 12초
time : 2.2505595684051514
time : 12.719176530838013
time : 21.030635595321655
time : 28.82224726676941
t3-2xlarge : 8cpu-32G
time : 2.090985059738159
time : 12.083971500396729
time : 20.379962682724
time : 28.582431316375732
...
time : 2.0908524990081787
time : 11.877388000488281
time : 19.952051162719727
time : 27.69434952735901
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
in_file2 = os.path.abspath('\\\\tsclient\\rdp_share\\doc2.doc')
out_file2 = os.path.abspath('\\\\tsclient\\rdp_share\\doc2.pdf')
in_file3 = os.path.abspath('\\\\tsclient\\rdp_share\\doc3.doc')
out_file3 = os.path.abspath('\\\\tsclient\\rdp_share\\doc3.pdf')


word = comtypes.client.CreateObject('Word.Application')
print("time :", time.time() - start)

doc = word.Documents.Open(in_file)
doc.SaveAs(out_file, FileFormat=wdFormatPDF)
doc.Close()
print("time :", time.time() - start)

doc = word.Documents.Open(in_file2)
doc.SaveAs(out_file2, FileFormat=wdFormatPDF)
doc.Close()
print("time :", time.time() - start)

doc = word.Documents.Open(in_file3)
doc.SaveAs(out_file3, FileFormat=wdFormatPDF)
doc.Close()

word.Quit()
print("time :", time.time() - start)