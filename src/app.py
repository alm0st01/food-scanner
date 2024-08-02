import time

from parse import Parse
from tools import extratools
import items
import decoder


def nutrient_receiver(user_input):
    tp = Parse(user_input)
    if tp.is_valid():
        print("\n")
        tp.print_table()
        user_input = extratools.mcq_input("\nDo you want this saved to your nutrient history?", ["yes", "no"])
        if user_input == "yes":
            print("Great! Your item is currently being saved")
            items.export_to_json(tp.get_dict())
            time.sleep(2)
            print("Item saved!")
        elif user_input == "no":
            print("Item removed.")

        extratools.enter_to_continue()

while True:
    user_input = extratools.mcq_input(
        "\nWhat would you like to do today?",
        ["manually input a barcode","scan barcode via camera","view my items","exit"]
    )

    if user_input == "manually input a barcode":
        user_input = input("Enter the 12 or 13 digit number next to the barcode located on your product: ")
        nutrient_receiver(user_input)
    elif user_input == "scan barcode via camera":
        print("NOTE: You are about to open another application to open your camera.")
        user_input = extratools.mcq_input("Do you want to continue?", ["yes", "no"])
        if user_input == "yes":
            barcode = decoder.live_detect(1)
            if barcode != None:
                nutrient_receiver(barcode)
        else:
            print("Action stopped.")
    elif user_input == "view my items":
        running = True

        items_gui = items.viewer_gui()
        running = items_gui.print_list(1)
        while running:
            running = items_gui.prompt_gui()
    elif user_input == "exit":
        print("\nThank you for trying out our app!")
        exit(0)

# chewy bar
# 7622210449283
# pistachios
# 074401760412
# sugar-free masala chai
# 8901095900317
# breadcrumbs
# 041196891027
# poland spring water
# 075720000715