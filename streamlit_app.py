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

# Check if data was returned before proceeding (to avoid errors)
if not pd_prod_data.empty:
    # Assign values from the returned row to variables
    price = f"${pd_prod_data['PRICE'].iloc[0]:.2f}"  # Ensures proper currency formatting
    file_name = pd_prod_data['FILE_NAME'].iloc[0]
    size_list = pd_prod_data['SIZE_LIST'].iloc[0]
    upsell = pd_prod_data['UPSELL_PRODUCT_DESC'].iloc[0]
    url = pd_prod_data['FILE_URL'].iloc[0]

    # Display the selected product details
    st.image(image=url, width=400, caption=product_caption)
    st.markdown(f"**Price:** {price}")
    st.markdown(f"**Sizes Available:** {size_list}")
    st.markdown(f"**Also Consider:** {upsell}")

    # Display the image URL for reference
    st.write(url)
else:
    st.error("No product data found for the selected color/style. Please try another option.")
