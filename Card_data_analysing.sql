SELECT * FROM data_analysis.cards;
-- CLEANING THE TABLE SEEING IF THERE ARE ANY OUTLIERS OR MISSING VALUES,
-- Are there any NULL values in critical columns like card_number, expires, client_id, or credit_limit? How will you handle them?
SELECT * FROM data_analysis.cards
WHERE card_number IS NULL OR expires IS NULL OR client_id IS NULL OR credit_limit IS NULL;

-- Validate Data Formats
-- is the expires column in a valid date format (e.g., YYYY-MM)?
-- Are year_pin_last_changed and acct_open_date in appropriate date formats?
select*from data_analysis.cards
 WHERE expires NOT LIKE '____-__';
 
 --  Detecting Outliers
 -- Are values for numeric fields like credit_limit and num_cards_issued reasonable?
-- Is year_pin_last_changed realistic?

select * from data_analysis.cards
where credit_limit > 0
or cvv >0
or card_number >0
or client_id > 0 
or id > 0
or num_cards_issued >0 
or year_pin_last_changed > YEAR(CURDATE());

--  Identifying Duplicate Records
-- Are there duplicate entries for critical fields like client_id or card_number?
SELECT client_id, COUNT(*) AS duplicate_count
FROM data_analysis.cards
GROUP BY client_id
HAVING COUNT(*) > 1;
-- after running this we find duplicates
-- will group records by client_id and card_number and find those with more than one occurrence.
SELECT client_id, card_number, COUNT(*) AS duplicate_count
FROM data_analysis.cards
GROUP BY client_id, card_number
HAVING COUNT(*) > 1;

-- retrieve all records for client_id and card_number combinations that have duplicates.
SELECT *
FROM data_analysis.cards
WHERE client_id IN (
    SELECT client_id
    FROM data_analysis.cards
    GROUP BY client_id, card_number
    HAVING COUNT(*) > 1
)
ORDER BY client_id, card_number;






-- using ROW_NUMBER() to rank duplicates and delete older ones.
WITH RankedRecords AS (SELECT *,ROW_NUMBER() OVER (
               PARTITION BY client_id, card_number 
               ORDER BY acct_open_date DESC) AS row_num
    FROM data_analysis.cards
)
-- Selecting only the records where row_num = 1, which are the latest records.
DELETE FROM data_analysis.cards
WHERE id IN (
    SELECT id
    FROM RankedRecords
    WHERE row_num > 1 
);

--  Verify if the  duplicates have been removed.
SELECT client_id, card_number, COUNT(*) AS record_count
FROM data_analysis.cards
GROUP BY client_id, card_number
HAVING COUNT(*) > 1;

-- NOW AS THE DATA HAS BEEN CLEANED, NOW I AM GOING TO ANALYSE IT 

-- Arranged the number of cards issued in descending order so that we can see which id has the maximum cards issued 
select* from data_analysis.cards order by num_cards_issued desc;

-- total number of cards issued?
select sum(num_cards_issued) as total_card_issued from data_analysis.cards;

-- What is the distribution of card_type? Which type is most commonly issued?
select card_type,count(*) as card_count from data_analysis.cards
group by card_type
order by card_count desc;

-- how many people have more than one card issued ?
select  client_id,count(*) as cards_issued from data_analysis.cards
where num_cards_issued >1
group by client_id
order by cards_issued desc;

-- total num of cards have chip?
select sum(num_cards_issued) as total_chip_cards  from data_analysis.cards
where has_chip='yes';

-- checking how many cards have chip by card_type?
select card_type,count(*) as total_chip_card from data_analysis.cards
where has_chip = 'Yes' 
group by card_type
order by total_chip_card;
          
-- What is the average, minimum, and maximum credit_limit? How does it vary by card_brand?
select card_brand,
avg(credit_limit) as avg_credit_limit,
max(credit_limit) as max_credit_limit,
min(credit_limit) as min_credit_limit
from data_analysis.cards
group by card_brand;

-- How many cards are close to expiry?
SELECT COUNT(*) AS expiring_soon 
FROM data_analysis.cards
WHERE expires BETWEEN '2024-01' AND '2024-12';

-- How many cards are flagged as being on the dark web?
select count(*) as flagged_cards from data_analysis.cards where card_on_dark_web='yes';

-- What is the average number of years since the PIN was last changed?
select avg( 2024 - year_pin_last_changed) as avg_number from data_analysis.cards  ;

-- Which year had the most account openings?
select YEAR(acct_open_date) as y, count(*) as cnt from data_analysis.cards
group by y
order by cnt desc;

