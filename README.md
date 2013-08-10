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
 
 
## Start Django Development server or use manage.py
 * You should not simply start manage.py by itself, because then you do not use the virtual environment. Instead you have to choose between the following two possibilities:
  + always use: `../venv/bin/python manage.py`
  + OR: type: `. venv/bin/acticate` to bind the virtual environment to your current shell. Then you can type ./manage.py. You need to activate the virtual environment whenever you (re)open a new shell/terminal window. (Dont forget the dot at the beginning). Your shell should look like this:
  
    `(venv)bob@hispc:~/code/openscad-seamlesslib-servers`
    
    
