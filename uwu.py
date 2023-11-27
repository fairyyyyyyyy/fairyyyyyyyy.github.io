import csv

# Dictionary to store total sales for each seller
total_sales = {}

# Dictionary to store processed Transaction IDs for each seller
processed_transactions = {}

# Read the input CSV file
with open('data.csv', 'r') as infile:
    reader = csv.DictReader(infile)

    # Iterate through each row in the CSV
    for row in reader:
        seller = row['Seller']
        transaction_id = row['Transaction ID']
        total_price = row['Total Price']

        # If the Transaction ID is not processed for the seller, update total sales
        if transaction_id not in processed_transactions.get(seller, set()):
            # Extract the numeric value from the 'Total Price' field (remove 'g')
            price_value = int(total_price[:-1])

            # Update the total sales for the seller
            total_sales[seller] = total_sales.get(seller, 0) + price_value

            # Mark the Transaction ID as processed for the seller
            processed_transactions.setdefault(seller, set()).add(transaction_id)

# Write the results to a new CSV file
with open('output_totals.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)

    # Write header
    writer.writerow(['Seller', 'Total Sales'])

    # Write seller and total sales to the output file
    for seller, total_sale in total_sales.items():
        writer.writerow([seller, f'{total_sale}g'])
