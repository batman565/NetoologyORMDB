import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from module import create_table, Publisher, Book, Shop, Sale, Stock


def find_publisher_sale(author):
    if author.isdigit():
        search_filter = Publisher.id == author
    else:
        search_filter = Publisher.name == author

    query = (session.query(Book.title, Shop.name, Sale.price, Sale.data_sale)
             .join(Publisher, Publisher.id == Book.id_publisher)
             .join(Stock, Stock.id_book == Book.id)
             .join(Shop, Stock.id_shop == Shop.id)
             .join(Sale, Sale.id_stock == Stock.id)
             .filter(search_filter)
             .all())
    for title, name, price, data_sale in query:
        print(f"{title} | {name} | {price} | {data_sale}")


def filling_tables():
    a = Publisher(name="Пушкин")
    b = Book(title="Капитанская дочка", id_publisher=1)
    c = Book(title="Евгений Онегин", id_publisher=1)
    d = Book(title="Письмо Татьяне", id_publisher=1)
    e = Shop(name="Буквоед")
    f = Shop(name="Читай город")
    g = Stock(id_book=1, id_shop=2, count=10)
    h = Stock(id_book=3, id_shop=1, count=5)
    r = Stock(id_book=2, id_shop=1, count=10)
    q = Sale(price=400.0, data_sale="09-12-2024", id_stock=1, count=3)
    w = Sale(price=600.0, data_sale="03-11-2024", id_stock=2, count=3)
    j = Sale(price=550.0, data_sale="02-12-2024", id_stock=3, count=3)
    session.add_all([a, b, c, d, e, f, g, h, r, q, w, j])
    session.commit()


DSN = "postgresql://postgres:12345@localhost:5432/NetologyDBROM"
engine = sq.create_engine(DSN)
create_table(engine)

if __name__ == "__main__":
    Session = sessionmaker(bind=engine)
    session = Session()
    publisher_name_or_id = input("Введите имя или идентификатор издателя: ")
    filling_tables()
    find_publisher_sale(publisher_name_or_id)

    session.close()
