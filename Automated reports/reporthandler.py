from reportlab.pdfgen import canvas

c=canvas.Canvas("test.pdf", pagesize=(612,792))#this size is a letter size
c.drawString(50,780, "Hello world")
c.showPage()
c.save()
