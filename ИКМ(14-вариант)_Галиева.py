'''
Реализуйте с помощью двусвязного циклического списка следующую игру:
Ученики школы встают в круг. Один ученик пишет программу, генерирующую
случайное целое число из промежутка [–10;10]. Если выпало положительное
число, то отсчет ведется «по часовой стрелке», если отрицательное, то «против
часовой». Ученик, на котором остановился счет, не выбывает из круга, а делает
«доброе дело» и уровень его рейтинга увеличивается на 1. Следующий отсчет
начинается с ученика, стоящего в круге рядом с тем, который только что делал
«доброе дело», с правого (если отсчет ведется по часовой стрелке) или с левого
(против часовой). После того, как игра всем надоела, нужно вывести список
учеников в порядке невозрастания рейтинга. Если имеется несколько
учеников с одинаковым рейтингом, то их нужно выводить в том порядке, в
котором они поступили в список. Исходный список фамилий учеников для
игры находится в текстовом файле. В начале игры рейтинг каждого ученика
равен 0. Во время игры нужно выводить протокол: какое случайное число
выпало, какой ученик делал доброе дело и рейтинг ученика после совершения
доброго дела. Количество раундов игры вводится пользователем с
клавиатуры
'''



import random

# Класс, представляющий одного ученика в списке
class StudentNode:
    def __init__(self, name, order):
        self.name = name
        self.rating = 0
        self.prev = None
        self.next = None
        self.order = order # Порядок добавления для стабильной сортировки

# Класс кольцевого двусвязного списка для хранения учеников
class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None # Начало списка
        self.size = 0  # Количество учеников в списке

    # Метод добавления нового ученика в конец списка
    def append(self, name):
        new_node = StudentNode(name, self.size)  # Создаём новый узел с порядковым номером
        if self.head is None:
            # Если список пуст, новый узел указывает сам на себя (кольцо из одного элемента)
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            # Иначе вставляем новый узел в конец списка
            tail = self.head.prev
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self.head
            self.head.prev = new_node
        self.size += 1

    # Итератор для прохода по всем узлам списка
    def __iter__(self):
        if not self.head:
            return
        current = self.head
        for _ in range(self.size):
            yield current
            current = current.next

    # Метод для получения списка всех узлов
    def to_list(self):
        return list(self.__iter__())

# Класс для работы с файлом учеников: чтение и добавление новых фамилий
class StudentFileHandler:
    def __init__(self, filename):
        self.filename = filename  # Имя файла для хранения фамилий

    # Чтение учеников из файла и создание списка
    def read_students(self):
        students = CircularDoublyLinkedList()
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                for line in f:
                    name = line.strip()
                    if name:
                        students.append(name)
        except FileNotFoundError:
            print(f"Файл '{self.filename}' не найден. Будет создан новый файл при добавлении учеников.")
        except IOError as e:
            print(f"Ошибка при чтении файла '{self.filename}': {e}")
        return students

    # Добавление новых фамилий в файл с клавиатуры
    def add_students(self):
        print("Введите новые фамилии учеников для добавления в файл.")
        print("Для завершения ввода оставьте строку пустой и нажмите Enter.")
        try:
            with open(self.filename, 'a', encoding='utf-8') as f:
                while True:
                    try:
                        surname = input("Фамилия: ").strip()
                    except KeyboardInterrupt:
                        # Обработка прерывания ввода пользователем
                        print("\nВвод прерван пользователем.")
                        break
                    if surname == '':
                        # Пустая строка — выход из цикла ввода
                        break
                    f.write(surname + '\n')  # Записываем фамилию в файл
            print("Новые фамилии успешно добавлены в файл.\n")
        except IOError as e:
            print(f"Ошибка при записи в файл '{self.filename}': {e}")

# Класс, управляющий игрой
class Game:
    def __init__(self, students):
        self.students = students  # Кольцевой список учеников

    # Метод запуска игры на заданное количество раундов
    def play(self, rounds):
        if self.students.size == 0:
            print("Список учеников пуст.")
            return

        current = self.students.head  # Начинаем с головы списка

        for round_num in range(1, rounds + 1):
            # Генерируем случайный шаг от -10 до 10, исключая 0
            step = random.randint(-10, 10)
            while step == 0:
                step = random.randint(-10, 10)

            direction = "по часовой стрелке" if step > 0 else "против часовой стрелки"
            steps_count = abs(step)

            # Двигаемся по кругу на заданное количество шагов
            for _ in range(steps_count):
                current = current.next if step > 0 else current.prev

            # Ученик, на котором остановились, делает доброе дело — увеличиваем рейтинг
            current.rating += 1

            # Выводим информацию о раунде
            print(f"Раунд {round_num}: Выпало число {step} ({direction}). "
                  f"Ученик {current.name} сделал доброе дело. Рейтинг: {current.rating}")

            # Следующий отсчёт начинается с ученика рядом с current
            current = current.next if step > 0 else current.prev

    # Метод вывода отсортированного списка учеников по рейтингу
    def print_sorted_students(self):
        student_list = self.students.to_list()
        # Сортируем по рейтингу по убыванию, при равенстве — по порядку добавления
        student_list.sort(key=lambda s: (-s.rating, s.order))

        print("\nСписок учеников в порядке невозрастания рейтинга:")
        for s in student_list:
            print(f"{s.name}: {s.rating}")

# Класс для обработки ввода пользователя
class InputHandler:
    def get_positive_int(self, prompt):
        # Метод для безопасного ввода положительного целого числа
        while True:
            try:
                value = input(prompt)
                num = int(value)
                if num <= 0:
                    print("Пожалуйста, введите положительное число.")
                    continue
                return num
            except ValueError:
                print("Ошибка: введите целое число.")
            except KeyboardInterrupt:
                print("\nВвод прерван пользователем.")
                return None

# Главная функция программы
def main():
    filename = "students.txt"  # Имя файла с фамилиями учеников
    file_handler = StudentFileHandler(filename)

    # Сначала даём возможность добавить новых учеников в файл
    file_handler.add_students()

    # Читаем учеников из файла в кольцевой список
    students = file_handler.read_students()

    input_handler = InputHandler()
    rounds = input_handler.get_positive_int("Введите количество раундов игры: ")
    if rounds is None:
        # Если ввод прерван, завершаем программу
        return

    game = Game(students)
    print("\nНачинаем игру!\n")
    game.play(rounds)              # Запускаем игру
    game.print_sorted_students()  # Выводим результаты

if __name__ == "__main__":
    main()