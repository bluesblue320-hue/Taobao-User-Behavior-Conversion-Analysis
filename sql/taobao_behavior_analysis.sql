-- Taobao User Behavior & Conversion Funnel Analysis
-- PostgreSQL SQL queries for the cleaned_user_behavior.csv dataset.
--
-- Suggested table schema after importing data:
-- CREATE TABLE user_behavior (
--     user_id BIGINT,
--     item_id BIGINT,
--     category_id BIGINT,
--     behavior_type VARCHAR(10),
--     behavior_name_en VARCHAR(50),
--     behavior_name_cn VARCHAR(20),
--     timestamp BIGINT,
--     behavior_time TIMESTAMP,
--     date DATE,
--     hour INT,
--     weekday VARCHAR(20)
-- );

-- 1. Total behaviors, UV, items, and categories
SELECT
    COUNT(*) AS total_behaviors,
    COUNT(DISTINCT user_id) AS uv,
    COUNT(DISTINCT item_id) AS item_count,
    COUNT(DISTINCT category_id) AS category_count
FROM user_behavior;

-- 2. Behavior type counts and share
SELECT
    behavior_type,
    behavior_name_en,
    behavior_name_cn,
    COUNT(*) AS behavior_count,
    ROUND(COUNT(*)::NUMERIC / SUM(COUNT(*)) OVER (), 4) AS behavior_share
FROM user_behavior
GROUP BY behavior_type, behavior_name_en, behavior_name_cn
ORDER BY behavior_count DESC;

-- 3. Daily active users
SELECT
    date,
    COUNT(DISTINCT user_id) AS dau
FROM user_behavior
GROUP BY date
ORDER BY date;

-- 4. Daily purchase count and purchase users
SELECT
    date,
    COUNT(*) AS purchase_count,
    COUNT(DISTINCT user_id) AS purchase_users
FROM user_behavior
WHERE behavior_type = 'buy'
GROUP BY date
ORDER BY date;

-- 5. Hourly behavior distribution
SELECT
    hour,
    behavior_type,
    COUNT(*) AS behavior_count,
    COUNT(DISTINCT user_id) AS active_users
FROM user_behavior
GROUP BY hour, behavior_type
ORDER BY hour, behavior_type;

-- 6. Top 10 categories by purchase
SELECT
    category_id,
    COUNT(*) AS purchase_count,
    COUNT(DISTINCT user_id) AS buyer_count
FROM user_behavior
WHERE behavior_type = 'buy'
GROUP BY category_id
ORDER BY purchase_count DESC, buyer_count DESC
LIMIT 10;

-- 7. Browse-to-purchase conversion rate at user level
WITH user_flags AS (
    SELECT
        user_id,
        MAX(CASE WHEN behavior_type = 'pv' THEN 1 ELSE 0 END) AS has_pv,
        MAX(CASE WHEN behavior_type = 'buy' THEN 1 ELSE 0 END) AS has_buy
    FROM user_behavior
    GROUP BY user_id
)
SELECT
    SUM(has_pv) AS pv_users,
    SUM(has_buy) AS buyer_users,
    ROUND(SUM(has_buy)::NUMERIC / NULLIF(SUM(has_pv), 0), 4) AS browse_to_purchase_rate
FROM user_flags;

-- 8. Add-to-cart to purchase conversion rate at user level
WITH user_flags AS (
    SELECT
        user_id,
        MAX(CASE WHEN behavior_type = 'cart' THEN 1 ELSE 0 END) AS has_cart,
        MAX(CASE WHEN behavior_type = 'buy' THEN 1 ELSE 0 END) AS has_buy
    FROM user_behavior
    GROUP BY user_id
)
SELECT
    SUM(has_cart) AS cart_users,
    SUM(CASE WHEN has_cart = 1 AND has_buy = 1 THEN 1 ELSE 0 END) AS cart_and_buy_users,
    ROUND(
        SUM(CASE WHEN has_cart = 1 AND has_buy = 1 THEN 1 ELSE 0 END)::NUMERIC
        / NULLIF(SUM(has_cart), 0),
        4
    ) AS cart_to_purchase_rate
FROM user_flags;

-- 9. Favorite-to-purchase conversion rate at user level
WITH user_flags AS (
    SELECT
        user_id,
        MAX(CASE WHEN behavior_type = 'fav' THEN 1 ELSE 0 END) AS has_fav,
        MAX(CASE WHEN behavior_type = 'buy' THEN 1 ELSE 0 END) AS has_buy
    FROM user_behavior
    GROUP BY user_id
)
SELECT
    SUM(has_fav) AS favorite_users,
    SUM(CASE WHEN has_fav = 1 AND has_buy = 1 THEN 1 ELSE 0 END) AS favorite_and_buy_users,
    ROUND(
        SUM(CASE WHEN has_fav = 1 AND has_buy = 1 THEN 1 ELSE 0 END)::NUMERIC
        / NULLIF(SUM(has_fav), 0),
        4
    ) AS favorite_to_purchase_rate
FROM user_flags;

-- 10. User repurchase rate
WITH user_purchase AS (
    SELECT
        user_id,
        COUNT(*) AS purchase_count
    FROM user_behavior
    WHERE behavior_type = 'buy'
    GROUP BY user_id
)
SELECT
    COUNT(*) AS total_buyers,
    SUM(CASE WHEN purchase_count >= 2 THEN 1 ELSE 0 END) AS repurchase_users,
    ROUND(
        SUM(CASE WHEN purchase_count >= 2 THEN 1 ELSE 0 END)::NUMERIC
        / NULLIF(COUNT(*), 0),
        4
    ) AS repurchase_rate
FROM user_purchase;

-- 11. Users who added to cart but did not purchase
WITH user_flags AS (
    SELECT
        user_id,
        MAX(CASE WHEN behavior_type = 'cart' THEN 1 ELSE 0 END) AS has_cart,
        MAX(CASE WHEN behavior_type = 'buy' THEN 1 ELSE 0 END) AS has_buy
    FROM user_behavior
    GROUP BY user_id
)
SELECT
    COUNT(*) AS cart_without_purchase_users
FROM user_flags
WHERE has_cart = 1 AND has_buy = 0;

-- 12. High-value users Top 20
SELECT
    user_id,
    COUNT(*) FILTER (WHERE behavior_type = 'buy') AS purchase_count,
    COUNT(DISTINCT item_id) FILTER (WHERE behavior_type = 'buy') AS distinct_items_bought,
    COUNT(DISTINCT category_id) FILTER (WHERE behavior_type = 'buy') AS distinct_categories_bought,
    COUNT(DISTINCT date) AS active_days,
    (
        COUNT(*) FILTER (WHERE behavior_type = 'buy') * 5
        + COUNT(DISTINCT item_id) FILTER (WHERE behavior_type = 'buy') * 2
        + COUNT(DISTINCT category_id) FILTER (WHERE behavior_type = 'buy')
        + COUNT(DISTINCT date)
    ) AS value_score
FROM user_behavior
GROUP BY user_id
HAVING COUNT(*) FILTER (WHERE behavior_type = 'buy') > 0
ORDER BY value_score DESC, purchase_count DESC
LIMIT 20;

-- 13. User behavior funnel with CTE
WITH user_funnel AS (
    SELECT
        user_id,
        MAX(CASE WHEN behavior_type = 'pv' THEN 1 ELSE 0 END) AS viewed,
        MAX(CASE WHEN behavior_type = 'fav' THEN 1 ELSE 0 END) AS favorited,
        MAX(CASE WHEN behavior_type = 'cart' THEN 1 ELSE 0 END) AS added_to_cart,
        MAX(CASE WHEN behavior_type = 'buy' THEN 1 ELSE 0 END) AS purchased
    FROM user_behavior
    GROUP BY user_id
),
funnel_steps AS (
    SELECT '01_viewed' AS step, COUNT(*) AS users FROM user_funnel WHERE viewed = 1
    UNION ALL
    SELECT '02_favorited' AS step, COUNT(*) AS users FROM user_funnel WHERE viewed = 1 AND favorited = 1
    UNION ALL
    SELECT '03_added_to_cart' AS step, COUNT(*) AS users FROM user_funnel WHERE viewed = 1 AND added_to_cart = 1
    UNION ALL
    SELECT '04_purchased' AS step, COUNT(*) AS users FROM user_funnel WHERE viewed = 1 AND purchased = 1
)
SELECT
    step,
    users,
    ROUND(users::NUMERIC / FIRST_VALUE(users) OVER (ORDER BY step), 4) AS conversion_from_view
FROM funnel_steps
ORDER BY step;

-- 14. Window function: highest purchase category by day
WITH daily_category_purchase AS (
    SELECT
        date,
        category_id,
        COUNT(*) AS purchase_count
    FROM user_behavior
    WHERE behavior_type = 'buy'
    GROUP BY date, category_id
),
ranked AS (
    SELECT
        date,
        category_id,
        purchase_count,
        DENSE_RANK() OVER (PARTITION BY date ORDER BY purchase_count DESC) AS purchase_rank
    FROM daily_category_purchase
)
SELECT
    date,
    category_id,
    purchase_count
FROM ranked
WHERE purchase_rank = 1
ORDER BY date, category_id;

-- 15. Stricter user-item sequential funnel
-- This checks whether later behavior happened after earlier behavior for the same user and item.
WITH first_events AS (
    SELECT
        user_id,
        item_id,
        MIN(behavior_time) FILTER (WHERE behavior_type = 'pv') AS pv_time,
        MIN(behavior_time) FILTER (WHERE behavior_type = 'fav') AS fav_time,
        MIN(behavior_time) FILTER (WHERE behavior_type = 'cart') AS cart_time,
        MIN(behavior_time) FILTER (WHERE behavior_type = 'buy') AS buy_time
    FROM user_behavior
    GROUP BY user_id, item_id
)
SELECT
    COUNT(*) AS user_item_pairs,
    COUNT(*) FILTER (WHERE pv_time IS NOT NULL) AS viewed_pairs,
    COUNT(*) FILTER (WHERE cart_time IS NOT NULL) AS carted_pairs,
    COUNT(*) FILTER (WHERE buy_time IS NOT NULL) AS bought_pairs,
    COUNT(*) FILTER (WHERE pv_time IS NOT NULL AND cart_time >= pv_time) AS pv_to_cart_pairs,
    COUNT(*) FILTER (WHERE pv_time IS NOT NULL AND buy_time >= pv_time) AS pv_to_buy_pairs,
    COUNT(*) FILTER (WHERE cart_time IS NOT NULL AND buy_time >= cart_time) AS cart_to_buy_pairs,
    ROUND(
        COUNT(*) FILTER (WHERE pv_time IS NOT NULL AND buy_time >= pv_time)::NUMERIC
        / NULLIF(COUNT(*) FILTER (WHERE pv_time IS NOT NULL), 0),
        4
    ) AS pv_to_buy_pair_rate,
    ROUND(
        COUNT(*) FILTER (WHERE cart_time IS NOT NULL AND buy_time >= cart_time)::NUMERIC
        / NULLIF(COUNT(*) FILTER (WHERE cart_time IS NOT NULL), 0),
        4
    ) AS cart_to_buy_pair_rate
FROM first_events;

-- 16. Category-level conversion analysis
SELECT
    category_id,
    COUNT(*) FILTER (WHERE behavior_type = 'pv') AS pv_count,
    COUNT(*) FILTER (WHERE behavior_type = 'fav') AS fav_count,
    COUNT(*) FILTER (WHERE behavior_type = 'cart') AS cart_count,
    COUNT(*) FILTER (WHERE behavior_type = 'buy') AS buy_count,
    ROUND(
        COUNT(*) FILTER (WHERE behavior_type = 'buy')::NUMERIC
        / NULLIF(COUNT(*) FILTER (WHERE behavior_type = 'pv'), 0),
        4
    ) AS browse_to_buy_rate,
    ROUND(
        COUNT(*) FILTER (WHERE behavior_type = 'buy')::NUMERIC
        / NULLIF(COUNT(*) FILTER (WHERE behavior_type = 'cart'), 0),
        4
    ) AS cart_to_buy_rate
FROM user_behavior
GROUP BY category_id
HAVING COUNT(*) FILTER (WHERE behavior_type = 'pv') >= 30
ORDER BY buy_count DESC, browse_to_buy_rate DESC
LIMIT 20;
