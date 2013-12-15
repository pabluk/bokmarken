Bokmärken
=========

_A self-hosted shelf for storing links for easy visual reference_.

Bokmärken is a Swedish word, meaning _Bookmarks_ in English.

Bokmärken was heavily inspired by Minne, a linkshelf project of [socketubs](https://github.com/socketubs).

You can see it in action at [bokmarken.com](http://bokmarken.com/).  
It also includes an REST API to import/export and play with your links. For details and examples see [bokmarken.com/api](http://bokmarken.com/api/).

[![Build Status](https://travis-ci.org/pabluk/bokmarken.png?branch=master)](https://travis-ci.org/pabluk/bokmarken)


Screenshots
-----------

A responsive design for every device.

[![Desktop screenshot](http://bokmarken.com/static/screenshots/desktop-lo-res.jpg)](http://bokmarken.com/static/screenshots/desktop-hi-res.png)

[![Mobile screenshot](http://bokmarken.com/static/screenshots/mobile-lo-res.jpg)](http://bokmarken.com/static/screenshots/mobile-hi-res.png)


Installation
------------

On a Debian or Ubuntu system, you need to install the following packages:

```bash
sudo apt-get install libxml2-dev libxslt1-dev libpq-dev
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


Contributing
------------

Want to contribute? Great! Bug reports, code and documentation patches are greatly appreciated.

Please file bugs and send pull requests using the [issue tracker](https://github.com/pabluk/bokmarken/issues).


License
-------

Licensed under [AGPL v3](http://www.gnu.org/licenses/agpl-3.0.txt). See [LICENSE](https://raw.github.com/pabluk/bokmarken/master/LICENSE) for details.
