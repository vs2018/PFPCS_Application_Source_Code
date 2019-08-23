#Data Source: https://www.doogal.co.uk/UKPostcodes.php
postcodes_m = ["AB10 1AB",
"AL1 1AG",
"B1 1AY",
"BA1 0AQ",
"BB1 1AB",
"BD1 1AF",
"BH1 1AA",
"BL0 0AA",
"BN1 1AA",
"BR4 9AE",
"CA1 1AA",
"BS1 1AD",
"CF10 1AA",
"CH1 1AF",
"CR0 0AA",
"CV1 1AH",
"CW1 2AF",
"DD1 1AA",
"DE1 1AA",
"DG1 1AA",
"DH1 1AB",
"DL1 1AA",
"DN1 1AA",
"DT1 1AA",
"DY1 1AE",
"EC1A 1AA",
"E1 0AA",
"EH1 1AD",
"EN1 1AA",
"EX1 1AE",
"FK1 1AA",
"FY1 1AD",
"G1 1DA",
"GL1 1AE",
"GU1 1AA",
"HA0 1AB",
"HD1 1AA",
"HG1 1AA",
"HP1 1AB",
"HR1 1AA",
"HS1 2AD",
"HU1 1AA",
"HX1 1AA",
"IV1 1AA",
"KA1 1AD",
"KT1 1AA",
"KW1 4AA",
"KY1 1AB",
"L1 0AA",
"LA1 1AA",
"LD1 5AB",
"LE1 1AD",
"LL11 1AA",
"LN1 1AB",
"LS1 1AZ",
"LU1 1AA",
"M1 1AD",
"MK1 1AX",
"ML1 1AA",
"N1 0AA",
"NE1 1AD",
"NG1 1AA",
"NN1 1AF",
"NP10 0AA",
"NW1 0AA",
"OL1 1AA",
"OX1 1AA",
"PA1 1AD",
"PE1 1AB",
"PH1 0AD",
"PL1 1AE",
"PO1 1AA",
"PR0 2AA",
"RG1 1AF",
"RH1 1AA",
"S1 1AA",
"SA1 1AA",
"SE1 0AA",
"SG1 1AA",
"SM1 1AA",
"SK1 1AL",
"SL0 0AA",
"SN1 1AE",
"SO14 0AA",
"SP1 1AD",
"SR1 1AE",
"ST1 1AP",
"SW10 0AA",
"SY1 1AA",
"TD1 1AA",
"TA1 1AA",
"TF1 1AA",
"TQ1 1AG",
"TR1 1AA",
"TS1 1AA",
"TW1 1AA",
"W10 4AA",
"WC1A 1AB",
"WA1 1AF",
"WD17 1AA",
"WF1 1AA",
"WN1 1AA",
"WR1 1AA",
"WS1 1AA",
"WV1 1AA",
"YO1 0FA",
"ZE1 0AA"]

#Data Source: https://www.doogal.co.uk/UKPostcodes.php
city = ["Aberdeen City",
"St Albans",
"Birmingham",
"Bath and North East Somerset",
"Blackburn with Darwen",
"Bradford",
"Bournemouth, Christchurch and Poole",
"Bury",
"Brighton and Hove",
"Bromley",
"Carlisle",
"Bristol, City of",
"Cardiff",
"Cheshire West and Chester",
"Croydon",
"Coventry",
"Cheshire East",
"Dundee City",
"Derby",
"Dumfries and Galloway",
"County Durham",
"Darlington",
"Doncaster",
"Dorset",
"Dudley",
"Islington",
"Tower Hamlets",
"City of Edinburgh",
"Enfield",
"Exeter",
"Falkirk",
"Blackpool",
"Glasgow City",
"Gloucester",
"Guildford",
"Brent",
"Kirklees",
"Harrogate",
"Dacorum",
"Herefordshire, County of",
"Na h-Eileanan Siar",
"Kingston upon Hull, City of",
"Calderdale",
"Highland",
"East Ayrshire",
"Kingston upon Thames",
"Highland",
"Fife",
"Liverpool",
"Lancaster",
"Powys",
"Leicester",
"Wrexham",
"Lincoln",
"Leeds",
"Luton",
"Manchester",
"Milton Keynes",
"North Lanarkshire",
"Islington",
"Newcastle upon Tyne",
"Nottingham",
"Northampton",
"Newport",
"Camden",
"Oldham",
"Oxford",
"Renfrewshire",
"Peterborough",
"Perth and Kinross",
"Plymouth",
"Portsmouth",
"Preston",
"Reading",
"Reigate and Banstead",
"Sheffield",
"Swansea",
"Southwark",
"Stevenage",
"Sutton",
"Stockport",
"South Bucks",
"Swindon",
"Southampton",
"Wiltshire",
"Sunderland",
"Stoke-on-Trent",
"Hammersmith and Fulham",
"Shropshire",
"Scottish Borders",
"Somerset West and Taunton",
"Telford and Wrekin",
"Torbay",
"Cornwall",
"Middlesbrough",
"Richmond upon Thames",
"Westminster",
"Camden",
"Warrington",
"Watford",
"Wakefield",
"Wigan",
"Worcester",
"Walsall",
"Wolverhampton",
"York",
"Shetland Islands"]

import datetime
#Source: Requests library - get function to send HTTP request, URL: https://2.python-requests.org/en/master/
import requests
import json
import time

def api_call():
    for code in postcodes_m:
        #Adapted from: https://panel.ukvehicledata.co.uk/Code-Examples-Python.aspx
        result = requests.get(f'https://uk1.ukvehicledata.co.uk/api/datapackage/FuelPriceData?v=2&api_nullitems=1&auth_apikey=270a5ba1-4ff1-4876-8ebf-3cddd33d66b6&user_tag=&key_postcode={code}')
        json_object = result.json()
        #Adapted from: Author:phihag, Date:Sep 6 '12 at 22:23, URL:https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
        with open(f'data-{code}.json', 'w') as outfile:
            json.dump(json_object, outfile, indent=2)
        #Source: https://www.pythoncentral.io/pythons-time-sleep-pause-wait-sleep-stop-your-code/
        #Source: Author: user1720897, Date: May 25 '15 at 16:53, URL:https://stackoverflow.com/questions/30442757/measuring-the-http-response-time-with-requests-library-in-python-am-i-doing-it
        time.sleep(result.elapsed.total_seconds())

def master_file():
    obj = {
        "Date": [],
        "SearchPostCode": [],
        "City": [],
        "DistanceFromSearchPostcode": [],
        "Brand": [],
        "Name": [],
        "Street": [],
        "Town": [],
        "County": [],
        "PostCode": [],
        "FuelType": [],
        "Price": [],
        "TimeRecorded": []
    }

    today = datetime.date.today()
    today = str(today)

    for num,code in enumerate(postcodes_m,start=0):
        #Adapted from: Author:lcastillov, Date:Jul 28 '16 at 18:53, URL:https://stackoverflow.com/questions/38644480/reading-json-file-with-python-3
        with open(f'data-{code}.json', 'r') as f:
            data = json.load(f)


        for d in data['Response']['DataItems']['FuelStationDetails']['FuelStationList']:

            for p in d['FuelPriceList']:
                obj['Date'].append(today)
                obj['SearchPostCode'].append(data['Request']['DataKeys']['Postcode'])
                print(city[num])
                obj['City'].append(city[num])
                obj['DistanceFromSearchPostcode'].append(d['DistanceFromSearchPostcode'])
                obj['Brand'].append(d['Brand'])
                obj['Name'].append(d['Name'])
                obj['Street'].append(d['Street'])
                obj['Town'].append(d['Town'])
                obj['County'].append(d['County'])
                obj['PostCode'].append(d['Postcode'])
                obj['FuelType'].append(p['FuelType'])
                obj['Price'].append(p['LatestRecordedPrice']['InPence'])
                obj['TimeRecorded'].append(p['LatestRecordedPrice']['TimeRecorded'])

    #Adapted from: Author:phihag, Date:Sep 6 '12 at 22:23, URL:https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
    with open(f'master_json_{today}.json', 'w') as outfile:
        json.dump(obj, outfile, indent=2)

##############################################################################################################################
def concat_dataframes():
    dates = [
    "2019-05-30",
    "2019-05-31",
    "2019-06-01",
    "2019-06-02",
    "2019-06-03",
    "2019-06-04",
    "2019-06-05",
    "2019-06-06",
    "2019-06-07",
    "2019-06-08",
    "2019-06-09",
    "2019-06-10",
    "2019-06-11",
    "2019-06-12",
    "2019-06-13",
    "2019-06-14",
    "2019-06-15",
    "2019-06-16",
    "2019-06-17",
    "2019-06-18",
    "2019-06-19"
    ]
    #Source: Pandas library used for creating a DataFrame, URL: https://pandas.pydata.org/pandas-docs/stable/
    from pandas import DataFrame
    import pandas as pd

    df = []

    for date in dates:
        #Adapted from: Author:lcastillov, Date:Jul 28 '16 at 18:53, URL:https://stackoverflow.com/questions/38644480/reading-json-file-with-python-3
        with open(f'master_json_{date}.json', 'r') as f:
                d = json.load(f)
                df.append(DataFrame(d))

    #Source: Author: WeNYoBen, Date:Dec 26 '18 at 3:48, URL:https://stackoverflow.com/questions/53927219/pandas-concat-two-data-frames-one-with-and-one-without-headers
    df1 = pd.concat(df, axis=0)

    #Source: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_csv.html
    df1.to_csv("master_data_file.csv",index=False)

api_call()
master_file()
