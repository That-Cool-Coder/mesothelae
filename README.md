# mesothelae

A chat program using flask backend and basic html frontend

The documentation isn't hugely organised yet so just scroll down until you find the heading you want

For testing the password to account `ADMIN` is `getSmartNow`.
Please change this and remove this paragraph when account testing is no longer needed.

## Setup
(only for linux server with apache2 - windows is too hard)

Prerequisites: python >= 3.6, pip3

Step 1: Clone this repo into the public directory of the server

Step 2: Install some things for WSGI:
```
sudo apt-get install libapache2-mod-wsgi-py3 python-dev
```

Step 3: Install python packages (make sure you use sudo, or else they won't be installed globally):
```
sudo -H pip3 install Flask
sudo -H pip3 install argon2-cffi
```

Step 3: Go into where your site's configuration file is (probably `/etc/apache2/sites-available/000-default-le-ssl.conf`) and add this line to inside the top `VirtualHost` block:
```
WSGIScriptAlias /mesothelae/api /to/public/directory/mesothelae/mesothelae.wsgi
```

Step 4: Create a directory `/var/ww/wpd/mesothelae/` (to hold the databases) if it doesn't exist and set its permissions to octal `0777`. Then go to the folder of the repo and run `/setup_databases.py`.

Step 5: Restart apache2 - something like `sudo systemctl restart apache2`

## Database structure

The databases are made with `pythondb`, a library that I coded. To see the structure, look in `api/setup_databases.py`.

## Response format

Responses sent from the API always have a standard format. This is an example:
```
{"status":"WARNING","statusCode":"INVALID_PASSWORD"}
```

The two fields `status` and `statusCode` will always be present, and other data like generated session id or whatever can be added (in the same nesting level as the status)

#### Statuses:

There are three statuses:
```
OK
WARNING
ERROR
```
The 'master copy' is stored in an enum `api/status.py`, so if this documentation is wrong, just look there. Statuses should be `WITH_CAPS_AND_UNDERSCORES`. There's also a mirror in `commonScripts/Status.js`. If the two disagree, update the JS to match the Python.

###### OK
This is fairly obvious: everything is totally ok. For instance, the user tried logging in and their details were correct. Another example is if they send a chat message and it gets added to the room just fine.

###### WARNING
This is for when the **client side** has done something wrong. For instance, when the password is wrong or when the request format is incorect. In other words, when there's a problem but the API is not at fault. When this occurs, the client side should show the user the issue and maybe pop up a little text box.

###### ERROR
This is for when something unexpected happened on the **server side**. For instance, the user that was just looked up doesn't exist, or the database can't be accessed, or some other major problem. When this occurs, the client side should show an intrusive pop up that states the `statusCode` (see below) so that it can be reported

#### Status codes
There are a bunch of status codes and you can find them in `api/status_code.py`. Statuse codes should be `WITH_CAPS_AND_UNDERSCORES`. Basically, they state some details about the status - eg `INVALID_PASSWORD` or `DATABASE_CORRUPTED`. If the status is `OK`, then the status code is `OK`. if possible, don't write warning/error in the code, as it's probably redundant. In some errors it's handy, however. Just make things readable. There's also a mirror in `commonScripts/StatusCode.js`. If the two disagree, update the JS to match the Python.