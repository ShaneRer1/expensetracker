from datetime import datetime   
expenses = [{'date': '08-09-2025 23:57:42', 'category': 'Groceries', 'amount': 87.99, 'description': 'Grocery shop at coles'}, 
            {'date': '08-09-2025 23:58:33', 'category': 'Travel', 'amount': 12.65, 'description': 'Uber to work'}]

def get_Category():
    categories = [
        "Food and Dining",
        "Travel",
        "Utilities",
        "Entertainment",
        "Upgrades",
        "Health and Fitness",
        "Education",
        "Shopping",
        "Groceries",
        "Miscellaneous"
    ]

    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category}")

    while True:
        try:
            choice = int(input("\nSelect a category: "))
            if 1<= choice <= len(categories):
                print(f"You selected: {categories[choice - 1]}")
                return categories[choice - 1]
            else:
                raise ValueError("Invalid option. Please select a valid category number.")
        except ValueError:
            print("Invalid input, please enter a number corresponding to a category instead.")

def get_Amount():
    while True:
        try:
            amount = float(input("Enter Amount: "))
            if amount <0:
                raise ValueError("Amount cannot be negative. Please enter a valid amount.")
            return amount
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")

while True:
    print("\nTrack your stuff boss\n" \
    "Options:\n" \
    "1. Add expense\n" \
    "2. View expenses\n" \
    "3. Total expenses\n" \
    "4. Exit\n")
    choice = input("Enter Choice: ")

    if choice == '1':
        now = datetime.now()
        date = now.strftime("%d-%m-%Y %H:%M:%S")
        #category = input("Enter Category: ")
        category = get_Category()
        amount = get_Amount()          
        description = input("Enter short description: ")
        expenses.append({"date": date, "category": category, "amount": amount, "description": description})

    elif choice == '2':
        print(f"{'Date':<20} | {'Category':<20} | {'Amount':<10} | {'Description':<30}")
        print("-" * 80)
        for expense in expenses:
            print(f"{expense['date']:<20} | {expense['category']:<20} | ${expense['amount']:<10.2f} | {expense['description']:<30}")
            #print(expense)

    elif choice == '3':
        total = sum(expense['amount'] for expense in expenses)
        print(f"Total Expenses: ${total}")
            
    elif choice == '4':
        print("See ya later samurai")
        break

    else:
        print("Invalid Input")


