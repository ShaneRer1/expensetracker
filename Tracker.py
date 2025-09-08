expenses = [{'date': '23', 'category': '02', 'amount': 23.0, 'description': 'fresh'}, {'date': '23-25-02', 'category': 'sfsd', 'amount': 1236.0, 'description': 'frd'}]
while True:
    print("Track your stuff boss\n" \
    "Options:\n" \
    "1. Add expense\n" \
    "2. View expenses\n" \
    "3. Total expenses\n" \
    "4. Exit\n")
    choice = input("Enter Choice: ")

    if choice == '1':
        date = input("Enter date (YY-MM-DD): ")
        category = input("Enter Category: ")
        amount = float(input("Enter Amount: "))
        description = input("Enter short description: ")
        expenses.append({"date": date, "category": category, "amount": amount, "description": description})

    elif choice == '2':
        print(f"{'Date':<10}\t{'Category':<10}\t{'Amount':<10}\t{'Description':<10}")
        for expense in expenses:
            print(f"{expense['date']:<10} | {expense['category']:<10} | ${expense['amount']:<10} | {expense['description']:<10}")

    elif choice == '3':
        total = sum(expense['amount'] for expense in expenses)
        print(f"Total Expenses: ${total}")
            
    elif choice == '4':
        print("See ya later samurai")
        break

    else:
        print("Invalid Input")