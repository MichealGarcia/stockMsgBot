# Create Virtual Environment:
    conda create -n Stockbot python=3
# Install necessary packages:
    pip install searchtweets
    pip install python_dotenv
    pip install twilio (npm install twilio-cli -g)
# What does the project do?
    This project is focused on scraping tweets through text specific searches, and then aggregating the text with a list of ticker names. Then texting Twilio approved numbers the list.
    - The current code uses the search term "takeover chatter"
# What is this project for?
    I created this project to automate searching twitter, and escape the media rabbithole. 
    - With this project I can reduce the time it would take to count the most common stocks mentioned in recent posts.
# Why is it different
    The project is scalable. 
    - The focus is to eventually use the application on a daily basis. If possible, I want it to b available to anyone/everyone. So that if they text a phone number itll text back the list of stocks mentioned in the last x amount of hours.
    
