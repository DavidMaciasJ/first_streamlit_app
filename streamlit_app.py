import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom\'s New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#changing the index of the dataframe
my_fruit_list=my_fruit_list.set_index('Fruit')
#allow to choose the index from the dataframe
fruits_selected=streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  #streamlit.text(fruityvice_response.json())
  # write your own comment -what does the next line do? transforms the json text to data frame
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  # write your own comment - what does this do? shows the dataframe
  return fruityvice_normalized


streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please enter a fruit to get info')
  else:
    back_from_function=get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()


#snowflake related functions
streamlit.header("The fruit load list contains")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur :
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()  
# add a button to get
if streamlit.button ('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows=get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
  




streamlit.header('What would you like to add?')

def insert_new_in_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur :
    my_cur.execute("insert into fruit_load_list values ('"+new_fruit+"')")
    return "thanks for adding:" + new_fruit
  
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
# add a button to load
if streamlit.button ('Add new fruit'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  answer=insert_new_in_snowflake(add_my_fruit)
  streamlit.text(answer)


streamlit.stop()
