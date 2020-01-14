MangaPy -- Serving up your manga

Right now its super basic. It will crawl a directory and plop manga and chapters into the database.

For the time being it is structured like so:  
`/root_dir/<manga-series>/<manga-chapter>.(zip|cbz)`

That just happens to be how my library is laid out. I plan on expanding the possibilities in the future. Or you can if you want. Your choice.

As soon as I get a stable interface for requesting manga and chapters from the server, I plan on starting to work on metadata. That is a super important part of this project.

To try this out for yourself...

1. The default library path is in both `mangapy/schema.py` and `mangapy/crawler.py`. Change these to the location you'll be using.  
2. Run `python mangapy/schema.py` to initialize the database. I don't plan on any migrations until I can feel like I am comfortable with the current schema.  
3. Run `python mangapy/crawler.py` to crawl your library folders. There is literally no indication of progress. I have ~125 series and ~2500 chapters and it only takes a few seconds to do an initial crawl.  
4. Run `python mangapy/server.py`, and mozy your way over to <your-url>:5000. Give it a good `/<number>` and it will list out that manga series and the chapters that are there.

Enjoy! If you have a specific library structure or suggestion, please open an issue. I am not however planning on writing a frontend for this. I do however plan to write an extension for inorichi/tachiyomi when I get to that point.  
As far as authentication is concerned, I haven't thought that one through yet. I'd hate to have yet another login system. Possible integration into LDAP or OpenID (thats still a thing, right?) is the most probable. I will absolutely not add any kind of Google/Facebook/Microsoft account or whatever integration. I don't care if Jesus Christ himself tells me to do it. No.
