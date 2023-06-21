from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from tables import *

app = Flask(__name__)

# Konfiguracja połączenia do bazy danych
username = 'root'
password = ''
hostname = 'localhost'
port = 3306
database_name = 'cinema_db'
DATABASE_URI = f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database_name}'

# Utworzenie silnika bazy danych
engine = create_engine(DATABASE_URI)

# Utworzenie sesji
Session = sessionmaker(bind=engine)
session = Session()

ticket_prices = {
    "normal": 30,
    "child": 10,
    "student": 18
}

@app.route('/')
def main():
    return render_template('main_page.html')

@app.route('/worker')
def worker():
    return render_template('worker.html')

@app.route('/clients')
def clients():
    # Pobieranie wszystkich klientów
    clients = session.query(Client).all()
    
    # Przygotowanie danych klientów
    clients_data = []
    for client in clients:
        clients_data.append({
            'id_client': client.id_client,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'email': client.email,
            'type': client.type
        })

    # Zamknięcie sesji
    session.close()

    # Renderowanie szablonu z danymi
    return render_template('clients.html', clients=clients_data)

@app.route('/delete-client/<client_id>', methods=['DELETE'])
def delete_client(client_id):
    try:
        # Pobranie klienta o określonym ID z bazy danych
        client = session.query(Client).filter_by(id_client=client_id).first()

        if client:
            # Znalezienie wszystkich transakcji powiązanych z klientem
            transactions = session.query(Transaction).filter_by(id_client=client.id_client).all()

            # Iteracja przez transakcje i usunięcie powiązanych biletów
            for transaction in transactions:
                tickets = session.query(Ticket).filter_by(id_transaction=transaction.id_transaction).all()

                # Iteracja przez bilety i usunięcie
                for ticket in tickets:
                    session.delete(ticket)

                # Usunięcie transakcji
                session.delete(transaction)

            # Usunięcie klienta
            session.delete(client)
            session.commit()
            session.close()
            return {'message': 'Klient został pomyślnie usunięty wraz z powiązanymi biletami i transakcjami.'}
        else:
            return {'error': 'Nie znaleziono klienta o podanym ID.'}
    except IntegrityError:
        session.rollback()
        return {'error': 'Wystąpił błąd podczas usuwania klienta. Sprawdź, czy nie ma żadnych powiązanych rekordów.'}


@app.route('/movies')
def movies():
    # Pobieranie wszystkich filmów
    movies = session.query(Movie).all()
    movies_data = []
    for movie in movies:
        movies_data.append({
            'id_movie': movie.id_movie,
            'title': movie.title,
            'year_of_prod': movie.year_of_prod,
            'director': movie.director,
            'country': movie.country,
            'duration': movie.duration,
            'language': movie.language,
            'dimension': movie.dimension
        })

    # Zamknięcie sesji
    session.close()

    # Renderowanie szablonu z danymi
    return render_template('movies.html', movies=movies_data)

@app.route('/delete-movie/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    try:
        # Pobranie filmu o określonym ID z bazy danych
        movie = session.query(Movie).filter_by(id_movie=movie_id).first()

        if movie:
            # Znalezienie wszystkich seansów powiązanych z filmem
            shows = session.query(Show).filter_by(id_movie=movie.id_movie).all()

            # Iteracja przez seanse i usunięcie powiązanych biletów
            for show in shows:
                tickets = session.query(Ticket).filter_by(id_show=show.id_show).all()

                # Iteracja przez bilety i usunięcie
                for ticket in tickets:
                    session.delete(ticket)

                # Usunięcie seansu
                session.delete(show)

            # Usunięcie filmu
            session.delete(movie)
            session.commit()
            session.close()
            return {'message': 'Film został pomyślnie usunięty wraz z powiązanymi seansami i biletami.'}
        else:
            return {'error': 'Nie znaleziono filmu o podanym ID.'}
    except IntegrityError:
        session.rollback()
        return {'error': 'Wystąpił błąd podczas usuwania filmu. Sprawdź, czy nie ma żadnych powiązanych rekordów.'}





@app.route('/shows')
def shows():
    # Wykonanie złączenia (join) pomiędzy tabelami 'show', 'movie' i 'room'
    shows = session.query(Show, Movie, Room).join(Movie, Show.id_movie == Movie.id_movie).join(Room, Show.id_room == Room.id_room).all()

    # Przygotowanie danych seansów
    shows_data = []
    for show, movie, room in shows:
        shows_data.append({
            'id_show': show.id_show,
            'title': movie.title,
            'director': movie.director,
            'year_of_prod': movie.year_of_prod,
            'date': show.date,
            'time': show.time,
            'room': room.id_room  # Zakładam, że nazwa sali znajduje się w polu 'name' encji Room
        })

    # Zamknięcie sesji
    session.close()

    # Renderowanie szablonu z danymi
    return render_template('shows.html', shows=shows_data)

@app.route('/delete-show/<show_id>', methods=['DELETE'])
def delete_show(show_id):
    try:
        # Pobranie seansu o określonym ID z bazy danych
        show = session.query(Show).filter_by(id_show=show_id).first()

        if show:
            # Znalezienie wszystkich biletów powiązanych z danym seansem
            tickets = session.query(Ticket).filter_by(id_show=show.id_show).all()

            # Iteracja przez bilety i usunięcie
            for ticket in tickets:
                session.delete(ticket)

            # Usunięcie seansu
            session.delete(show)
            session.commit()
            session.close()
            return {'message': 'Seans został pomyślnie usunięty wraz z powiązanymi biletami.'}
        else:
            return {'error': 'Nie znaleziono seansu o podanym ID.'}
    except IntegrityError:
        session.rollback()
        return {'error': 'Wystąpił błąd podczas usuwania seansu. Sprawdź, czy nie ma żadnych powiązanych rekordów.'}



@app.route('/transactions')
def transactions():
    # Wykonanie złączenia (join) pomiędzy tabelami 'transaction' i 'client'
    transactions = session.query(Transaction, Client).join(Client, Transaction.id_client == Client.id_client).all()

    # Przygotowanie danych transakcji
    transactions_data = []
    for transaction, client in transactions:
        transactions_data.append({
            'id_transaction': transaction.id_transaction,
            'id_client': transaction.id_client,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'email': client.email,
            'date': transaction.date,
            'amount': transaction.amount,
            'currency': transaction.currency,
            'status': transaction.status,
            'pay_method': transaction.pay_method
        })

    # Zamknięcie sesji
    session.close()

    # Renderowanie szablonu z danymi
    return render_template('transactions.html', transactions=transactions_data)

@app.route('/delete-transaction/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    try:
        # Pobranie transakcji o określonym ID z bazy danych
        transaction = session.query(Transaction).filter_by(id_transaction=transaction_id).first()

        if transaction:
            # Znalezienie wszystkich biletów powiązanych z daną transakcją
            tickets = session.query(Ticket).filter_by(id_transaction=transaction.id_transaction).all()

            # Iteracja przez bilety i usunięcie
            for ticket in tickets:
                session.delete(ticket)

            # Usunięcie transakcji
            session.delete(transaction)
            session.commit()
            session.close()
            return {'message': 'Transakcja została pomyślnie usunięta wraz z powiązanymi biletami.'}
        else:
            return {'error': 'Nie znaleziono transakcji o podanym ID.'}
    except IntegrityError:
        session.rollback()
        return {'error': 'Wystąpił błąd podczas usuwania transakcji. Sprawdź, czy nie ma żadnych powiązanych rekordów.'}



@app.route('/tickets')
def tickets():
    # Wykonanie złączenia (join) pomiędzy tabelami 'ticket', 'transaction' i 'show'
    #tickets = session.query(Ticket, Transaction, Show, Movie).join(Transaction).join(Show).join(Movie).all()
    tickets = session.query(Ticket, Transaction, Show, Movie).join(Transaction).join(Show).join(Movie).filter(Transaction.status == 'completed').all()


    # Przygotowanie danych biletów
    tickets_data = []
    for ticket, transaction, show, movie in tickets:
        tickets_data.append({
            'id_ticket': ticket.id_ticket,
            'id_transaction': ticket.id_transaction,
            'id_room': show.id_room,
            'row': ticket.row,
            'seat': ticket.seat,
            'movie_title': movie.title,
            'date': show.date,
            'time': show.time
        })

    # Zamknięcie sesji
    session.close()

    # Renderowanie szablonu z danymi
    return render_template('tickets.html', tickets=tickets_data)


@app.route('/sell-ticket-reserved')
def tickets_reserved():
    # Wykonanie złączenia (join) pomiędzy tabelami 'ticket', 'transaction' i 'show'
    tickets = session.query(Ticket, Transaction, Show, Movie).join(Transaction).join(Show).join(Movie).filter(Transaction.status == 'pending').all()

    # Przygotowanie danych biletów
    tickets_data = []
    for ticket, transaction, show, movie in tickets:
        tickets_data.append({
            'id_ticket': ticket.id_ticket,
            'id_transaction': ticket.id_transaction,
            'id_room': show.id_room,
            'row': ticket.row,
            'seat': ticket.seat,
            'status': transaction.status,
            'movie_title': movie.title,
            'date': show.date,
            'time': show.time
        })

    # Zamknięcie sesji
    session.close()

    # Renderowanie szablonu z danymi
    return render_template('tickets_reserved.html', tickets=tickets_data)


@app.route('/delete-ticket/<ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    try:
        # Pobranie biletu o określonym ID z bazy danych
        ticket = session.query(Ticket).filter_by(id_ticket=ticket_id).first()

        if ticket:
            # Usunięcie biletu
            session.delete(ticket)
            session.commit()
            session.close()
            return {'message': 'Bilet został pomyślnie usunięty.'}
        else:
            return {'error': 'Nie znaleziono biletu o podanym ID.'}
    except IntegrityError:
        session.rollback()
        return {'error': 'Wystąpił błąd podczas usuwania biletu. Sprawdź, czy nie ma żadnych powiązanych rekordów.'}


@app.route('/pending-to-completed-ticket/<ticket_id>', methods=['GET'])
def update_ticket_status(ticket_id):
    try:
        # Pobranie biletu o określonym ID z bazy danych
        ticket = session.query(Ticket).filter_by(id_ticket=ticket_id).first()

        if ticket:
            transaction = ticket.transaction  # Pobranie powiązanej transakcji
            transaction.status = "completed"  # Aktualizacja statusu transakcji
            session.commit()  # Zapisanie zmian w bazie danych
            session.close()
            return {'message': 'Status biletu został pomyślnie zmieniony na "completed".'}
        else:
            return {'error': 'Nie znaleziono biletu o podanym ID.'}
    except Exception as e:
        session.rollback()
        return {'error': 'Wystąpił błąd podczas zmiany statusu biletu: {}'.format(str(e))}




@app.route('/add-client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        client_type = request.form['client_type']

        # Tworzenie nowego klienta
        new_client = Client(first_name=first_name, last_name=last_name, email=email, type=client_type)

        # Dodawanie klienta do bazy danych
        session.add(new_client)
        session.commit()

        return 'Klient został dodany do bazy danych.'

    return render_template('add_client.html')


@app.route('/add-movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        # Pobieranie danych z formularza
        title = request.form['title']
        director = request.form['director']
        year_of_prod = int(request.form['year_of_prod'])
        country = request.form['country']
        duration = int(request.form['duration'])
        language = request.form['language']
        dimension = request.form['dimension']

        # Tworzenie nowego obiektu Movie
        new_movie = Movie(title=title, director=director, year_of_prod=year_of_prod, country=country,
                          duration=duration, language=language, dimension=dimension)

        # Dodawanie filmu do bazy danych
        session.add(new_movie)
        session.commit()

        return 'Film został dodany do bazy danych.'
    
    return render_template('add_movie.html')

@app.route('/add-show', methods=['GET', 'POST'])
def add_show():
    if request.method == 'POST':
        # Pobieranie danych z formularza
        movie_id = int(request.form['movie'])
        room_id = int(request.form['room'])
        date = request.form['date']
        time = request.form['time']

        # Pobieranie filmu na podstawie wybranego ID
        movie = session.query(Movie).get(movie_id)

        # Pobieranie sali na podstawie wybranego ID
        room = session.query(Room).get(room_id)

        # Tworzenie nowego obiektu Show
        new_show = Show(id_movie=movie_id, id_room=room_id, date=date, time=time)

        # Dodawanie seansu do bazy danych
        session.add(new_show)
        session.commit()

        return "Seans został dodany do bazy danych"

    # Pobieranie listy filmów dla rozwijanej listy w formularzu
    movies = session.query(Movie).all()
    rooms = session.query(Room).all()

    return render_template('add_show.html', movies=movies, rooms=rooms)


def check_seat_availability(room_id, row, seat):
    try:
        room = session.query(Room).filter_by(id_room=room_id).first()

        if room:
            if int(row) <= room.num_of_rows and int(seat) <= room.seats_per_row:
                return True, room.num_of_rows, room.seats_per_row
            else:
                return False, room.num_of_rows, room.seats_per_row
        else:
            return False, None, None
    except Exception as e:
        # Obsługa błędu
        return False, None, None


@app.route('/sell-ticket', methods=['GET', 'POST'])
def sellticket():
    if request.method == 'POST':
        client_id = int(request.form['client_id'])
        show_id = int(request.form['show_id'])
        row = request.form['row']
        seat = request.form['seat']
        client_type = request.form["client_type"]
        pay_method = request.form["pay_method"]

        amount = ticket_prices[client_type]

        ticket_exists = session.query(Ticket).filter_by(id_show=show_id, row=row, seat=seat).first()
        if ticket_exists is not None:
            return "Podane miejsce jest juz zajete!"

        # Sprawdzenie zakresu wybranego miejsca
        room_id = session.query(Show.id_room).filter_by(id_show=show_id).scalar()
        is_available, num_of_rows, seats_per_row = check_seat_availability(room_id, row, seat)
        if not is_available:
            return f"Wybrane miejsce jest poza zakresem. Wymiary: {num_of_rows} x {seats_per_row}"

        transaction = Transaction(id_client=client_id, date=datetime.now(), amount=amount, currency="PLN", status="completed", pay_method=pay_method)
        session.add(transaction)
        session.commit()
        session.flush()

        # Tworzenie nowego klienta
        new_ticket = Ticket(id_show=show_id, row=row, seat=seat, id_transaction=transaction.id_transaction)

        # Dodawanie klienta do bazy danych
        session.add(new_ticket)
        session.commit()

        return 'Bilet został dodany do bazy danych.'


    shows = session.query(Show, Movie, Room).join(Movie, Show.id_movie == Movie.id_movie).join(Room, Show.id_room == Room.id_room).all()

    # Przygotowanie danych seansów
    shows_data = []
    for show, movie, room in shows:
        shows_data.append({
            'id_show': show.id_show,
            'title': movie.title,
            'director': movie.director,
            'year_of_prod': movie.year_of_prod,
            'date': show.date,
            'time': show.time,
            'room': room.id_room  # Zakładam, że nazwa sali znajduje się w polu 'name' encji Room
        })

    clients = session.query(Client).all()
    
    # Przygotowanie danych klientów
    clients_data = []
    for client in clients:
        clients_data.append({
            'id_client': client.id_client,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'email': client.email,
            'type': client.type
        })
    
    return render_template('sell_ticket.html', clients=clients_data, shows=shows_data)




@app.route('/buy-ticket', methods=['GET', 'POST'])
def buyticket():
    if request.method == 'POST':
        show_id = int(request.form['show_id'])
        row = request.form['row']
        seat = request.form['seat']
        client_type = request.form["client_type"]
        pay_method = request.form["pay_method"]
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        amount = ticket_prices[client_type]

        ticket_exists = session.query(Ticket).filter_by(id_show=show_id, row=row, seat=seat).first()
        if ticket_exists is not None:
            return "Podane miejsce jest juz zajete!"

        # Sprawdzenie zakresu wybranego miejsca
        room_id = session.query(Show.id_room).filter_by(id_show=show_id).scalar()
        is_available, num_of_rows, seats_per_row = check_seat_availability(room_id, row, seat)
        if not is_available:
            return f"Wybrane miejsce jest poza zakresem. Wymiary: {num_of_rows} x {seats_per_row}"

        
        if pay_method in ["blik", "przelew"]:
            status = "completed"
        else:
            status = "pending"

        client = session.query(Client).filter_by(first_name=first_name, last_name=last_name, email=email).first()
        if not client:
            client = Client(first_name=first_name, last_name=last_name, email=email, type=client_type)
            session.add(client)
            session.commit()
            session.flush()

        transaction = Transaction(id_client=client.id_client, date=datetime.now(), amount=amount, currency="PLN", status=status, pay_method=pay_method)
        session.add(transaction)
        session.commit()
        session.flush()

        # Tworzenie nowego klienta
        new_ticket = Ticket(id_show=show_id, row=row, seat=seat, id_transaction=transaction.id_transaction)

        # Dodawanie klienta do bazy danych
        session.add(new_ticket)
        session.commit()

        return 'Bilet został dodany do bazy danych.'


    shows = session.query(Show, Movie, Room).join(Movie, Show.id_movie == Movie.id_movie).join(Room, Show.id_room == Room.id_room).all()

    # Przygotowanie danych seansów
    shows_data = []
    for show, movie, room in shows:
        shows_data.append({
            'id_show': show.id_show,
            'title': movie.title,
            'director': movie.director,
            'year_of_prod': movie.year_of_prod,
            'date': show.date,
            'time': show.time,
            'room': room.id_room  # Zakładam, że nazwa sali znajduje się w polu 'name' encji Room
        })

    clients = session.query(Client).all()
    
    # Przygotowanie danych klientów
    clients_data = []
    for client in clients:
        clients_data.append({
            'id_client': client.id_client,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'email': client.email,
            'type': client.type
        })
    
    return render_template('buy_ticket.html', clients=clients_data, shows=shows_data, prices=ticket_prices)


if __name__ == '__main__':
    app.run(debug=False)
