import csv
import random
import string

def random_string(length=6):
    return ''.join(random.choices(string.ascii_uppercase, k=length))

# List of sample food products with corresponding product numbers
food_products = [
    ("APPLE", "APL123"), ("BANANA", "BAN456"), ("CARROT", "CAR789"), 
    ("DAIRY", "DAI012"), ("EGGPLANT", "EGG345"), ("FIG", "FIG678"), 
    ("GRAPE", "GRA901"), ("HONEY", "HON234"), ("ICE_CREAM", "ICE567"), 
     ("KALE", "KAL123"), ("LEMON", "LEM456"), ("LIME", "LIM789"),
    ("MANGO", "MAN789"), ("NECTARINE", "NEC012"), ("ORANGE", "ORA345"), 
    ("POTATO", "POT678"), ("QUINOA", "QUI901"), ("RICE", "RIC234"), 
    ("STRAWBERRY", "STR567"), ("TOMATO", "TOM890"), 
    ("VANILLA", "VAN456"), ("WATERMELON", "WAT789"), 
    ("YOGURT", "YOG345"), ("ZUCCHINI", "ZUC678"), ("BROCCOLI", "BRO901"), 
    ("CABBAGE", "CAB234"), ("DILL", "DIL567"), ("GARLIC", "GAR890")
]

# Define the number of rows
num_rows = 1000

# Open the file in write mode and empty the contents
with open('./data/sample.csv', 'w', newline='') as file:
    file.truncate(0)
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(["Order Number", "Year", "Month", "Day", "Product Number", "Product Name", "Count", "Extra Col1", "Extra Col2"])
    
    # Write the data rows
    for i in range(1, num_rows + 1):
        order_number = i
        year = random.choice([2021, 2022, 2023, 2024])
        month = str(random.randint(1, 12)).zfill(2)
        day = str(random.randint(1, 28)).zfill(2)
        product_name, product_number = random.choice(food_products)
        count = round(random.uniform(1, 1000), 2)
        extra_col1 = random_string(15)
        extra_col2 = random_string(15)
        
        writer.writerow([order_number, year, month, day, product_number, product_name, count, extra_col1, extra_col2])

print("Sample data CSV generated successfully.")
