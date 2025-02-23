# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
import requests



# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your customer smoothie!
    """
)

# option = st.selectbox('How would you like to be connected?',
#                      ('Email','Home Phone','Mobile Phone'))

# st.write('Your selected:', option)

# option = st.selectbox('What is your favorite fruit?',
#                      ('Banana','Strawberries','Peaches'))
# st.write('Your favorite fruit is:', option)

name_on_order = st.text_input('Name on Smoothie: ')
st.write('The name on your smoothei will be '+name_on_order)


cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()


ingredients_list = st.multiselect(
    'Choose up yo 5 ingrediants'
    ,my_dataframe
    ,max_selections=5
)
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''

    for fruit in ingredients_list:
        ingredients_string+=fruit+' '

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)  Values(
       '"""+ingredients_string+"""', '"""+name_on_order+"""')"""
    
    # st.write(my_insert_stmt)
    # st.write(my_insert_sql)
    time_to_insert = st.button('Submit Order')
    # st.write(time_to_insert)

    if time_to_insert :
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")
if ingredients_list:
    ingredients_string = ''
    for fruits in ingredients_list:
        ingredients_string+=fruit+" "
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruits, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruits,' is ', search_on, '.')
        st.subheader(fruit+" Nutrition Information")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit)
        st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
