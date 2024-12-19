### PARA RODAR LOCAMENTE O SCRIPT

1. Clone o repositório e instale as dependêcias.
    1.1 Para isso utilize pip install -r requirements.txt

2. Tenha sua própria API Key.
    2.1 Este script utiliza o google gemini 1.5 flash, você deve criar sua prórpia API Key em https://ai.google.dev/gemini-api/docs/api-key?hl=pt-br.
    2.2 Com esta chave em mãos, crie um arquivo chamado config.py, dentro dele atribua sua Key a uma constate com nome de API_KEY (ex: API_KEY = "SUA_KEY")

3. Instale tesseract em sua máquina (windows version)
    3.1 Siga este tutorial no youtube até o minuto 1:50 https://www.youtube.com/watch?v=2kWvk4C1pMo&list=LL&index=1&t=138s&ab_channel=JayMartMedia.
    3.2 Certifique-se de que o diretório o qual instalou o Tesseract é o mesmo referenciado no código.
    3.3 Após baixe este arquivo https://github.com/tesseract-ocr/tessdata/blob/main/por.traineddata e copie para dentro da pasta \Tesseract-OCR\tessdata.

4. Rode a API.
    4.1 Basta utilizar o comando "uvicorn main:app --reload"