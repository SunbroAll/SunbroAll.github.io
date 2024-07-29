import os
import requests
import time
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
import cv2
import numpy as np

app = FastAPI()

# Предварительно заданные ссылки для замены лица
target_image_urls = [
    'https://i.postimg.cc/J7pJbRbp/1.png',
    'https://uc804b222d66b685597d9f1a5596.previews.dropboxusercontent.com/p/thumb/ACVRyfV-NtwfH4-fcXofm4VwAl94trFZincIoqXSjmisyIeXTozxbXHRxrufLud4nlod28iPMctoKzzyCFiKCfTe3V6HKWkiIvnop9rBF1Zh9jex2jKMMmYs9eNq-NKgL6w3KrgUBlOa-xZSVCvGprqw2cWET41Ji9Z49yv2Dirj42OMb5KOIWWUpu_NZn3leETX6INBoapu9UKBXDTiDWJaY64hH9Q5MAl-qafuuyB8Kw8WPQgkAjiTxHFBg8jFvPY4ubQj-S_SD4wAdnW8ZhSStvoca8Tj6mre1QS6ypeGxs5qoUE1PKuJJerqNYFenVQEs2V8j63GTSFtiJovoW1SQmQYTFDyhMW_TCnsVm7vBQ/p.png',
    'https://i.postimg.cc/bJbbxn9b/3.png',
    'https://i.postimg.cc/FR9mp5jZ/4.png',
    'https://i.postimg.cc/NMfqT8cC/5.png',
    'https://i.postimg.cc/pXrq5nQs/6.png',
    'https://i.postimg.cc/Gmh5XLN9/7.png',
    'https://i.postimg.cc/J76Q8zwZ/7.png',
]

api_key = 'clysfcx8w000hmf09e6y51l1y'
faceswap_api_url = 'https://api.magicapi.dev/api/v1/capix/faceswap/faceswap/v1/image'
result_api_url = 'https://api.magicapi.dev/api/v1/capix/faceswap/result/'

# Путь к папке с логотипами
logo_folder = 'hair'  # Убедитесь, что путь к папке правильный

# Создаем папку для статических файлов, если ее нет
os.makedirs("static", exist_ok=True)

# Модель данных для входных данных
class FaceSwapRequest(BaseModel):
    swap_url: str
    target_index: int

# Функция для отправки запроса на faceswap API
def send_faceswap_request(target_url, swap_url):
    headers = {
        'accept': 'application/json',
        'x-magicapi-key': api_key,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = f'target_url={target_url}&swap_url={swap_url}'

    response = requests.post(faceswap_api_url, headers=headers, data=data)
    return response.json()

# Функция для получения результата faceswap
def retrieve_faceswap_result(request_id):
    headers = {
        'accept': 'application/json',
        'x-magicapi-key': api_key,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = f'request_id={request_id}'
    
    response = requests.post(result_api_url, headers=headers, data=data)
    return response.json()

# Функция для наложения логотипа
def overlay_logo(background_image_path, logo_path):
    try:
        background = Image.open(background_image_path).convert("RGBA")
        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize(background.size)
        
        combined = Image.alpha_composite(background, logo)
        
        output_filename = f"combined_image_{int(time.time())}.png"
        output_path = os.path.join("static", output_filename)
        combined.save(output_path, format='PNG')
        
        return output_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error overlaying logo: {str(e)}")

# Функция для апскейлинга изображения
def upscale_image(image, scale_factor):
    width, height = image.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    return image.resize((new_width, new_height), Image.LANCZOS)

# Функция для увеличения глаз
def apply_magnifying_glass_effect(image, center, radius, scale):
    output = image.copy()
    h, w = image.shape[:2]
    for y in range(h):
        for x in range(w):
            dist = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
            if dist < radius:
                factor = 1 + (scale - 1) * (1 - dist / radius) ** 2
                new_x = center[0] + (x - center[0]) * factor
                new_y = center[1] + (y - center[1]) * factor
                new_x = np.clip(new_x, 0, w - 1)
                new_y = np.clip(new_y, 0, h - 1)
                output[y, x] = image[int(new_y), int(new_x)]
    return output

def detect_and_enlarge_eyes(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in eyes:
        eye_center = (x + w // 2, y + h // 2)
        radius = w // 2
        image = apply_magnifying_glass_effect(image, eye_center, radius, 0.75)
    return image

@app.post("/faceswap/")
def faceswap(request: FaceSwapRequest):
    if request.target_index < 0 or request.target_index >= len(target_image_urls):
        raise HTTPException(status_code=400, detail="Invalid target index")
    
    swap_url = request.swap_url
    target_url = target_image_urls[request.target_index]
    
    faceswap_response = send_faceswap_request(target_url, swap_url)
    
    if 'image_process_response' in faceswap_response and faceswap_response['image_process_response']['status'] == 'OK':
        request_id = faceswap_response['image_process_response']['request_id']
        
        # Ждем некоторое время перед получением результата (если требуется)
        time.sleep(5)  # Ждем 5 секунд для примера
        
        result_response = retrieve_faceswap_result(request_id)
        
        if 'image_process_response' in result_response and result_response['image_process_response']['status'] == 'OK':
            processed_image_url = result_response['image_process_response']['result_url']
            
            # Загрузка изображения для обработки
            response = requests.get(processed_image_url)
            image = Image.open(BytesIO(response.content))

            # Апскейлинг изображения
            scale_factor = 2.0  # Фактор масштабирования (например, увеличиваем в 2 раза)
            upscaled_image = upscale_image(image, scale_factor)

            # Преобразование изображения обратно в массив numpy для дальнейшей обработки
            image = np.array(upscaled_image)

            # Увеличение глаз
            image = detect_and_enlarge_eyes(image)

            # Сохранение временного изображения
            temp_image_path = 'temp_enlarged_eyes.png'
            cv2.imwrite(temp_image_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

            # Определение пути к логотипу на основе target_index
            logo_path = os.path.join(logo_folder, f"{request.target_index}.png")

            # Наложение логотипа
            final_image_path = overlay_logo(temp_image_path, logo_path)
            final_image_url = f"/static/{os.path.basename(final_image_path)}"
            
            return {"processed_image_url": processed_image_url, "final_image_url": final_image_url}
        else:
            raise HTTPException(status_code=500, detail="Error retrieving face swap result")
    else:
        raise HTTPException(status_code=500, detail="Error initiating face swap")

# Подключаем папку для статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
