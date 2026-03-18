import sqlite3
from datetime import datetime

DB_NAME = "expenses.db"


def create_connection():
    return sqlite3.connect(DB_NAME)


def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL
    )
    """)


def add_expense(cursor, conn):
    try:
        amount = float(input("Miktar: ").strip())
    except ValueError:
        print("Geçersiz sayı girdin.")
        return

    category = input("Kategori: ").strip()

    if not category:
        print("Kategori boş olamaz.")
        return

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
        (amount, category, date)
    )
    conn.commit()
    print("Harcama eklendi.")


def show_expenses(cursor):
    cursor.execute("SELECT id, amount, category, date FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()

    if not rows:
        print("Kayıt bulunamadı.")
        return

    print("\n--- Tüm Harcamalar ---")
    for row in rows:
        expense_id, amount, category, date = row
        print(f"ID: {expense_id} | Miktar: {amount} | Kategori: {category} | Tarih: {date}")


def total_expense(cursor):
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    print(f"Toplam harcama: {total}")


def filter_by_category(cursor):
    category = input("Filtrelemek istediğin kategori: ").strip()

    if not category:
        print("Kategori boş olamaz.")
        return

    cursor.execute(
        "SELECT id, amount, category, date FROM expenses WHERE category = ? ORDER BY date DESC",
        (category,)
    )
    rows = cursor.fetchall()

    if not rows:
        print("Bu kategoriye ait kayıt bulunamadı.")
        return

    print(f"\n--- '{category}' kategorisindeki harcamalar ---")
    for row in rows:
        expense_id, amount, category, date = row
        print(f"ID: {expense_id} | Miktar: {amount} | Kategori: {category} | Tarih: {date}")


def delete_expense(cursor, conn):
    try:
        expense_id = int(input("Silmek istediğin harcama ID: ").strip())
    except ValueError:
        print("Geçersiz ID girdin.")
        return

    cursor.execute("SELECT id FROM expenses WHERE id = ?", (expense_id,))
    row = cursor.fetchone()

    if row is None:
        print("Bu ID'ye sahip kayıt bulunamadı.")
        return

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    print("Kayıt silindi.")


def main():
    conn = create_connection()
    cursor = conn.cursor()
    create_table(cursor)

    while True:
        print("\n===== Harcama Takip Sistemi =====")
        print("1. Harcama ekle")
        print("2. Tüm harcamaları listele")
        print("3. Toplam harcamayı göster")
        print("4. Kategoriye göre filtrele")
        print("5. Harcama sil")
        print("6. Çıkış")

        choice = input("Seçimin: ").strip()

        if choice == "1":
            add_expense(cursor, conn)
        elif choice == "2":
            show_expenses(cursor)
        elif choice == "3":
            total_expense(cursor)
        elif choice == "4":
            filter_by_category(cursor)
        elif choice == "5":
            delete_expense(cursor, conn)
        elif choice == "6":
            print("Programdan çıkılıyor.")
            break
        else:
            print("Geçersiz seçim yaptın.")

    conn.close()


if __name__ == "__main__":
    main()