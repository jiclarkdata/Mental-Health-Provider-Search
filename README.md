# Mental-Health-Provider-Search
## __Description__:
This repository is a tool to find Mental Health Provider contact information. At time of publishing, the repository includes code to search the [NPPES provider database] (https://npiregistry.cms.hhs.gov/search) using their API to return a spreadsheet of providers that match the search criteria.

Many individuals who have sought mental healthcare services struggle to find a provider who meets their needs. There are a vast number of sources of provider information across the internet. Websites such as Psychology Today (https://www.psychologytoday.com/us) privatize therapist information, so users cannot find their phone number or email to contact. Instead, Psychology Today uses a messaging feature and creates unique phone numbers so they can track messages and calls coming from their website. This means that providers who post their information across multiple platforms often have to keep track of updating multiple sources of information.

All health care providers in the U.S. are required to register with the NPPES. This makes their registry a good first source of provider information which can be appended to using scraping techniques for other websites, like Psychology Today, in the future.

The intent of this repository is to add additional code for other sources of provider information in the future. Users will add their search criteria in the "Input.py" file, which can be imported into other python files to feed additional queries.

The output of the NPI Search file is an excel file with multiple sheets. There is one sheet that can be used as a master list of providers meeting their search criteria, with all of the available taxonomies (healthcare areas of expertise) for each provider. Users can filter for only certain taxonomies using the dummy columns. The other sheet is a list of providers with one row per provider, only including providers with phone numbers. This sheet can be used to track phone calls to certain providers. Once saved locally, a user could add a new column to indicate if they have interest in or have called each provider to aid their search.

Future development of this repository could include a front end mechanism for non-technical users in order to help as many people as possible access mental healthcare resources.

## __Setup__:
1. Clone this repo
2. Install necessary packages
- Requests
- Pandas
- Openpyxl
3. Run the file “Input.py” to enter search criteria.
Searchable Columns (Columns marked “Yes” in the Data Dictionary)
- Zip Code
- City
- 2-Digit State (e.g. CA)
- 10-Digit NPI Number
- Provider First Name
- Provider Last Name
4. Run the “NPI_Provider_Search.py” file to get the XLSX document with provider information.

## __Data Dictionary__:
*Note: There is no column for Data Type because all columns are converted to string in python.

|	Output Column	|	NPPES JSON Field Name	|	Example	|	Description	|	Available as Input Search? (Yes or Blank)	|
|	-------------	|	-------------	|	-------------	|	-------------	|	-------------	|
|	NPI_Number	|	number	|	1699123448	|	Unique ID, always 10 digits.	|	Yes	|
|	City	|	addresses[1].city	|	SALEM	|		|	Yes	|
|	State	|	addresses[1].state	|	OR	|	Always just two capital letters.	|	Yes	|
|	Zip	|	addresses[1].postal_code	|	973010198	|	Can be either the 5 or 9-digit zip code.	|	Yes	|
|	Phone_Number	|	addresses[1].telephone_number	|	503-390-5637	|		|		|
|	First_Name	|	basic.first_name	|	JANE	|		|	Yes	|
|	Last_Name	|	basic.last_name	|	SMITH	|		|	Yes	|
|	Middle_Name	|	basic.middle_name	|	MARIE	|		|		|
|	Credential	|	basic.credential	|	MFT	|	This will include their license credential type.	|		|
|	Sole_Proprietor	|	basic.sole_proprietor	|	NO	|	This indicates if they are a sole proprietor or part of business (different from Enumeration Type.	|		|
|	Gender	|	basic.gender	|	F	|	M or F	|		|
|	Taxonomy	|	taxonomies[0].desc	|	Counselor	|	References the Provider’s classification of practice. This is used to filter for mental health providers.	|		|
|	Enumeration_Type	|	enumeration_type	|	NPI-1	|	*Not displayed in output Always NPI-1, which refers to Individual Providers (as opposed to Organizational Providers).	|		|
|	address_purpose*	|	addresses[1].address_purpose	|	MAILING	|	*Not displayed in output Always Mailing, because there are multiple types of addresses and mailing is the most reliable source of phone number.	|		|

## __Contact__:
Jessica Clark: jessica.clark97@gmail.com
