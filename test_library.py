import unittest
from main import Library  # Импортируем наш класс Library
from io import StringIO
import sys


class TestLibrary(unittest.TestCase):

    def setUp(self):
        """Устанавливаем начальные условия для тестов."""
        self.library = Library()
        self.library.library = []  # Очищаем библиотеку перед каждым тестом

    def test_add_book(self):
        """Тестирование добавления книги."""
        self.library.add_book("Test Title", "Test Author", 2021)
        self.assertEqual(len(self.library.library), 1)
        self.assertEqual(self.library.library[0]['title'], "Test Title")
        self.assertEqual(self.library.library[0]['author'], "Test Author")
        self.assertEqual(self.library.library[0]['year'], 2021)
        self.assertEqual(self.library.library[0]['status'], "в наличии")

    def test_delete_book(self):
        """Тестирование удаления книги."""
        self.library.add_book("Test Title", "Test Author", 2021)
        book_id = self.library.library[0]['id']
        self.library.delete_book(book_id)
        self.assertEqual(len(self.library.library), 0)

    def test_delete_nonexistent_book(self):
        """Тестирование удаления несуществующей книги."""
        self.library.delete_book(999)  # id, которого нет в библиотеке
        self.assertEqual(len(self.library.library), 0)  # Ожидаем, что библиотека пуста

    def test_search_books(self):
        """Тестирование поиска книг."""
        self.library.add_book("Test Title", "Test Author", 2021)
        self.library.add_book("Another Title", "Another Author", 2022)
        found_books = self.library.search_books("Test Title", "title")
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0]['title'], "Test Title")

    def test_display_books(self):
        """Тестирование отображения всех книг."""
        self.library.add_book("Test Title", "Test Author", 2021)
        self.library.add_book("Another Title", "Another Author", 2022)

        # Перенаправляем стандартный вывод в буфер
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            self.library.display_books()
            output = out.getvalue().strip()
            self.assertIn("ID:", output)
            self.assertIn("Название:", output)
        finally:
            sys.stdout = saved_stdout

    def test_update_status(self):
        """Тестирование изменения статуса книги."""
        self.library.add_book("Test Title", "Test Author", 2021)
        book_id = self.library.library[0]['id']
        self.library.update_status(book_id, "выдана")
        self.assertEqual(self.library.library[0]['status'], "выдана")

    def test_update_status_nonexistent_book(self):
        """Тестирование изменения статуса несуществующей книги."""
        self.library.update_status(999, "выдана")  # id, которого нет в библиотеке
        self.assertEqual(len(self.library.library), 0)  # Ожидаем, что библиотека пуста

if __name__ == '__main__':
    unittest.main()
