import pytesseract
from pdf2image import convert_from_path
import re

caminho_poppler = r"C:\Program Files\Poppler\poppler-24.08.0\Library\bin"
caminho_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = caminho_tesseract

caminho_pdf = r"C:\Users\Paulo Mauricio\Downloads\certidão negativa trabalhista.pdf"
images = convert_from_path(caminho_pdf, poppler_path=caminho_poppler)

def extrair_informacoes(texto):
    nome_pattern = r'Nome:\s*([\s\S]*?)(?=\nCNPJ:)'
    cnpj_pattern = r'CNPJ:\s*([\d\.\/-]+)'
    certidao_pattern = r"Certidão n[ºo]*:\s*([\d/]+)"
    expedicao_pattern = r'Expedição:\s*(\d{2}/\d{2}/\d{4})'
    validade_pattern = r'Validade:\s*(\d{2}/\d{2}/\d{4})'

    nome = re.search(nome_pattern, texto)
    cnpj = re.search(cnpj_pattern, texto)
    certidao = re.search(certidao_pattern, texto)
    expedicao = re.search(expedicao_pattern, texto)
    validade = re.search(validade_pattern, texto)

    return {
        'Nome': nome.group(1).strip() if nome else None,
        'CNPJ': cnpj.group(1) if cnpj else None,
        'Certidão': certidao.group(1) if certidao else None,
        'Expedição': expedicao.group(1) if expedicao else None,
        'Validade': validade.group(1) if validade else None
    }

text_completed = ""
for image in images:
    text = pytesseract.image_to_string(image, lang="por")
    text_completed += text + "\n"

caminho_saida1 = r"C:\Users\Paulo Mauricio\Downloads\imagem_texto.txt"

informacoes = extrair_informacoes(text_completed)

with open(caminho_saida1, 'w', encoding='utf-8') as arquivo_saida:
    arquivo_saida.write(f"Nome: {informacoes['Nome']}\n")
    arquivo_saida.write(f"CNPJ: {informacoes['CNPJ']}\n")
    arquivo_saida.write(f"Certidão: {informacoes['Certidão']}\n")
    arquivo_saida.write(f"Expedição: {informacoes['Expedição']}\n")
    arquivo_saida.write(f"Validade: {informacoes['Validade']}\n")

print(f"Informações específicas salvas em {caminho_saida1}")