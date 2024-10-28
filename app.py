from flask import Flask, render_template, request, redirect, url_for
from forms import BookForm
from books_dao import BooksDao

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

book_dao = BooksDao('books.db')
book_dao.create_table()

# Hauptseite
@app.route('/')
def index():
    return render_template('index.html')

# Seite zum Hinzufügen von Büchern
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        book_dao.add_book(form.title.data, form.author.data, form.year.data)
        return redirect(url_for('view_books'))
    return render_template('add_book.html', form=form)

# Neue Route: Seite zur Suche von Büchern
@app.route('/search', methods=['POST'])
def search_books():
    query = request.form.get('query')
    books = book_dao.search_books(query)
    # Rückgabe der Bücher zusammen mit dem Suchstatus
    return render_template('view_books.html', books=books, search_active=True)

# Hauptseite zum Anzeigen aller Bücher
@app.route('/books')
def view_books():
    books = book_dao.get_all_books()
    return render_template('view_books.html', books=books, search_active=False)

# Seite zum Bearbeiten eines Buches
@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = book_dao.get_book_by_id(book_id)
    if book is None:
        return redirect(url_for('view_books'))

    form = BookForm(data={'title': book[1], 'author': book[2], 'year': book[3]})
    if form.validate_on_submit():
        book_dao.update_book(book_id, form.title.data, form.author.data, form.year.data)
        return redirect(url_for('view_books'))
    return render_template('edit_book.html', form=form, book_id=book_id)

# Route zum Löschen eines Buches
@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book_dao.delete_book(book_id)
    return redirect(url_for('view_books'))

if __name__ == '__main__':
    app.run(debug=True)
