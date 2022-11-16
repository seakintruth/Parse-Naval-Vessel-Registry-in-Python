# prerequisits are:
# pip install pandas bs4 lxml pyarrrow
# maybe ... pip install hml5lib ...?

import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from random import randint as rand_between
from pathlib import Path
# pretend to be a browser: https://stackoverflow.com/a/43590290
url = 'https://www.nvr.navy.mil/QUICKFIND/SHIPSDETAIL_HULLBYNAME_ALL.HTML'
header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

s = requests.session()
r = s.get(url, stream=True, headers=header) 
# get the list of all ships by hull name
table_NVR = pd.read_html(r.text, flavor='bs4')
df_ship_names = pd.DataFrame(table_NVR[1][[0,1]][3:])
df_ship_names.columns = ["Hull","Name"]

# Get the list of all URLS
soup = BeautifulSoup(r.text, 'html.parser') 
urls = []
for link in soup.find_all('a'):    
    data = link.get('href')
    id_value = link.get('id')
    if id_value == 'MainContent_rptr1_HullLink_0':
        urls.append('https://www.nvr.navy.mil/SHIPDETAILS/' + data[15:])
r.close()
s.close()

# columns for the main dataframe
column_names = [
    "Hull",
    "Name",
    "Name (Hull)", 
    "Ship Alt Title",
    "Ship Type",
    "Class", 
    "UIC",
    "Status",
    "Fleet",
    "Date Status Last Changed",
    "Homeport",
    "Maintenance Category",
    "Berth",
    "Force",
    "Builder",
    "Award Date",
    "Commission Date",
    "Keel Date",
    "Inactivation Date",
    "Launch Date",
    "Decommission Date",
    "Delivery Date",
    "InService Date",
    "Out Service Date",
    "Stricken Date",
    "Overall Length",
    "Waterline Length",
    "Extreme Beam",
    "Waterline Beam",
    "Max Navigational Draft",
    "Draft Limit",
    "Light Displacement",
    "Full Displacement",
    "Dead Weight",
    "Hull Material",
    "No. of Propellers",
    "No. of Waterjets",
    "Propulsion Type",
    "Accommodations Officers",
    "Accommodations Enlisted",
    "Custodian",
    "Planning Yard",
    "Nuclear Planning Yard",
    "Ships Program Manager",
    "Comments",
    "Last Updated"
]

df_ship_detail = pd.DataFrame(columns = column_names, index = range(len(df_ship_names)))
# set data frame values to strings
df_ship_detail = df_ship_detail.astype(str)
df_ship_names = df_ship_names.astype(str)
count_url = 0
sleep(rand_between(500,1500)/1000) # being polite to the web server 0.5 to 1.5 seconds between calls

for link_url in urls:
    try:
        s = requests.session()
        r_url = s.get(link_url, stream=True, headers=header) 
        table_ship = pd.read_html(r_url.text) #, flavor='bs4')
        r_url.close()
        s.close()
        ship_name = df_ship_names.iloc[count_url]['Name']
        ship_hull = df_ship_names.iloc[count_url]['Hull']
        df_ship_detail.loc[count_url]['Hull'] = ship_hull
        df_ship_detail.loc[count_url]['Name'] = ship_name
        df_ship_detail.loc[count_url]['Name (Hull)'] =  table_ship[2][1][0]
        df_ship_detail.loc[count_url]['Ship Alt Title'] = table_ship[2][1][1]
        df_ship_detail.loc[count_url]['Ship Type'] = table_ship[2][1][2]
        df_ship_detail.loc[count_url]['Class'] = table_ship[2][2][6]
        df_ship_detail.loc[count_url]['UIC'] = table_ship[2][8][6]
        df_ship_detail.loc[count_url]['Status'] = table_ship[2][2][7]
        df_ship_detail.loc[count_url]['Fleet'] = table_ship[2][8][7]
        df_ship_detail.loc[count_url]['Date Status Last Changed'] = table_ship[2][2][8]
        df_ship_detail.loc[count_url]['Homeport'] = table_ship[2][8][8]
        df_ship_detail.loc[count_url]['Maintenance Category'] =  table_ship[2][2][9]
        df_ship_detail.loc[count_url]['Berth'] = table_ship[2][8][9]
        df_ship_detail.loc[count_url]['Force'] =  table_ship[2][2][10]
        df_ship_detail.loc[count_url]['Builder'] =   table_ship[2][2][11]
        df_ship_detail.loc[count_url]['Award Date'] = table_ship[2][2][14]
        df_ship_detail.loc[count_url]['Commission Date'] = table_ship[2][8][14]
        df_ship_detail.loc[count_url]['Keel Date'] = table_ship[2][2][15]
        df_ship_detail.loc[count_url]['Inactivation Date'] = table_ship[2][8][15]
        df_ship_detail.loc[count_url]['Launch Date'] = table_ship[2][2][16]
        df_ship_detail.loc[count_url]['Decommission Date'] = table_ship[2][8][16]
        df_ship_detail.loc[count_url]['Delivery Date'] = table_ship[2][2][18]
        df_ship_detail.loc[count_url]['InService Date'] = table_ship[2][8][18]
        df_ship_detail.loc[count_url]['Out Service Date'] = table_ship[2][8][19]
        df_ship_detail.loc[count_url]['Stricken Date'] = table_ship[2][8][20]
        df_ship_detail.loc[count_url]['Overall Length'] = table_ship[2][2][24]
        df_ship_detail.loc[count_url]['Waterline Length'] = table_ship[2][8][24]
        df_ship_detail.loc[count_url]['Extreme Beam'] = table_ship[2][2][25]
        df_ship_detail.loc[count_url]['Waterline Beam'] =  table_ship[2][8][25]
        df_ship_detail.loc[count_url]['Max Navigational Draft'] = table_ship[2][2][26]
        df_ship_detail.loc[count_url]['Draft Limit'] =  table_ship[2][8][26]
        df_ship_detail.loc[count_url]['Light Displacement'] = table_ship[2][2][27]
        df_ship_detail.loc[count_url]['Full Displacement'] = table_ship[2][8][27]
        df_ship_detail.loc[count_url]['Dead Weight'] = table_ship[2][2][28]
        df_ship_detail.loc[count_url]['Hull Material'] =  table_ship[2][3][29]
        df_ship_detail.loc[count_url]['No. of Propellers'] = table_ship[2][2][30]
        df_ship_detail.loc[count_url]['No. of Waterjets'] = table_ship[2][3][31]
        df_ship_detail.loc[count_url]['Propulsion Type'] = table_ship[2][3][32]
        df_ship_detail.loc[count_url]['Accommodations Officers'] =  table_ship[2][5][33]
        df_ship_detail.loc[count_url]['Accommodations Enlisted'] = table_ship[2][5][34]
        df_ship_detail.loc[count_url]['Custodian'] = table_ship[2][4][37]
        df_ship_detail.loc[count_url]['Planning Yard'] = table_ship[2][4][38]
        df_ship_detail.loc[count_url]['Nuclear Planning Yard'] = table_ship[2][4][39]
        df_ship_detail.loc[count_url]['Ships Program Manager'] = table_ship[2][4][40]
        df_ship_detail.loc[count_url]['Comments'] = table_ship[2][4][41]
        df_ship_detail.loc[count_url]['Last Updated'] = table_ship[2][4][42]
    except Exception as e:
        try:
<<<<<<< HEAD
            if (Path.cwd() / 'NVR_Error.csv').is_file:
                header_line = ''
            else:
=======
            header_line = ''
            if (Path.cwd() / 'NVR_Error.csv').is_file:
>>>>>>> e127ac923851bbb8a92120dadc79a5c3d81e1c73
                header_line = '"Timestamp","Page Number","Hull","Name","URL"\n'
            f_error = open('NVR_Error.csv','a')
            f_error.write( header_line +
                f'"{str(pd.Timestamp.utcnow().asm8)}",'+
                f'"{count_url}",'+
                f'"{ship_hull}",'+
                f'"{ship_name}",'+
                f'{link_url}\n'
            )
            f_error.close()
        except Exception:
            # If an error occurs in the error handler, ignore this error
            pass

    count_url+=1    
    sleep(rand_between(500,1500)/1000) # being polite to the web server 0.5 to 1.5 seconds between calls should take roughly 1.3 hours to run
    if count_url % 25 == 0 :    
        # Write the results to a draft file every 25 pages - capture progress
        df_ship_detail[:count_url].to_csv("NVR_Dataset_Draft.csv",sep=',',na_rep='',index=False,index_label=False,quoting=1,quotechar='"')

# Write results when completed 
df_ship_detail.to_csv("NVR_Dataset.csv",sep=',',na_rep='',index=False,index_label=False,quoting=1,quotechar='"')
df_ship_detail.to_feather("NVR_Dataset.feather")

# Delete the draft files
path_cwd = Path.cwd()
path_draft_csv = (path_cwd  / 'NVR_Dataset_Draft.csv')

if path_draft_csv.is_file() == True:
    path_draft_csv.unlink() # missing_ok=True)

path_draft_feather = (path_cwd  / 'NVR_Dataset_Draft.feather')
if path_draft_feather.is_file() == True:
<<<<<<< HEAD
    path_draft_feather.unlink() # missing_ok=True)
=======
    path_draft_feather.unlink() # missing_ok=True)
>>>>>>> e127ac923851bbb8a92120dadc79a5c3d81e1c73
