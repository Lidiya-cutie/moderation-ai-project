import unittest
from ultralytics import YOLO

class TestYOLOModel(unittest.TestCase):
    def test_yolo_model_loading(self):
        # Проверка загрузки модели YOLO
        model = YOLO("data/models/yolo_apteka.pt")
        self.assertIsNotNone(model, "Модель YOLO не загружена")

    def test_yolo_prediction(self):
        # Проверка предсказания модели YOLO
        model = YOLO("data/models/yolo_apteka.pt")
        results = model.predict(source="data/images/test_image.jpg", conf=0.5)
        self.assertTrue(len(results) > 0, "Модель YOLO не вернула результаты")

if __name__ == "__main__":
    unittest.main()
