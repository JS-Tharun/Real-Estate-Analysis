-- SQLBook: Code
show databases;

use real_estate;

select * from agents;
select * from buyers;
select * from listings;
select * from property_attributes;
select * from sales;

-- Property & Pricing Analysis
-- Q1. What is the average listing price by city?
select
	City,
	round(avg(Price), 2)
from listings
group by City;

-- Q2. What is the average price per square foot by property type?
with price_sqft as (
select 
	property_type,
    round(sum(price), 2) as total_price,
    round(sum(sqft), 2) as total_sqft
from listings
group by property_type)
select 
	property_type,
    round((total_price/total_sqft), 2) as price_per_sqft
from price_sqft;

-- Q3. How does furnishing status impact property prices?
with property_price as 
(select 
	l.listing_id,
    l.property_type as property_type,
    l.price as price,
    l.sqft,
    p.furnishing_status as fur_status,
    p.attribute_id
from listings l
left join property_attributes p
on l.listing_ID = p.listing_id)
select
	fur_status as Furnishing_Status,
    round(avg(price), 2) as Avg_House_Price
from property_price
group by fur_status
order by Avg_House_Price desc;

-- avg price based on city as well

with cost_table as(
select
    p.furnishing_status as fur_stat,
    l.city as city,
    l.price as price
from property_attributes p
inner join listings l
on p.listing_id=l.listing_id)
select
	city,
	fur_stat,
    round(avg(price), 2) as avg_price
from cost_table
group by
	city,
    fur_stat
order by
	city,
    fur_stat;

-- Q4. Do properties closer to metro stations command higher prices?
SELECT
    CASE 
        WHEN p.metro_distance <= 10 THEN 'Less Than 10'
        ELSE 'More Than 10'
    END AS Distance_KM,
    
    COUNT(*) AS Total_Properties,
    ROUND(AVG(p.metro_distance), 2) AS Avg_Distance,
    ROUND(AVG(l.price), 2) AS Avg_Price

FROM property_attributes p
INNER JOIN listings l
    ON p.listing_id = l.listing_id

GROUP BY 
    CASE 
        WHEN p.metro_distance <= 10 THEN 'Less Than 10'
        ELSE 'More Than 10'
    END;


