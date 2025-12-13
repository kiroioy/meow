from abc import ABC, abstractmethod
from typing import List

class Animal(ABC):
    def __init__(self, name: str):
        self.name = name
    @abstractmethod
    def make_sound(self):
        pass

    def eat(self, food: 'Feed'):
        print(f"{self.name} ест {food.name}")

class Cow(Animal):
    def make_sound(self):
        print(f"{self.name} говорит: Мууу!")

class Chicken(Animal):
    def make_sound(self):
        print(f"{self.name} говорит: Ко-ко-ко!")

class Feed(ABC):
    def __init__(self, name: str, nutrition: int):
        self.name = name
        self.nutrition = nutrition
    @abstractmethod
    def display_info(self):
        pass

class Hay(Feed):
    def __init__(self):
        super().__init__("сено", nutrition=15)
    def display_info(self):
        print(f"{self.name} (пищ. ценность: {self.nutrition}) - подходит для коров")

class Grain(Feed):
    def __init__(self):
        super().__init__("зерно", nutrition=8)

    def display_info(self):
        print(f"{self.name} (пищ. ценность: {self.nutrition}) - подходит для кур")

class FarmFactory(ABC):
    "абстрактная фабрика для создания связанных объектов фермы"
    @abstractmethod
    def create_animal(self, name: str) -> Animal:
        pass
    @abstractmethod
    def create_feed(self) -> Feed:
        pass

class CowFarmFactory(FarmFactory):
    "фабрика для создания объектов, связанных с коровами"
    def create_animal(self, name: str) -> Animal:
        return Cow(name)

    def create_feed(self) -> Feed:
        return Hay()

class ChickenFarmFactory(FarmFactory):
    "фабрика для создания объектов, связанных с курами"
    def create_animal(self, name: str) -> Animal:
        return Chicken(name)

    def create_feed(self) -> Feed:
        return Grain()

class Building:
    def __init__(self, building_type: str):
        self.type = building_type
    def display_info(self):
        print(f"Постройка типа: {self.type}")

class Staff:
    def __init__(self, role: str):
        self.role = role
    def work(self):
        print(f"{self.role} работает на ферме")


class Farm:
    def __init__(self):
        self.animals: List[Animal] = []
        self.feed_supply: List[Feed] = []
        self.buildings: List[Building] = []
        self.staff: List[Staff] = []
    def add_animal(self, animal: Animal):
        self.animals.append(animal)
    def add_feed(self, feed: Feed):
        self.feed_supply.append(feed)
    def add_building(self, building: Building):
        self.buildings.append(building)
    def add_staff(self, worker: Staff):
        self.staff.append(worker)
    def feed_animals(self):
        print("\nКормление животных")
        for animal in self.animals:
            for feed in self.feed_supply:
                if (isinstance(animal, Cow) and isinstance(feed, Hay)) or \
                        (isinstance(animal, Chicken) and isinstance(feed, Grain)):
                    animal.eat(feed)
                    break

    def info_farm(self):
        print("информация о ферме")
        print("\nЖивотные:")
        for animal in self.animals:
            animal.make_sound()
        print("\nЗапасы корма:")
        for feed in self.feed_supply:
            feed.display_info()
        print("\nПостройки:")
        for building in self.buildings:
            building.display_info()
        print("\nПерсонал:")
        for worker in self.staff:
            worker.work()

def main():
    my_farm = Farm()
    cow_factory = CowFarmFactory()
    chicken_factory = ChickenFarmFactory()
    print("Добавляем корову и её корм:")
    cow = cow_factory.create_animal("Бурёнка")
    cow_feed = cow_factory.create_feed()
    my_farm.add_animal(cow)
    my_farm.add_feed(cow_feed)
    print(f"Создана корова: {cow.name}")
    print(f"Создан корм: {cow_feed.name}")
    print("\nДобавляем курицу и её корм:")
    chicken = chicken_factory.create_animal("Ряба")
    chicken_feed = chicken_factory.create_feed()
    my_farm.add_animal(chicken)
    my_farm.add_feed(chicken_feed)
    print(f"Создана курица: {chicken.name}")
    print(f"Создан корм: {chicken_feed.name}")
    print("\nДобавляем ещё одну корову:")
    cow2 = cow_factory.create_animal("Зорька")
    cow_feed2 = cow_factory.create_feed()
    my_farm.add_animal(cow2)
    my_farm.add_feed(cow_feed2)
    print(f"Создана корова: {cow2.name}")
    print(f"Создан корм: {cow_feed2.name}")
    print("\nДобавляем постройки:")
    my_farm.add_building(Building("Сарай для коров"))
    print("  Добавлен: Сарай для коров")
    my_farm.add_building(Building("Курятник"))
    print("  Добавлен: Курятник")
    my_farm.add_building(Building("Склад кормов"))
    print("  Добавлен: Склад кормов")
    print("\nДобавляем персонал:")
    my_farm.add_staff(Staff("Фермер"))
    print("  Найман: Фермер")
    my_farm.add_staff(Staff("Ветеринар"))
    print("  Найман: Ветеринар")
    my_farm.add_staff(Staff("Доярка"))
    print("  Найман: Доярка")
    my_farm.info_farm()
    my_farm.feed_animals()
if __name__ == "__main__":
    main()

