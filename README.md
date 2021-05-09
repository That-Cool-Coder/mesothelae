# mesothelae

A chat program using flask

## Setup
(only for linux server with apache2 - windows is too hard)

Prerequisites: python >= 3.6, pip3

Step 1: Clone this repo into the public directory of the server

Step 2: Install some things for WSGI:
```
sudo apt-get install libapache2-mod-wsgi-py3 python-dev
```

Step 3: Install python packages:
```
pip3 install Flask
```

Step 3: Go into where your site's configuration file is (probably `/etc/apache2/sites-available/000-default-le-ssl.conf`) and add this line to inside the top `VirtualHost` block:
```
WSGIScriptAlias /mesothelae /to/public/directory/mesothelae/mesothelae.wsgi
```

Step 4: Create a directory `/var/wpd/mesothelae` if it doesn't exist and set its permissions to octal `0777`. Then go to the folder of the repo and run `/setup_database.py`.

Step 5: Restart apache2 - something like `sudo systemctl restart apache2`