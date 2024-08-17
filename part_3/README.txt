1) install postgreSQL
2) brew services start postgresql -> start the server
3) psql postgres -> access postreSQL terminal
4)
create database mydatabase;
create user myuser with password 'mypassword';
grant all privileges on database mydatabase to myuser;
\q
5) launch create_database.py to create the table
6) launch read_database.py to check that the table exists and prints the 5 first lines
