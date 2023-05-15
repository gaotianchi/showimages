"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

import hashlib
import json
import os
import random

from PIL import Image




class ImageHandler:

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
                "image_name": image_name,
                "file_size": file_size,
                "image_format": image_format,
                "image_size": image_size,
                "image_hash": image_hash
            }
        except IOError:
            print(f"无法打开图片: {image_name} !")
            return None
        

class ImageProcessor:

    handler = ImageHandler()

    def __init__(self, from_image_dir, output_image_dir, output_report_dir) -> None:
        self.from_image_dir = from_image_dir
        self.output_image_dir = output_image_dir
        self.output_report_dir = output_report_dir

    def process(self):
        image_names = os.listdir(self.from_image_dir)
        for image_name in image_names:
            image_path = os.path.join(self.from_image_dir, image_name)

            try:
                self._process_image(image_path)
            except:
                print(f"无法处理图片：{image_name}")

    def _process_image(self, image_path):

        self.handler.set_image_path(image_path)

        image_data = self.handler.get_image_data()
        image_info = self.handler.get_image_info()

        # 在这里处理图片二进制数据并返回处理过后的二进制数据
        # 现在假设已经对图片做过了处理，并得到了新的图片数据以及分析结果
        # 其中分析结果用随机数据代替

        featureless_image_dir = os.path.join(self.output_image_dir, "featureless")
        featureless_report_dir  = os.path.join(self.output_report_dir, "featureless")
        feature_image_dir  = os.path.join(self.output_image_dir, "feature")
        feature_report_dir  = os.path.join(self.output_report_dir, "feature")

        for i in (featureless_image_dir, featureless_report_dir, feature_image_dir, feature_report_dir):
            if not os.path.exists(i):
                os.makedirs(i)

        # 处理过后的图片数据
        new_image_data = image_data
        new_image_name = image_info["image_hash"] + "." + image_info["image_format"]
        report_name = image_info["image_hash"] + ".json"

        # 处理的结果报告
        # 一般信息
        general_1 = random.randint(1, 10)
        general_2 = random.randint(1, 10)
        
        # 特征信息
        feature_1 = random.choice([True, False])

        # 将报告以字典的形式储存
        report_message = dict(general_1=general_1, general_2=general_2, feature_1=feature_1, image_hash=image_info["image_hash"])
        
        if feature_1:
            image_output_path = os.path.join(featureless_image_dir, new_image_name)
            report_output_path = os.path.join(featureless_report_dir, report_name)
        else:
            image_output_path = os.path.join(feature_image_dir, new_image_name)
            report_output_path = os.path.join(feature_report_dir, report_name)

        
        try:
            with open(image_output_path, "wb") as image:
                image.write(new_image_data)
            
            with open(report_output_path, "w") as report:
                json.dump(report_message, report)

        except IOError:
            print(f"保存文件失败：{new_image_name}")

        
if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    from_image_dir = os.path.join(basedir, "test1")
    output_image_dir = os.path.join(basedir, "test2")
    output_report_dir = os.path.join(basedir, "test3")

    processor = ImageProcessor(from_image_dir, output_image_dir, output_report_dir)
    processor.process()