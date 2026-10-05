USE  oyo;
SELECT * FROM oyo_city;
select * from oyo_sales1;

-- 1.	Start with some basic EDA - total records , No of Hotels & Total Cities etc.
select count(s.booking_id) as total_record , 
count(distinct c.hotel_id) as number_of_hotel ,count(distinct c.city) as number_of_cities
 from oyo_city c
 join oyo_sales1 s
 on c.hotel_id = s.hotel_id;
 
-- 2.	No of  hotels in different cities
select city, count(hotel_id) as no_of_hotels_in_this_city
from oyo_city 
group by city;

-- 3. Average room rates of different cities
select c.city, 
       round(avg(s.amount / (s.no_of_rooms * datediff(s.check_out, s.check_in))), 2) as avg_room_rate_per_day
from oyo_city c
join oyo_sales1 s on c.hotel_id = s.hotel_id
where datediff(s.check_out, s.check_in) > 0
  and s.no_of_rooms > 0
group by c.city;

-- 4.	Cancellation rates of different cities
select c.city,sum(case when s.status ="Cancelled" then 1 else 0 end )*100/count(s.booking_id) as cancellation_rate
from oyo_city c
join oyo_sales1 s
on c.hotel_id=s.hotel_id
group by c.city;


-- 5.	No of bookings of different cities in Jan Feb Mar Months.
select c.city, count(s.booking_id) as no_of_booking
from oyo_city c
join oyo_sales1 s                                 
on c.hotel_id=s.hotel_id
where month(s.date_of_booking) in (1,2,3)
group by c.city;

-- 6.	What is the total number of bookings and the average number of rooms per booking?
select count(booking_id) as no_of_booking ,
      avg(no_of_rooms)as avg_no_rooms_per_booking 
from oyo_sales1;

-- 7.	What are the top 5 cities with the highest number of bookings?
select c.city,count(s.booking_id) as no_booking
from oyo_city c
join oyo_sales1 s                             
on c.hotel_id=s.hotel_id
group by c.city
order by no_booking desc
limit 5 ;

-- 8.	How do bookings distribute across different statuses (e.g., confirmed, canceled, pending)?
select status,
    count(booking_id) as total_bookings
from oyo_sales1
group by status;

-- 9.	What is the total revenue generated and the total discount given?-------------------------------------------
select hotel_id,sum(amount) as total_revenue ,
 sum(discount) as total_discount
from oyo_sales1
group by hotel_id;

-- 10. Total revenue and total discount per city
select c.city,
       round(sum(s.amount), 2) as total_revenue,
       round(sum(s.discount), 2) as total_discount,
       round(sum(s.discount) * 100 / sum(s.amount), 2) as discount_percentage
from oyo_city c
join oyo_sales1 s on c.hotel_id = s.hotel_id
group by c.city;

-- 11.	How many bookings were for single rooms vs. multiple rooms?
with cte as (select 
case 
when no_of_rooms = 1 then "single_room"
else "multiple_room"
end as room_type
from oyo_sales1)
select room_type,Count(room_type)
from cte 
group by room_type;

-- 12.	What is the average length of stay (in days) for bookings?
select avg(datediff(check_out, check_in)) as avg_length_of_stay
from oyo_sales1;

-- 13.	Which customers have made the most bookings (top 10 by booking count)?
select customer_id, count(booking_id) as no_of_bookings
from oyo_sales1
group by  customer_id
order by no_of_bookings desc
limit 10;

-- 14.	What is the average discount percentage applied to bookings?
select avg(discount/amount*100) as avg_dis_percent
from oyo_sales1;