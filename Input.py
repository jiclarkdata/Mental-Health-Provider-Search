# Instructions:
# Run each cell below in order, entering the Search Terms as needed in the second cell of code. You can search by location (Zip Code, City, or State) or Provider Information (NPI Number, first, and/or last name) if known.

# Skip any search criteria you do not need by hitting enter.

# Be sure to format exactly as indicated to avoid errors.

import pandas as pd

# Enter Search Terms
zip = input("Enter Zip Code:")
state = input("Enter 2-Digit State (e.g. CA) *NOTE: if you enter a State, you MUST also enter a City: ")
city = input("Enter City: ")
npiNumber = input("Enter 10-Digit NPI Number:")
firstName = input("Enter Provider First Name: ")
lastName = input("Enter Provider Last Name: ")

data = {'postal_code': [zip], 'city': [city], 'state': [state], 
        'number': [npiNumber], 'first_name': [firstName], 'last_name': [lastName]}

inputData_df = pd.DataFrame(data)
inputData_df

inputData_df.to_csv("input.csv", index=False)

print("Input Done.")



