import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🍓 Build Your Own Smoothie 🥝🍇')

#add fruit data funtion
def get_fruityvice_data(this_fruit_choice):  
   #get response
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
   #Normalize response
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   #display fruityvice as data frame
   return fruityvice_normalized

#get list from snowflake
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values('" + new_fruit + "')")
    return "Thanks for adding " + new_fruit


#my_fruit_list list picker
fruits_selected = streamlit.multiselect("Pick Some Fruits: ", list(my_fruit_list.index),['Avocado', 'Strawberries'])

#filter lost to show selected fruits only
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display my_fruit_list list
streamlit.dataframe(fruits_to_show)

#New section to show fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")

try:
 fruit_choice = streamlit.text_input('What fruit would you like information about?')
 if not fruit_choice:
   streamlit.error("Please select a fruit to get information.")
 else:
   fruityvice_response = get_fruityvice_data(fruit_choice)
   streamlit.dataframe(fruityvice_response)
except URLError as e:
  streamlit.error()
  
#snowflake section
streamlit.header("View our Fruit List - Add your Favorites!")
#button function to load the list
if streamlit.button('Get Fruit Load List'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 my_data_row = get_fruit_load_list()
 my_cnx.close()
 streamlit.dataframe(my_data_row)

#input text for snowflake funtion
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  message = insert_row_snowflake(add_my_fruit)
  my_cnx.close()
  streamlit.write(message)
