# Import python packages
import streamlit as st
import os
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f"🥤 Customize Your Smoothie! 🥤")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")


# 1. Cleaned up the URL string
url = "https://my.smoothiefroot.com/api/fruit/watermelon"
smoothiefroot_response = requests.get(url)

# 2. Check if the request succeeded, then extract the data
if smoothiefroot_response.status_code == 200:
    # Use .json() if the API returns JSON, or .text if it returns raw text
    fruit_data = smoothiefroot_response.json() 
    
    # Use st.write or st.json to display the data beautifully
    st.json(fruit_data)
else:
    st.error(f"Failed to fetch data. Status code: {smoothiefroot_response.status_code}")

