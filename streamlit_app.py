import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError   #For error message handling

streamlit.title('My Parents Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')


# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


#Create the repeatable code block (called a 'Function")
def get_fruityvice_data(thisfruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())  #Take the json version of the response and convert to normalize it
    return fruityvice_normalized     #Output the normalized data onto the screen
#New Section To Display Fruityvice API Response
# Display New Fruit menu by connecting to Fruityvice.com or Display Fruity Vice API response 
streamlit.header('Fruityvice Fruit Advice')
try:
    fruit_choice = streamlit.text_input('What Fruit would you like information about?')  #Creating a variable fruity_choice to be used as input to FruityVice as an input API call
    if not fruit_choice:
        streamlit.error('Please select a valid Fruit choice')
    else:
        streamlit.write('The user entered', fruit_choice)
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
                #'''#import requests
                #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
                #streamlit.text(fruityvice_response.json())    # This writes the json data to the screen
                #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())  #Take the json version of the response and convert to normalize it
                #streamlit.dataframe(fruityvice_normalized)     #Output the normalized data onto the screen'''
except URLError as e:
    streamlit.error()

#Move fruit load list query and load it to a Button Action from Streamlit user interface
streamlit.text("The Fruit Load list contains:")
#Snowflake Related Functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT *from fruit_load_list")
        return my_cur.fetchall()

# Add the Button to load fruit to snowflake
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

    #Do not run any code beyond this point
#streamlit.stop()

#Challenge lab - Add a second entry fruit to the app selectio
add_my_fruit = streamlit.text_input('What Fruit do you like to add?', 'Apple')
streamlit.write('Thanks for adding', add_my_fruit)
my_cur.execute("insert into fruit_load_list values (' "+add_my_fruit+" '))
