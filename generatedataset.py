import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

categories = {
    'Baby Gear': ['Walker', 'Stroller', 'Car Seat'],
    'Furniture': ['Cradle', 'High Chair', 'Study Table'],
    'Battery Operated': ['Car', 'Bike', 'Jeep'],
    'Baby Safety': ['Safety Gate', 'Bed Rail'],
    'Toys': ['Scooter', 'Ride-on']
}

# Generate synthetic sales data
data = []
start_date = datetime.now() - timedelta(days=365)

for _ in range(5000):
    category = random.choice(list(categories.keys()))
    product = random.choice(categories[category])
    product_id = f"{category[:2].upper()}_{random.randint(10000, 99999)}"
    sale_date = start_date + timedelta(days=random.randint(0, 365))
    units_sold = random.randint(1, 10)
    price_per_unit = random.uniform(500, 5000)
    revenue = round(units_sold * price_per_unit, 2)
    
    data.append([
        product_id, product, category, sale_date.date(), units_sold, price_per_unit, revenue
    ])

df = pd.DataFrame(data, columns=[
    'Product_ID', 'Product_Name', 'Category', 'Date', 'Units_Sold', 'Price_Per_Unit', 'Revenue'
])

df.to_csv('baybee_sales_data.csv', index=False)
print("Dataset generated successfully!")
