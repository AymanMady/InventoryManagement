from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# Créez une fonction pour générer le PDF
def create_pdf(file_name):
    c = canvas.Canvas(file_name, pagesize=letter)

    # Texte en arabe
    arabic_text = "مرحبا بكم في Python!"
    # Inversez le texte en arabe pour un affichage correct
    bidi_text = get_display(reshape(arabic_text))
    print(bidi_text)

    # Écrivez le texte sur le PDF
    c.drawString(100, 700, bidi_text)

    # Sauvegardez le PDF
    c.save()

# Appelez la fonction pour créer le PDF
create_pdf("exemple_arabe.pdf")
