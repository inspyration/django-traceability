What is it?
===========

#) Traceability features
    #) User actions
    #) Actor management
    #) Proxy management

Summary
=======

#) prerequisites
#) create a virtual environment
#) use the virtual environment
#) install requirements
#) Run the server

prerequisites
=============

This project is based on Python 3 only and uses Django 1.7.1.

    # aptitude install python3 python3-pip

You must install either virtualenv or virtualenvwrapper

Install virtualenv
------------------

Using *pip*

    # pip3 install virtualenv

Install virtualenvwrapper
-------------------------

Using *pip*

    # pip3 install virtualenvwrapper

Then, you must add this 3 lines at the end of ~/.bashrc

    export WORKON_HOME = /.virtualenvs
    mkdir -p $WORKON_HOME
    source ~/.local/bin/virtualenvwrapper.sh

Create a virtual environment
============================

When using virtualenv, you may want to create a virtual environment for each project

Using *virtualenv*

    $ virtualenv -p python3 my_virtualenv_name

Using *virtualenvwrapper*

    $ mkvirtualenv -p python3 my_virtualenv_name

Using virtual environment
=========================

Each time you want to use the project, you must use the virtual environment

Using *virtualenv*

    $ source my_virtualenv_name/bin/activate

Using *virtualenvwrapper*

    $ workon your_virtual_env_name

You can check if the virtual environment is active with

    $ which python

Install requirements
====================

In order to use your project for the first time, you must install all requirements

    $ pip install -r requirements.txt

How to run the Server
=====================

Now, run the server and enjoy it !

    $ ./manage.py runserver

