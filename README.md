# Mental-Health-Provider-Search
This repository is a tool to find Mental Health Provider contact information. At time of publishing, the repository includes code to search the [NPPES provider database] (https://npiregistry.cms.hhs.gov/search) using their API to return a spreadsheet of providers that match the search criteria.

Many individuals who have sought mental healthcare services struggle to find a provider who meets their needs. There are a vast number sources of provider information across the internet. Websites such as [Psychology Today] (https://www.psychologytoday.com/us) privatize Therapist information, so users cannot find their phone number or email to contact. Instead, Psychology Today uses a messaging feature and creates unique phone numbers so they can track messages and calls coming from their website. This means that providers who post their information across multiple platforms often have to keep track of updating multiple sources of information.

All health care providers in the U.S. are required to register with the NPPES. This makes their registry a good first source of provider information which can be appended to using scraping techniques for other websites, like Psyschology Today, in the future.

The intent of this repository is to add additional code for other sources of provider information in the future. Users will add their search criteria in the "Input.py" file, which can be imported into other python files to feed additional queries.

The output of the NPI Search file is an excel file with multiple sheets. There is one sheet that can be used as a master list of providers meeting their search criteria, with all of the available taxonomies (healthcare areas of expertise) for each provider. Users can filter for only certain taxonomies using the dummy columns. The other sheet is a list or providers with one row per provider, only including providers with phone numbers. This sheet can be used to track phone calls to certain providers. Once saved locally, a user could add a new column to indicate if they have interest in or have called each provider to aid their search.

Future development of this repository could include a front end mechanism for non-technical users in order to help as many people as possible access mental healtcare resources.
