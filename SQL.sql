-- SQLBook: Code
show databases;

use real_estate;

-- Property & Pricing Analysis
-- Q1. What is the average listing price by city? (Currently in Use)
select
    City,
    round(avg(Price), 2) 
from listings
group by City
order by City;

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
  from price_sqft
  order by Price_Per_Sqft;
  
-- Updated Code (Currently in Use)
select
	Property_Type,
    round(avg(Price_Per_Sqft), 2) as Avg_Price_Per_Sqft
from
	(select
		Property_Type,
		(price/sqft) as Price_Per_Sqft
	from listings) T
group by
	Property_Type;

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
	case Metro_Distance_In_KM
		when '0-2' then 1
        when '2-5' then 2
		when '5-10' then 3
        when '10-15' then 4
        when '15+' then 5
	end;
    
-- based on city 
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
    case Metro_Distance_In_KM
		when '0-2' then 1
        when '2-5' then 2
		when '5-10' then 3
        when '10-15' then 4
        when '15+' then 5
	end;
    
    
    

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
    Furnishing_Status desc;

     


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
    
    
    
    
    
-- Q8. How does year built influence listing price? (Currently in Use)
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
    
    
    
    
    
-- Q9. Which Cities have the higest median property prices? (Currently in Use)

select
	City,
	round(avg(Price), 2) as Median_Price
from
	(select
		City,
		Price,
		row_number() over (
			partition by city
			order by price
		) as Row_Num,
		count(*) over (
			partition by city
		) as Total_Count
	from listings) T
where row_num in (
	Floor((Total_Count + 1) / 2),
    Floor((Total_Count + 2) / 2)
)
group by
	City
order by
	City;
    
    
    
    
-- Q10. How are properties distributed across price buckets? (Currently in Use)
select 
	
	T3.Price_Bucket,
    T3.Total_Properties,
    T3.Avg_Price,
    T3.Min_Price,
    T3.Max_Price,
    T2.Top_Property_Type as Top_Property_Type,
    T2.Property_Count as Top_Property_Count
    
from
	(select
			Price_Bucket,
			Property_Type as Top_Property_Type,
			Property_Count
	from
		(select
			CASE
				WHEN price >= 100000 AND price < 500000 THEN '100K - 500K'
				WHEN price >= 500000 AND price < 1000000 THEN '500K - 1M'
				WHEN price >= 1000000 AND price < 2000000 THEN '1M - 2 M'
				WHEN price >= 2000000 AND price < 3000000 THEN '2M - 3M'
				WHEN price >= 3000000 AND price < 4000000 THEN '3M - 4M'
				WHEN price >= 4000000 AND price < 5000000 THEN '4M - 5M'
			END AS Price_Bucket,
			property_type,
			count(*) as Property_Count,
			row_number() over(
				partition by
					CASE
						WHEN price >= 100000 AND price < 500000 THEN '100K - 500K'
						WHEN price >= 500000 AND price < 1000000 THEN '500K - 1M'
						WHEN price >= 1000000 AND price < 2000000 THEN '1M - 2 M'
						WHEN price >= 2000000 AND price < 3000000 THEN '2M - 3M'
						WHEN price >= 3000000 AND price < 4000000 THEN '3M - 4M'
						WHEN price >= 4000000 AND price < 5000000 THEN '4M - 5M'
					END 
					order by count(*) desc
			) as Row_Num
		from listings
		group by
			Price_Bucket,
			Property_Type) T1
	where Row_Num = 1) T2
	inner join
		(
			SELECT

				CASE
					WHEN price >= 100000 AND price < 500000 THEN '100K - 500K'
					WHEN price >= 500000 AND price < 1000000 THEN '500K - 1M'
					WHEN price >= 1000000 AND price < 2000000 THEN '1M - 2 M'
					WHEN price >= 2000000 AND price < 3000000 THEN '2M - 3M'
					WHEN price >= 3000000 AND price < 4000000 THEN '3M - 4M'
					WHEN price >= 4000000 AND price < 5000000 THEN '4M - 5M'
				END AS Price_Bucket,
				count(*) as Total_Properties,
				round(avg(price), 2) as Avg_Price,
				MIN(price) AS Min_Price,
				MAX(price) AS Max_Price
				
			FROM listings
			GROUP BY Price_Bucket
			ORDER BY
				CASE Price_Bucket
					WHEN '100K - 500K' THEN 1
					WHEN '500K - 1M' THEN 2
					WHEN '1M - 2 M' THEN 3
					WHEN '2M - 3M' THEN 4
					WHEN '3M - 4M' THEN 5
					WHEN '4M - 5M' THEN 6
				END
		) T3
on T2.Price_Bucket = T3.Price_Bucket
order by
CASE T3.Price_Bucket
	WHEN '100K - 500K' THEN 1
	WHEN '500K - 1M' THEN 2
	WHEN '1M - 2 M' THEN 3
	WHEN '2M - 3M' THEN 4
	WHEN '3M - 4M' THEN 5
	WHEN '4M - 5M' THEN 6
END;





-- Sales & Market Performance Analysis

-- Q11. What is the average days on market by city? (Currently in Use)
select
    l.City,
    round(avg(s.Days_On_Market), 0) as Avg_Days_On_Market
from sales s
inner join listings l
on s.Listing_ID = l.Listing_ID
group by
	l.City
order by
	City;
    
    
    
    
    
-- Q12. Which property types sell the fastest? (Currently in Use)
select
	l.Property_Type,
    round(avg(s.Days_On_Market), 0) as Avg_Days_On_Sale,
    min(s.Days_On_Market) as Min_Days_On_Market,
    max(s.Days_On_Market) as Max_Days_On_Market
from sales s
inner join listings l
on s.Listing_ID = l.Listing_ID
group by
	l.Property_Type
order by
	Avg_Days_On_Sale;
    
    
    
    
    
-- Q13. What percentage of properties are sold above listing price? (Currently in use)
select
	case 
		when s.Sale_Price > l.Price then 'Above Listed Price'
        when s.Sale_Price <= l.Price then 'Equal and Below Listed Price'
	end as Property_Sold_At,
	count(*) as Property_Count,
    round(( 100 * count(*)) / (select count(*) as Total_Properties
		from sales s
		inner join listings l
		on s.Listing_ID = l.Listing_ID), 2) Percentage_Sold
from sales s
inner join listings l
on s.Listing_ID = l.Listing_ID
group by
	Property_Sold_At;
    
    
    
    
    
-- Q14. What is the sale-to-list price ratio by city? 
with Price_Table as (select
	l.City,
	avg(s.Sale_Price) as Avg_Sale_Price,
    avg(l.Price) as Avg_List_Price
from sales s
inner join listings l
on s.Listing_ID = l.Listing_ID
group by
	City)
select
	City,
    round(Avg_Sale_Price/Avg_List_Price, 4) as Sale_To_List_Price_Ratio
from Price_Table
order by
	City;
    
-- updated code (Currently in Use)
select
	city,
    round(avg(ratio), 4) as Sale_To_List_Price_Ratio
from
(select 
	City,
	l.Price,
    s.Sale_Price,
    (s.Sale_Price/l.Price) as ratio
from 
	sales s
inner join listings l
on s.Listing_ID = l.Listing_ID) T
group by
	city;
    
    
    
    
    
-- Q15. Which listings took more than 90 days to sell? (Currently in Use)
select 
	s.Listing_ID,
    s.Days_On_Market,
    s.Date_Sold,
    l.Date_Listed,
    s.Sale_Price,
    l.Price as Listed_Price,
    l.City,
    l.Property_Type
from sales s
inner join listings l
on s.Listing_ID = l.Listing_ID
where s.Days_On_Market > 90
order by
	Listing_ID;
    



-- Q16. How does metro distance affect time on market? (Currently in Use)
select
	case
		when p.metro_distance < 2 then '0-2'
        when p.metro_distance < 5 && p.metro_distance >= 2 then '2-5'
        when p.metro_distance < 10 && p.metro_distance >= 5 then '5-10'
        when p.metro_distance < 15 && p.metro_distance >= 10 then '10-15'
        when p.metro_distance >= 15 then '15+'
	end as Metro_Distance_In_KM,
    round(avg(s.Days_on_Market), 0) as Avg_Days_On_Market,
    min(s.Days_On_Market) as Min_Days_On_Market,
    max(s.Days_On_Market) as Max_Days_On_Market
from
	sales s
	inner join property_attributes p
	on s.listing_id=p.listing_id
group by
	Metro_Distance_In_KM
order by
	case Metro_Distance_In_KM
		when '0-2' then 1
        when '2-5' then 2
        when '5-10' then 3
        when '10-15' then 4
        when '15+' then 5
	end;
    




-- Q17. What is the monthly sales trend? (Currently in Use)
select
	case
		when Month(Date_Sold) = 1 then 'Jan'
		when Month(Date_Sold) = 2 then 'Feb'
		when Month(Date_Sold) = 3 then 'Mar'
		when Month(Date_Sold) = 4 then 'Apr'
		when Month(Date_Sold) = 5 then 'May'
		when Month(Date_Sold) = 6 then 'Jun'
		when Month(Date_Sold) = 7 then 'Jul'
		when Month(Date_Sold) = 8 then 'Aug'
		when Month(Date_Sold) = 9 then 'Sep'
		when Month(Date_Sold) = 10 then 'Oct'
		when Month(Date_Sold) = 11 then 'Nov'
		when Month(Date_Sold) = 12 then 'Dec'
	end as Month_Sold,
	Year(Date_Sold) as Year_Sold,
    count(*) as Total_Properties_Sold,
    round(sum(Sale_Price), 2) as Total_Sale_Amount,
	round(avg(Sale_Price), 2) as Avg_Sale_Price,
    min(Sale_Price) as Min_Sale_Price,
    max(Sale_Price) as Max_Sale_Price
from sales
group by
	Month_Sold,
    Year_Sold
order by
	year_Sold,
	case Month_Sold
		when 'Jan' then 1
		when 'Feb' then 2
		when 'Mar' then 3
		when 'Apr' then 4
		when 'May' then 5
		when 'Jun' then 6
		when 'Jul' then 7
		when 'Aug' then 8
		when 'Sep' then 9
		when 'Oct' then 10
		when 'Nov' then 11
		when 'Dec' then 12
	end;    
    
    

-- Q18. Which properties are currently unsold? 
-- Property Details (Currently in Use)
select 
	l.Listing_ID,
    l.City,
    l.Property_Type,
    l.Date_Listed
from listings l
left join sales s
on l.Listing_ID = s.Listing_ID
where s.Sale_Price is NULL;

-- Unsold Properties Analysis (Currently in Use)
select
	City,
    Property_Type,
    count(*) as Total_Unsold_Properties
from
(select 
	l.Listing_ID,
    l.City,
    l.Property_Type,
    l.Date_Listed
from listings l
left join sales s
on l.Listing_ID = s.Listing_ID
where s.Sale_Price is NULL) T
group by
	City,
    Property_Type
order by 
	city,
    Property_Type;



-- Agent Performance
-- Q19. Which agents have closed the most sales? (Currently in Use)
select
	*
from(select
	dense_rank() over(
		order by Deals_Closed desc
    ) as Agent_Rank,
	Agent_ID,
    Deals_Closed as Total_Sales,
    Commission_Rate,
    Rating,
    Years_Of_Experience,
    Avg_Closing_Days
from agents) T
where Agent_Rank between 1 and 10;





-- Q20. Who are the top agents by total sales revenue? (Currently in Use)
select
	*
from(select
	dense_rank() over(
		order by sum(s.Sale_Price) desc
    ) as Agent_Rank,
    l.Agent_ID,
    round(sum(s.Sale_Price), 2) as Total_Sales_Amount
from sales s
inner join listings l
on s.Listing_ID=l.Listing_ID
group by
	l.Agent_ID) T
where Agent_Rank between 1 and 10;




-- Q21. Which agents close deals fastest? 
-- top 10 agents with lowest avg closing days (Currently in Use)
select *
from
(select
	dense_rank() over(
		order by Avg_Closing_Days
	) as Agent_Rank,
	Agent_ID,
    Avg_Closing_Days,
    Deals_Closed,
    Commission_Rate,
    Years_Of_Experience,
    Rating
from agents) T
where Agent_Rank between 1 and 10;

-- agents recorded with the lowest closing days (Currently in Use)
select 
    l.Agent_ID,
    s.Days_On_Market as Days_Taken,
    l.Listing_ID,
    l.Date_Listed,
    s.Date_Sold
from listings l
inner join sales s
on l.Listing_ID = s.Listing_ID
where 
	s.Days_On_Market = (select min(Days_On_Market) from sales)
order by 
	l.Date_Listed;

    
-- Q22. Does experience correlate with deals closed?
-- Avg Deals based on yrs of experience (Currently in Use)
select 
	Years_Of_Experience,
    count(*) as Num_Of_Agents,
    round(avg(Deals_Closed), 0) as Avg_Deals_Closed
from agents
group by Years_Of_Experience
order by Years_Of_Experience;

-- Table to for correlation (Currently in Use)
select 
	Years_Of_Experience,
    Deals_Closed
from agents;




-- Q23. Do agents with higher ratings close deals faster? (Currently in Use)
select
    case
		when a.Rating between 1 and 2 then '1-2'
		when a.Rating between 2 and 3 then '2-3'
		when a.Rating between 3 and 4 then '3-4'
		when a.Rating between 4 and 5 then '4-5'
	end as Agent_Rating,
    round(avg(s.Days_On_Market), 0) as Avg_Closing_Days,
    min(s.Days_On_Market) as Lowest_Closing_Days,
    max(s.Days_On_Market) as Highest_Closing_Days,
    count(*) as Agent_Count
from 
	sales s
inner join listings l
on s.Listing_ID = l.Listing_ID
inner join agents a
on l.Agent_ID = a.Agent_ID
group by Agent_Rating;




-- Q24. What is the average commission earned by each agent? (Currently in Use)
select 
    l.Agent_ID,
    round(avg((a.Commission_Rate / 100) * s.Sale_Price), 2) as Avg_Commission_Earned
from sales s
inner join listings l
    on s.Listing_ID = l.Listing_ID
inner join agents a
    on l.Agent_ID = a.Agent_ID
group by l.Agent_ID
order by Avg_Commission_Earned;




-- Q25. Which agents currently have the most active listings? (Currently in Use)
select *
from
	(select
		dense_rank() over(
			order by count(*) desc
		) as Agent_Rank,
		Agent_ID,
		count(*) as Active_Property_Count
	from(
		select l.Agent_ID
		from listings l
		left join sales s
		on l.Listing_ID = s.Listing_ID
		where s.Date_Sold is not NULL) T1
	group by
		Agent_ID
	order by
		Active_Property_Count desc) T2
where Agent_Rank between 1 and 10;






--  Buyer & Financing Behavior
-- Q26. What percentage of buyers are investors vs end users? (Currently in Use)
select 
    Buyer_Type,
    round((100 * count(*) / (select count(*) from buyers)), 2) as Percentage
from buyers
group by
	Buyer_Type;

    
    
    
    
    
-- Q27. Which cities have the highest loan uptake rate? (Currently in Use)
select
	dense_rank() OVER(
		ORDER BY round((100 * (T1.Count) / T2.Total_Buyers), 2) desc
    ) as City_Rank,
	T1.City,
    T1.Count,
    round((100 * (T1.Count) / T2.Total_Buyers), 2) as Percentage
from
	(select 
		l.City,
		b.Loan_Taken,
		count(b.Loan_Taken) as Count
	from 
		buyers b
	inner join
		listings l
	on b.Listing_ID = l.Listing_ID
	group by
		l.City,
		b.Loan_Taken) T1
inner join
	(select
		l.City,
		count(*) as Total_Buyers
	from 
		buyers b
	inner join
		listings l
	on b.Listing_ID = l.Listing_ID
	group by
		l.City) T2
on T1.City = T2.City
where Loan_Taken = True;
    
-- alt version
select
	dense_rank() OVER(
		order by round( 100.0 * sum(case when b.Loan_Taken = TRUE then 1 else 0 end)
        / count(*), 2) desc
    ) as City_Rank,
    l.City,
    sum(case when b.Loan_Taken = TRUE then 1 else 0 end) as Count,
    round(
        100.0 * sum(case when b.Loan_Taken = TRUE then 1 else 0 end)
        / count(*), 2
    ) as Percentage_Loan_Taken
from buyers b
inner join listings l
    on b.Listing_ID = l.Listing_ID
    
group by l.City;




-- Q28. What is the average loan amount by buyer type? (Currently in Use)
select
	Buyer_Type,
    round(avg(Loan_Amount), 2) as Avg_Loan_Amount
from buyers
where loan_taken = True
group by
	Buyer_Type;
    
    
    
    
-- Q29. Which payment mode is most commonly used? (Currently in Use)
select
	dense_rank() over(
		order by (100 * count(*) / (select count(*) from buyers)) desc
    ) as Payment_Method_Rank,
	Payment_Method,
    count(*) as Count,
	(100 * count(*) / (select count(*) from buyers)) as Percentage
from buyers
group by
	Payment_Method;
    
    
    
    
-- Q30. Do loan-backed purchases take longer to close? (Currently in Use)
select
	case
		when b.Loan_Taken = True then 'Yes'
		when b.Loan_Taken = False then 'No'
	end as Loan_Taken,
    count(*) as Count,
    round(avg(s.Days_On_Market), 0) as Avg_Days_On_Market,
    min(s.Days_On_Market) as Lowest_Days_On_Market,
    max(s.Days_On_Market) as Highest_Days_On_Market,
    round(stddev(s.Days_On_Market), 2) as Std_Deviation
from sales s
inner join
	buyers b
on s.Listing_ID = b.Listing_ID
group by
	b.Loan_Taken
order by
	Avg_Days_On_Market desc;
