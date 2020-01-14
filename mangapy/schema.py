# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mangapy.db'
DB: SQLAlchemy = SQLAlchemy(APP)
API = Api(APP)


class Chapter(DB.Model):

    _id = DB.Column('id', DB.Integer, primary_key=True)
    path = DB.Column(DB.Unicode)
    manga = DB.Column(DB.Integer, ForeignKey('manga_manga.id'))

    def __init__(self, chapter_path):
        self.path = chapter_path


class Manga(DB.Model):

    __tablename__ = 'manga_manga'

    _id = DB.Column('id', DB.Integer, primary_key=True)
    library = DB.Column(DB.Unicode, ForeignKey('manga_library.path'))
    path = DB.Column(DB.Unicode)
    chapters = relationship(Chapter.__name__)

    def __init__(self, manga_path, library_path):
        self.path = manga_path
        self.library = library_path


class Library(DB.Model):

    __tablename__ = 'manga_library'

    _id = DB.Column('id', DB.Integer, primary_key=True)
    path = DB.Column(DB.Unicode)

    def __init__(self, library_path: str):
        self.path = library_path


def initialize_db():
    if not os.path.exists('mangapy.db'):
        DB.create_all()
        lib = Library('/home/docker/dionysus/manga/manga') # todo: remove this
        DB.session.add(lib)
        DB.session.commit()


if __name__ == '__main__':
    initialize_db()
