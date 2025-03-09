# Import necessary packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import pandas as pd

# Set up the Streamlit app title
st.title("Zena's Amazing Athleisure Catalog")

# Establish a connection to the active Snowflake session
session = get_active_session()

# Retrieve a list of colors or styles from the database for user selection
table_colors = session.sql("SELECT color_or_style FROM catalog_for_website")
pd_colors = table_colors.to_pandas()

# Convert the list of colors into a dropdown selector in the Streamlit app
option = st.selectbox('Pick a sweatsuit color or style:', pd_colors['COLOR_OR_STYLE'])  # Fixed column reference

# Fetch product details from the database based on the selected color/style
query = f"""
SELECT file_name, price, size_list, upsell_product_desc, file_url 
FROM catalog_for_website 
WHERE color_or_style = %s;
"""
table_prod_data = session.sql(query, params=[option])  # Using parameterized query to prevent SQL injection
pd_prod_data = table_prod_data.to_pandas()




