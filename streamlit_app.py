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







