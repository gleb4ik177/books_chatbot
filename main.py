from src.postgres import print_books, value_of_attribute
from src.yagpt import response, answer_by_type
def main():
    print_books()
    book_number = input('Введите номер книжки: ')
    query = input('Введите запрос: ')
    question_type = response(query)
    answer_by_type(question_type, book_number)

if __name__ == "__main__":
    main()