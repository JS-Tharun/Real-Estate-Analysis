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

-- Q4. Do properties closer to metro stations command higher prices?
select 
	*
from listings l
inner join property_attributes p
on p.listing_id = l.listing_id
order by metro_distance;

