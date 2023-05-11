from datetime import date, timedelta
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


class Rental(db.Model):
    __tablename__ = 'rental'
    id = db.Column(db.Integer, primary_key=True)
    bookId = db.Column(db.Integer, nullable=False)
    clientId = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    startDate = db.Column(db.Date, nullable=False, default=date.today())
    endDate = db.Column(db.Date, nullable=False, default=date.today())


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publishmentYear = db.Column(db.Integer(), nullable=False)
    pages = db.Column(db.Integer(), nullable=False)


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    mail = db.Column(db.String(255), nullable=False)
    birthDate = db.Column(db.Integer(), nullable=False)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/books/")
def books():
    books = db.session.execute(db.select(Book).order_by(Book.title)).scalars()
    return render_template("Books.html", books=books)


@app.route("/clients/")
def clients():
    clients = db.session.execute(db.select(Client).order_by(Client.name)).scalars()
    return render_template("Clients.html", clients=clients)


@app.route("/books/Rentals/")
def rentals():
    rentals = [r for r in db.session.execute(db.select(Rental).order_by(Rental.id)).scalars()]
    books = [b for b in db.session.execute(db.select(Book).order_by(Book.title)).scalars()]
    clients = [c for c in db.session.execute(db.select(Client).order_by(Client.name)).scalars()]
    return render_template("Rentals.html", rentals=rentals, clients=clients, books=books)


@app.route("/books/Add")
def addBooks():
    return render_template("AddBook.html")


@app.route("/books/Rent")
def addRental():
    books = db.session.execute(db.select(Book).order_by(Book.title)).scalars()
    clients = db.session.execute(db.select(Client).order_by(Client.name)).scalars()
    return render_template("AddRental.html", clients=clients, books=books)


@app.route("/clients/Add")
def addClients():
    return render_template("AddClient.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        pages = request.form['pages']
        publishmentYear = request.form['publishmentYear']
        book = Book(
            title=title,
            author=author,
            publishmentYear=publishmentYear,
            pages=pages,
        )
        db.session.add(book)
        db.session.commit()
        return redirect("/books")
    return redirect("/books")


@app.route('/delete', methods=['POST'])
def delete_book():
    book_id = request.form['book_to_delete']
    Book.query.filter_by(id=book_id).delete()
    db.session.commit()
    return redirect('books')


@app.route("/add_client", methods=["GET", "POST"])
def add_client():
    if request.method == "POST":
        name = request.form['name']
        mail = request.form['mail']
        birthDate = request.form['birthDate']
        client = Client(
            name=name,
            mail=mail,
            birthDate=birthDate,
        )
        db.session.add(client)
        db.session.commit()
        return redirect("/clients")
    return redirect("/clients")


@app.route('/delete1', methods=['POST'])
def delete_client():
    client_id = request.form['client_to_delete']
    Client.query.filter_by(id=client_id).delete()
    db.session.commit()
    return redirect('/clients')


@app.route("/add_rental", methods=["GET", "POST"])
def add_rental():
    if request.method == "POST":
        client_id = request.form.get('clients_select')
        book_id = request.form.get('books_select')
        days = request.form['days']
        endDate = date.today() + timedelta(days=int(days))
        # Create rental object
        rental = Rental(
            bookId=book_id,
            clientId=client_id,
            duration=days,
            endDate=endDate,
        )

        # Add rental to the database
        db.session.add(rental)
        db.session.commit()
        return redirect('/books')
    return redirect('/books')


if __name__ == "__main__":
    app.run(port=5005, debug=True)
