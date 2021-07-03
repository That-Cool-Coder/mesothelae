# mesothelae

A chat program using Flask backend and some sort of HTML frontend.

## Contents of README
- [About this branch](#about-this-branch)
- [Deployment instructions](#deployment-instructions)

## About this branch

This branch (`app`) holds the actual main program. For documentation, look at `README.md` in the main branch.

## Deployment instructions

(Only for Linux servers with apache2 (aka httpd) - Windows and nginx is too hard)

Prerequisites:
- Python >= 3.6
- Pip for Python 3

Step 1: Clone this repo into `/var/www/` and switch to this branch

Step 2: Install some things for WSGI to work:
```
sudo apt-get install libapache2-mod-wsgi-py3 python-dev
```

Step 3: Install python packages (make sure you use sudo, or else they won't be installed globally):
```
sudo -H pip3 install Flask
# sudo -H pip3 install argon2-cffi (not needed currently)
```

Step 4: Go into where your site's configuration file is (`/etc/apache2/sites-available/000-default-le-ssl.conf` on Ubuntu by default) and add this line to inside the top VirtualHost block:
```
WSGIScriptAlias /mesothelae/api /var/www/mesothelae/mesothelae.wsgi
```

Step 5: Create a folder `/var/www/mesothelae_data` and set its permissions to everyone can do everything.

Step 6: Restart Apache2 - probably `sudo systemctl restart apache2`.