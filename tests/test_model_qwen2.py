import unittest
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from PIL import Image

class TestQwen2VLModel(unittest.TestCase):
    def test_qwen2vl_model_loading(self):
        # Проверка загрузки модели Qwen2VL
        model = Qwen2VLForConditionalGeneration.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")
        processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")
        self.assertIsNotNone(model, "Модель Qwen2VL не загружена")
        self.assertIsNotNone(processor, "Процессор Qwen2VL не загружен")

    def test_qwen2vl_prediction(self):
        # Проверка предсказания модели Qwen2VL
        model = Qwen2VLForConditionalGeneration.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")
        processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")
        image = Image.open("data/images/test_image.jpg")
        inputs = processor(image, return_tensors="pt")
        outputs = model.generate(**inputs, max_new_tokens=50)
        self.assertTrue(len(outputs) > 0, "Модель Qwen2VL не вернула результаты")

if __name__ == "__main__":
    unittest.main()
