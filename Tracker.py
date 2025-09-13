from datetime import datetime, timedelta
import os
import json
import csv

# =========================
# Expense Tracker Functions
# =========================

expenses = []
budgets = {}      # key: (month-year, category), value: budget amount
recurring = []    # list of dicts: {'category','amount','description','frequency','last_added'}

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
            choice = input("\nSelect a category (number or name): ").strip()
            if not choice:
                print("Please choose a category.")
                continue
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(categories):
                    return categories[choice - 1]
            match = next((c for c in categories if c.lower() == choice.lower()), None)
            if match:
                return match
            print("Invalid input, try again.")
        except Exception:
            print("Invalid input.")

def get_Amount():
    while True:
        try:
            amount_str = input("Enter Amount: ").strip()
            amount = float(amount_str)
            if amount < 0:
                print("Amount cannot be negative.")
                continue
            return amount
        except ValueError:
            print("Invalid amount. Enter numeric value.")

def get_Description():
    description = input("Enter short description: ").strip()
    return description if description else "No Description"

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_expenses():
    try:
        with open('expenses.json', 'w') as file:
            json.dump(expenses, file, indent=2)
        with open('budgets.json', 'w') as bf:
            json.dump(budgets, bf, indent=2)
        with open('recurring.json', 'w') as rf:
            json.dump(recurring, rf, indent=2)
    except Exception as e:
        print(f"Error saving files: {e}")

def load_expenses():
    global expenses, budgets, recurring
    try:
        with open('expenses.json', 'r') as file:
            expenses = json.load(file)
    except FileNotFoundError:
        expenses = []
    try:
        with open('budgets.json', 'r') as bf:
            budgets = json.load(bf)
    except FileNotFoundError:
        budgets = {}
    try:
        with open('recurring.json', 'r') as rf:
            recurring = json.load(rf)
    except FileNotFoundError:
        recurring = []

def filter_expenses_by_date():
    while True:
        date_str = input("Enter date (DD-MM-YYYY) or leave empty for today's expenses: ").strip()
        try:
            if not date_str:
                filtered = todays_expenses()
                print("\nToday's Expenses:")
            else:
                filter_date = datetime.strptime(date_str, "%d-%m-%Y").date()
                filtered = [e for e in expenses if datetime.strptime(e['date'], "%d-%m-%Y %H:%M:%S").date() == filter_date]
                print(f"\nExpenses on '{date_str}':")
            if filtered:
                print(f"{'Date':<20} | {'Category':<20} | {'Amount':<10} | {'Description':<30}")
                print("-" * 90)
                for e in filtered:
                    print(f"{e['date']:<20} | {e['category']:<20} | ${e['amount']:<10.2f} | {e['description']:<30}")
            else:
                print("No expenses found.")
            input("\nPress Enter to continue...")
            break
        except ValueError:
            print("Invalid date format. Use DD-MM-YYYY.")

def todays_expenses():
    today = datetime.now().date()
    return [e for e in expenses if datetime.strptime(e['date'], "%d-%m-%Y %H:%M:%S").date() == today]

# =====================
# Edit Expense
# =====================
def edit_expense():
    if not expenses:
        print("No expenses to edit.")
        input("\nPress Enter to continue...")
        return
    print(f"{'Index':<6} | {'Date':<20} | {'Category':<20} | {'Amount':<10} | {'Description':<30}")
    print("-" * 100)
    for i, e in enumerate(expenses, start=1):
        print(f"{i:<6} | {e['date']:<20} | {e['category']:<20} | ${e['amount']:<10.2f} | {e['description']:<30}")
    try:
        idx = int(input("\nEnter the index of the expense to edit: ").strip())
        if not (1 <= idx <= len(expenses)):
            print("Index out of range.")
            input("\nPress Enter to continue...")
            return
        exp = expenses[idx - 1]
        print("\nEditing this expense (leave blank to keep current value):")
        new_cat = input("New category or press 'c' to pick from list: ").strip()
        if new_cat.lower() == 'c':
            new_cat = get_Category()
        if new_cat:
            exp['category'] = new_cat
        new_amount = input("New amount (blank to keep): ").strip()
        if new_amount:
            try:
                val = float(new_amount)
                if val >= 0:
                    exp['amount'] = val
            except ValueError:
                print("Invalid amount; keeping old value.")
        new_desc = input("New description (blank to keep): ").strip()
        if new_desc:
            exp['description'] = new_desc
        expenses[idx - 1] = exp
        save_expenses()
        print("Expense updated successfully!")
    except ValueError:
        print("Invalid input.")
    input("\nPress Enter to continue...")

# =====================
# Delete Expense
# =====================
def delete_expense():
    if not expenses:
        print("No expenses to delete.")
        input("\nPress Enter to continue...")
        return
    print(f"{'Index':<6} | {'Date':<20} | {'Category':<20} | {'Amount':<10} | {'Description':<30}")
    print("-" * 100)
    for i, e in enumerate(expenses, start=1):
        print(f"{i:<6} | {e['date']:<20} | {e['category']:<20} | ${e['amount']:<10.2f} | {e['description']:<30}")
    try:
        idx = int(input("\nEnter the index of the expense to delete: ").strip())
        if not (1 <= idx <= len(expenses)):
            print("Index out of range.")
            input("\nPress Enter to continue...")
            return
        confirm = input(f"Are you sure you want to delete expense [{idx}]? (y/n): ").strip().lower()
        if confirm in ('y','yes'):
            expenses.pop(idx-1)
            save_expenses()
            print("Expense deleted.")
        else:
            print("Deletion canceled.")
    except ValueError:
        print("Invalid input.")
    input("\nPress Enter to continue...")

# =====================
# Monthly / Weekly Summary
# =====================
def monthly_summary():
    choice = input("Enter month and year (MM-YYYY) or leave blank for current month: ").strip()
    try:
        if not choice:
            now = datetime.now()
            month, year = now.month, now.year
        else:
            month, year = map(int, choice.split('-'))
        totals = {}
        month_total = 0.0
        for e in expenses:
            edate = datetime.strptime(e['date'], "%d-%m-%Y %H:%M:%S")
            if edate.month == month and edate.year == year:
                cat = e['category']
                totals[cat] = totals.get(cat,0.0) + float(e['amount'])
                month_total += float(e['amount'])
        if month_total==0:
            print("No expenses found.")
        else:
            print(f"\nSummary for {month:02d}-{year}:")
            print(f"{'Category':<25} | {'Total':>10}")
            print("-"*40)
            for cat, amt in sorted(totals.items(), key=lambda x:x[1], reverse=True):
                print(f"{cat:<25} | ${amt:>9.2f}")
            print(f"{'Month Total':<25} | ${month_total:>9.2f}")
    except Exception:
        print("Invalid input.")
    input("\nPress Enter to continue...")

def weekly_summary():
    choice = input("Enter week start date (DD-MM-YYYY) or leave blank for this week: ").strip()
    try:
        if not choice:
            today = datetime.now().date()
            start = today - timedelta(days=today.weekday())
        else:
            start = datetime.strptime(choice, "%d-%m-%Y").date()
        end = start + timedelta(days=6)
        totals = {}
        week_total = 0.0
        for e in expenses:
            edate = datetime.strptime(e['date'], "%d-%m-%Y %H:%M:%S").date()
            if start <= edate <= end:
                cat = e['category']
                totals[cat] = totals.get(cat,0.0) + float(e['amount'])
                week_total += float(e['amount'])
        if week_total==0:
            print("No expenses found in this week.")
        else:
            print(f"\nSummary {start} to {end}:")
            print(f"{'Category':<25} | {'Total':>10}")
            print("-"*40)
            for cat, amt in sorted(totals.items(), key=lambda x:x[1], reverse=True):
                print(f"{cat:<25} | ${amt:>9.2f}")
            print(f"{'Week Total':<25} | ${week_total:>9.2f}")
    except Exception:
        print("Invalid date format.")
    input("\nPress Enter to continue...")

# =====================
# Search Expenses
# =====================
def search_expenses():
    if not expenses:
        print("No expenses to search.")
        input("\nPress Enter to continue...")
        return
    print("\nSearch options:\n1. Keyword\n2. Category\n3. Amount range")
    sel = input("Choose search type (1/2/3): ").strip()
    results = []
    if sel=='1':
        kw = input("Enter keyword: ").strip().lower()
        results = [e for e in expenses if kw in e['description'].lower()]
    elif sel=='2':
        cat = get_Category()
        results = [e for e in expenses if e['category'].lower() == cat.lower()]
    elif sel=='3':
        try:
            low = float(input("Min amount: ").strip())
            high = float(input("Max amount: ").strip())
            if low>high:
                low, high = high, low
            results = [e for e in expenses if low <= float(e['amount']) <= high]
        except ValueError:
            print("Invalid amount.")
            input("\nPress Enter to continue...")
            return
    else:
        print("Invalid choice.")
        input("\nPress Enter to continue...")
        return
    if results:
        print(f"\nFound {len(results)} expenses:")
        print(f"{'Date':<20} | {'Category':<20} | {'Amount':<10} | {'Description':<30}")
        print("-"*100)
        for e in results:
            print(f"{e['date']:<20} | {e['category']:<20} | ${e['amount']:<10.2f} | {e['description']:<30}")
    else:
        print("No matching expenses found.")
    input("\nPress Enter to continue...")

# =====================
# Budget Tracking
# =====================
def set_budget():
    print("\n--- Set Monthly Budget ---")
    category = get_Category()
    month_year = input("Enter month and year (MM-YYYY): ").strip()
    try:
        datetime.strptime("01-"+month_year, "%d-%m-%Y")
        amount = float(input(f"Enter budget for {category} in {month_year}: ").strip())
        budgets[f"{month_year}-{category}"] = amount
        save_expenses()
        print("Budget saved!")
    except Exception:
        print("Invalid input.")
    input("\nPress Enter to continue...")

def check_budget():
    print("\n--- Budget Status ---")
    now = datetime.now()
    month_year = f"{now.month:02d}-{now.year}"
    for key, value in budgets.items():
        if key.startswith(month_year):
            cat = key.split('-',2)[-1]
            spent = sum(e['amount'] for e in expenses if e['category']==cat and datetime.strptime(e['date'],"%d-%m-%Y %H:%M:%S").month==now.month)
            print(f"{cat:<20} | Budget: ${value:<10.2f} | Spent: ${spent:<10.2f} | Remaining: ${value-spent:<10.2f}")
    input("\nPress Enter to continue...")

# =====================
# Recurring Expenses
# =====================
def add_recurring():
    print("\n--- Add Recurring Expense ---")
    category = get_Category()
    amount = get_Amount()
    description = get_Description()
    freq = input("Enter frequency ('weekly' or 'monthly'): ").strip().lower()
    if freq not in ('weekly','monthly'):
        print("Invalid frequency.")
        return
    recurring.append({'category': category, 'amount': amount, 'description': description, 'frequency': freq, 'last_added': None})
    save_expenses()
    print("Recurring expense added.")
    input("\nPress Enter to continue...")

def apply_recurring():
    now = datetime.now()
    any_added = False
    for r in recurring:
        add_flag = False
        last = r['last_added']
        if last:
            last_date = datetime.strptime(last, "%d-%m-%Y")
            if r['frequency']=='weekly' and (now.date() - last_date.date()).days >=7:
                add_flag = True
            elif r['frequency']=='monthly' and now.month != last_date.month:
                add_flag = True
        else:
            add_flag = True
        if add_flag:
            date_str = now.strftime("%d-%m-%Y %H:%M:%S")
            expenses.append({'date': date_str, 'category': r['category'], 'amount': r['amount'], 'description': r['description']})
            r['last_added'] = now.strftime("%d-%m-%Y")
            any_added = True
    if any_added:
        save_expenses()

# =====================
# Export / Import
# =====================
def export_expenses():
    choice = input("Export as (1) CSV or (2) JSON? ").strip()
    if choice=='1':
        filename = input("Enter filename (without extension): ").strip() + ".csv"
        with open(filename,'w',newline='') as f:
            writer = csv.DictWriter(f,fieldnames=['date','category','amount','description'])
            writer.writeheader()
            for e in expenses:
                writer.writerow(e)
        print(f"Exported to {filename}")
    elif choice=='2':
        filename = input("Enter filename (without extension): ").strip() + ".json"
        with open(filename,'w') as f:
            json.dump(expenses,f,indent=2)
        print(f"Exported to {filename}")
    else:
        print("Invalid choice.")
    input("\nPress Enter to continue...")

def import_expenses():
    choice = input("Import from (1) CSV or (2) JSON? ").strip()
    if choice=='1':
        filename = input("Enter CSV filename: ").strip()
        try:
            with open(filename,'r') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    row['amount'] = float(row['amount'])
                    expenses.append(row)
                    count +=1
            save_expenses()
            print(f"{count} expenses imported from {filename}")
        except Exception as e:
            print(f"Error importing CSV: {e}")
    elif choice=='2':
        filename = input("Enter JSON filename: ").strip()
        try:
            with open(filename,'r') as f:
                data = json.load(f)
                expenses.extend(data)
            save_expenses()
            print(f"{len(data)} expenses imported from {filename}")
        except Exception as e:
            print(f"Error importing JSON: {e}")
    else:
        print("Invalid choice.")
    input("\nPress Enter to continue...")

# =====================
# Main Loop
# =====================
load_expenses()
apply_recurring()

while True:
    clear_console()
    print("\nTrack your stuff boss\nOptions:")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Total expenses")
    print("4. View expense by category")
    print("5. View expense by date")
    print("6. Edit expense")
    print("7. Delete expense")
    print("8. Monthly summary")
    print("9. Weekly summary")
    print("10. Search expenses")
    print("11. Set budget")
    print("12. Check budget status")
    print("13. Add recurring expense")
    print("14. Export expenses")
    print("15. Import expenses")
    print("16. Exit")
    
    choice = input("\nEnter choice: ").strip()
    
    if choice=='1':
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        category = get_Category()
        amount = get_Amount()
        description = get_Description()
        expenses.append({'date': now,'category':category,'amount':amount,'description':description})
        save_expenses()
        print("Expense saved.")
        input("\nPress Enter to continue...")
    elif choice=='2':
        if not expenses:
            print("No expenses recorded.")
        else:
            print(f"{'Date':<20} | {'Category':<20} | {'Amount':<10} | {'Description':<30}")
            print("-"*90)
            for e in expenses:
                print(f"{e['date']:<20} | {e['category']:<20} | ${e['amount']:<10.2f} | {e['description']:<30}")
        input("\nPress Enter to continue...")
    elif choice=='3':
        total = sum(e['amount'] for e in expenses)
        print(f"Total Expenses: ${total:.2f}")
        input("\nPress Enter to continue...")
    elif choice=='4':
        category = get_Category()
        filtered = [e for e in expenses if e['category']==category]
        if filtered:
            print(f"{'Date':<20} | {'Category':<20} | {'Amount':<10} | {'Description':<30}")
            print("-"*90)
            for e in filtered:
                print(f"{e['date']:<20} | {e['category']:<20} | ${e['amount']:<10.2f} | {e['description']:<30}")
        else:
            print("No expenses in this category.")
        input("\nPress Enter to continue...")
    elif choice=='5':
        filter_expenses_by_date()
    elif choice=='6':
        edit_expense()
    elif choice=='7':
        delete_expense()
    elif choice=='8':
        monthly_summary()
    elif choice=='9':
        weekly_summary()
    elif choice=='10':
        search_expenses()
    elif choice=='11':
        set_budget()
    elif choice=='12':
        check_budget()
    elif choice=='13':
        add_recurring()
    elif choice=='14':
        export_expenses()
    elif choice=='15':
        import_expenses()
    elif choice=='16':
        save_expenses()
        print("Goodbye!")
        break
    else:
        print("Invalid choice.")
        input("\nPress Enter to continue...")
