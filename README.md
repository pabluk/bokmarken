Bokmärken
=========

_A self-hosted shelf for storing links for easy visual reference_.

Bokmärken is a Swedish word, meaning _Bookmarks_ in English.

Bokmärken was heavily inspired by Minne, a linkshelf project of [socketubs](https://github.com/socketubs).

You can see it in action at [bokmarken.com](http://bokmarken.com/).  
It also includes a REST API to import/export and play with your links. For details and examples see [bokmarken.com/api](http://bokmarken.com/api/).

[![Build Status](https://travis-ci.org/pabluk/bokmarken.png?branch=master)](https://travis-ci.org/pabluk/bokmarken)


Screenshots
-----------

A responsive design for every device.

[![Desktop screenshot](http://bokmarken.com/static/screenshots/desktop-lo-res.jpg)](http://bokmarken.com/static/screenshots/desktop-hi-res.png)

[![Mobile screenshot](http://bokmarken.com/static/screenshots/nexus4-lo-res.jpg)](http://bokmarken.com/static/screenshots/nexus4-hi-res.png)


Installation
------------

On a Debian or Ubuntu system, you need to install the following packages:

```bash
sudo apt-get install libxml2-dev libxslt1-dev
```

and create a `virtualenv`:

```bash
cd ~/
git clone https://github.com/pabluk/bokmarken.git
cd bokmarken
virtualenv virtenv
source virtenv/bin/activate
pip install -r requirements.txt
python manage.py syncdb --migrate --noinput
python manage.py createsuperuser --username=admin --email=admin@localhost  # enter a password for the admin user
python manage.py runserver
```

Open your browser at `http://localhost:8000/` and sign in with your credentials.

By default links are stored in a SQLite3 database. If you want to use another database backend supported by Django,
for example PostgreSQL, you need to install additional packages:

```bash
sudo apt-get install libpq-dev
```

on the already created and activated `virtualenv`:

```bash
pip install psycopg2==2.5.1
```

and finally, add your database settings on `bokmarken/local_settings.py`.
See this [page](https://docs.djangoproject.com/en/dev/ref/settings/#databases) for more details
about database settings on Django.


Contributing
------------

Want to contribute? Great! Bug reports, code and documentation patches are greatly appreciated.  
Please file bugs and send pull requests using the [issue tracker](https://github.com/pabluk/bokmarken/issues).


Credits
-------

The image used by default on links without thumbnails is licensed under a Creative Commons license
by [gpoo](http://www.flickr.com/photos/gpoo/9004993292/).


License
-------

Licensed under [AGPL v3](http://www.gnu.org/licenses/agpl-3.0.txt). See [LICENSE](https://raw.github.com/pabluk/bokmarken/master/LICENSE) for details.
