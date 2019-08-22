import requests
import json
import pandas as pd

# from fuel_prediction_algorithm import *
# from fuel_maps_api import *
from fuel_prediction_algorithm_class import *
from fuel_maps_api_class import *

# from fuel_model import *
import datetime


class Processor:
    def __init__(self, brand, town, county, post_code, fuel_type, price, search):
        self.brand = brand
        self.town = town
        self.county = county
        self.post_code = post_code
        self.fuel_type = fuel_type
        self.price = price
        self.search = search
        self.master = pd.read_csv("master_data_file_updated.csv")
        # self.data = self.save()
        # self.predictor_result = None
        # self.transformer_result = None
        print(
            self.brand,
            self.town,
            self.county,
            self.post_code,
            self.fuel_type,
            self.price,
            self.search,
            "Processor init output",
        )

    def generate_outcode(self, post_code):
        print(post_code, "Processor generate_outcode input")
        ###print("•••••••••••••••••••••••••••••••••••••••••ENTERING GENERATE OUTCODE FUNCTION - INSIDE",post_code)
        outcode = post_code.split(" ")[0]
        result = ""
        for chr in outcode:
            if chr.isalpha():
                result += chr

        # #print("•••••••••••••••••••••••••••••••••••••••••INSIDE GENERATE OUTCODE FUNCTION - OUTCODE",outcode)
        # #print("•••••••••••••••••••••••••••••••••••••••••RESULT OF GENERATE OUTCODE FUNCTION - INSIDE",result)
        print(result, "Processor generate_outcode output")
        return result

    def generate_matching_post_codes(self, outcode, unique_post_codes):
        print(
            outcode, unique_post_codes, "Processor generate_matching_post_codes input"
        )
        ##print("•••••••••••••••••••••••••••••••••••••••••ENTERING GENERATE MATCHING POST CODES FUNCTION - INSIDE FUNCTION",outcode,unique_post_codes)
        matching_post_codes = []
        for pc in unique_post_codes:
            outcode_master = self.generate_outcode(pc)
            # #print("•••••••••••••••••••••••••••••••••••••••••ENTERING GENERATE MATCHING POST CODES FUNCTION - INSIDE FUNCTION - GENERATE_OUTCODE",outcode_master,outcode)

            if outcode == outcode_master:
                matching_post_codes.append(pc)
        # print("•••••••••••••••••••••••••••••••••••••••••RESULT OF GENERATE MATCHING POST CODES FUNCTION - INSIDE FUNCTION",matching_post_codes)
        print(matching_post_codes, "Processor generate_matching_post_codes output")
        return matching_post_codes

    # def get_coordinates(self,post_code):
    #     print(post_code,"Processor get_coordinates input")
    #     r = requests.get(f"https://api.postcodes.io/postcodes/{post_code}")
    #     r = r.json()
    #     lat = r['result']['latitude']
    #     lon = r['result']['longitude']
    #     print(lat,lon,"Processor get_coordinates output")
    #     return lat,lon

    def get_relevant_post_codes(self, df):
        print(df, "Processor get_relevant_post_codes input")
        # print("•••••••••••••••••••••••••••••••••••••••••ENTERING GET RELEVANT POST CODES FUNCTION",post_code,df)
        unique_post_codes = df["PostCode"].unique().tolist()
        # unique_post_codes = self.generate_unique_col_values("PostCode",df)
        # print("•••••••••••••••••••••••••••••••••••••••••INSIDE GENERATE LATLON OBJ FUNCTION - OBTAIN UNIQUE POST CODES",unique_post_codes)
        outcode = self.generate_outcode(self.post_code)
        # print("•••••••••••••••••••••••••••••••••••••••••INSIDE GENERATE LATLON OBJ FUNCTION - OBTAIN OUTCODES",outcode)
        matching_post_codes = self.generate_matching_post_codes(
            outcode, unique_post_codes
        )
        # print("•••••••••••••••••••••••••••••••••••••••••INSIDE  GENERATE LATLON OBJ FUNCTION - GENERATE MATCHING POST CODES",matching_post_codes)
        print(matching_post_codes, "Processor get_relevant_post_codes output")
        return matching_post_codes

    def generate_latlon_obj(self, matching_pc_list):
        print(matching_pc_list, "Processor generate_latlon_obj input")

        # print("•••••••••••••••••••••••••••••••••••••••••ENTERING GENERATE LATLON OBJ FUNCTION",matching_pc_list)
        latlon_list = []
        for idx, pc in enumerate(matching_pc_list):
            # lat,lon = get_coordinates(pc)
            try:
                latlon = MapboxDirections.generate_latlon(pc)
            except IndexError as e:
                # print(e)
                latlon = MapboxDirections.generate_latlon(matching_pc_list[idx - 1])
            lat, lon = latlon[1], latlon[0]
            # print("•••••••••••••••••••••••••••••••••••••••••INSIDE GENERATE LATLON OBJ FUNCTION ----- CALLING GET COORDINATES",lat,lon)
            latlon_list.append((lat, lon))
        # print("•••••••••••••••••••••••••••••••••••••••••INSIDE GENERATE LATLON OBJ FUNCTION ----- LATLON_LIST VARIABLE",latlon_list)
        latlon_obj = []
        for data in latlon_list:
            # print("•••••••••••••••••••••••••••••••••••••••••INSIDE GENERATE LATLON OBJ FUNCTION ----- APPENDING LAT/LON TO LAT/LON OBJ",data)
            latlon_obj.append({"latitude": data[0], "longitude": data[1]})
        print(latlon_obj, "Processor generate_latlon_obj output")
        return latlon_obj

    def call_distance_api(self, lat, lon, obj, matching_pc_list):
        print(lat, lon, obj, matching_pc_list, "Processor call_distance_api input")
        # print("entering call distance api",lat,lon,obj,matching_pc_list)
        api_data = {
            "origins": [{"latitude": lat, "longitude": lon}],
            "destinations": obj,
            "travelMode": "driving",
        }

        headers = {"Content-Type": "application/json", "Content-Length": "450"}
        r = requests.post(
            "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?key=AmM7OZ0sgIaFYe-IFV1nQQ7Q-IO2Yd--qdtoTO9OTKOHOe4gS4osOrtgsWVa5lxx",
            data=json.dumps(api_data),
            headers=headers,
        )
        r = r.json()
        distances = []
        for idx, data in enumerate(r["resourceSets"][0]["resources"][0]["results"]):
            distances.append(
                {"post_code": matching_pc_list[idx], "distance": data["travelDistance"]}
            )
        sorted_list = sorted(distances, key=lambda k: k["distance"])
        # print(sorted_list,"call distance api sorted distances")
        sorted_post_codes = [d["post_code"] for d in sorted_list]
        # print("result of call distance api", sorted_post_codes)
        print(sorted_post_codes, "Processor call_distance_api output")
        return sorted_post_codes

    def nearest_postcode(self, df):
        print(df, "Processor nearest_postcode input")
        # print("•••••••••••••••••••••••••••••••••••••••••ENTERING NEAREST POSTCODES FUNCTION",post_code,county,town,df)
        # lat,lon = get_coordinates(post_code)
        latlon = MapboxDirections.generate_latlon(self.post_code)
        lat, lon = latlon[1], latlon[0]
        # print("•••••••••••••••••••••••••••••••••••••••••RESULT OF GET COORDINATES FUNCTION",lat,lon)
        matching_pc = self.get_relevant_post_codes(df)
        # print("•••••••••••••••••••••••••••••••••••••••••RESULT OF GET RELEVANT POST CODES FUNCTION",matching_pc)
        obj = self.generate_latlon_obj(matching_pc)
        # print("•••••••••••••••••••••••••••••••••••••••••RESULT OF GET GENERATE LATLON OBJ FUNCTION",obj)
        nearest_pc_list = self.call_distance_api(lat, lon, obj, matching_pc)
        print(nearest_pc_list, "Processor nearest_postcode output")
        return nearest_pc_list

    def generate_brand_filtered_df(self, bool):
        print(bool, "Processor generate_brand_filtered_df input")
        # print("•••••••••••••••••••••••••••••••••••••••••ENTERING GENERATE BRAND FILTERED DF FUNCTION",brand,df,bool)
        unique_brands = self.master["Brand"].unique().tolist()
        # unique_brands = self.generate_unique_col_values("Brand",df)
        # print("UNIQUE BRANDS",unique_brands)
        supermarkets = ["TESCO", "MORRISONS", "ASDA", "SAINSBURYS"]
        brands_filter = []
        for supermarket in supermarkets:
            for self.brand in unique_brands:
                if supermarket in self.brand:
                    brands_filter.append(self.brand)
        if bool == True:
            df = self.master[self.master["Brand"].isin(brands_filter)]
        else:
            df = self.master[~self.master["Brand"].isin(brands_filter)]
        print(df, "Processor generate_brand_filtered_df output")
        return df

    def determine_brand_type(self):
        print("Processor determine_brand_type input")
        for supermarket in ["TESCO", "MORRISONS", "ASDA", "SAINSBURYS"]:
            if supermarket in self.brand:
                # print(supermarket,brand,"the brand is in supermarket")
                result = True
            else:
                result = False
        print(result, "Processor determine_brand_type output")
        return result

    def transformer(self):
        print("Processor transformer input")
        ###print("3.4")
        # print("#################INPUTS TO PREDICTION PRE-PROCESSING FUNCTION",brand,county,town,post_code,fuel_type,frequency,search)
        dataframe_post_codes = self.master["PostCode"].unique().tolist()
        # dataframe_post_codes = self.generate_unique_col_values("PostCode",self.master)
        # print("#################DATAFRAME POST CODES LENGTH",len(dataframe_post_codes))
        # print(dataframe_post_codes)
        if self.post_code not in dataframe_post_codes:
            brand_type_bool = self.determine_brand_type()
            # print("#################RESULT OF DETERMINE BRAND TYPE",brand_type_bool)
            if brand_type_bool == True:
                # print(len(self.master),'master df length')
                df = self.generate_brand_filtered_df(True)
                # print("#################SUPERMARKET FILTERED DATAFARME",df)
                # print(len(df),"supermarket df")
            else:
                df = self.generate_brand_filtered_df(False)
                # print("#################OIL COMPANY FILTERED DATAFARME",df)
                # print(len(df),"oil df")
            post_code_list = self.nearest_postcode(df)
            # print("#################RESULT OF CALLING NEAREST POST CODE FUNCTION",post_code_list)
            for p_code in post_code_list:
                post_code = p_code
                # print(p_code,fuel_type,"before filtered dataframe for nearest post code")
                df1 = self.master[
                    (self.master["PostCode"] == p_code)
                    & (self.master["FuelType"] == self.fuel_type)
                ]
                # print("#################FILTERED DATAFRAME FOR NEAREST POST CODE",df1)
                if len(df1) > 0:
                    break
        else:
            df1 = self.master[
                (self.master["PostCode"] == self.post_code)
                & (self.master["FuelType"] == self.fuel_type)
                & (self.master["Brand"] == self.brand)
            ]
            # print("#################FILTERED DATAFRAME FOR ACTUAL POST CODE",df1)
        df1 = df1.loc[~df1.index.duplicated(keep="first")]
        # self.transformer_result = df1
        print(df1, "Processor transformer output")
        return df1

    def predictor(self, df1):
        print(df1, "Processor predictor input")
        # print("#################INPUTS TO PREDICTION PROCESSING FUNCTION",df1,frequency,fuel_type,brand,post_code)
        df2 = df1[["Date", "Price"]]
        # print(df2)
        df2["Date"] = pd.to_datetime(df2["Date"])
        df2.set_index("Date", inplace=True)
        today = pd.Timestamp("today").strftime("%Y-%m-%d")
        df_today = pd.DataFrame({"Date": [str(today)], "Price": self.price})
        df_today["Date"] = pd.to_datetime(df_today["Date"])
        df_today.set_index("Date", inplace=True)
        # print(df_today,"new today df")
        df2 = pd.concat([df2, df_today])
        # print(df2,"concatenated")
        df2 = df2.loc[~df2.index.duplicated(keep="first")]
        df2 = df2.resample(rule="1D").interpolate()
        # print("#################INPUTS TO PREDICTION FORECAST DAILY FUNCTION ARIMA MODEL CLASS",df2,frequency,fuel_type,brand,post_code)
        model = ArimaModel(df2, "Price", 1, self.fuel_type, self.brand, self.post_code)
        result = model.prediction()
        # self.predictor_result = result
        print(result, "Processor predictor output")
        return result

    def loader(self):
        print("Processor loader input")
        df1 = self.transformer()
        # print("#####################RESULT FROM CALLING PREDICTION PRE-PROCESSING",df1)
        result = self.predictor(df1)
        # print("###################RESULT FROM CALLING PREDICTION PROCESSING",result)
        confidence = result["Error"].iloc[0]
        prediction = result["Prediction"].iloc[0]
        model = result["Model"].iloc[0]
        # if frequency == 1:
        #     prediction = result['Prediction'].iloc[0]
        # elif frequency == 7:
        #     prediction = list(result['Prediction'])
        print(prediction, confidence, model, result, df1, "Processor loader output")
        return (prediction, confidence, model, result, df1)

    def save(self):
        p_obj = {
            "1-Day Price Prediction": None,
            "1-Day Prediction Confidence": None,
            "1-Day Prediction Model": None,
        }
        try:
            tomorrow_price, tomorrow_confidence, tomorrow_model, prediction, df = (
                self.loader()
            )
        except Exception as e:
            # print(e,"#########################EXCEPTION OCCURED IN PREDICTION CAUSING CONFIDENCE TO BE 9999 ###########################################################")
            tomorrow_price, tomorrow_confidence, tomorrow_model = (
                self.price,
                99999,
                "N/A",
            )
        p_obj["1-Day Price Prediction"] = tomorrow_price
        p_obj["1-Day Prediction Confidence"] = tomorrow_confidence
        p_obj["1-Day Prediction Model"] = tomorrow_model
        p_obj["prediction"] = prediction
        p_obj["df"] = df
        print(p_obj, "Processor save output")
        return p_obj
