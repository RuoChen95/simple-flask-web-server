# simple-flask-web-server
It's a simple web server coded by Ruochen Xie, which has the function of creating, reading, updating and deleting data in restaurant and menu using flask and sqlAlchemy.

This is one of the projects from udacity full-stack nanodegree.

## Example of output
If running locally, it's a website which has a url: http://0.0.0.0:5000/ showing a list of fack restaurants, users can crud them and their menu.

## Design of the code
 1. connect db
 2. define router
 2. define session
 3. execute sql using session
 4. import results into html templates or redirect to another url

## Improvements
 1. Implement a decorator function to check user login status
 2. Implement the ON DELETE CASCADE
 3. Include the csrf_token, flask-seasurf, dealing with the CRUD problem

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
  
### Setting up the Database:

  You can use the restaurantmenu.db directly or using the following command to creat a clean restaurantmenu.db:

  1. Create the database using the command:`python database_setup.py`
  2. Use `python setmenus.py` to populate the database
  
  The database includes two tables which can be observed through database_setup.py:
  * The restaurant table includes the name and id.
  * The menue table includes the name, id, price, description, restaurant_id.
  
### Set up
  The web server contains four features:

  1. The CRUD of restaurant table
  2. The CRUD of menu table
  3. Return menu info using JSON
  4. authentication of github account

  run it using 
  ```
    python webserverUsingFlask.py
  ```

## Application Code Style

  Passing the pycodestyle (`pycodestyle --first webserverUsingFlask.py`) checking.