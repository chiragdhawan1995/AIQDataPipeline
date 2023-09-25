create schema aiq_sales;

create table aiq_sales.users_sales(
order_id bigint,
customer_id bigint,
product_id bigint,
quantity integer,
price float,
order_date date,
name varchar(250),
username varchar(255),
email varchar(255),
lat float,
lng float,
temp float,
weather_desc varchar(100)
);


create table aiq_sales.sales_per_customer
(
customer_id bigint,
total_sale float
);

create table aiq_sales.total_orders_per_product
(
product_id bigint,
total_orders integer
);

create table aiq_sales.product_sales
(
product_id bigint,
sales_count integer
);

create table aiq_sales.sale_per_month
(
sale_year integer,
sale_month integer,
total_sale float
);

create table aiq_sales.avg_sale_per_weather
(
weather_desc varchar(200),
avg_sale float
);