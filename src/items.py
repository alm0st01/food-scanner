import json
from prettytable import PrettyTable
from tools import extratools

json_root = "food-scanner/userdata/food.json"


def export_to_json(product_dict: dict):
    try:
        with open(json_root, "r", encoding='utf-8') as file:
            jdata = json.load(file)
    except json.JSONDecodeError:
        jdata = dict({})
    for key, value in product_dict.items():
        if key in jdata:
            jdata[key].update(value)
        else:
            jdata[key] = value

    with open(json_root, "w", encoding='utf-8') as file:
        json.dump(jdata, file, ensure_ascii=False, indent=4)


class viewer_gui:
    def __init__(self):
        self.item_count = 0

        with open(json_root, "r", encoding='utf-8') as file:
            self.jdata = json.load(file)
        for key, value in self.jdata.items():
            for i in value.items():
                self.item_count += 1
        self.pages = self.item_count//5 + 1
        self.curr_page = -1

    def print_list(self, page_num: int):
        if self.item_count == 0:
            print("\nThere are currently no items to view. Check out some items first!")
            return False

        self.curr_page = page_num

        first_item = {}
        count = 0
        goal_count = (page_num-1)*5 + 1
        page_list = {
            goal_count: {},
            goal_count+1: {},
            goal_count+2: {},
            goal_count+3: {},
            goal_count+4: {},
        }

        for key, value in self.jdata.items():
            for term in value.values():
                count += 1
                if count == goal_count:
                    page_list[goal_count] = term
                elif count - 1 == goal_count:
                    page_list[goal_count+1] = term
                elif count - 2 == goal_count:
                    page_list[goal_count+2] = term
                elif count - 3 == goal_count:
                    page_list[goal_count+3] = term
                elif count - 4 == goal_count:
                    page_list[goal_count+4] = term

        months = ['January','February','March','April','May','June','July','August','September','October','November','December']
        table_list = PrettyTable(['Item no.','Name','Brand','Date'])
        for key, value in page_list.items():
            if value != {}:
                item_time: str = (f"{months[value.get('time', {}).get('month', 1)-1]} "
                                  f"{value.get('time', {}).get('day', {})}, "
                                  f"{value.get('time', {}).get('year', {})}"
                                  f" at {value.get('time', {}).get('hour', {})}"
                                  f":{str(value.get('time', {}).get('minute', {})).zfill(2)}"
                                  f" {value.get('time', {}).get('am/pm', {})}")
                table_list.add_row([key, value.get('names', {}).get('name', 'N/A'), value.get('names', {}).get('brands', '--'), item_time])

        print(table_list)
        PREV = ""
        NEXT = ""
        if self.curr_page == 1:
            PREV = "\33[91m"+"<|   "+"\33[0m"
        else:
            PREV = "\33[92m"+"<|   "+"\33[0m"

        if self.curr_page == self.pages:
            NEXT = "\33[91m"+"   |>"+"\33[0m"
        else:
            NEXT = "\33[92m"+"   |>"+"\33[0m"
        print((PREV+f"Page {page_num} of {self.pages}"+NEXT).center(75))
        print("\n")
        return True

    def prompt_gui(self):
        choices = ["go to the previous page", "go to the next page","exit to main menu"]
        if self.curr_page == 1:
            choices.remove("go to the previous page")
        if self.curr_page == self.pages:
            choices.remove("go to the next page")


        user_input = extratools.mcq_input("What would you like to do now?", choices)

        if user_input == "go to the previous page":
            self.print_list(self.curr_page-1)
        elif user_input == "go to the next page":
            self.print_list(self.curr_page+1)
        elif user_input == "exit to main menu":
            print("Action Stopped.")
            return False
        return True