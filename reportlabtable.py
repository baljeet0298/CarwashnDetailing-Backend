# import reportlab.platypus
# import reportlab.lib.pagesizes
# import reportlab.platypus
#
# import reportlab.lib
# data=[["q","w"],
#       ["q","w"],
#       ["q","w"],
#       ["q","w"]]
# pdf=SimpleDocTemplate("new2.pdf",pagesize=letter)
# table=Table(data)
#
# style=TableStyle([('BACKGROUND',(0,0),(0,-1),colors.green),
#                   ('TEXTCOLOR',(1,0),(-1,-1),colors.whitesmoke),
#                   ('ALIGN',(0,0),(-1,-1),'CENTER'),
#                   ('FONT-NAME',(0,0),(-1,-1),'Courier-Bold'),
#                   ('FONT_SIZE',(1,0),(-1,-1),12),
#                   ('FONT_SIZE',(0,0),(0,-1),14),
#                 ('BACKGROUND',(1,0),(-1,-1),colors.beige)])
# table.setStyle(style)
# table=Table(data)
# element=[]
# element.append(table)
# pdf.build(element)
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter,inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Image
from reportlab.pdfgen import canvas
doc=canvas.Canvas("4.pdf")
#doc = SimpleDocTemplate("3.pdf", pagesize=letter)
doc.setTitle("Car Wash N Detailing : Invoice")
doc.drawCenteredString(290,720, "Invoice")
doc.line(30,710,550,710)
# container for the 'Flowable' objects
# elements = []
#
# I = Image('static/logo.jpeg')
# I.drawHeight = 1.75*in n4vq":z '[xl'd64.........ch*I.drawHeight / I.drawWidth
# I.drawWidth = 1.75*inch
# elements.append(I)
#
# data= [['00', '01'],
# ['10', '11'],
# ['20', '21'],
# ['30', '31']]
# t=Table(data)
# t.setStyle(TableStyle([('BACKGROUND',(0,0),(1,0),colors.green),
# ('TEXTCOLOR',(1,0),(-1,-1),colors.black),
#                   ('ALIGN',(0,0),(-1,-1),'CENTER'),
#                   ('FONT-NAME',(0,0),(-1,-1),'Courier-Bold'),
#                   ('FONT_SIZE',(1,0),(-1,-1),12),
#                   ('FONT_SIZE',(0,0),(0,-1),14),
#                 ('BACKGROUND',(1,0),(-1,-1),colors.beige)]))
# elements.append(t)
# write the document to disk
#doc.build(elements)
doc.save()