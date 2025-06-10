# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd
# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie")

name_on_order = st.text_input('Name on smoothie: ')
st.write('Name on your smoothie will be', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# st.dataframe(data= my_dataframe, use_container_width = True)
# st.stop()

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect('Choose 5', my_dataframe, max_selections=5)
if ingredients_list:
    ing_str = ''
    for f in ingredients_list:
        ing_str+=f+' '
                
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
       # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(f+ ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + f)
        st_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width= True)
        
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ing_str+ """', '"""+name_on_order+"""')"""
 

    time_to_insert = st.button('Submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

