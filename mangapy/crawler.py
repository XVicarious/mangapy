# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

import os
from pathlib import Path

from schema import DB, Manga, Chapter, Library

lib_path = '/manga'


def library_crawler(library_path: Path):
    library = DB.session.query(Library).filter(Library.path == str(library_path)).first()
    for series in os.listdir(library_path):
        manga = DB.session.query(Manga).filter(Manga.path == series).first()
        if not manga:  # if the manga doesn't exist, create it
            manga = Manga(series)
            library.manga.extend([manga])  # add it to the library
        for chapter in os.listdir(library_path / series):
            chap = DB.session.query(Chapter).filter(Chapter.path == chapter, Chapter.manga == manga).first()
            if chap:  # if the chapter already exists, continue on
                continue
            chap = Chapter(chapter)
            manga.chapters.extend([chap])
    DB.session.commit()


def just_list(library_path):
    for chapter in DB.session.query(Chapter):
        print(chapter.path, chapter.number)


# library_crawler(Path(lib_path))
# just_list(Path(lib_path))
