#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from flask_restful import Resource

from schema import APP, API, Manga, DB


class ApiManga(Resource):
    def get(self, manga_id: int):
        manga: Manga = DB.session.query(Manga).filter(Manga._id == manga_id).first()
        if not manga:
            return {'Error': '404'}
        return {
            'title': manga.path,
            'path': manga.full_path,
            'chapters': {
                chapter.number: {'name': chapter.path, 'pages': chapter.pages} for chapter in manga.chapters
            },
            'qt': str(datetime.utcnow().timestamp()),
        }


API.add_resource(ApiManga, '/<string:manga_id>')


if __name__ == '__main__':
    APP.run(debug=True, host='0.0.0.0')
