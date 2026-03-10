from numpy import True_
import streamlit as st
from utils.utils import execute_query

st.set_page_config(
    page_title="Query Statements",
    layout='wide'
)

st.title("Query Statements")

tab_property_pricing, tab_sales_market, tab_agent_performance, tab_buyer = st.tabs(["Property & Pricing Analysis", "Sales & Market Performance", "Agent Performance", "Buyer & Financing Behavior"])

with tab_property_pricing:
    queries = {
        "1. What is the average listing price by city?": "select City, round(avg(Price), 2) as Avg_Price from listings group by City order by City",

        "2. What is the average price per square foot by property type?": "select Property_Type, round(avg(Price_Per_Sqft), 2) as Avg_Price_Per_Sqft from (select Property_Type, (price/sqft) as Price_Per_Sqft from listings) T group by Property_Type order by Avg_Price_Per_Sqft",

        "3. How does furnishing status impact property prices?": "select p.furnishing_status as Furnishing_Status, count(*) as Total_Properties, round(avg(l.price), 2) as Avg_Price, min(l.price) as Min_Price, max(l.price) as Max_Price from listings l left join property_attributes p on l.listing_ID = p.listing_id group by Furnishing_Status order by Avg_Price",

        "4. Do properties closer to metro stations command higher prices?" : 
        
        """
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
        """,

        "5. Are rented properties priced differently from non-rented ones?" : """
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
        """,

        "6. How do bedrooms and bathrooms affect pricing?" : """
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
        """,

        "7. Do properties with parking and power backup sell at higher prices?" : """
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
                Avg_Price;
        """,

        "8. How does year built influence listing price?" : """
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
        """,

        "9. Which cities have the highest median property prices?" : """
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
        """,

        "10. How are properties distributed across price buckets?" : """
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
        """

    }

    with st.container(border=True):
        selected_query = st.selectbox(
            label="Choose a Query",
            options= list(queries.keys()),
            index=None,
            placeholder="Select Query"
        )   
    
        st.write("Query Result")
        if selected_query != None:
            result_df = execute_query(queries[selected_query])
            st.dataframe(result_df)
        else:
            st.caption("No Query Selected")

with tab_sales_market:
    queries = {
        "1. What is the average days on market by city?" : """
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
        """,

        "2. Which property types sell the fastest?" : """
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
        """,

        "3. What percentage of properties are sold above listing price?" : """
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
        """,

        "4. What is the sale-to-list price ratio by city?" : """
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
        """,

        "5. Which listings took more than 90 days to sell?" : """
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
        """,

        "6. How does metro distance affect time on market?" : """
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
        """,

        "7. What is the monthly sales trend?" : """
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
        """,
        
        "8. Which properties are currently unsold?" : """
            select 
                l.Listing_ID,
                l.City,
                l.Property_Type,
                l.Date_Listed
            from listings l
            left join sales s
            on l.Listing_ID = s.Listing_ID
            where s.Sale_Price is NULL;
        """
    }

    with st.container(border=True):
        selected_query = st.selectbox(
            label="Choose a Query",
            options= list(queries.keys()),
            index=None,
            placeholder="Select Query"
        )

        st.write("Query Result")
        if selected_query != None:
            result_df = execute_query(queries[selected_query])
            st.dataframe(result_df)
        
        else:
            st.caption("No Query Selected")

with tab_agent_performance:
    queries = {
        "1. Which agents have closed the most sales?" : """
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
        """,

        "2. Who are the top agents by total sales revenue?" : """
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
        """,

        "3. Which agents close deals fastest?" : """
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
        """,

        "4. Does experience correlate with deals closed?" : """
            select 
                Years_Of_Experience,
                count(*) as Num_Of_Agents,
                round(avg(Deals_Closed), 0) as Avg_Deals_Closed
            from agents
            group by Years_Of_Experience
            order by Years_Of_Experience;

        """,
        "5. Do agents with higher ratings close deals faster?" : """
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
        """,

        "6. What is the average commission earned by each agent?" : """
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
        """,

        "7. Which agents currently have the most active listings?" : """
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
        """
    }

    with st.container(border=True):
        selected_query = st.selectbox(
            label="Choose a Query",
            options= list(queries.keys()),
            index=None,
            placeholder="Select Query"
        )

        st.write("Query Result")
        if selected_query != None:
            result_df = execute_query(queries[selected_query])
            st.dataframe(result_df)

        else:
            st.caption("No Query Selected")


with tab_buyer:
    queries = {
        "1. What percentage of buyers are investors vs end users?" : """
            select 
                Buyer_Type,
                round((100 * count(*) / (select count(*) from buyers)), 2) as Percentage
            from buyers
            group by
                Buyer_Type;
        """,

        "2. Which cities have the highest loan uptake rate?" : """
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
        """,
        "3. What is the average loan amount by buyer type?" : """
            select
                Buyer_Type,
                round(avg(Loan_Amount), 2) as Avg_Loan_Amount
            from buyers
            where loan_taken = True
            group by
                Buyer_Type;
        """,
        "4. Which payment mode is most commonly used?" : """
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
        """,
        "5. Do loan-backed purchases take longer to close?" : """
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
        """
    }

    with st.container(border=True):
        selected_query = st.selectbox(
            label="Choose a Query",
            options= list(queries.keys()),
            index=None,
            placeholder="Select Query"
        )

        st.write("Query Result")
        if selected_query != None:
            result_df = execute_query(queries[selected_query])
            st.dataframe(result_df)

        else:
            st.caption("No Query Selected")