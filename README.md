AccelaConfigTracking
====================

This is a simple script, that can be used to track changes to the Accela (or any database really) using Git.  What the script does is:
* Looks for sql files containing sql statements in a folder, 
* Execute those sql statements on a database, 
* Store the results in a CSV file with the same name as the sql file
* Load the CSV file into a Git Repo
* Commit any changes in the CSV file to the Repo

To Use
-------

Create SQL queries that show the configuration settings you want to track.  Two examples are included, many more can be found on Accela Community. Put these sql queries in a folder.  Setup the global variables (see below). Run the script. Make changes to the configuration. Run script again. View the changes in a Git repo viewer.

Requirements
-------------------

1) Python must be installed.  I’m using python 2.7, but should work for most versions.
2) pypyodbc must be made available.  It is the complied pycode is included, however you may wish to download and install it from https://code.google.com/p/pypyodbc/
3) Git must be installed.  I just use the Git that was installed when I installed GitHub for Windows, but you can install it separately.  http://git-scm.com/downloads
4) Git Repo Viewer.  I use GitHub Windows, but any viewer should work.  https://windows.github.com/

Note, I developed this over time, and have not tried to set it up on a fresh system.  There may be a few other things you need to do before it will work.  

Setup
-----

You will have to modify three global variables for the script to work

1)	path:    This is the location of where your SQL files are located.  It will also be the location of your git repo and where the CSV files are stored.
2)	gitExe:  This is the path to the git executable.  
3)	connectString:  This is the ODBC connection string.  My example is for MS SQL Server.  There are many examples available on the internet.
