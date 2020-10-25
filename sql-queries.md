SQL queries to achieve the following.

##### From subscription histories table find
  * Number of new customers every month
  ```shell script
    sql: with data as (
    select subscription_id, min(period_start) as start_date 
    from subscription_histories 
    where status = "TRIAL"
    group by 1
    )
    select extract(year from start_date), extract(month from start_date) month, count(*) new_customer
    from data 
    group by 1,2 order by 1,2
  ``` 
  * No of Upgrades and Upgrade value in every month (revenue amount increase in a month compared to 
    the same subscription in previous month)
  ```shell script
    sql: select distinct subscription_id, year, month, upgrades, amt as rev_amt, 
    (amt - lag(amt) over(partition by subscription_id order by year,month)) upgrade_value
    from (
    select subscription_id,extract(year from period_start) year,extract(month from period_start) month,count(*) upgrades, sum(amount) as amt
    from subscription_histories 
    where status = "ACTIVE"
    group by 1,2,3 order by 2,3
    )
  ``` 
  * Churn rate:
  ```shell script
    sql: 
    with active_cust as (
    select extract(year from period_start) year,extract(month from period_start) month, count(distinct subscription_id) active
    from subscription_histories 
    where status = "ACTIVE"
    group by 1,2
    ),
    cancelled_cust as (
    select extract(year from period_start) year,extract(month from period_start) month, count(distinct subscription_id) cancelled
    from subscription_histories 
    where status = "CANCELLED"
    group by 1,2
    )
    select distinct extract(year from m.period_start) year,extract(month from m.period_start) month, 
    safe_divide(
    case 
      when cc.cancelled is null then 0 
      else cc.cancelled 
    end, 
    case 
      when lag(ac.active) over (order by extract(year from m.period_start),extract(month from m.period_start)) is null then 0 
      else ac.active 
    end
    ) as churn_rate
    from subscription_histories m
    left join active_cust ac on extract(year from m.period_start) = ac.year and extract(month from m.period_start) = ac.month  
    left join cancelled_cust cc on extract(year from m.period_start) = cc.year and extract(month from m.period_start) = cc.month  
    order by 3 desc
  ``` 
  

##### From subscription histories table find
  * Calculate Account receivable at the end of every month 
  (Total invoices raised before end of the month - Total payments received before end of the month) - 
  use amount,amount_paid and paid_at columns
  ```shell script
    sql: 
    with a as (
    SELECT extract(year from invoice_date) year,extract(month from invoice_date) month, count(distinct invoice_id) as invoices
    FROM invoices 
    group by 1,2
    ),
    b as (
    SELECT extract(year from invoice_date) year,extract(month from invoice_date) month, sum(total) as amt
    FROM invoices 
    where status = "PAID"
    group by 1,2
    )
    select a.year, a.month, 
    (a.invoices - case when b.amt is null then 0 else b.amt end) as acc_receivable
    from a 
    left join b on a.year = b.year and a.month = b.month 
  ``` 
  * Identify the percentage of invoices voided at every moth ( Invoices voided in a month/ Total invoices raised in a month)
  ```shell script
    sql: 
    with a as (
    SELECT extract(year from invoice_date) year,extract(month from invoice_date) month, count(distinct invoice_id) as invoices
    FROM invoices 
    group by 1,2
    ),
    b as (
    SELECT extract(year from invoice_date) year,extract(month from invoice_date) month, count(distinct invoice_id) as voided
    FROM invoices 
    where status = "VOIDED"
    group by 1,2
    )
    select a.year, a.month, safe_divide(a.invoices, case when b.voided is null then 0 else b.voided end) as voided_perc
    from a 
    left join b on a.year = b.year and a.month = b.month 
  ```   
  * Plan wise paid invoices every month
  ```shell script
    sql: 
    SELECT sp.plan, extract(year from i.invoice_date) year,extract(month from i.invoice_date) month,count(distinct i.invoice_id) paid_invoices
    FROM subscription_plan sp
    left join invoices i 
    on sp.subscription_id = i.subscription_id 
    where i.status = "PAID"
    group by 1,2,3 order by 1 
  ``` 

* Note: Using Biguqery sql syntax for the above queries.