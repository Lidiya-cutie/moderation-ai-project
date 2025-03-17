import unittest
import time
from scripts.process_images import process_image

class TestPerformance(unittest.TestCase):
    def test_processing_time(self):
        # Проверка времени обработки 10 000 макетов
        start_time = time.time()
        for _ in range(10000):
            process_image("data/images/test_image.jpg")
        end_time = time.time()
        total_time = end_time - start_time
        self.assertLessEqual(total_time, 600, "Время обработки 10 000 макетов превышает 10 минут")

if __name__ == "__main__":
    unittest.main()
