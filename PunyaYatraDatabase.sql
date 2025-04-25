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
 

create table restaurant_booking(name varchar(40) ,restaurant_name varchar(50),restaurant_location varchar(50),email varchar(30),date_of_booking date,time_of_booking time,total_people int,total_table int);

select * from restaurant_booking;



create table hotel_booking(name varchar(40),
hotel_name varchar(50),hotel_location varchar(50),
email varchar(30),
room_type varchar(20),
ac_type varchar(10),
total_people int,total_room int,
reporting_date date,reporting_time time,
exit_date date,exit_time time);

select * from hotel_booking;
