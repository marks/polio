# notes on requirements/tips for deploy of Polio to Rackspace

# ACTIVE
- IN PROGRESS * work on script

# BACKLOG
- set up manual push to Rackspace, AWS
* separate runtime & development dependencies
* server configuration - apache, django / wsgi)
* take prod settings out of git
* remove database passwords from git

# DONE
- create polio user on RS
- set up SSH stuff

# deploy back-end
- ssh into rackspace, sudo into john's user
- cd $DOCROOT
- do stuff in deploy.sh
- (frequently migrate fails & gives SQL error message.this is hard.)
- maybe bounce apache

# deploy front-end
- on local machine, run 'gulp dist-ui' to build front-end. (need django for django admin interface)
- scp zip file to rackspace
- unzip zip file to static document root
- chgrp -R www-data *

# notes on deploy of Polio to AWS
- run 'gulp dist' to create two dist files
- scp them to aws
- unzip to appropariate directory
- in python directory, run stuff from deploy.sh
- in static files directory, change everything to www-data

on build server... how we want it to work w/Jenkins
===
- dependencies - python (2.7.*),pip, node/npm
- install dependencies - npm install && pip install -r requirements.txt (maybe needed for tests and gulp dist)
- run tests (which need to be developed...?)
- if they fail, explode
- if they succeed...
  - run 'gulp dist'
  - copy to AWS or rackspace
  - on remote server, unzip in proper folders
  - install dependencies on back-end, server  configuration (differences between AWS and RackSpace)
  - in back-end folder do stuff in deploy.sh (and delete pyc files)
  - in front-end folder, change everything to www-data
