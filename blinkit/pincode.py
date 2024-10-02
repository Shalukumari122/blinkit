# # import time
# #
# # import pandas as pd
# # from geopy.geocoders import Nominatim
# # from geopy.exc import GeocoderTimedOut, GeocoderInsufficientPrivileges
# #
# # # Load the Excel file
# # file_path = 'C:\\Users\\shalu.kumari\\Desktop\\blinkit_roshi_pincode.xlsx'  # Update this path to your file's location
# # df = pd.read_excel(file_path)
# #
# # # Strip any leading/trailing spaces from the column names
# # df.columns = df.columns.str.strip()
# #
# # # Print the columns to check their names
# # print("Column names:", df.columns)
# #
# # # Initialize the geocoder
# # geolocator = Nominatim(user_agent="blinkit.com")
# # # geolocator = Nominatim(user_agent="your_email@example.com")  # Replace with your own email or website
# #
# # # Function to get latitude and longitude
# #
# # def get_lat_lon(row):
# #     try:
# #         location = geolocator.geocode(f"{row['Areas']}, {row['City']}, {row['Pincode']}")
# #         if location:
# #             return pd.Series([location.latitude, location.longitude])
# #         time.sleep(1)  # Add a delay of 1 second between requests
# #     except GeocoderTimedOut:
# #         return pd.Series([None, None])
# #     except GeocoderInsufficientPrivileges as e:
# #         print(f"Error: {e}")
# #         return pd.Series([None, None])
# #     return pd.Series([None, None])
# #
# # # Apply the function to the DataFrame
# # df[['Latitude', 'Longitude']] = df.apply(get_lat_lon, axis=1)
# #
# # # Save the results to a new Excel file
# # output_file_path = 'output_with_lat_lon.xlsx'  # Change the path if needed
# # df.to_excel(output_file_path, index=False)
# #
# # print("Latitude and Longitude added successfully!")
df_pincodes = pd.read_excel('C:\\Users\\shalu.kumari\\Desktop\\blinkit_roshi_pincode.xlsx')
# pincodes_list = df_pincodes.values.tolist()
pincodes_list = df_pincodes.apply(lambda row: ','.join(row.values.astype(str)), axis=1).tolist()

for pincode in pincodes_list:
# for pincode in ['122012']:
    item = BlinkitItem()
    # pincodes = list(df_pincodes[city])
    # for pincode in ["110007"]:
        # city = 'Mumbai'

    sleep(3)
    # url1 = f"https://blinkit.com/mapAPI/autosuggest_google?query={city} {pincode} ".replace(' ', '%20')
    url1 = f"https://blinkit.com/mapAPI/autosuggest_google?query={pincode} ".replace(' ', '%20')
    # url1 = f"https://blinkit.com/mapAPI/autosuggest_google?query={city.lower()} {pincode}".replace(' ', '%2C')
    headers = {
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9,gu;q=0.8',
                    'app_client': 'consumer_web',
                    'app_version': '52434332',
                    'auth_key': 'c761ec3633c22afad934fb17a66385c1c06c5472b4898b866b7306186d0bb477',
                    'content-type': 'application/json',
                    'device_id': '87433dca-7b1d-4af9-a4ab-1a7fbd22036e',
                    'priority': 'u=1, i',
                    'referer': 'https://blinkit.com/',
                    'rn_bundle_version': '1009003012',
                    'session_uuid': '4a3de0a6-720e-4575-b480-3168f68fac9c',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                    'web_app_version': '1008010016',
                }
    try:
        data1 = requests.get(url=url1,headers=headers).json()
        try:
            predictions_list = data1['predictions']
        except:
            predictions_list = None

        for predictions in predictions_list:
            try:
                placeid = predictions['place_id']
            except:
                placeid = None

            if placeid:
                url2 = f'https://blinkit.com/mapAPI/place-detail?placeId={placeid}'
                data2 = requests.get(url2,headers=headers).json()
                try:
                    lat = data2['result']['geometry']['location']['lat']
                    lng = data2['result']['geometry']['location']['lng']
                except:
                    lat,lng = None,None

                url3 = f"https://blinkit.com/visibility?latitude={lat}&longitude={lng}"
                h2 = {
                        'accept': '*/*',
                        'accept-language': 'en-US,en;q=0.9,gu;q=0.8',
                        'app_client': 'consumer_web',
                        'app_version': '52434332',
                        'auth_key': 'c761ec3633c22afad934fb17a66385c1c06c5472b4898b866b7306186d0bb477',
                        'content-type': 'application/json',
                        'device_id': '87433dca-7b1d-4af9-a4ab-1a7fbd22036e',
                        'priority': 'u=1, i',
                        'referer': 'https://blinkit.com/',
                        'rn_bundle_version': '1009003012',
                        'session_uuid': '4a3de0a6-720e-4575-b480-3168f68fac9c',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                        'web_app_version': '1008010016',
                    }
                data3 = requests.get(url3, headers=h2).json()
                if data3['serviceable']:
                    item['pincode'] = pincode
                    item['lat'] = str(lat)
                    item['`long`'] = str(lng)
                    item['serviceable'] = True

                    field_list = list(item)
                    column_name = ','.join(field_list)
                    values = list(map(lambda x: '%s', list(item.values())))
                    str_values = ','.join(values)
                    insert_query = "INSERT INTO zip_latlong_table(" + column_name + ")" + 'VALUES' + "(" + str_values + ")"
                    cursor.execute(insert_query, tuple(list(item.values())))
                    db.commit()
                    print("item inserted successfully============")
                    print(pincode)
                    break

                else:
                    try:
                        item['pincode'] = pincode
                        item['lat'] = str(lat)
                        item['`long`'] = str(lng)
                        item['serviceable'] = False

                        field_list = list(item)
                        column_name = ','.join(field_list)
                        values = list(map(lambda x: '%s', list(item.values())))
                        str_values = ','.join(values)
                        insert_query = "INSERT INTO zip_latlong_table(" + column_name + ")" + 'VALUES' + "(" + str_values + ")"
                        cursor.execute(insert_query, tuple(list(item.values())))
                        db.commit()
                        print("item inserted successfully============")
                        print(pincode)
                        # break
                    except:
                        pass
                # else:
                #     if lat and lng:
                #         with open('pincodes.json', 'r') as f:
                #             data = f.read()
                #         data = json.loads(data)
                #         city_data = data[city]
                #         city_data[pincode] = [lat, lng]
                #         data[city] = city_data
                #         with open('pincodes.json', 'w') as e:
                #             e.write(json.dumps(data, indent=2))
            print(pincode)
    except Exception as e:
        print(e)
        print(f"error in {pincode}")
