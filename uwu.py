import csv
import re

def extract_data(line):
    match = re.search(r'"@([^&]+)&@([^&]+)&\|H0:item:(\d+):\d+:.*?&(\d+)&(true|false)&(\d+)&([^&]+)&([^&]+)&([^&]+)', line)
    if match:
        return {
            'seller_username': f"@{match.group(1)}",
            'buyer_username': f"@{match.group(2)}",
            'item_id': match.group(3),
            'transaction_id': match.group(4),
            'is_true': match.group(5),
            'price': match.group(6),
            'guild': match.group(7),
            'item': match.group(8),
            'details': match.group(9)
        }
    else:
        print(f"Skipped line: {line.strip()}")
        return None



def main(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        csv_writer = csv.DictWriter(outfile, fieldnames=['seller_username', 'buyer_username', 'item_id', 'transaction_id', 'is_true', 'price', 'guild', 'item', 'details'])
        csv_writer.writeheader()

        found_data = False  # Flag to indicate whether valid data has been found

        for line in infile:
            if not found_data:
                # Skip lines until a valid pattern is found
                if re.search(r'"@([^&]+)&@([^&]+)&\|H0:item:(\d+):\d+:.*?&(\d+)&(true|false)&(\d+)&([^&]+)&([^&]+)&([^&]+)', line):
                    found_data = True
            else:
                data = extract_data(line)
                if data:
                    csv_writer.writerow(data)

if __name__ == "__main__":
    input_file = r'C:\Users\attra\OneDrive\Documents\Elder Scrolls Online\live\SavedVariables\MasterMerchant.lua'
    output_file = 'output.csv'

    main(input_file, output_file)
