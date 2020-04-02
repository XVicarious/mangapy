# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

import random
from pathlib import Path
import re
import zipfile
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

chapter_re = re.compile(r'(?:Ch(?:\.|apter)\s?|#)(\d+(?:\.\d+)?)')


class Chapter(DB.Model):

    _id = DB.Column('id', DB.Integer, primary_key=True)
    path = DB.Column(DB.Unicode)
    _manga_id = DB.Column(DB.Integer, ForeignKey('manga_manga.id'))
    manga = relationship("Manga", back_populates='chapters')
    number = DB.Column(DB.Integer)
    part_number = DB.Column(DB.Integer)
    _volume_id = DB.Column(DB.Integer, ForeignKey('manga_volume.id'))
    volume = relationship("Volume", back_populates='chapters')

    def __init__(self, chapter_path, chapter_num=None, part_num=None):
        self.path = chapter_path
        self.number = chapter_num
        self.part_number = part_num
        #self._number = chapter_num

    @property
    def pages(self):
        return len(zipfile.ZipFile(self.full_path).namelist())

    @property
    def full_path(self):
        return str(Path(self.manga.full_path, self.path))


class Volume(DB.Model):

    __tablename__ = 'manga_volume'

    _id = DB.Column('id', DB.Integer, primary_key=True)
    _manga_id = DB.Column(DB.Integer, ForeignKey('manga_manga.id'))
    number = DB.Column(DB.Integer)
    chapters = relationship(Chapter.__name__, back_populates='volume')
    manga = relationship('Manga', back_populates='volumes')

    def __init__(self, volume_number: int):
        self.number = volume_number


class Manga(DB.Model):

    __tablename__ = 'manga_manga'

    _id = DB.Column('id', DB.Integer, primary_key=True)
    _library_id = DB.Column(DB.Integer, ForeignKey('manga_library.id'))
    library = relationship("Library", back_populates='manga')
    path = DB.Column(DB.Unicode)
    title = DB.Column(DB.Unicode)
    chapters = relationship(Chapter.__name__, back_populates='manga')
    volumes = relationship(Volume.__name__, back_populates='manga')

    def __init__(self, manga_path):
        self.path = manga_path

    @property
    def full_path(self):
        return str(Path(self.library.path, self.path))


class Library(DB.Model):

    __tablename__ = 'manga_library'

    _id = DB.Column('id', DB.Integer, primary_key=True)
    path = DB.Column(DB.Unicode)
    manga = relationship(Manga.__name__, back_populates='library')

    def __init__(self, library_path: str):
        self.path = library_path
