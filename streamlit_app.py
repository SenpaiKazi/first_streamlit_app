import streamlit
import pandas
import requests


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
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#Normalize response
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
streamlit.header('Fruityvice Fruit Advice!')
streamlit.dataframe(fruityvice_response.json())
#display fruityvice as data frame
streamlit.dataframe(fruityvice_normalized)
