import json
import requests
from datetime import datetime
from prettytable import PrettyTable

class Parse:

    def __init__(self, barcode):
        self.barcode = barcode
        self.site_json = json.loads(requests.get(f'https://world.openfoodfacts.org/api/v0/product/{barcode}.json').text)

        ctime = datetime.now()
        self.date = str(ctime.year) + "_" + str(ctime.day) + "_" + str(ctime.month)

        now = datetime.now()
        mid = now.replace(hour=0, minute=0, second=0, microsecond=0)
        self.seconds = (now - mid).seconds

        hour = int(self.seconds//3600)
        minute = int((self.seconds%3600)/60)
        am_pm = ""
        if hour >= 12:
            am_pm = "PM"
        else:
            am_pm = "AM"
        hour %= 12
        if hour == 0:
            hour = 12

        self.fields = {
            "calories": 'energy-kcal',
            "fat": 'fat',
            "carbs": 'carbohydrates',
            "sodium": 'sodium',
            "sugar": 'sugars',
            "fiber": 'fiber',
            "protein": 'proteins'
        }


        self.product_dict = {
            self.date: {
                self.seconds: {
                    "barcode": self.barcode,
                    "time": {
                        "year": ctime.year,
                        "month": ctime.month,
                        "day": ctime.day,
                        "hour": hour,
                        "minute": minute,
                        "am/pm": am_pm
                    },
                    "names": {
                        "brands": "--",
                        "name": "--"
                    },
                    "nutriments": {
                        "calories": "0",
                        "fat": "0",
                        "carbs": "0",
                        "sodium": "0",
                        "sugar": "0",
                        "fiber": "0",
                        "protein": "0"
                    },
                    "units": {
                        "calories": "",
                        "fat": "",
                        "carbs": "",
                        "sodium": "",
                        "sugar": "",
                        "fiber": "",
                        "protein": ""
                    }
                }
            }
        }


    def is_valid(self):
        if self.site_json["status_verbose"] == "product found":
            print("\nProduct found!")
            return True
        elif self.site_json["status_verbose"] == "product not found":
            print("\nProduct not found")
            return False
        else:
            print("Product not found")
            return False

    def get_brands(self):
        try:
            brand = self.site_json['product']['brands']
        except:
            brand = "N/A"
        return brand

    def get_prod_name(self):
        try:
            prod_name = self.site_json['product']['product_name']
        except:
            prod_name = "N/A"
        return prod_name



    def make_units(self):

        for key in self.fields.keys():
            try:
                self.product_dict[self.date][self.seconds]['units'][key] = self.site_json['product']['nutriments'][self.fields[key]+'_unit']

                if key == "sodium" and self.product_dict[self.date][self.seconds]['units'][key] == "g":
                    self.product_dict[self.date][self.seconds]['units'][key] = "mg"
            except:
                self.product_dict[self.date][self.seconds]['units'][key] = ""


    def format_to_dict(self) -> dict:
        self.make_units()

        self.product_dict[self.date][self.seconds]['names']['brands'] = self.get_brands()
        self.product_dict[self.date][self.seconds]['names']['name'] = self.get_prod_name()

        for key in self.fields.keys():
            try:
                self.product_dict[self.date][self.seconds]['nutriments'][key] = self.site_json['product']['nutriments'][self.fields[key]+'_serving']
                if key == "sodium" and self.make_units() == "mg":
                    self.product_dict[self.date][self.seconds]['nutriments'][key] = int(self.product_dict[self.date][self.seconds]['nutriments'][key])*1000
            except:
                if self.product_dict[self.date][self.seconds]['units'][key] != "":
                    self.product_dict[self.date][self.seconds]['nutriments'][key] = "0"
                else:
                    self.product_dict[self.date][self.seconds]['nutriments'][key] = "--"
        return self.product_dict

    def get_dict(self):
        return self.product_dict

    def print_table(self):
        dict1 = self.format_to_dict()

        print("Name:",self.get_prod_name())
        print("Brand:",self.get_brands())
        table = PrettyTable(['Serving ', ' Information'])
        for key, value in dict1[self.date][self.seconds]['nutriments'].items():
            table.add_row([key,str(value)+" "+self.product_dict[self.date][self.seconds]['units'][key]])
        print(table)

# API Source Link
# https://world.openfoodfacts.org/api/v0/product/[barcode].json