# simple-flask-web-server
It's a simple web server, which has the function of creating, reading, updating and deleting data in restaurant and menu using flask and sqlAlchemy which is coded by Ruochen Xie.

This is one of the projects from udacity full-stack nanodegree.

## Example of output
If running locally, it's a website which has a url: http://0.0.0.0:5000/ showing a list of fack restaurants, users can crud them and their menu.

## Design of the code
 1. connect db
 2. define router
 2. define session
 3. execute sql using session
 4. import results into html templates or redirect to another url

## How to run it

### Setup Project:
  1. Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/)
  2. Download or Clone [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository. The file have a directory called vagrant.
  3. Put the project and the vangrant setup file into the same directory.
  
### Launching the Virtual Machine:
  1. Launch the Vagrant VM inside Vagrant sub-directory in the downloaded fullstack-nanodegree-vm repository using command:

  ```
    $ vagrant up
  ```
  2. Then Log into this using command:
  
  ```
    $ vagrant ssh
  ```
  3. Change directory to /vagrant and look around with ls.
  
### Setting up the database:
  1. Create the database using the command:`python database_setup.py`
  2. Use `python lotsofmenus.py` to populate the database
  
  The database includes two tables:
  * The restaurant table includes the name and id.
  * The menue table includes the name, price, description, restaurant_id.
  
### Set up
  The web server contains three features:

  1. The CRUD of restaurant table
  2. The CRUD of menue table
  3. Return menue info using JSON

  run it using 
  ```
    python webserverUsingFlask.py
  ```

### Application code style

  Passing the pycodestyle (`pycodestyle --first webserverUsingFlask.py`) checking.