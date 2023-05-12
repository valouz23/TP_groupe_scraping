import PyPDF2

# Ouverture du PDF en lecture binaire 
pdf_file = open('automatisation.pdf', 'rb')

# Création d'un objet pour lire le document PDF 
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Comptage du nombre de pages
num_pages = len(pdf_reader.pages)

# Création d'une variable pour stocker le texte extrait de toutes les pages
text = ''

# Boucle pour naviguer sur toutes les pages du PDF et extraire le contenu 
for page in range(num_pages):
    # Récupération de la page correspondante 
    page_obj = pdf_reader.pages[page]
    
    # Extraction du texte de la page pour le stockage dans une variable 
    extracted_text = page_obj.extract_text()
    
    # Ajout du texte extrait de la page dans la variable 
    text += extracted_text

pdf_file.close()

print(text)
