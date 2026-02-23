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
    count(*) as Total_Properties,
    round(avg(price), 2) as Avg_House_Price
from property_price
group by fur_status
order by Avg_House_Price desc;

-- alt version
select 
	p.furnishing_status as Furnishing_Status,
    count(*) as Total_Properties,
    round(avg(l.price), 2) as Avg_Price,
    min(l.price) as Min_Price,
    max(l.price) as Max_Price
from listings l
left join property_attributes p
on l.listing_ID = p.listing_id
group by
	Furnishing_Status
order by
	Avg_Price desc;

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
    
-- alt version
select
	l.city as City,
	p.furnishing_status as Furnishing_Status,
    count(*) as Total_Properties,
    round(avg(l.price), 2) as Avg_Price,
    min(l.price) as Min_Price,
    max(l.price) as Max_Price
from listings l
left join property_attributes p
on l.listing_ID = p.listing_id
group by
	City,
	Furnishing_Status
order by
	City,
	Avg_Price desc;
    
    
    

-- Q4. Do properties closer to metro stations command higher prices?
SELECT
	l.city as City,
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
	City,
    CASE 
        WHEN p.metro_distance <= 10 THEN 'Less Than 10'
        ELSE 'More Than 10'
    END
Order by
	City,
	Avg_Price;
    
-- alt version (currently in use)

SELECT
	CASE
		when p.metro_distance <= 2 then '0-2'
		when p.metro_distance <= 5 && p.metro_distance > 2 then '2-5'
		when p.metro_distance <= 10 && p.metro_distance > 5 then '5-10'
		when p.metro_distance <= 15 && p.metro_distance > 10 then '10-15'
		else '15+'
	END AS Metro_Distance_In_KM,
	
	COUNT(*) AS Total_Properties,
    min(l.price) as Min_Price,
    max(l.price) as Max_Price,
    ROUND(AVG(l.price), 2) AS Avg_Price
	
FROM property_attributes p
INNER JOIN listings l
	ON p.listing_id = l.listing_id

GROUP BY 
	Metro_Distance_In_KM
ORDER BY 
	Min_Price;

-- based on city (currently in use)
SELECT
	l.city as City,
    CASE
        when p.metro_distance <= 2 then '0-2'
        when p.metro_distance <= 5 && p.metro_distance > 2 then '2-5'
        when p.metro_distance <= 10 && p.metro_distance > 5 then '5-10'
        when p.metro_distance <= 15 && p.metro_distance > 10 then '10-15'
        else '15+'
    END AS Metro_Distance_In_KM,
    
    COUNT(*) AS Total_Properties,
    min(l.price) as Min_Price,
    max(l.price) as Max_Price,
    ROUND(AVG(l.price), 2) AS Avg_Price
    
FROM property_attributes p
INNER JOIN listings l
    ON p.listing_id = l.listing_id

GROUP BY 
	City,
    Metro_Distance_In_KM
ORDER BY
	City,
    Min_Price;
    
    
    

-- Q5. Are rented properties priced differently from non-rented ones?

-- only rent status (Currently in use)
select 

	case
		when is_rented is True then 'Yes'
		else 'No'
	end as Property_Rented,
    count(*) as Total_Properties,
    min(l.Price) as Min_Price,
    max(l.Price) as Max_Price,
    round(avg(l.Price), 2) as Avg_Price
    
FROM property_attributes p
INNER JOIN listings l
    ON p.listing_id = l.listing_id
    
group by
	Property_Rented;
    
-- based on furnishing status (Currently in Use)

select 

	case
		when is_rented is True then 'Yes'
		else 'No'
	end as Property_Rented,
    p.Furnishing_Status as Furnishing_Status,
    count(*) as Total_Properties,
    min(l.Price) as Min_Price,
    max(l.Price) as Max_Price,
    round(avg(l.Price), 2) as Avg_Price
    
FROM property_attributes p
INNER JOIN listings l
    ON p.listing_id = l.listing_id
    
group by
	Furnishing_Status,
	Property_Rented
order by
	Property_Rented,
    Avg_Price;

     


-- Q6. How do bedrooms and bathrooms affect pricing?

-- Only bedroom (Currently in Use)
select 

	p.Bedroom as Bedroom_Count,
    count(*) as Total_Properties,
    min(l.price) as Min_Price,
    max(l.price) as Max_Price,
    round(avg(l.price), 2) as Avg_Price
    
FROM property_attributes p
INNER JOIN listings l
    ON p.listing_id = l.listing_id
    
group by
	Bedroom_Count
order by
	bedroom_count;
    
-- only bathroom (Currently in Use)
select 

	p.bathroom as Bathroom_Count,
    count(*) as Total_Properties,
    min(l.price) as Min_Price,
    max(l.price) as Max_Price,
    round(avg(l.price), 2) as Avg_Price
    
FROM property_attributes p
INNER JOIN listings l
    ON p.listing_id = l.listing_id

group by
	Bathroom_Count
order by
	Bathroom_Count;

-- both bedroom and bathroom (Currently in Use)
select

	p.bedroom as Bedroom_Count,
    p.bathroom as Bathroom_Count,
    count(*) as Total_Properties,
    min(l.price) as Min_Price,
    max(l.price) as Max_Price,
    round(avg(l.price), 2) as Avg_Price

FROM property_attributes p
INNER JOIN listings l
    ON p.listing_id = l.listing_id
    
group by
	bedroom,
    bathroom
order by
	Bedroom_Count,
    Bathroom_Count;
    
    
    
    
-- Q7. Do properties with parking and power backup sell at higher prices?

-- parking only
select
	case
		when p.parking_available is True then 'Yes'
		else 'No'
	end as Parking_Available,
	count(*) as Total_Properties,
	round(avg(l.price), 2) as Avg_Price,
	min(l.price) as Min_Price,
	max(l.price) as Max_Price
FROM property_attributes p
INNER JOIN listings l
	ON p.listing_id = l.listing_id
group by
	Parking_Available
order by
	Avg_Price desc;
    
-- power backup only
select
	
	case
		when p.power_backup is True then 'Yes'
        else 'No'
	end as Power_Backup_Available,
    count(*) as Total_Properties,
    round(avg(l.price), 2) as Avg_Price,
    min(l.price) as Min_Price,
    max(l.price) as Max_Price
FROM property_attributes p
INNER JOIN listings l
    ON p.listing_id = l.listing_id
group by
	Power_Backup_Available
order by
	Avg_Price desc;
    
-- both parking and power together (Currently in Use)

select

	case
			when p.parking_available is True then 'Yes'
			else 'No'
		end as Parking_Available,
	case
		when p.power_backup is True then 'Yes'
        else 'No'
	end as Power_Backup_Available,
    count(*) as Total_Properties,
    round(avg(l.price), 2) as Avg_Price,
    min(l.price) as Min_Price,
    max(l.price) as Max_Price
	
FROM property_attributes p
INNER JOIN listings l
    ON p.listing_id = l.listing_id
    
group by
	Parking_Available,
    Power_Backup_Available
order by
	Parking_Available,
    Power_Backup_Available;

-- both parking and power together based on city
select 
	l.city as City,
    case
		when p.parking_available is True then 'Yes'
        else 'No'
	end as Parking_Available,
    case
		when p.power_backup is True then 'Yes'
        else 'No'
	end as Power_Backup,
    count(*) as Total_Properties,
    round(avg(l.price), 2) as Avg_Price,
    min(l.price) as Min_Price,
    max(l.price) as Max_Price
FROM property_attributes p
INNER JOIN listings l
    ON p.listing_id = l.listing_id
group by
	City,
    Parking_Available,
    Power_Backup
order by
	City,
    Parking_Available,
    Power_Backup;
    
-- Q8. How does year built influence listing price?
select

	p.Year_Built as Year_Built,
    count(*) as Total_Properties,
    round(avg(l.Price), 2) as Avg_Price,
    min(l.Price) as Min_Price,
    max(l.Price) as Max_Price
    
FROM property_attributes p
INNER JOIN listings l
    ON p.listing_id = l.listing_id
    
group by
	Year_Built
order by
	Year_Built;

