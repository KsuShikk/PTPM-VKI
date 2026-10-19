import unittest
from src.Delivery import calculate_delivery_cost


class TestDelivery(unittest.TestCase):

    # 1. Проверка обычной доставки
    def test_calculate_standard_delivery(self):
        result = calculate_delivery_cost(2.0, 100, "обычный")
        self.assertEqual(result, (700, "2026-09-04"))

    # 2. Проверка минимально допустимого веса
    def test_calculate_delivery_with_minimum_weight(self):
        result = calculate_delivery_cost(0.1, 100, "обычный")
        self.assertEqual(result, (700, "2026-09-04"))

    # 3. Проверка веса ниже допустимого
    def test_reject_weight_below_minimum(self):
        result = calculate_delivery_cost(0.09, 100, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    # 4. Проверка веса выше допустимого
    def test_reject_weight_above_maximum(self):
        result = calculate_delivery_cost(50.1, 100, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    # 5. Проверка расстояния ниже допустимого
    def test_reject_distance_below_minimum(self):
        result = calculate_delivery_cost(2.0, 0, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    # 6. Проверка расстояния выше допустимого
    def test_reject_distance_above_maximum(self):
        result = calculate_delivery_cost(2.0, 5001, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    # 7. Проверка хрупкой посылки
    def test_calculate_fragile_package(self):
        result = calculate_delivery_cost(2.0, 100, "хрупкий")
        self.assertEqual(result, (1000, "2026-09-04"))

    # 8. Проверка опасной посылки
    def test_calculate_dangerous_package(self):
        result = calculate_delivery_cost(2.0, 100, "опасный")
        self.assertEqual(result, (1700, "2026-09-04"))

    # 9. Проверка экспресс-доставки
    # def test_calculate_express_delivery(self):
    #     result = calculate_delivery_cost(2.0, 100, "обычный", True)
    #     self.assertEqual(result, (350, "2026-09-04"))

    # 10. Проверка недопустимого типа посылки
    def test_reject_invalid_package_type(self):
        result = calculate_delivery_cost(2.0, 100, "нестандартный")
        self.assertEqual(result, (-1, "0000-00-00"))


if __name__ == "__main__":
    unittest.main()