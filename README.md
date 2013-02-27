CurrentCostPi
=============

A Python script designed for the Raspberry Pi to read data from a Current Cost meter using the USB-Serial connection.

I've not invested much time in this script - it's configured for my setup and requires manual configuration changes if you wish to use it for yourself.

Installation wise, I don't have any documentation on exactly what you need. From memory, I think it's:
* Python
* MySQL
* Python serial library
* Pyton MySQLdb library

You need to manually configure the MySQL database - the tables and stored procedures should all be in database.sql. The username and password for the database are stored in plain text in database_processor.py

To run the program, launch main.py. If everything is working, it should start outputting messages to the TTY.

You will need to figure out the date of birth for your current cost meter and update the value in main.py to match. To do this, I personally run main.py so it captures a single reading and then work out how many days wrong the date value it places in the database is.

I don't plan on spending huge amounts of time on this project, as I have a young child and prefer to use the free time I have to play games and generally relax! Feel free to do what you wish with my code - if nothing else, it shows the basic principals to get everything working.