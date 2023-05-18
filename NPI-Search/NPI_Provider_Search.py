# Queries NPI Registry using their API and saves the results in an Excel File with provider information formatted and organized by use case. This program flattens the JSON data structure so that each nested value is represented as a separate column in the table.
# 
# There will be one sheet with one row of Provider Information per unique provider. This list is intended to aid a user in visualizing and tracking providers to try calling.
# 
# There will be one sheet with one row of Provider Information per unique provider+taxonomy combination. This is intended to allow a user to filter by the particular taxonomy they are looking for, e.g. "Counselor, Addiction (Substance Use Disorder)" and find all providers with that specialty.

# Import required libraries
import requests
import pandas as pd

# Import search criteria
search_df = pd.read_csv("input.csv")
search_df

# Create a DataFrame with only the search criteria
search_df2 = search_df.dropna(axis=1)
search_df2

# Convert the DataFrame to a dictionary
first_row_dict = search_df.to_dict()
print(first_row_dict)

#Convert the used search terms to a dictionary
searchTerms = {}

col_index = 0

while col_index < len(search_df2.columns):
    # get the name of the current column
    col_name = search_df2.columns[col_index]

    # get the value of the first row in the current column
    value = search_df2[col_name][0]
    
    # assign the value of the first row to a variable with the same name as the column
    searchTerms[col_name] = value
    
    # increment the column index counter
    col_index += 1

# print the resulting dictionary of variables
print(searchTerms)

# Use the search terms to append the api URL
searchTerms_input = {}

col_index = 0

npi_url_base = "https://npiregistry.cms.hhs.gov/api/?version=2.1&use_first_name_alias=True&pretty=TRUE&enumeration_type=NPI-1&limit=100"
npi_url = npi_url_base

while col_index < len(search_df2.columns):
    # get the name of the current column
    col_name = search_df2.columns[col_index]

    # get the value of the first row in the current column
    value = search_df2[col_name][0]
    
    # create the search term suffix
    term = "&"+col_name+"="+value
    print(term)
    
    npi_url = npi_url + term

    # increment the column index counter
    col_index += 1
    
print(npi_url)

# Open the csv with all the appropriate taxonomies. Used to filter only for mental health providers

taxonomies = pd.read_csv("NPI_Taxonomies.csv", usecols=['Taxonomies'])
taxonomies = taxonomies[taxonomies.columns[0]].values.tolist()
taxonomies = [x for x in taxonomies if not(pd.isnull(x)) == True]
print(taxonomies)

# Create a dictionary of URLs with one version per Taxonomy, to perform multiple API calls (since you cannot search for multiple taxonomies at once)

v = 1 # URL version number
url_versions = {} # empty dictionary to store different versions of the URLs based on taxonomy
for t in taxonomies:
    # create the search term suffix
    term = "&taxonomy_description="+t
    
    # create the URL
    url = npi_url+term

    # save the URL as a new dictionary item
    url_versions[v] = url
    
    # increase the counter
    v+= 1
    
    print(url)
    
print(url_versions)

# Search NPI registry and store results
i = 1
addresses_df = pd.DataFrame()
basic_info_df = pd.DataFrame()
taxonomies_df = pd.DataFrame()
result_df = pd.DataFrame()

for url_version in url_versions.values():
    # get the requests from the URL
    response = requests.get(url_version)    

    # If there are no results for that taxonomy, it will make a successful request but with an error in the result. 
    # Simply skip this search term
    if "Errors" in response.json():
        print("Version",i,": No Results")
    
    # Otherwise, response status code 200 means it has succeeded; will only continue if the API call is successful
    elif response.status_code == 200:
        print("Version",i,": Success")
        # convert addresses of result to DF
        addresses_df1 = pd.json_normalize(
            response.json()["results"], 
            record_path=['addresses'], # Looks in the address path of the json
            meta=['number'], # Uses the NPI number column as metadata for each record
            errors='ignore') # Avoid raising a key error if key isn't present
        addresses_df = pd.concat([addresses_df, addresses_df1], ignore_index=True)
        #basic_info_df = pd.json_normalize(response.json()["basic"], errors='ignore')
        basic_info_df1 = pd.json_normalize(
            response.json(),['results'], # Looks in the basic_info path of the json
            errors='ignore')
        basic_info_df = pd.concat([basic_info_df, basic_info_df1], ignore_index=True)
        taxonomies_df1 = pd.json_normalize(
            response.json()["results"], 
            record_path=['taxonomies'],
            meta=['number'], # Uses the NPI number column as metadata for each record
            errors='ignore')
        taxonomies_df = pd.concat([taxonomies_df, taxonomies_df1], ignore_index=True)
    # Otherwise, print the error code for troublelshooting
    else:
        print("Version",i,"Error: API request returned status code ",response.status_code)
    # increase the counter
    i+= 1

# Merge all of the DataFrames created in the API search above
result_df = addresses_df.merge(basic_info_df, on='number')
result_df = result_df.merge(taxonomies_df, on='number')
result_df

#Rename columns for easier readability

result_df.rename(columns={"number":"NPI_Number",
                          "basic.first_name": "First_Name",
                          "basic.last_name": "Last_Name",
                          "basic.middle_name": "Middle_Name",
                          "basic.gender": "Gender",
                          "basic.credential": "Credential",
                          "basic.sole_proprietor": "Sole_Proprietor",
                          "telephone_number": "Phone_Number",
                          "desc": "Taxonomy",
                          "state_x":"State",
                          "enumeration_type": "Enumeration_Type",
                          "city":"City",
                          "postal_code":"Zip"
                         }, inplace=True)
result_df.head()

# Select columns to keep (instead of drop, in case NPI adds columns later)
result_df = result_df[['NPI_Number','Enumeration_Type','address_purpose','City', 'State', 'Zip',
       'Phone_Number','First_Name', 'Last_Name', 'Middle_Name', 'Credential',
       'Sole_Proprietor', 'Gender','basic.status','Taxonomy']]
result_df.head()

# Clean the DataFrame
    #Keep only Mailing address lines, to remove duplicate entries and keep only Active NPIs. Remove columns no longer needed like status.
result_df_mail = result_df.loc[result_df['address_purpose'] == 'MAILING']
result_df_status = result_df_mail.loc[result_df_mail['basic.status'] == 'A']
result_df_2 = result_df_status.drop(columns=['Enumeration_Type', 'address_purpose','basic.status'])
result_df_2.head()

# Create dummy variables from the "Taxonomy" column
result_df_taxonomy_search = pd.get_dummies(result_df_2, columns=['Taxonomy'], prefix="Taxonomy")
result_df_taxonomy_search.head()

# Remove Duplicates (and the taxonomy column) to get a list of unique providers
result_df_unique = result_df_2.drop_duplicates(subset="NPI_Number", keep='first', inplace=False, ignore_index=False)
result_df_unique = result_df_unique.dropna(subset=['Phone_Number'])
result_df_unique

# Save the results to an Excel file with one sheet per DataFrame above.
with pd.ExcelWriter('NPI_Provider_Info.xlsx') as writer:  
    result_df_unique.to_excel(writer, sheet_name='Unique_Provider_List')
    result_df_taxonomy_search.to_excel(writer, sheet_name='Providers_by_Taxonomy')