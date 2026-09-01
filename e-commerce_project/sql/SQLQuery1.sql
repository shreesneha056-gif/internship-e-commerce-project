---CREATE database Internship;

---Overview

SELECT * FROM order_item_refunds

SELECT * FROM order_items

SELECT * FROM orders

SELECT * FROM products

SELECT * FROM website_pageviews

SELECT * FROM website_sessions



---Count Rows

Select COUNT(*) as total_count_order_item_refunds
FROM order_item_refunds

Select COUNT(*) as total_count_order_items 
FROM order_items

Select COUNT(*) as total_count_orders
FROM orders

Select COUNT(*) as total_count_products
FROM products

Select COUNT(*) as total_count_website_pageviews
FROM website_pageviews

Select COUNT(*) as total_count_website_sessions
FROM website_sessions

---check

SELECT website_session_id, COUNT(*) as Count
FROM website_sessions 
GROUP BY website_session_id 
HAVING COUNT(*) > 1;


SELECT order_id, COUNT(*) as Count
FROM orders 
GROUP BY order_id 
HAVING COUNT(*) > 1;

SELECT order_item_refund_id, COUNT(*) as Count
FROM order_item_refunds
GROUP BY order_item_refund_id 
HAVING COUNT(*) > 1;

SELECT website_pageview_id, COUNT(*) as Count
FROM website_pageviews
GROUP BY website_pageview_id 
HAVING COUNT(*) > 1;

---NEGATIVE VALUE CHECK

SELECT * FROM orders;

SELECT * 
FROM orders 
WHERE price_usd <=0 OR cogs_usd <=0;

SELECT * FROM order_item_refunds

SELECT *
FROM order_item_refunds
WHERE refund_amount_usd<=0;

SELECT * FROM order_items

SELECT * 
FROM order_items 
WHERE price_usd <=0 OR cogs_usd <=0;

SELECT * FROM products

SELECT * FROM website_pageviews;

SELECT * FROM website_sessions;

---NULL value check 
EXEC sp_help 'order_item_refunds';

SELECT sum(iif(order_item_refund_id is null , 1,0)) as null_order_item_refund_id,
	   sum(iif(created_at is null, 1,0)) as null_created_at,
	   sum(iif(order_item_id is null,1,0)) as null_order_item_id,
	   sum(iif(order_id is null,1,0)) as null_order_id,
	   sum(iif(refund_amount_usd is null,1,0)) as null_refund_amount_usd
FROM order_item_refunds;

EXEC sp_help 'order_items';

SELECT sum(iif(order_item_id is null , 1,0)) as null_order_item_id,
	   sum(iif(created_at is null, 1,0)) as null_created_at,
	   sum(iif(order_id is null,1,0)) as null_order_id,
	   sum(iif(product_id is null,1,0)) as null_product_id,
	   sum(iif(is_primary_item is null,1,0)) as null_is_primary_item,
	   sum(iif(price_usd is null,1,0)) as null_price_usd,
	   sum(iif(cogs_usd is null,1,0)) as null_cogs_usd
FROM order_items;

EXEC sp_help 'orders';


SELECT sum(iif(order_id is null , 1,0)) as null_order_id,
	   sum(iif(created_at is null, 1,0)) as null_created_at,
	   sum(iif(website_session_id is null,1,0)) as null_website_session_id,
	   sum(iif(user_id is null,1,0)) as null_user_id,
	   sum(iif(primary_product_id is null,1,0)) as null_primary_product_id,
	   sum(iif(items_purchased is null,1,0)) as null_items_purchased,
	   sum(iif(price_usd is null,1,0)) as null_price_usd,
	   sum(iif(cogs_usd is null,1,0)) as null_cogs_usd
FROM orders;

EXEC sp_help 'website_pageviews';


SELECT sum(iif(website_pageview_id is null , 1,0)) as null_website_pageview_id,
	   sum(iif(created_at is null, 1,0)) as null_created_at,
	   sum(iif(website_session_id is null,1,0)) as null_website_session_id,
	   sum(iif(pageview_url ='NULL',1,0)) as null_pageview_url
FROM website_pageviews;

EXEC sp_help 'website_sessions';

SELECT sum(iif(website_session_id is null , 1,0)) as null_session_id,
	   sum(iif(created_at is null, 1,0)) as null_created_at,
	   sum(iif(user_id is null,1,0)) as null_user_id,
	   sum(iif(is_repeat_session is null,1,0)) as null_is_repeat_session,
	   sum(iif(utm_source ='NULL',1,0)) as null_utm_source,---YES
	   sum(iif(utm_campaign ='NULL',1,0)) as null_utm_campaign,---YES
	   sum(iif(utm_content ='NULL',1,0)) as null_utm_content,---YES
	   sum(iif(device_type ='NULL',1,0)) as null_device_type,
	   sum(iif(http_referer ='NULL',1,0)) as null_http_referer---YES
FROM website_sessions;

---dtype 

EXEC sp_help 'order_item_refunds';

EXEC sp_help 'order_items';

EXEC sp_help 'orders';

EXEC sp_help 'products';

EXEC sp_help 'website_pageviews';

EXEC sp_help 'website_sessions';


---Primary key check

SELECT  * FROM order_item_refunds

SELECT COUNT(*) as Total_Rows, COUNT(DISTINCT order_item_refund_id) as Unique_Rows
FROM order_item_refunds;

SELECT * FROM order_items

SELECT COUNT(*) as Total_Rows, COUNT(DISTINCT order_item_id) as Unique_Rows
FROM order_items;

Select* From orders;

SELECT COUNT(*) as Total_Rows, COUNT(DISTINCT order_id) as Unique_Rows
FROM orders;

SELECT * FROM products;

SELECT *FROM website_pageviews;

SELECT COUNT(*) as Total_Rows, COUNT(DISTINCT website_pageview_id) as Unique_Rows
FROM website_pageviews;

SELECT * FROM website_sessions;

SELECT COUNT(*) as Total_Rows, COUNT(DISTINCT website_session_id) as Unique_Rows
FROM website_sessions;

---Join cheeck and Orphan FK check

SELECT a.*
FROM website_pageviews as a
LEFT JOIN website_sessions as b
ON a.website_session_id = b.website_session_id
WHERE b.website_session_id IS NULL;

SELECT a.*
FROM orders as a
LEFT JOIN website_sessions as b
ON a.website_session_id = b.website_session_id
WHERE b.website_session_id IS NULL;

SELECT a.*
FROM order_items as a
LEFT JOIN orders as b 
ON a.order_id = b.order_id
WHERE b.order_id IS NULL;

SELECT a.*
FROM order_items as a
LEFT JOIN products as b 
ON a.product_id = b.product_id
WHERE b.product_id IS NULL;

SELECT a.*
FROM order_item_refunds as a
LEFT JOIN order_items as b 
ON a.order_item_id = b.order_item_id
WHERE b.order_item_id IS NULL;

SELECT a.*
FROM order_item_refunds as a
LEFT JOIN orders as b 
ON a.order_id = b.order_id
WHERE b.order_id IS NULL;


---Dashboard-1

SELECT * FROM order_item_refunds;

SELECT * FROM order_items;

SELECT * FROM orders;

SELECT * FROM products;

SELECT * FROM website_pageviews;

SELECT * FROM website_sessions;


---Total Sessions

SELECT COUNT(DISTINCT website_session_id) AS total_sessions
FROM website_sessions;

---Conversion Rate

SELECT * FROM website_sessions;
SELECT * FROM orders;

SELECT COUNT(DISTINCT b.order_id) * 100.0 / COUNT(DISTINCT a.website_session_id) AS conversion_rate
FROM website_sessions AS a
LEFT JOIN orders AS b
ON a.website_session_id = b.website_session_id;

---Bounce Rate

SELECT * FROM website_pageviews;

WITH pageviews_per_session AS (
    SELECT website_session_id, COUNT(*) AS num_pageviews
    FROM website_pageviews
    GROUP BY website_session_id
)
SELECT SUM(IIF(num_pageviews=1,1,0)) * 100.0 / COUNT(*) AS bounce_rate_pct
FROM pageviews_per_session;

---Average Pages per Session

SELECT * FROM website_sessions;
SELECT * FROM website_pageviews;

SELECT COUNT(b.website_pageview_id) * 1.0 / COUNT(DISTINCT a.website_session_id) AS avgerage_pages_per_session
FROM website_sessions as a
LEFT JOIN website_pageviews as b 
ON a.website_session_id = b.website_session_id;

---Sessions trend over time

SELECT * FROM website_sessions;

SELECT FORMAT(created_at, 'yyyy-MM') AS session_month, COUNT(DISTINCT website_session_id) AS sessions
FROM website_sessions
GROUP BY FORMAT(created_at, 'yyyy-MM')
ORDER BY session_month;

---Sessions by device type

SELECT device_type, COUNT(DISTINCT website_session_id) AS sessions
FROM website_sessions
GROUP BY device_type;

---homepage -> product -> cart -> billing -> thank you

SELECT * FROM website_pageviews;

SELECT pageview_url, COUNT(pageview_url) as count_pageview_url
FROM website_pageviews
GROUP BY pageview_url;

ALTER TABLE website_pageviews
ADD
	page_name VARCHAR(50);

SELECT * FROM website_pageviews;

UPDATE website_pageviews
SET
	page_name = IIF(pageview_url = '/home' , 'home_page',IIF(pageview_url LIKE '%products%' , 'product',
				IIF(pageview_url LIKE '/cart%' , 'cart', IIF(pageview_url LIKE '/billing%' , 'billing',
				IIF(pageview_url LIKE '/thank-you%' , 'thank_you', 'unknown')))));

SELECT * FROM website_pageviews;

SELECT page_name, COUNT(page_name) as count_pageview_url
FROM website_pageviews
GROUP BY page_name;

SELECT
    COUNT(DISTINCT IIF(pageview_url = '/home' , website_session_id ,NULL)) AS homepage,
    COUNT(DISTINCT IIF(pageview_url LIKE '/products%' , website_session_id , NULL)) AS product_page,
    COUNT(DISTINCT IIF (pageview_url LIKE '/cart%' , website_session_id , NULL)) AS cart,
    COUNT(DISTINCT IIF (pageview_url LIKE '/billing%' , website_session_id , NULL)) AS billing,
    COUNT(DISTINCT IIF (pageview_url LIKE '/thank-you%' , website_session_id , NULL)) AS thank_you
FROM website_pageviews;

---Top landing pages (the FIRST page viewed in each session)

SELECT * FROM website_pageviews;
SELECT * FROM website_sessions;

WITH first_pageview AS (
    SELECT website_session_id, pageview_url,ROW_NUMBER() OVER (PARTITION BY website_session_id ORDER BY created_at ASC) AS rn
    FROM website_pageviews
)
SELECT pageview_url AS landing_page, COUNT(*) AS sessions_landed
FROM first_pageview
WHERE rn = 1
GROUP BY pageview_url
ORDER BY sessions_landed DESC;

---DASHBOARD 2: Marketing Channel Performance

--- Sessions this period

SELECT * FROM website_sessions;

SELECT COUNT(DISTINCT website_session_id) AS sessions
FROM website_sessions;

--- Blended conversion rate
SELECT COUNT(DISTINCT b.order_id) * 100.0 / COUNT(DISTINCT a.website_session_id) AS conversion_rate_pct
FROM website_sessions AS a
LEFT JOIN orders AS b
ON a.website_session_id = b.website_session_id;

--- Revenue this period
SELECT SUM(price_usd) AS total_revenue
FROM order_items;

--- Revenue by Channel

SELECT a.utm_source, SUM(c.price_usd) AS revenue
FROM website_sessions AS a
JOIN orders AS b
    ON a.website_session_id = b.website_session_id
JOIN order_items AS c
    ON b.order_id = c.order_id
GROUP BY a.utm_source
ORDER BY revenue DESC;

--- Sessions by channel, over time (stacked bar source)

SELECT FORMAT(created_at, 'yyyy-MM') AS session_month,utm_source, COUNT(DISTINCT website_session_id) AS sessions
FROM website_sessions
GROUP BY FORMAT(created_at, 'yyyy-MM'), utm_source
ORDER BY session_month;

--- Conversion rate by campaign

SELECT * FROM website_sessions;
SELECT * FROM website_pageviews;

SELECT a.utm_campaign, COUNT(DISTINCT b.order_id) * 100.0 / COUNT(DISTINCT a.website_session_id) AS conversion_rate_pct
FROM website_sessions AS a
LEFT JOIN orders AS b
ON a.website_session_id = b.website_session_id
GROUP BY a.utm_campaign
ORDER BY conversion_rate_pct DESC;

--- Source share of sessions (donut)
SELECT utm_source, COUNT(DISTINCT website_session_id) * 100.0 / SUM(COUNT(DISTINCT website_session_id)) OVER ()  AS pct_share
FROM website_sessions
GROUP BY utm_source;

---DASHBOARD 3

---Total Revenue
SELECT SUM(price_usd) AS total_revenue FROM order_items;

---Total Profit
SELECT SUM(price_usd - cogs_usd) AS total_profit FROM order_items;

--- AOV (Average Order Value)
SELECT SUM(oi.price_usd) * 1.0 / COUNT(DISTINCT oi.order_id) AS aov
FROM order_items oi;

--- Refund Rate

SELECT * FROM order_items
SELECT * FROM order_item_refunds;

SELECT COUNT(b.order_item_refund_id) * 100.0 / COUNT(a.order_item_id) AS refund_rate_pct
FROM order_items AS a
LEFT JOIN order_item_refunds AS b
ON a.order_item_id = b.order_item_id;

---Cumulative revenue growth

SELECT * FROM order_items;


SELECT FORMAT(created_at, 'yyyy-MM') AS month, SUM(price_usd) AS monthly_revenue, 
	SUM(SUM(price_usd)) OVER (ORDER BY FORMAT(created_at, 'yyyy-MM')) AS cumulative_revenue
FROM order_items
GROUP BY FORMAT(created_at, 'yyyy-MM')
ORDER BY month;

--- Product revenue split

SELECT b.product_name, SUM(a.price_usd) AS revenue
FROM order_items AS a
JOIN products AS b 
ON a.product_id = b.product_id
GROUP BY b.product_name
ORDER BY revenue DESC;