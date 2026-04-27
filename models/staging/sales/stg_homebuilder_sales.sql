{{ config(materialized='view') }}

select
*
from
{{ source('rhodes_sales', 'homebuilder_sales_raw')}}