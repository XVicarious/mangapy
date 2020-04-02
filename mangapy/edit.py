#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from mangapy.schema import DB, Manga, Chapter, Library, Volume, APP

bp = Blueprint('edit', __name__, url_prefix='/edit')


def get_libraries():
    libraries = DB.session.query(Library).all()
    return [[lib._id, lib.path] for lib in libraries]

@bp.route('/manga', methods=('GET', 'POST'))
def edit():
    manga_id = request.args.get('id')
    edit_manga: Manga = DB.session.query(Manga).filter(Manga._id == manga_id).first()
    mydict = {
        'manga': {
            'path': edit_manga.path,
            'library': edit_manga.library._id,
            'volumes': [
                {
                    'id': vol._id, 
                    'number': vol.number
                } for vol in edit_manga.volumes],
            'chapters': [
                {
                    'id': chap._id,
                    'path': chap.path,
                    'number': chap.number,
                    'part': chap.part_number if chap.part_number else 0,
                    'volume': chap.volume._id if chap.volume else None,
                } for chap in edit_manga.chapters],
        },
        'defaults': {
            'libraries': get_libraries()
        }
    }
    APP.logger.info(mydict)
    return render_template('edit/manga.html', mydict=mydict)
