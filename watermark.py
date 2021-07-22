# dependencies PyPDF2, to install use pip install PyPDF2
# To use this
# python3 watermark.py "your text watermark" path/input.pdf path/output.pdf

from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import sys

packet = io.BytesIO()
argsLen = len(sys.argv)
args = sys.argv

if 3 > argsLen :
    raise Exception('Watermark and the input file must be defined')

txtWatermark = args[1]
INPUT_FILE = args[2]

try :
   OUTPUT_FILE = args[3]
except:
   OUTPUT_FILE = args[2] + '.watermarked'

# Read your existing PDF
existing_pdf = PdfFileReader(open(INPUT_FILE, "rb"))

# get pdf width and height then calculate appropriate watermark placement
# watermark will place on middle right translate to 90 deg
# Note : width will less to -10px to place a watermark in pdfRight - 10 px
width = -int(existing_pdf.getPage(0).mediaBox.getWidth() - 5)
height = existing_pdf.getPage(0).mediaBox.getHeight()
calculatedHeight = height * 75 / 100
finalHeight = int(height - calculatedHeight)

# Create canvas then place it in a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
can.setFont('Helvetica', 5)
can.saveState()
can.rotate(90)
can.drawString(finalHeight, width, txtWatermark)
can.restoreState()
can.save()

# Move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
output = PdfFileWriter()

# Add the "watermark" (which is the new pdf) on all the existing page
pageNum = existing_pdf.getNumPages()
for i in range(pageNum):
    page = existing_pdf.getPage(i)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

# Finally, write "output" to a real file
outputStream = open(OUTPUT_FILE, "wb")
output.write(outputStream)
outputStream.close()
