import streamlit
import pandas
import requests
import snowflake.connector


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🍓 Build Your Own Smoothie 🥝🍇')

#my_fruit_list list picker
fruits_selected = streamlit.multiselect("Pick Some Fruits: ", list(my_fruit_list.index),['Avocado', 'Strawberries'])

#filter lost to show selected fruits only
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display my_fruit_list list
streamlit.dataframe(fruits_to_show)

#New section to show fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered:', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#Normalize response
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#display fruityvice as data frame
streamlit.dataframe(fruityvice_normalized)

#snowflake section
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("fruit load list contains:")
streamlit.dataframe(my_data_row)

#input text for snowflake funtion
add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'Jackfruit')
streamlit.write('Thanks for adding', fruit_choice)
