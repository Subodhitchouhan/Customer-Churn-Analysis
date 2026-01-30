-- Create a new database named 'db_Churn'
CREATE DATABASE db_Churn
use db_Churn
Select * from stg_Churn -- This will Display all records from the stg_Churn table


-- DATA EXPLORATION QUERIES 


 -- This query groups the records in the stg_Churn table by the gender column and counts the number of occurrences of each
 -- It also calculates the percentage
 -- count(*) will 
SELECT Gender, Count(Gender) as TotalCount,
Count(Gender) * 100.0 / (Select Count(*) from stg_Churn)  as Percentage
from stg_Churn
Group by Gender

-- This query groups the records in the stg_Churn table by the Contract column and counts the number of occurrences of each
-- It also calculates the percentage
SELECT Contract, Count(Contract) as TotalCount,
Count(Contract) * 100.0 / (Select Count(*) from stg_Churn)  as Percentage
from stg_Churn
Group by Contract

-- This query groups the records in the stg_Churn table by the Customer_Status column and counts the number of occurrences of each
-- It also calculates the total revenue and revenue percentage for each customer status
-- total revenue percentage is calculated by dividing the total revenue for each customer status by the overall total revenue
SELECT Customer_Status, Count(Customer_Status) as TotalCount, Sum(Total_Revenue) as TotalRev,
Sum(Total_Revenue) / (Select sum(Total_Revenue) from stg_Churn) * 100  as RevPercentage
from stg_Churn
Group by Customer_Status


-- This query groups the records in the stg_Churn table by the State column and counts the number of occurrences of each
-- It also calculates the percentage
-- count(*) will give total number of records in the table
-- Multiplying by 100.0 to get percentage value
-- Ordering the result in descending order based on percentage
SELECT State, Count(State) as TotalCount,
Count(State) * 100.0 / (Select Count(*) from stg_Churn)  as Percentage
from stg_Churn
Group by State
Order by Percentage desc


-- This query retrieves distinct values from the Internet_Type column in the stg_Churn table
-- This helps to identify all unique types of internet services used by customers
SELECT DISTINCT Internet_Type from stg_Churn


-- EXPLORE AND CLEAN :
-- Find Null values in each column and remove null as per the column values 

-- 1.) Data Exploration – Check Nulls

/* DATA QUALITY CHECK: NULL COUNTS
   This query scans the 'stg_Churn' table and counts how many missing 
   (NULL) values exist for every single column.
*/

SELECT 
    /* The pattern used for every column is:
       1. CASE WHEN [Column] IS NULL THEN 1 ELSE 0 END 
          -> This turns every NULL into a 1 and every valid value into a 0.
       2. SUM(...) 
          -> This adds up all those 1s to give you the total count of missing values.
    */

    -- Demographic Info Null Checks
    SUM(CASE WHEN Customer_ID IS NULL THEN 1 ELSE 0 END) AS Customer_ID_Null_Count,
    SUM(CASE WHEN Gender IS NULL THEN 1 ELSE 0 END) AS Gender_Null_Count,
    SUM(CASE WHEN Age IS NULL THEN 1 ELSE 0 END) AS Age_Null_Count,
    SUM(CASE WHEN Married IS NULL THEN 1 ELSE 0 END) AS Married_Null_Count,

    -- Location and Relationship Checks
    SUM(CASE WHEN State IS NULL THEN 1 ELSE 0 END) AS State_Null_Count,
    SUM(CASE WHEN Number_of_Referrals IS NULL THEN 1 ELSE 0 END) AS Number_of_Referrals_Null_Count,
    SUM(CASE WHEN Tenure_in_Months IS NULL THEN 1 ELSE 0 END) AS Tenure_in_Months_Null_Count,

    -- Services and Features Checks
    -- (Checks if any service flags like Phone, Internet, or Security are missing)
    SUM(CASE WHEN Value_Deal IS NULL THEN 1 ELSE 0 END) AS Value_Deal_Null_Count,
    SUM(CASE WHEN Phone_Service IS NULL THEN 1 ELSE 0 END) AS Phone_Service_Null_Count,
    SUM(CASE WHEN Multiple_Lines IS NULL THEN 1 ELSE 0 END) AS Multiple_Lines_Null_Count,
    SUM(CASE WHEN Internet_Service IS NULL THEN 1 ELSE 0 END) AS Internet_Service_Null_Count,
    -- ... [Logic repeats for all service columns like Online_Security, Streaming_TV, etc.]

    -- Financial and Billing Checks
    SUM(CASE WHEN Monthly_Charge IS NULL THEN 1 ELSE 0 END) AS Monthly_Charge_Null_Count,
    SUM(CASE WHEN Total_Charges IS NULL THEN 1 ELSE 0 END) AS Total_Charges_Null_Count,
    SUM(CASE WHEN Total_Revenue IS NULL THEN 1 ELSE 0 END) AS Total_Revenue_Null_Count,

    -- Churn Outcome Checks
    -- (Note: These might have high NULL counts naturally if a customer hasn't churned yet)
    SUM(CASE WHEN Customer_Status IS NULL THEN 1 ELSE 0 END) AS Customer_Status_Null_Count,
    SUM(CASE WHEN Churn_Category IS NULL THEN 1 ELSE 0 END) AS Churn_Category_Null_Count,
    SUM(CASE WHEN Churn_Reason IS NULL THEN 1 ELSE 0 END) AS Churn_Reason_Null_Count

FROM stg_Churn;



-- 2.) Remove null and insert the new data into Prod table

/* DATA TRANSFORMATION & TABLE CREATION
   This script performs an 'ETL' (Extract, Transform, Load) process.
   It creates a new table 'prod_Churn' based on 'stg_Churn'.
*/

SELECT 
    -- 1. Pass-through Columns (These are kept as-is)
    Customer_ID,
    Gender,
    Age,
    Married,
    State,
    Number_of_Referrals,
    Tenure_in_Months,

    /* 2. Data Cleaning (Handling NULLs)
       ISNULL(Column, 'Default') checks if a value is missing.
       If missing, it replaces it with the specified string.
    */
    ISNULL(Value_Deal, 'None') AS Value_Deal, -- Replaces NULL deals with 'None'
    Phone_Service,
    ISNULL(Multiple_Lines, 'No') As Multiple_Lines, -- Defaults to 'No' if missing
    Internet_Service,
    ISNULL(Internet_Type, 'None') AS Internet_Type,
    
    -- Filling 'No' for all optional add-on services
    ISNULL(Online_Security, 'No') AS Online_Security,
    ISNULL(Online_Backup, 'No') AS Online_Backup,
    ISNULL(Device_Protection_Plan, 'No') AS Device_Protection_Plan,
    ISNULL(Premium_Support, 'No') AS Premium_Support,
    ISNULL(Streaming_TV, 'No') AS Streaming_TV,
    ISNULL(Streaming_Movies, 'No') AS Streaming_Movies,
    ISNULL(Streaming_Music, 'No') AS Streaming_Music,
    ISNULL(Unlimited_Data, 'No') AS Unlimited_Data,

    -- Financial columns (Kept as-is)
    Contract,
    Paperless_Billing,
    Payment_Method,
    Monthly_Charge,
    Total_Charges,
    Total_Refunds,
    Total_Extra_Data_Charges,
    Total_Long_Distance_Charges,
    Total_Revenue,

    -- Categorizing Churn logic
    Customer_Status,
    -- If no churn category/reason exists (Active customers), label as 'Others'
    ISNULL(Churn_Category, 'Others') AS Churn_Category,
    ISNULL(Churn_Reason, 'Others') AS Churn_Reason

/* 3. INTO Clause:
   This creates the 'prod_Churn' table automatically and inserts 
   the transformed data into it.
*/
INTO [db_Churn].[dbo].[prod_Churn]

-- 4. FROM Clause: The source raw data table.
FROM [db_Churn].[dbo].[stg_Churn];

Select * from prod_Churn;


 
 
 -- Create View for Power BI :


/* DATA SEGMENTATION USING VIEWS : These commands create virtual layers over your 'prod_Churn' table 
                                   to separate historical data from new customer data.
*/

-- 1. Create a View for Analysis (Churn vs. Retention)
/* 
This filter excludes new 'Joined' customers. It focuses only on customers who have been with the company  long enough to either stay or leave.
*/

CREATE VIEW vw_ChurnData AS
SELECT * FROM prod_Churn  
WHERE Customer_Status IN ('Churned', 'Stayed');

-- 2. Create a View for Onboarding (New Customers)
/* 
This filter captures only the newest members. These are usually excluded from churn rate calculations because they haven't had time to churn yet.
*/

CREATE VIEW vw_JoinData AS
SELECT * FROM prod_Churn 
WHERE Customer_Status = 'Joined';