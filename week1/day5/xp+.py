'''
🌟 Exercise 1 : Student Grade Summary
Instructions
You are given a dictionary containing student names as keys and lists of their grades as values. Your task is to create a summary report that calculates the average grade for each student, assigns a letter grade, and determines the class average.



Initial Data:


student_grades = {
    "Alice": [88, 92, 100],
    "Bob": [75, 78, 80],
    "Charlie": [92, 90, 85],
    "Dana": [83, 88, 92],
    "Eli": [78, 80, 72]
}


Requirements:
Calculate the average grade for each student and store the results in a new dictionary called student_averages.
Assign each student a letter grade (A, B, C, D, F) based on their average grade according to the following scale, and store the results in a dictionary called student_letter_grades:
A: 90 and above
B: 80 to 89
C: 70 to 79
D: 60 to 69
F: Below 60
Calculate the class average (the average of all students’ averages) and print it.
Print the name of each student, their average grade, and their letter grade.
Hints:
Use loops to iterate through the student_grades dictionary.
You may use sum() and len() functions to help calculate averages.
Initialize empty dictionaries for student_averages and student_letter_grades before filling them with data.'''
student_grades = {
    "Alice": [88, 92, 100],
    "Bob": [75, 78, 80],
    "Charlie": [92, 90, 85],
    "Dana": [83, 88, 92],
    "Eli": [78, 80, 72]
}
student_averages = {}
student_letter_grades = {}
total_average = 0
for student, grades in student_grades.items():
    average = sum(grades) / len(grades)
    student_averages[student] = average
    total_average += average
    
    if average >= 90:
        student_letter_grades[student] = 'A'
    elif average >= 80:
        student_letter_grades[student] = 'B'
    elif average >= 70:
        student_letter_grades[student] = 'C'
    elif average >= 60:
        student_letter_grades[student] = 'D'
    else:
        student_letter_grades[student] = 'F'
class_average = total_average / len(student_grades)
print(f"Class Average: {class_average:.2f}")
for student in student_grades:
    print(f"{student}: Average Grade = {student_averages[student]:.2f}, Letter Grade = {student_letter_grades[student]}")
'''
Exercise 2: Data Analysis
'''
sales_data = [
    {"customer_id": 1, "product": "Smartphone", "price": 600, "quantity": 1, "date": "2023-04-03"},
    {"customer_id": 2, "product": "Laptop", "price": 1200, "quantity": 1, "date": "2023-04-04"},
    {"customer_id": 1, "product": "Laptop", "price": 1000, "quantity": 1, "date": "2023-04-05"},
    {"customer_id": 2, "product": "Smartphone", "price": 500, "quantity": 2, "date": "2023-04-06"},
    {"customer_id": 3, "product": "Headphones", "price": 150, "quantity": 4, "date": "2023-04-07"},
    {"customer_id": 3, "product": "Smartphone", "price": 550, "quantity": 1, "date": "2023-04-08"},
    {"customer_id": 1, "product": "Headphones", "price": 100, "quantity": 2, "date": "2023-04-09"},
]

total_revenue_per_product = {}
for sale in sales_data:
    product = sale["product"]
    revenue = sale["price"] * sale["quantity"]
    if product in total_revenue_per_product:
        total_revenue_per_product[product] += revenue
    else:
        total_revenue_per_product[product] = revenue
print("Total Revenue per Product:")
for product, revenue in total_revenue_per_product.items():
    print(f"{product}: ${revenue}")

customer_spending = {}
for sale in sales_data:
    customer_id = sale["customer_id"]
    revenue = sale["price"] * sale["quantity"]
    if customer_id in customer_spending:
        customer_spending[customer_id] += revenue
    else:
        customer_spending[customer_id] = revenue
print("\nTotal Spending per Customer:")
for customer_id, spending in customer_spending.items():
    print(f"Customer {customer_id}: ${spending}")

for sale in sales_data:
    sale["total_price"] = sale["price"] * sale["quantity"]
print("\nSales Data with Total Price:")
for sale in sales_data: 
    print(sale)

high_value_transactions= [sale for sale in sales_data if sale["total_price"] > 500]
high_value_transactions_sorted = sorted(high_value_transactions, key=lambda x: x["total_price"], reverse=True)
print("\nHigh-Value Transactions (Total Price > $500):")
for transaction in high_value_transactions_sorted:
    print(transaction)


purchases_per_customer = {}
for sale in sales_data:
    customer_id = sale["customer_id"]
    if customer_id in purchases_per_customer:
        purchases_per_customer[customer_id] += 1
    else:
        purchases_per_customer[customer_id] = 1

loyal_customers = [customer_id for customer_id, count in purchases_per_customer.items() if count > 1]
print("\nLoyal Customers (More than 1 Purchase):")
for customer_id in loyal_customers:
    print(f"Customer {customer_id}")


'''Bonus: Insights and Analysis:

Calculate the average transaction value for each product category.
Identify the most popular product based on the quantity sold.
Provide insights into how these analyses could inform the company’s marketing strategies.'''
average_transaction_value_per_product = {}
for product in total_revenue_per_product:
    average_transaction_value_per_product[product] = total_revenue_per_product[product] / sum(sale["quantity"] for sale in sales_data if sale["product"] == product)
print("\nAverage Transaction Value per Product:")
for product, avg_value in average_transaction_value_per_product.items():
    print(f"{product}: ${avg_value:.2f}")
quantity_sold_per_product = {}
for sale in sales_data:
    product = sale["product"]
    quantity = sale["quantity"]
    if product in quantity_sold_per_product:
        quantity_sold_per_product[product] += quantity
    else:
        quantity_sold_per_product[product] = quantity
most_popular_product = max(quantity_sold_per_product, key=quantity_sold_per_product.get)
print(f"\nMost Popular Product: {most_popular_product} (Quantity Sold: {quantity_sold_per_product[most_popular_product]})")

  
    