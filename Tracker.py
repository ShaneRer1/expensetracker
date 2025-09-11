from datetime import datetime
import os
import json

#expenses = [{'date': '08-09-2025 23:57:42', 'category': 'Groceries', 'amount': 87.99, 'description': 'Grocery shop at coles'}, 
            #{'date': '08-09-2025 23:58:33', 'category': 'Travel', 'amount': 12.65, 'description': 'Uber to work'}]

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

def get_Description():
    description = input("Enter short description: ")
    description = description.strip()
    if not description:
        description = "No Description"
    return description

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_expenses():
    try:
        with open('expenses.json', 'w') as file:
            json.dump(expenses, file)
    except Exception as e:
        print(f"Error saving file{e}")

def load_expenses():
    try:
        with open('expenses.json', 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading existing expenses: {e}")
        return []

# Daily Expense Tracker, refreshes each day to 0 expenses function
while True:
    expenses = load_expenses()

    print("\nTrack your stuff boss\n" \
    "Options:\n" \
    "1. Add expense\n" \
    "2. View expenses\n" \
    "3. Total expenses\n" \
    "4. View expense by category\n" \
    "5. Exit\n")
    choice = input("Enter Choice: ")

    if choice == '1': #Add expense
        now = datetime.now()
        date = now.strftime("%d-%m-%Y %H:%M:%S")
        
        category = get_Category()
        amount = get_Amount()          

        description = get_Description()
        print("\nReview your expense:")
        print(f"Date: {date}\nCategory: {category}\nAmount: ${amount}\nDescription: {description}")
        while True:
            confirm = input("\nDo you want to save this expense? (y/n)").lower()
            if confirm in ['y', 'yes', '']:
                expenses.append({"date": date, "category": category, "amount": amount, "description": description})
                print("Expense saved successfully!")
                save_expenses()
                clear_console()
                break

            elif confirm in ['n', 'no']:
                print("Expense not saved.")
                break
            else:
                print("Try again, Invalid Input")

    elif choice == '2': #View expenses
        clear_console()
        print(f"{'Date':<20} | {'Category':<20} | {'Amount':<10} | {'Description':<30}")
        print("-" * 80)
        for expense in expenses:
            print(f"{expense['date']:<20} | {expense['category']:<20} | ${expense['amount']:<10.2f} | {expense['description']:<30}")
            #print(expense)
        input("\nPress Enter to continue...")

    elif choice == '3': #Total expenses
        clear_console()
        total = sum(expense['amount'] for expense in expenses)
        print(f"Total Expenses: ${total}")
        input("\nPress Enter to continue...")

    elif choice == '4': #View expense by category
        clear_console()
        category = get_Category()
        filtered_expenses = [expense for expense in expenses if expense['category'] == category]
        if filtered_expenses:
            print(f"\nExpenses in category '{category}':")
            print(f"{'Date':<20} | {'Category':<20} | {'Amount':<10} | {'Description':<30}")
            print("-" * 80)
            for expense in filtered_expenses:
                print(f"{expense['date']:<20} | {expense['category']:<20} | ${expense['amount']:<10.2f} | {expense['description']:<30}")
                input("\nPress Enter to continue...")
        else:
            print(f"No expenses found in category '{category}'.")        
    
    elif choice == '5': #Exit
        save_expenses()
        print("See ya later samurai")
        break

    else:
        print("Invalid Input")


