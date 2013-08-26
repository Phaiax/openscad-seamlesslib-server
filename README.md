openscad-seamlesslib-server
===========================

Web interface to create and API to recieve modules online



# Installation for Development

## Prerequesites

 * Install virtualenv:
  + `# apt-get install python-setuptools`
  + `# easy_install virtualenv`

## Create Virualenv
 * Ubuntu users take care of: (https://bugs.launchpad.net/ubuntu/+source/python2.7/+bug/1115466)
  + `sudo ln -s plat-x86_64-linux-gnu/_sysconfigdata_nd.py /usr/lib/python2.7`
 * `cd` to the root directory of this repository
 * execute `create-virtual-environment.sh`
 * execute `install-xapian-into-virtual-environment.sh`
 
 
## Start Django Development server or use manage.py
 * You should not simply start manage.py by itself, because then you do not use the virtual environment. Instead you have to this:
  + type: `source venv/bin/acticate` to bind the virtual environment to your current shell. 
  + Then you can type ./manage.py commands.
  + You need to activate the virtual environment whenever you (re)open a new shell/terminal window.  Your shell should look like this:
    `(venv)bob@hispc:~/code/openscad-seamlesslib-servers`
 * Init database:
  + `./manage.py syncdb`
  + `./manage.py migrate`
    
  
## Develop (start development server)
 * `source venv/bin/activate`
 * `./start-development-server.sh`
 * `./tests.sh web` or `./tests.sh api`
 * look into these files to see how ./manage.py is called
  
# Installation on a web server (For public operation, no development)

### Get Code
 * clone this repository into a path, not accessible via web
 * `cd` to the root directory of this repository

### Install Virtual Environment and additional libraries
 * execute `create-virtual-environment.sh`
  * as i tried this, pip did not installed all modules, so you may need to
   * activate the virtual environment (`source venv/bin/activate`)
   * pip install ______  for every module in etc/requirements.txt
 * execute `install-xapian-into-virtual-environment.sh`

### Create Database
 * create an empty mysql database
 * copy the etc/settings_server_example.py into src/seamless/settings_server.py
  * You may want to store that file in /home/username/foobar/ and only create a symlink to this file in src/seamless
  * insert db settings
  * adjust all pathes to your needs
  * replace SECRET_KEY with other random stuff
 * while virtual environment activated, cd into src/ and do
  * `./manage.py shell --settings=seamless.settings_server` This should open a shell. If not, something did go wrong and you need to fix that first.
  * `./manage.py syncdb --settings=seamless.settings_server`
  * `./manage.py migrate --settings=seamless.settings_server` <- You can call this whenever the db structure has changed (eg after `git pull`). (backup first)

### Make available for apache (mod_fcgi)
 * Don't use mod_python! (refer to Xapian documentation)
 * For mod_fcgi:
  * copy etc/seamless-fcgi-example into your fcgi-bin/ path
   * `chmod 755 fcgi-bin/seamless-fcgi`
   * adjust all path variables, and don't forget the shebang in line 1
   * adjust the name of your settings file (without .py)
  * copy the htaccess-example (renaming into .htaccess) into your web directory
   * modify the Rewrite rule to match your fcgi-script name
  * Open the web application with your browser. It should work (without static files yet)
   * If not, refer to your server log, set Debug=True temporarily in your settings_server.py or take a look at the fcgi-out.log file

#### Server static files
  * create the /static/ folder in your webroot directory (maybe /html/)  (That directory you had set STATIC_ROOT in settings_server.py to)
   * `./manage.py collectstatic --settings=seamless.settings_server`
   * now some files should have been copied into the /static folder
   * You always need to do this when you added new static files to the orgin static folders (eg openscad-seamlesslib-server/src/web/static/....)
   * Remember to execute all ./manage.py commands while virtual environment activated

#### Build search index (need for cronjob or runwhen)
  * Refresh the search index (you need to do this manually)
   * Build your search index once, then only do updates
    *  `./manage.py rebuild_index --settings=seamless.settings_server`
   * Set a cron job to update your search index periodically
    * `source /home/MMMMMMMMMMMMM/openscad-seamlesslib-server/venv/bin/activate && /home/MMMMMMMMMMMMM/openscad-seamlesslib-server/src/manage.py update_index --settings=seamless.settings_server && deactivate`

### Howto kill the server (for restart after update or config changes)
  * If your want to restart the server (after update or config change), try
   * `killall <fcgi-script-name>`
   * execute this until you get the message: No process found
   * or
   * `while \`killall seamless-django\`; do sleep 0.1; done`
