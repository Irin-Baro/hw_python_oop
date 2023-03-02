from dataclasses import dataclass, asdict
from typing import ClassVar, Dict, Sequence, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    MESSAGE: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.'
                              )

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_H: ClassVar[int] = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод будет реализован в дочерних классах')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[int] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.MIN_IN_H
                )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 0.035
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 0.029
    M_IN_SEC: ClassVar[float] = 0.278
    СM_IN_M: ClassVar[int] = 100

    height: float

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.weight
                + ((self.get_mean_speed()
                 * self.M_IN_SEC) ** 2
                 / (self.height
                 / self.СM_IN_M))
                * self.CALORIES_MEAN_SPEED_SHIFT
                * self.weight)
                * self.duration
                * self.MIN_IN_H
                )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 1.1
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[int] = 2

    length_pool: float
    count_pool: float

    def get_mean_speed(self):
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration
                )

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                * self.CALORIES_MEAN_SPEED_SHIFT
                * self.weight
                * self.duration
                )


WORKOUT_TYPES: Dict[str, Type[Training]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: Sequence[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type in WORKOUT_TYPES:
        return WORKOUT_TYPES[workout_type](*data)
    raise ValueError('Неизвестный тип тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    info = InfoMessage.get_message(training.show_training_info())
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
