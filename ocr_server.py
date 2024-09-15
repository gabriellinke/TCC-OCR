import easyocr
import logging
import re
from fastapi import FastAPI, UploadFile, File
import uvicorn

# Configura o nível de logging para ERROR para suprimir avisos do EasyOCR
logging.getLogger('easyocr').setLevel(logging.ERROR)

# Inicializa o modelo EasyOCR
reader = easyocr.Reader(['pt'])

# Expressão regular para exatamente 6 dígitos numéricos
six_digit_pattern = re.compile(r'^\d{6}$')

# Inicializa o FastAPI
app = FastAPI()

# Endpoint FastAPI para upload da imagem e retorno do OCR
@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Utiliza o EasyOCR para ler o texto da imagem
        result = reader.readtext(contents)

        for item in result:
            text = item[1]  # Penúltima string (texto)
            confidence = round(item[2], 2)  # Último número truncado para 2 casas decimais

            # Verifica se o texto contém exatamente 6 dígitos numéricos
            if six_digit_pattern.match(text):
                print(f"{text}, {confidence}")
                return {"assetNumber": text, "confidenceLevel": confidence}

        # Retorna null se não houver texto com 6 dígitos
        print(f"Asset number não encontrado")
        return {"assetNumber": None, "confidenceLevel": None}
     
    except Exception as e:
        print(f"Erro: {str(e)}")
        return {"assetNumber": None, "confidenceLevel": None}

    finally:
        file.file.close()
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

