from fastapi import FastAPI, UploadFile, File, HTTPException
from PyPDF2 import PdfReader
from pytesseract import image_to_string, pytesseract
import google.generativeai as genai
import json
from config import API_KEY
import re
import os
from io import BytesIO
from PIL import Image
import fitz 

# Configure o caminho do executável do Tesseract (alterar conforme seu sistema)
pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Key do Google Gemini API
genai.configure(api_key=f"{API_KEY}")  

app = FastAPI(title="PDF Data Extraction API", version="1.0", description="Extrai dados de PDFs e imagens usando FastAPI e Google Gemini 1.5 Flash.")

def extract_text_from_image(image):
    try:
        text = image_to_string(image, lang="por")
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar OCR na imagem: {str(e)}")
    
def extract_text_from_pdf(file):
    try:
        # Tenta extrair texto de PDFs desbloqueados
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        if text.strip():
            return text
        else:
            # Salva o arquivo temporariamente no disco
            temp_file_path = "temp.pdf"
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(file.read())

            # Usa fitz para abrir o PDF e converter as páginas em imagens
            doc = fitz.open(temp_file_path)
            ocr_text = ""
            
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)  # Carrega a página
                pix = page.get_pixmap(dpi=300)  # Converte a página para imagem (pixmap)
                
                # Verifica se a imagem é RGB ou Grayscale e converte para PIL
                mode = "RGB" if pix.n == 3 else "L"
                img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
            
                # Salva a imagem para debug
                debug_image_path = f"debug_page_{page_num + 1}.png"
                img.save(debug_image_path, "PNG")
                print(f"Imagem da página {page_num + 1} salva em: {debug_image_path}")
            
                # Realiza OCR na imagem
                ocr_text += extract_text_from_image(img) + "\n"

            # Remove o arquivo temporário
            doc.close()  # Fecha o documento para garantir que o arquivo não seja bloqueado
            os.remove(temp_file_path)

            return ocr_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o arquivo: {str(e)}")
    
def extract_data_with_gemini(text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        A partir do texto de escritura a seguir, extraia as seguintes informações:
        - Nome completo do Outorgante 
        - Nacionalidade do Outorgante
        - Estado civil do Outorgante
        - Documento de indetificação do Outorgante
        - Endereço do Outorgante
        - Nome completo do Outorgado 
        - Nacionalidade do Outorgado
        - Estado civil do Outorgado
        - Documento de indetificação do Outorgado
        - Endereço do Outorgado
        

        Se alguma informação não estiver presente, retorne 'N/A'.

        Texto:
        {text}

        Retorne a resposta no formato JSON, por exemplo:
        {{
            "nome_Outorgante": "João da Silva",
            "nacionalidade_Outorgante": "brasileiro",
            "estadoCivil_Outorgante": "solteiro",
            "documentoIdentificador_Outorgante": "258788991",
            "endereco_Outorgante": "Rua Exemplo, 123, Bairro Exemplo, Cidade, Estado",
            "nome_Outorgado": "Isabela Ferreira",
            "nacionalidade_Outorgado": "brasileiro",
            "estadoCivil_Outorgado": "solteira",
            "documentoIdentificador_Outorgado": "20765057760",
            "endereco_Outorgado": "Rua Exemplo, 123, Bairro Exemplo, Cidade, Estado",
        }}
        """
        response = model.generate_content(prompt)
        
        # Usa regex para capturar apenas o conteúdo JSON válido
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if not match:
            raise ValueError("Resposta do Gemini não contém JSON válido.")

        clean_json = match.group(0)

        # Converte o conteúdo capturado para um dicionário
        json_data = json.loads(clean_json)

        return json_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar com o Gemini: {str(e)}")

@app.post("/extract", summary="Extrai dados do PDF", description="Recebe um PDF e retorna os dados extraídos (nome, endereço, data de nascimento) em JSON.")
async def extract_data(file: UploadFile = File(...)):
    try:
        # Verifica o tipo do arquivo enviado
        if file.content_type in ["application/pdf"]:
            # Processa PDFs
            text = extract_text_from_pdf(file.file)
        elif file.content_type in ["image/jpeg", "image/png"]:
            # Processa imagens
            image = Image.open(file.file)
            text = extract_text_from_image(image)
        else:
            raise HTTPException(status_code=400, detail="O arquivo deve ser um PDF, JPG ou PNG.")

        # Extrai dados com o modelo do Gemini
        extracted_data = extract_data_with_gemini(text)

        return {"dados_extraidos": extracted_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))