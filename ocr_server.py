import easyocr
import logging
import re
from fastapi import FastAPI, UploadFile, File, HTTPException
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
@app.post("/")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Tipo de arquivo inválido. Por favor, faça upload de imagens.")

    try:
        contents = await file.read()

        # Utiliza o EasyOCR para ler o texto da imagem
        result = reader.readtext(contents)

        for item in result:
            text = item[1]  # Penúltima string (texto)
            confidence = round(item[2], 2)  # Último número truncado para 2 casas decimais

            # Verifica se o texto contém exatamente 6 dígitos numéricos
            if six_digit_pattern.match(text):
                logging.info(f"{text}, {confidence}")
                return {"assetNumber": text, "confidenceLevel": confidence}

        # Retorna null se não houver texto com 6 dígitos
        logging.error(f"Asset number não encontrado")
        return {"assetNumber": None, "confidenceLevel": None}
     
    except Exception as e:
        logging.error(f"Erro: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        file.file.close()
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

