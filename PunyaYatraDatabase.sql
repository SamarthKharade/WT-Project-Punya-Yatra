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

create table travel(SourcePlace varchar(20),
DestinationPlace varchar(20),TravelType varchar(10),
Travel_Name varchar(30),Travel_Time varchar(40),Price int);

insert into travel(SourcePlace,DestinationPlace,TravelType,Travel_name,Travel_Time,Price) values('Pune','Akkalkot','Train','Vande Bharat Express','12:00 PM - 4:00 PM','2500');
insert into travel(SourcePlace,DestinationPlace,TravelType,Travel_name,Travel_Time,Price) values('Pune','Akkalkot','Train','Rajdhani Express','4:00 PM - 8:00 PM','2000'),
('Pune','Shirdi','Train','Shatabdi Express','10:00 AM - 2:00 PM','1500'),
('Pune','Pandharpur','Train','Duronto Express"','6:00 AM - 10:00 AM','1800'),
('Pune','Tuljapur','Train','Shatabdi','9:00 AM - 1:00 PM','1000');

insert into travel(SourcePlace,DestinationPlace,TravelType,Travel_name,Travel_Time,Price) values('Pune','Akkalkot','Train','Rajdhani Express','4:00 PM - 8:00 PM','2000'),
('Pune','Shirdi','Train','Shatabdi Express','10:00 AM - 2:00 PM','1500'),
('Pune','Pandharpur','Train','Duronto Express"','6:00 AM - 10:00 AM','1800'),
('Pune','Tuljapur','Train','Shatabdi','9:00 AM - 1:00 PM','1000');

insert into travel(SourcePlace,DestinationPlace,TravelType,Travel_name,Travel_Time,Price) values('Pune','Akkalkot','Bus','VRL Travels','9:00 AM - 1:00 PM','700'),
('Pune','Shirdi','Bus','KSRTC','8:00 AM - 12:00 PM','600'),
('Pune','Shirdi','Bus','SRS Travels','6:00 PM - 10:00 PM','800'),
('Pune','Pandharpur','Bus','Neeta Travels','5:00 PM - 9:00 PM','850'),
('Pune','Tuljapur','Bus','KPN Travels','7:00 AM - 11:00 AM','750');
select * from travel;