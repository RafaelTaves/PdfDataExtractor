# PDF Data Extraction API

Esta API permite extrair dados de PDFs e imagens utilizando OCR (Tesseract) e processamento de PDFs (Poppler e PyPDF2). Ela pode ser usada para converter documentos em texto, sendo útil em aplicações como digitalização de documentos e análise de dados.

---

## 🚀 Como Rodar Localmente o Script

### 1. Clone o repositório e instale as dependências

git clone https://github.com/seu-repositorio.git  
cd seu-repositorio  
pip install -r requirements.txt  

### 2. Configure sua própria API Key
Este script utiliza o Google Gemini 1.5 Flash. Para isso, siga os passos abaixo:  

Crie sua API Key em https://ai.google.dev/gemini-api/docs/api-key?hl=pt-br.  
Crie um arquivo chamado config.py no diretório raiz do projeto.  
Adicione a seguinte linha no arquivo, substituindo "SUA_KEY" pela chave que você obteve:  
API_KEY = "SUA_KEY"  

### 3. Instale o Tesseract (Windows)

Siga este tutorial no youtube até o minuto 1:50 https://www.youtube.com/watch?v=2kWvk4C1pMo&list=LL&index=1&t=138s&ab_channel=JayMartMedia.  
Certifique-se de que o diretório onde você instalou o Tesseract é o mesmo referenciado no código (pytesseract.tesseract_cmd).  
Após baixe este arquivo https://github.com/tesseract-ocr/tessdata/blob/main/por.traineddata e copie para dentro da pasta \Tesseract-OCR\tessdata.  

### 4. Instale o Poppler (Necessário para o pdf2image)

Windows:  
Siga este tutorial no youtube até o minuto 1:07 https://www.youtube.com/watch?v=PyF1Vh9040Y&t=260s&ab_channel=FreePythonCode  
Certifique-se de que o diretório onde você instalou o poppler é o mesmo referenciado no código (poppler_path=r"poppler-24.08.0\Library\bin").  

### 5. Rode a API.
  
Basta utilizar o comando "uvicorn main:app --reload"  

