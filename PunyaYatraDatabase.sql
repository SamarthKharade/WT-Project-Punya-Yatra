create database punyayatra;
use punyayatra;


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    gender VARCHAR(10),
    age INT,
    countrycode VARCHAR(5),
    mobile VARCHAR(15),
    email VARCHAR(100),
    address TEXT,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(100)
);


select * from users;


create table restaurant_booking(name varchar(40) ,date_of_booking date,time_of_booking time,total_people int,total_table int);

select * from restaurant_booking;



