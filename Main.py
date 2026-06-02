from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union


# =====================================================================
# 1. OOP-ЗАВДАННЯ: КЛАСИ ТА СТРУКТУРА ДАНИХ
# =====================================================================


class Transport(ABC):
    """Абстрактний клас з атрибутами та абстрактним методом"""

    def __init__(self, route_number: str, departure: str):
        self.route_number = route_number
        self.departure = departure

    @abstractmethod
    def get_schedule(self) -> dict:
        """Абстрактний метод для отримання розкладу"""
        pass


class Bus(Transport):
    """Клас Автобус, що додає список зупинок (stops)"""

    def __init__(self, route_number: str, departure: str, stops: List[str]):
        super().__init__(route_number, departure)
        self.stops = stops

    def get_schedule(self) -> dict:
        return {
            "type": "Автобус",
            "route_number": self.route_number,
            "departure": self.departure,
            "stops": self.stops,
        }


class Train(Transport):
    """Клас Потяг, що додає станції (stations) та час у дорозі (travel_time_min)"""

    def __init__(
        self,
        route_number: str,
        departure: str,
        stations: List[str],
        travel_time_min: int,
    ):
        super().__init__(route_number, departure)
        self.stations = stations
        self.travel_time_min = travel_time_min

    def get_schedule(self) -> dict:
        return {
            "type": "Потяг",
            "route_number": self.route_number,
            "departure": self.departure,
            "stations": self.stations,
            "travel_time_min": self.travel_time_min,
        }


class Schedule:
    """Клас розкладу, що демонструє інкапсуляцію та поліморфізм"""

    def __init__(self):
        # Приватний словник для інкапсуляції маршрутів
        self.__routes: Dict[str, Transport] = {}

    def add_route(self, transport: Transport) -> None:
        """Додає маршрут у приватне сховище"""
        self.__routes[transport.route_number] = transport

    def find_route(self, route_number: str) -> Optional[Transport]:
        """Шукає маршрут за ключем-номером"""
        return self.__routes.get(route_number, None)

    def list_routes(self) -> List[dict]:
        """Поліморфний виклик get_schedule() для всіх об'єктів"""
        return [transport.get_schedule() for transport in self.__routes.values()]


# =====================================================================
# 2. ІНСТРУМЕНТ (TOOL) ДЛЯ AI-АГЕНТА
# =====================================================================


def get_transport_schedule(route_number: str) -> dict:
    """Функція-інструмент, яка створює систему розкладу та шукає потрібний рейс"""
    # Ініціалізація системи
    schedule_system = Schedule()

    # Заповнення системи заздалегідь визначеними маршрутами
    bus_1 = Bus(
        route_number="11А",
        departure="08:30",
        stops=["Центр", "Вул. Шевченка", "Автовокзал"],
    )
    bus_2 = Bus(
        route_number="52",
        departure="09:15",
        stops=["Залізничний вокзал", "Парк", "Лікарня"],
    )
    train_1 = Train(
        route_number="705К",
        departure="06:00",
        stations=["Київ-Пас.", "Львів", "Перемишль"],
        travel_time_min=420,
    )

    schedule_system.add_route(bus_1)
    schedule_system.add_route(bus_2)
    schedule_system.add_route(train_1)

    # Пошук маршруту за введеним номером
    route = schedule_system.find_route(route_number)

    # Повернення результату згідно з вимогами
    if route:
        schedule_data = route.get_schedule()
        schedule_data["found"] = True
        return schedule_data
    else:
        return {"found": False}


# =====================================================================
# 3. ДЕМОНСТРАЦІЯ ТА ІМІТАЦІЯ РОБОТИ AI-АГЕНТА
# =====================================================================


def ai_agent_respond(user_query: str, route_number: str):
    """Емуляція відповідей AI-агента українською мовою"""
    print(f"User: '{user_query}'")

    # Виклик інструменту агентом
    tool_result = get_transport_schedule(route_number)

    # Генерація фінальної відповіді на основі даних інструменту
    if tool_result["found"]:
        if tool_result["type"] == "Автобус":
            print(
                f"AI: Маршрут автобуса №{tool_result['route_number']} знайдено! "
                f"Він відправляється о {tool_result['departure']}. "
                f"Зупинки на шляху: {', '.join(tool_result['stops'])}.\n"
            )
        elif tool_result["type"] == "Потяг":
            print(
                f"AI: Розклад потяга №{tool_result['route_number']} успішно знайдено. "
                f"Час відправлення: {tool_result['departure']}. "
                f"Станції: {', '.join(tool_result['stations'])}. "
                f"Орієнтовний час у дорозі: {tool_result['travel_time_min']} хвилин.\n"
            )
    else:
        print(
            f"AI: На жаль, маршрут '{route_number}' не знайдено у нашій базі даних громадського транспорту.\n"
        )


# Виконання 3-х демонстраційних запитів користувача до агента
if __name__ == "__main__":
    print("--- ДЕМОНСТРАЦІЯ РОБОТИ AI-АГЕНТА (3 ЗАПИТИ) ---\n")

    # Запит 1 (Автобус)
    ai_agent_respond(
        "Підкажіть розклад автобуса 11А, де він зупиняється?", route_number="11А"
    )

    # Запит 2 (Потяг)
    ai_agent_respond(
        "Які станції проходить поїзд 705К та скільки часу займає подорож?",
        route_number="705К",
    )

    # Запит 3 (Неіснуючий рейс)
    ai_agent_respond(
        "Привіт! Мені треба розклад для маршруту №404, є такий?",
        route_number="404",
    )
