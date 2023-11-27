import re
import csv

# Read Lua data from the file
with open('C:/Users/attra/OneDrive/Documents/Elder Scrolls Online/live/SavedVariables/MasterMerchant.lua', 'r') as file:
    lua_data = file.read()

# Find the position/index of '[1] = ' in the Lua data
start_index = lua_data.find('[1] = ')

# Get the substring from the starting index
trimmed_lua_data = lua_data[start_index:]

# Define a pattern to extract item quantity
quantity_pattern = r'\|H0:item:[^&]+&(\d+)&([^&]+)&'

# Find all matches using the pattern in the trimmed Lua data
quantity_matches = re.findall(quantity_pattern, trimmed_lua_data)

# Define a pattern to extract seller, buyer names, item numbers, transaction IDs, total price, guild name, and item name
pattern = r'"@([^&]+)&@([^&]+)&\|H0:item:(\d+):[^&]+&\d+&(\d+)&[^&]+&(\d+)&([^&]+)&([^"]+)'

# Function to extract the item level
def extract_item_level(item_name):
    # Extract the item level (rr or cp followed by numbers) from the "Item Name"
    item_level_match = re.search(r'(?:\bcp|rr)\d+', item_name, re.IGNORECASE)
    if item_level_match:
        return item_level_match.group(0)

# Function to extract the item name
def extract_item_name(item_name):
    # Extract the item name before '&rr' or '&cp'
    item_name_match = re.search(r'^.*?(?=&(?:cp|rr))', item_name)
    if item_name_match:
        return item_name_match.group(0)

# Function to extract the quality of the item
def extract_item_quality(item_name):
    # Map color words to their respective qualities
    color_map = {
        'white': 'Normal',
        'green': 'Fine',
        'blue': 'Superior',
        'purple': 'Epic',
        'gold': 'Legendary'
    }

    # Extract the color from the "Item Name"
    for color, quality in color_map.items():
        if color in item_name.lower():
            return quality

    return 'Unknown'

# Function to extract the item type
def extract_item_type(item_name):
    # Remove the color-related words from the "Item Name"
    color_map = ['white', 'green', 'blue', 'purple', 'gold']
    for color in color_map:
        item_name = item_name.replace(color, '')

    # Extract the item type from the "Item Name" (after color-related words and before the last word)
    words = item_name.split()
    if len(words) > 1:
        return words[-2]
    return 'Unknown'

def extract_item_trait(item_name):
    # Split the item name by spaces and extract the last word as the trait
    words = item_name.split()
    if words:
        extracted_trait = words[-1]

        # Read traits from the file
        with open('traits.txt', 'r') as file:
            traits = file.read().splitlines()

        # Check if the extracted trait matches any trait from the file
        if extracted_trait.lower() in [trait.lower() for trait in traits]:
            return extracted_trait
        else:
            return ''

    return 'Unknown'

def extract_item_type2(item_name):
    # Split the item name by spaces and extract the last word as the trait
    words = item_name.split()
    if words:
        extracted_trait = words[-1]

        # Read traits from the file
        with open('traits.txt', 'r') as file:
            traits = file.read().splitlines()

        # Check if the extracted trait matches any trait from the file
        if extracted_trait.lower() in [trait.lower() for trait in traits]:
            return ''
        else:
            return extracted_trait

    return 'Unknown'

# Find all matches using the pattern in the trimmed Lua data
matches = re.findall(pattern, trimmed_lua_data)

with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Seller', 'Buyer', 'Item Number', 'Transaction ID', 'Item Quantity', 'Total Price', 'Guild Name', 'Item Name', 'Item Level', 'Quality', 'Type', 'Trait', 'Type2'])

    for match, quantity_match in zip(matches, quantity_matches):
        # Extract item quantity from the quantity match
        item_quantity_1, item_quantity_2 = quantity_match

        # Append 'g' after the total price
        total_price = f"{match[4]}g"

        # Extract item name from the item name
        item_name = extract_item_name(match[6])

        # Extract item level from the item name
        item_level = extract_item_level(match[6])

        # Replace 'None' with 'Unknown'
        item_level = item_level or 'Unknown'

        # Remove 'rr' and 'rr0' from the item level
        item_level = item_level.replace('rr0', '').replace('rr', '')

        # Extract item quality from the item name
        quality = extract_item_quality(match[6])

        # Extract item type from the item name
        item_type = extract_item_type(match[6])

        # Extract item trait from the item name
        item_trait = extract_item_trait(match[6])

        # Extract item type2 from the item name
        item_type2 = extract_item_type2(match[6])

        # Write each match to the CSV file including item quantity and transaction ID
        csv_writer.writerow([f'@{match[0]}', f'@{match[1]}', match[2], match[3], item_quantity_1, total_price, match[5], item_name, item_level, quality, item_type, item_trait, item_type2])

print("Extraction and parsing completed. Check 'data.csv'")
