#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import os
import magic
from zipfile import ZipFile
import yaml
from io import BytesIO
from flask import send_file
from flask_restful import Resource
from pathlib import Path
from crawler import library_crawler
from schema import APP, API, Manga, DB, Chapter, Library, Volume

manga_path = '/<string:manga_id>'
volume_path = manga_path + '/v/<string:volume>'
chapter_path = manga_path + '/c/<string:chapter>'
page_path = chapter_path + '/<string:page>'


@API.resource(manga_path)
class ApiManga(Resource):
    def get(self, manga_id: int):  # todo: support half chapters
        manga: Manga = DB.session.query(Manga).get(manga_id)
        if not manga:
            return {'Error': '404'}
        json_info = {
            'title': manga.path,
            'path': manga.full_path,
            'chapters': {
                volume.number: {
                    chapter.number: {
                        'name': chapter.path,
                        'pages': chapter.pages,
                    } for chapter in volume.chapters
                } for volume in manga.volumes
            },
            'qt': str(datetime.utcnow().timestamp()),
        }
        json_info['chapters']['no_vol'] = {
            chapter.number: {
                'name': chapter.path,
                'pages': chapter.pages,
            } for chapter in manga.chapters if chapter.volume == None
        }
        return json_info


@API.resource(volume_path)
class ApiVolume(Resource):
    def get(self, manga_id: int, volume: int):
        volumes = DB.session.query(Volume).filter(Volume._manga_id == manga_id, Volume.number == volume).all()
        if not len(volumes):
            return {'Error': '404', 'Type': 'Volume'}
        return {
            vol.number: {'chapters': len(vol.chapters)} for vol in volumes
        }


@API.resource(chapter_path)
class ApiChapter(Resource):
    def get(self, manga_id: int, chapter: str):
        chapters = DB.session.query(Chapter).filter(Chapter._manga_id == manga_id, Chapter.number == chapter).all()
        if not len(chapters):
            return {'Error': '404', 'Type': 'Chapter'}
        return {
            chap._id: {
                chap.number: chap.path
            } for chap in chapters
        }


def filename_to_int(filename):
    filename = filename.split('.')
    try:
        number = int(filename[0])
        return number
    except:  # todo: make this more robust? will I even need this in the future? probably not.
        APP.logger.info('Oops')
        return 0


@API.resource(page_path)
class ApiPage(Resource):  # todo: this is probably dangerous, we really should check that we have images before we serve them or whatever.
    def get(self, manga_id: int, chapter: str, page: int):
        chapter_obj = DB.session.query(Chapter).filter(Chapter._manga_id == manga_id, Chapter.number == chapter).first()
        if not chapter_obj:
            APP.logger.warning('No chapter found for Manga {0}, Chapter {1}'.format(manga_id, chapter))
            return
        ch_file = ZipFile(chapter_obj.full_path)
        sorted_namelist = sorted(ch_file.namelist())
        page = int(page)
        page_data = ch_file.open(sorted_namelist[page - 1]).read()
        m = magic.Magic(mime=True)
        mime: str = m.from_buffer(page_data)
        if not mime.startswith('image/'):
            return
        return send_file(BytesIO(page_data), mimetype=mime)


@API.resource('/')
class ApiRoot(Resource):
    def get(self):
        all_manga = DB.session.query(Manga).all()
        return {
            manga.path: {
                'manga_id': manga._id,
                'volumes': len(manga.volumes),
                'chapters': len(manga.chapters),
            } for manga in all_manga
        }


def check_libs():
    libraries = DB.session.query(Library).all()
    for path in APP.config.get('library_paths'):
        if not os.path.exists(path):
            continue
        if path not in [lib.path for lib in libraries]:
            DB.session.add(Library(path))
            library_crawler(Path(path))
    DB.session.commit()


if __name__ == '__main__':
    print('Starting MangaPy')
    with open('config.yml') as cfg:
        data = yaml.load(cfg, Loader=yaml.Loader)
        APP.config['library_paths'] = data['library_paths']
    if not os.path.exists('mangapy.db'):
        DB.create_all()
        DB.session.commit()
    check_libs()
    APP.run(debug=True, host='0.0.0.0')
