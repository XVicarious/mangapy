# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

import os
from pathlib import Path
import re

from progress.bar import Bar
from mangapy.schema import DB, Manga, Chapter, Library, Volume, APP

lib_path = '/home/docker/dionysus/manga/manga'

chapter_regex = re.compile(r'(?:Vol\.(?P<volume>\d+) )?(?:Ch\.(?P<chapter>\d+)(\.(?P<part>\d+))?)?')


def deep_anal(chap: Chapter):
    pass


def library_crawler(library_path: Path):
    APP.logger.info(library_path)
    library = DB.session.query(Library).filter(
        Library.path == str(library_path)
    ).first()
    process_paths = os.listdir(library_path)
    with Bar('Library', max=len(process_paths)) as bar:
        for series in os.listdir(library_path):
            manga = DB.session.query(Manga).filter(Manga.path == series).first()
            if not manga:  # if the manga doesn't exist, create it
                manga = Manga(series)
                library.manga.extend([manga])  # add it to the library
            chap_paths = os.listdir(library_path / series)
            with Bar(series, max=len(chap_paths)) as chap_bar:
                for chapter in os.listdir(library_path / series):
                    chap = DB.session.query(Chapter).filter(Chapter.path == chapter, Chapter.manga == manga).first()
                    if chap:  # if the chapter already exists, continue on
                        continue
                    chap_match = chapter_regex.match(chapter)
                    volume_number = chap_match.group('volume')
                    chap = Chapter(chapter, chap_match.group('chapter'), chap_match.group('part'))
                    if volume_number:  # if we get a volume number, find/create it, and add the chapter
                        volume = DB.session.query(Volume).filter(Volume.manga == manga, Volume.number == volume_number).first()
                        if not volume:
                            volume = Volume(volume_number)
                            manga.volumes.extend([volume])
                        volume.chapters.extend([chap])
                    manga.chapters.extend([chap])
                    chap_bar.next()
            bar.next()
    DB.session.commit()


def just_list(library_path):
    for chapter in DB.session.query(Chapter):
        print(chapter.path, chapter.number)


# library_crawler(Path(lib_path))
# just_list(Path(lib_path))
