# -*- coding: utf-8 -*-

import os
from pathlib import Path

from schema import DB, Manga, Chapter

lib_path = '/manga'


def library_crawler(library_path: Path):
    for series in os.listdir(library_path):
        manga = DB.session.query(Manga).filter(Manga.path == series).first()
        if not manga:
            manga = Manga(series, lib_path)
            DB.session.add(manga)
        for chapter in os.listdir(library_path / series):
            print('checking if {0} exists'.format(chapter))
            chap = DB.session.query(Chapter).filter(Chapter.path == chapter, Chapter.manga == manga._id).first()
            if chap:
                print('it does, continue')
                continue
            chap = Chapter(chapter)
            manga.chapters.extend([chap])
    DB.session.commit()


library_crawler(Path(lib_path))
