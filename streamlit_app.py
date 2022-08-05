
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#1) Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# Display the table on the page.
#streamlit.dataframe(my_fruit_list)


#2) Let's put a pick list here so they can pick the fruit they want to include
#streamlit.multiselect ("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

# Display the table on the page.
#streamlit.dataframe(my_fruit_list)



#3) Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect ("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


# #new section to display fruitvice api response
# streamlit.header("Fruityvice Fruit Advice!")
# fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
# streamlit.write('The user entered ', fruit_choice)

# # import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# # streamlit.text(fruityvice_response.json())


# # Normalize the fruitvice api response data from json version 
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# # output the normalized fruitvice api response data as a table  
# streamlit.dataframe(fruityvice_normalized)


#Create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
  fruitvice_response =  requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

#new section to display fruitvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_furityvice_data(fruit_choice) 
    streamlit.dataframe(back_from_function)
 

# #new section to display fruitvice api response
# streamlit.header("Fruityvice Fruit Advice!")
# try:
#   fruit_choice = streamlit.text_input('What fruit would you like information about?')
#   if not fruit_choice:
#     streamlit.error("Please select a fruit to get information.")
#   else:
#     fruitvice_response =  requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#     fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#     streamlit.dataframe(fruityvice_normalized)
 
# except URLError as e:
#   streamlit.error()
     

# #don't run anything past here while we troubleshoot
# streamlit.stop()

#connect Streamlit to Snowflake
# import snowflake.connector


# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT * from fruit_load_list")

# # my_data_row = my_cur.fetchone()  -- to get one row

# #to fetch all the data/rows
# my_data_rows = my_cur.fetchall()
# streamlit.header("The fruit load list contains:")
# streamlit.dataframe(my_data_rows)

streamlit.header("The fruit load list contains:")
#Snowflake related functions
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
        my_cnx.execute("select * from fruit_load_list")
        return my_cur.fetchall()

#add a button to load the fruit
if steamlit.button ('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_lost()
  streamlit.dataframe(my_data_rows)

  
#don't run anything past here while we troubleshoot
streamlit.stop()


#Allow the end user to add a fruit to the list 
fruit_choice = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding', fruit_choice)

#This will not work corretcly, but just go with it for now
my_cur.execute ("insert into fruit_load_list values ('from streamlit')")



