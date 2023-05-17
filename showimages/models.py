"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

import hashlib
import os
import random

from PIL import Image
import redis


class Handler:

    def __init__(self) -> None:
        pass


class RedisHandler(Handler):
    """Redis数据库操作句柄"""

    def __init__(self, host="localhost", port=6379) -> None:
        pool = redis.ConnectionPool(host=host, port=port)
        
        self.handler = redis.Redis(connection_pool=pool, decode_responses=True)

    def set_expiration_time(self, user_id: str, expiration_time: str):
        """添加或更新用户数据有效期"""
        self.handler.set(user_id, expiration_time)

    def set_report(self, image_id: str, report: dict):
        """添加图片报告数据"""
        self.handler.hset(image_id, mapping=report)

    def get_user_expiration_time(self, user_id: str):
        """获取用户的数据有效期"""
        return self.handler.get(user_id)
    
    def get_report(self, image_id: str):
        """获取报告"""
        return self.handler.hgetall(image_id)
    
    def delete_user(self, user_id):
        """删除用户"""
        self.handler.delete(user_id)


class ImageHandler(Handler):

    def set_image_path(self, image_path):
        self.path = image_path
    
    def get_image_data(self):
        """获取图片的二进制信息"""
        image_name = os.path.basename(self.path)

        try:
            with open(self.path, "rb") as f:
                image_data = f.read()
                
                return image_data
        except IOError:
            print(f"无法打开图片: {image_name}")
            return None

    def get_image_info(self):
        """获取图片的基础信息"""

        image_name = os.path.basename(self.path)
        file_size = os.path.getsize(self.path)

        if image_data := self.get_image_data():
            image_hash = hashlib.sha256(image_data).hexdigest()

        try:
            with Image.open(self.path) as image:
                image_format = image.format
                image_size = image.size

            return {
                "original_name": image_name,
                "original_path": self.path,
                "file_size": file_size,
                "image_format": image_format,
                "image_size": image_size,
                "image_hash": image_hash,
                "image_name": image_hash + '.' + image_format.lower(),
            }
        except IOError:
            print(f"无法打开图片: {image_name} !")
            return None
        

class ImageProcessor(Handler):

    image_handler = ImageHandler()
    redis_handler = RedisHandler()
    

    def __init__(self, upload_path, result_path) -> None:
        self.upload_path = upload_path
        self.result_path = result_path
        self.error_handler = ModelErrorHandler(self)

    def process(self):
        image_names = os.listdir(self.upload_path)
        for image_name in image_names:
            image_path = os.path.join(self.upload_path, image_name)

            try:
                self._process_image(image_path)
            except:
                self.error_handler.set_error_item(dict(image_name=image_name))

    def _process_image(self, image_path):

        self.image_handler.set_image_path(image_path)

        image_data = self.image_handler.get_image_data()
        image_info = self.image_handler.get_image_info()

        # 在这里处理图片二进制数据并返回处理过后的二进制数据
        # 现在假设已经对图片做过了处理，并得到了新的图片数据以及分析结果
        # 其中分析结果用随机数据代替

        # 处理过后的图片数据
        new_image_data = image_data
        new_image_name = image_info["image_name"]
        new_image_path = os.path.join(self.result_path, new_image_name)

        # 处理的结果报告
        # 一般信息
        general_1 = random.randint(1, 10)
        general_2 = random.randint(1, 10)
        
        # 特征信息
        feature_1 = random.randint(0, 1)
        feature_2 = random.randint(0, 1)

        # 将报告以字典的形式储存在 redis 缓存中
        report = dict(general_1=general_1, general_2=general_2, feature_1=feature_1, feature_2=feature_2)
        try:
            self.redis_handler.set_report(image_id=image_info["image_hash"], report=report)
        except:
            self.error_handler.set_error_item(dict(report=report))

        try:
            with open(new_image_path, "wb") as image:
                image.write(new_image_data)
        except IOError:
            self.error_handler.set_error_item(dict(new_image_path=new_image_path))


class ModelErrorHandler:

    def __init__(self, handler: Handler) -> None:
        self.handler = handler
        self.error_num = 0
        self.error_items = []

    def set_error_item(self, item: dict):
        self.error_num += 1
        self.error_items.append(item)
        

        
if __name__ == "__main__":
    pass