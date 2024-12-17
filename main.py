from fastapi import FastAPI, UploadFile, File, HTTPException
from PyPDF2 import PdfReader
import google.generativeai as genai
import json
from config import API_KEY
import re
import os


# Key do Google Gemini API
genai.configure(api_key=f"{API_KEY}")  

app = FastAPI(title="PDF Data Extraction API", version="1.0", description="Extrai dados de PDFs usando FastAPI e Google Gemini 1.5 Flash.")

def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler o PDF: {str(e)}")

def extract_data_with_gemini(text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        A partir do texto a seguir, extraia as seguintes informações:
        - Nome completo
        - Endereço
        - Data de nascimento (formato DD/MM/AAAA)

        Se alguma informação não estiver presente, retorne 'N/A'.

        Texto:
        {text}

        Retorne a resposta no formato JSON, por exemplo:
        {{
            "nome": "João da Silva",
            "endereco": "Rua Exemplo, 123, Bairro Exemplo, Cidade, Estado",
            "data_nascimento": "01/01/1990"
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
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="O arquivo deve ser um PDF.")

    try:
        text = extract_text_from_pdf(file.file)

        extracted_data = extract_data_with_gemini(text)

        return {"dados_extraidos": extracted_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
