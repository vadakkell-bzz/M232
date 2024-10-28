import sqlite3

class BooksDao:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_connection(self):
        """Stellt eine Verbindung zur SQLite-Datenbank her."""
        conn = sqlite3.connect(self.db_file)
        return conn

    def create_table(self):
        """Erstellt die Buch-Tabelle, falls sie nicht existiert."""
        conn = self.create_connection()
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER NOT NULL
                )
            ''')

    def add_book(self, title, author, year):
        """Fügt ein neues Buch zur Datenbank hinzu."""
        conn = self.create_connection()
        with conn:
            conn.execute('''
                INSERT INTO books (title, author, year)
                VALUES (?, ?, ?)
            ''', (title, author, year))

    def get_all_books(self):
        """Gibt alle Bücher aus der Datenbank zurück."""
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM books')
        return cur.fetchall()

    def search_books(self, query):
        """Gibt Bücher zurück, die dem Suchbegriff entsprechen."""
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM books WHERE title LIKE ?', ('%' + query + '%',))
        return cur.fetchall()

    def delete_book(self, book_id):
        """Löscht ein Buch anhand der ID."""
        conn = self.create_connection()
        with conn:
            conn.execute('DELETE FROM books WHERE id = ?', (book_id,))

    def get_book_by_id(self, book_id):
        """Holt ein Buch anhand der ID aus der Datenbank."""
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        return cur.fetchone()

    def update_book(self, book_id, title, author, year):
        """Aktualisiert die Daten eines Buches anhand der ID."""
        conn = self.create_connection()
        with conn:
            conn.execute('''
                UPDATE books
                SET title = ?, author = ?, year = ?
                WHERE id = ?
            ''', (title, author, year, book_id))
