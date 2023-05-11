import os
import hashlib
import json
import random


class ImageProcesser:

    def __init__(self, user_uploads, user_results_images, user_results_reports) -> None:
        self.user_uploads = user_uploads
        self.user_results_images = user_results_images
        self.user_results_reports = user_results_reports

    def _process_image(self, image_path):

        with open(image_path, 'rb') as f:
            image_data = f.read()

        image_name = os.path.basename(image_path)
        image_format = str(image_name).split('.')[1]
        image_hash = hashlib.sha256(image_data).hexdigest()
        position = random.randint(1, 10)
        error1 = random.randint(0, 3)
        error2 = random.randint(0, 3)
        new_image_name = f"{image_hash}.{image_format}"

        if error1 == 0 and error2 == 0:
            status = True
        else:
            status = False        

        if status:
            output_path = os.path.join(self.user_results_images, f"ok\\{new_image_name}")
        else:
            output_path = os.path.join(self.user_results_images, f"error\\{new_image_name}")

        with open(output_path, 'wb') as f:
            f.write(image_data)

        message = {
            "position": position,
            "error1": error1,
            "error2": error2,
            "status": status,
            "image_hash": image_hash,
            "image_name": image_name,
            "new_image_name": new_image_name
        }

        return message
    
    def _save(self, filename, data):

        with open(filename, 'w') as f:
            json.dump(data, f)

    def process(self):
        image_names = os.listdir(self.user_uploads)
        for image_name in image_names:
            image_path = os.path.join(self.user_uploads, image_name)
            message = self._process_image(image_path)
            resport_name = f"{message['image_hash']}.json"
            status = message['status']

            if status:
                output_path = os.path.join(self.user_results_reports, f"ok\\{resport_name}")
            else:
                output_path = os.path.join(self.user_results_reports, f"error\\{resport_name}")

            self._save(output_path, message)