create user webdev@localhost identified by 'phprocks';
create database webdev;
use webdev;

create table users
(
	username varchar(10) primary key,
	password char(64)
);

create table payinfo
(
	username varchar(10) primary key,
	cardnumber char(16),
	expiremonth char(3),
	expireyear int(2),
	ccv int(3),

	foreign key(username) references users(username),
	check (expiremonth in('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'))
);

create table food
(
	menunumber int primary key AUTO_INCREMENT,
	name varchar(30),
	description varchar(400),
	price float,
	picture varchar(30) unique
);

create table orders
(
	orderno int primary key AUTO_INCREMENT,
	username varchar(10),
	items_ordered varchar(999),
	total float,
	placed timestamp DEFAULT CURRENT_TIMESTAMP,
	fulfilled boolean,

	foreign key(username) references users(username)
);

create table address
(
	username varchar(10),
	line1 varchar(100),
	line2 varchar(100),
	town varchar(30),
	eircode varchar(7),

	foreign key(username) references users(username)
);

create view valid_orders as select * from orders join address using (username) join payinfo using (username);

grant all on webdev.* to webdev@localhost;
