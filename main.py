import json
import os
from typing import List, Dict


class Library:
    LIBRARY_FILE = 'library.json'

    def __init__(self):
        self.library = self.load_library()

    def load_library(self) -> List[Dict]:
        """
        Загружает данные из файла библиотеки.

        Returns:
            list: Список книг, загруженных из файла.
        """
        if os.path.exists(self.LIBRARY_FILE):
            try:
                with open(self.LIBRARY_FILE, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Ошибка: поврежден файл библиотеки.")
                return []
        return []

    def save_library(self) -> None:
        """
        Сохраняет данные в файл библиотеки.
        """
        with open(self.LIBRARY_FILE, 'w') as file:
            json.dump(self.library, file, indent=4)

    def add_book(self, title: str, author: str, year: int) -> None:
        """
        Добавляет книгу в библиотеку.

        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
        """
        book_id = max([book['id'] for book in self.library], default=0) + 1
        new_book = {
            'id': book_id,
            'title': title,
            'author': author,
            'year': year,
            'status': 'в наличии'
        }
        self.library.append(new_book)
        self.save_library()
        print(f"Книга '{title}' добавлена в библиотеку.")

    def delete_book(self, book_id: int) -> None:
        """
        Удаляет книгу из библиотеки по её id.

        Args:
            book_id (int): Уникальный идентификатор книги.
        """
        book_to_delete = next((book for book in self.library if book['id'] == book_id), None)
        if book_to_delete:
            self.library.remove(book_to_delete)
            self.save_library()
            print(f"Книга с id {book_id} удалена из библиотеки.")
        else:
            print(f"Книга с id {book_id} не найдена.")

    def search_books(self, query: str, field: str) -> List[Dict]:
        """
        Ищет книги по указанному полю и возвращает список найденных книг.

        Args:
            query (str): Строка поиска.
            field (str): Поле, по которому выполняется поиск ('title', 'author', 'year').

        Returns:
            list: Список найденных книг.
        """
        found_books = [book for book in self.library if query.lower() in str(book[field]).lower()]
        return found_books

    def display_books(self) -> None:
        """
        Отображает список всех книг в библиотеке.
        """
        if self.library:
            for book in self.library:
                print(
                    f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, Год: {book['year']}, Статус: {book['status']}")
        else:
            print("В библиотеке нет книг.")

    def update_status(self, book_id: int, status: str) -> None:
        """
        Изменяет статус книги в библиотеке.

        Args:
            book_id (int): Уникальный идентификатор книги.
            status (str): Новый статус книги ('в наличии' или 'выдана').
        """
        book_to_update = next((book for book in self.library if book['id'] == book_id), None)
        if book_to_update:
            book_to_update['status'] = status
            self.save_library()
            print(f"Статус книги с id {book_id} обновлен на '{status}'.")
        else:
            print(f"Книга с id {book_id} не найдена.")


def main() -> None:
    """
    Главная функция, запускающая интерфейс командной строки для управления библиотекой.
    """
    library = Library()
    print("Система управления библиотекой запущена.")

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отображение всех книг")
        print("5. Изменение статуса книги")
        print("6. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания книги: "))
            library.add_book(title, author, year)
        elif choice == '2':
            try:
                book_id = int(input("Введите id книги, которую нужно удалить: "))
                library.delete_book(book_id)
            except ValueError:
                print("Ошибка: id книги должен быть числом.")
        elif choice == '3':
            search_field = input("Введите поле для поиска (title, author, year): ")
            search_query = input("Введите запрос для поиска: ")
            found_books = library.search_books(search_query, search_field)
            print("Найденные книги:")
            for book in found_books:
                print(book)
        elif choice == '4':
            print("Список всех книг в библиотеке:")
            library.display_books()
        elif choice == '5':
            try:
                book_id = int(input("Введите id книги: "))
                status = input("Введите новый статус (в наличии или выдана): ")
                library.update_status(book_id, status)
            except ValueError:
                print("Ошибка: id книги должен быть числом.")
        elif choice == '6':
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
