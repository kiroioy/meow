import unittest
import meow2

class TestMeow2Functions(unittest.TestCase):
    def test_task_a1_sorted_by_producer(self):
        """A1: список должен быть отсортирован по производителю"""
        result = meow2.task_a1(meow2.producers, meow2.details)
        producers_list = [p for _, _, p in result]
        self.assertEqual(producers_list, sorted(producers_list))

    def test_task_a2_sum_for_zavod_detalei(self):
        """A2: проверяем суммарную стоимость для 'Завод деталей'"""
        result = meow2.task_a2(meow2.producers, meow2.details)
        target = next(r for r in result if r[0] == "Завод деталей")
        # 10+8=18
        self.assertEqual(target[1], 18)

    def test_task_a3_only_zavod(self):
        """A3: должны быть выбраны только производители, содержащие слово 'завод'"""
        result = meow2.task_a3(meow2.producers, meow2.details, meow2.details_producers)
        expected = {
            "Завод деталей",
            "Машиностроительный завод",
            "Завод МеталлПром",
        }
        self.assertEqual(set(result.keys()), expected)
    def test_task_a3_details_not_empty(self):
        """A3: у каждого завода должен быть хотя бы один элемент"""
        result = meow2.task_a3(meow2.producers, meow2.details, meow2.details_producers)
        for key, detail_list in result.items():
            self.assertGreater(len(detail_list), 0)

if __name__ == "__main__":
    unittest.main()