from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from .. import board

Base = declarative_base()


class Board(object):

    """base class for any board object in the database"""

    integer = Column(BigInteger, default=0)
    n = Column(Integer)
    wordSize = Column(Integer)

    def toBoard(self):
        return board.fromInt(self.integer, self.n, self.wordSize)


class Puzzle(Base, Board):
    __tablename__ = 'puzzles'

    id = Column(Integer, primary_key=True)

    @property
    def solved(self):
        return any([s.correct for s in self.solutions])


class Solution(Base, Board):
    __tablename__ = 'solutions'

    id = Column(Integer, primary_key=True)

    solver = Column(String)
    correct = Column(Boolean, default=False)
    runtime = Column(Float)

    puzzle_id = Column(Integer, ForeignKey('puzzles.id'))
    puzzle = relationship('Puzzle', backref=backref("solutions", remote_side=id),)
