from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey,Date
from sqlalchemy.orm import Relationship


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer,primary_key=True,index=True)
    name = Column(String, index=True)
    date_of_birth =Column(Date)
    email = Column(String)
    username = Column(String, index=True)
    password = Column(String)
    permission = Column(String)
    
    

class Movies(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer,primary_key=True,index=True)
    movie_name = Column(String, index=True)
    movie_description =Column(String)
    movie_status = Column(String)
    total_seats = Column(Integer, index=True)
    booked_seats = Column(Integer,index=True)
    available_seats = Column(String,index=True)

    # reservations = Relationship("Reservations", back_populates="movies")




class Reservations(Base):
    __tablename__ = "reservations"

    reserve_id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.user_id"),index=True)
    movie_id = Column(Integer, ForeignKey("movies.movie_id"),index=True)
    booked_seats = Column(Integer)

    # user = Relationship("Users", back_populates="reservations")
    # movie = Relationship("Movies", back_populates="reservations")



    






class Questions(Base):
    __tablename__ = "questions"

    id = Column(Integer,primary_key=True,index=True)
    question_text=Column(String, index=True)

class Choices(Base):
    __tablename__ ="choices"

    id = Column(Integer,primary_key=True,index=True)
    choice_text=Column(String, index=True)
    is_correct = Column(Boolean,default=False)
    question_id= Column(Integer,ForeignKey("questions.id"))