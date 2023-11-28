from fastapi import APIRouter, UploadFile
from ocrapi import SparkApi
from ocrapi.test import ocr_image
import uuid
import os
from model.models import Ingredient

ocrRouter = APIRouter()


@ocrRouter.post("/", description="用户上传图片，返回配料数据")
async def ocr_ingredient(file: UploadFile):
    # 生成唯一文件名
    file_extension = file.filename.split('.')[-1]
    unique_filename = str(uuid.uuid4()) + '.' + file_extension
    target_folder = "./file"
    os.makedirs(target_folder, exist_ok=True)
    target_path = os.path.join(target_folder, unique_filename)

    with open(target_path, 'wb') as f:
        for chunk in iter(lambda: file.file.read(1024), b''):
            f.write(chunk)

    ocr_tes = ocr_image(target_path)
    results = ocr_tes.result()
    final_list = []

    # 处理 OCR 结果
    for item in results:
        ingredient = await Ingredient.filter(chinese_name=item).first()
        if ingredient:
            imageUrl = 'http://127.0.0.1:8000' + target_path
            # data['imgUrl'] = imageUrl
            final_list.append(ingredient)
        else:
            final_list.append({
                '配料名': item,
                'error': '抱歉，数据库中没有找到这个配料信息'})

    # 返回响应
    return final_list
