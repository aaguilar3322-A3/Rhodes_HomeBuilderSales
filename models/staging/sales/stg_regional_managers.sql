{{ config(materialized='view') }}

select
*
from
{{ source('rhodes_sales', 'regional_managers_raw')}}