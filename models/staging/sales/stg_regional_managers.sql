{{ config(materialized='view') }}

select
*
from
{{ source('rhodes_sales', 'regional_managersdbt run_raw')}}