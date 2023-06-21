from sqlalchemy import MetaData, Column, Integer, String, DateTime, Date, Time, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Client(Base):
    __tablename__ = 'client'
    id_client = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False)
    type = Column(String(45), nullable=False)

class Movie(Base):
    __tablename__ = 'movie'
    id_movie = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    director = Column(String(45), nullable=False)
    year_of_prod = Column(Integer, nullable=False)
    country = Column(String(45), nullable=False)
    duration = Column(Integer, nullable=False)
    language = Column(String(45), nullable=False)
    dimension = Column(String(45), nullable=False)

class Room(Base):
    __tablename__ = 'room'
    id_room = Column(Integer, primary_key=True, autoincrement=True)
    num_of_rows = Column(Integer, nullable=False)
    seats_per_row = Column(Integer, nullable=False)

class Transaction(Base):
    __tablename__ = 'transaction'
    id_transaction = Column(Integer, primary_key=True, autoincrement=True)
    id_client = Column(Integer, ForeignKey('client.id_client'), nullable=False)
    date = Column(DateTime, nullable=False)
    amount = Column(DECIMAL(5,2), nullable=False)
    currency = Column(String(45), nullable=False)
    status = Column(String(45), nullable=False)
    pay_method = Column(String(45), nullable=False)
    client = relationship("Client")

class Show(Base):
    __tablename__ = 'show'
    id_show = Column(Integer, primary_key=True, autoincrement=True)
    id_movie = Column(Integer, ForeignKey('movie.id_movie'), nullable=False)
    id_room = Column(Integer, ForeignKey('room.id_room'), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    movie = relationship("Movie")
    room = relationship("Room")

class Ticket(Base):
    __tablename__ = 'ticket'
    id_ticket = Column(Integer, primary_key=True, autoincrement=True)
    id_transaction = Column(Integer, ForeignKey('transaction.id_transaction'), nullable=False)
    id_show = Column(Integer, ForeignKey('show.id_show'), nullable=False)
    row = Column(Integer, nullable=False)
    seat = Column(Integer, nullable=False)
    transaction = relationship("Transaction")
    show = relationship("Show")


# Dodanie powiązań zwrotnych dla relacji

Client.transactions = relationship('Transaction', order_by=Transaction.id_transaction, back_populates='client')
Movie.shows = relationship('Show', order_by=Show.id_show, back_populates='movie')
Room.shows = relationship('Show', order_by=Show.id_show, back_populates='room')
Transaction.tickets = relationship('Ticket', order_by=Ticket.id_ticket, back_populates='transaction')
Show.tickets = relationship('Ticket', order_by=Ticket.id_ticket, back_populates='show')
