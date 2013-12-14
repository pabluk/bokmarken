Bokmärken
=========

_A self-hosted shelf for storing links for easy visual reference_.

Bokmärken is a Swedish word, meaning _Bookmarks_ in English.

Bokmärken was heavily inspired by Minne, a linkshelf project of [socketubs](https://github.com/socketubs).

You can see it in action at http://bokmarken.com/

Screenshots
-----------

A responsive design for every device.

[![Desktop screenshot](http://bokmarken.com/static/screenshots/desktop-lo-res.jpg)](http://bokmarken.com/static/screenshots/desktop-hi-res.png)

[![Mobile screenshot](http://bokmarken.com/static/screenshots/mobile-lo-res.jpg)](http://bokmarken.com/static/screenshots/mobile-hi-res.png)


Installation
------------

With `virtualenv`:

```bash
$ cd ~/
$ git clone https://github.com/pabluk/bokmarken.git
$ cd bokmarken
$ virtualenv virtenv
$ source virtenv/bin/activate
$ pip install -r requirements.txt
$ python manage.py syncdb
$ python manage.py migrate
$ python manage.py runserver
```

Open your browser at `http://localhost:8000/`.


Contributing
------------

Want to contribute? Great! Bug reports and code and documentation patches are greatly appreciated.
Please file bugs and send pull requests using the [issue tracker](https://github.com/pabluk/bokmarken/issues).
