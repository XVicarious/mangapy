MangaPy -- Serving up your manga

Right now its super basic. It will crawl a directory and plop manga and chapters into the database.

For the time being it is structured like so:  
`/root_dir/<manga-series>/<manga-chapter>.(zip|cbz)`

That just happens to be how my library is laid out. I plan on expanding the possibilities in the future. Or you can if you want. Your choice.

As soon as I get a stable interface for requesting manga and chapters from the server, I plan on starting to work on metadata. That is a super important part of this project.

To try this out for yourself...

Run `python mangapy/server.py`. If `mangapy.db` doesn't exist, it will be created and then the library will be scanned. It doesn't check for new files at the current moment. You'll need a `config.yml`, and that looks like this:
```
library_paths:
  - /path/to/manga
  - /other/path/to/manga
```

That will make two separate libraries.  I don't plan on any migrations until I can feel like I am comfortable with the current schema.  There is a progress bar, probably. I have ~125 series and ~2500 chapters and it only takes a few seconds to do an initial crawl.  Finally, mozy your way over to <your-url>:5000. Give it a good `/<number>` and it will list out that manga series and the chapters that are there.

Path to request a volume: `/<manga-id>/v/<volume-number>`  
Path to request a chapter: `/<manga-id>/c/<chapter-number>`

It already has "half-chapter" support (kinda), meaning omakes or extras or whatever you want.  They get scanned as another chapter, but you can't really request them. 

Enjoy! If you have a specific library structure or suggestion, please open an issue. I am not however planning on writing a frontend for this. I do however plan to write an extension for inorichi/tachiyomi when I get to that point.  
As far as authentication is concerned, I haven't thought that one through yet. I'd hate to have yet another login system. Possible integration into LDAP or OpenID (thats still a thing, right?) is the most probable.
