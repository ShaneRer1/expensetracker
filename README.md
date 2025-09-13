# Expense Tracker CLI Application

A **Python-based Command Line Interface (CLI) Expense Tracker** to help users manage, monitor, and analyze their daily, weekly, and monthly expenses efficiently.

---

## Features

| Feature Category          | Description                                                                                                    |
| ------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Core Expense Tracking** | Add, view, and manage daily expenses with date, category, amount, and description. Filter by category or date. |
| **Expense Management**    | Edit or delete any recorded expense.                                                                           |
| **Summaries & Reports**   | Monthly and weekly summaries of expenses, broken down by category.                                             |
| **Search & Filtering**    | Search expenses by keyword, category, or amount range.                                                         |
| **Budget Management**     | Set monthly budgets per category and track spending status.                                                    |
| **Recurring Expenses**    | Schedule weekly or monthly recurring expenses automatically added to records.                                  |
| **Export / Import**       | Export expenses to CSV or JSON for backup; import CSV/JSON to restore or add multiple records.                 |
| **Future Enhancements**   | Graphs & visualization, Alerts & notifications, Currency support.                                              |

---

## Technologies Used

* Python 3.x
* `json` for storage
* `csv` for export/import
* `datetime` for date and time management
* CLI interface for cross-platform usage

---

## Getting Started

1. Clone the repository:

   ```bash
   git clone <your-repo-link>
   ```

2. Run the application:

   ```bash
   python expense_tracker.py
   ```

3. Follow the on-screen menu to track, edit, analyze, and manage your expenses.

---

## Menu Options

1. **Add Expense** - Record a new expense with details.
2. **View Expenses** - Display all expenses in a table.
3. **Total Expenses** - Show the total amount spent.
4. **View by Category** - Filter expenses by a category.
5. **View by Date** - Filter expenses by a specific date.
6. **Edit Expense** - Update any recorded expense.
7. **Delete Expense** - Remove an expense permanently.
8. **Monthly Summary** - View total expenses for a month, broken down by category.
9. **Weekly Summary** - View total expenses for a week, broken down by category.
10. **Search Expenses** - Search by keyword, category, or amount range.
11. **Set Budget** - Define monthly budgets per category.
12. **Check Budget Status** - Compare spending against set budgets.
13. **Add Recurring Expense** - Schedule weekly or monthly recurring expenses.
14. **Export Expenses** - Export all expenses to CSV or JSON.
15. **Import Expenses** - Import expenses from CSV or JSON files.
16. **Exit** - Save all changes and exit the program.

---

## License

This project is open source and available under the MIT License.
s