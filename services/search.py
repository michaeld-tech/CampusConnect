import sqlite3
from database import get_connection


def search_items():


    print("\n========== SEARCH CAMPUS ITEMS ==========")
    print("1. Search by item name")
    print("2. Search by category")
    print("3. Search by location")
    print("0. Return to main menu")

    choice = input("\nChoose a search option: ").strip()

    search_options = {
        "1": "item_name",
        "2": "category",
        "3": "location"
    }

    if choice == "0":
        return

    if choice not in search_options:
        print("\nInvalid option. Please try again.")
        return

    keyword = input("Enter your search term: ").strip()

    if not keyword:
        print("\nSearch term cannot be empty.")
        return

    column = search_options[choice]

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = f"""
            SELECT id, item_name, category, description,
                   item_type, location, item_date, status
            FROM items
            WHERE {column} LIKE ?
            ORDER BY id DESC
        """

        cursor.execute(query, (f"%{keyword}%",))
        results = cursor.fetchall()

        if not results:
            print("\nNo matching items found.")
            return

        print("\n========== SEARCH RESULTS ==========")

        for item in results:
            print("\n------------------------------------")
            print(f"Item ID: {item[0]}")
            print(f"Item Name: {item[1]}")
            print(f"Category: {item[2]}")
            print(f"Description: {item[3]}")
            print(f"Type: {item[4]}")
            print(f"Location: {item[5]}")
            print(f"Date: {item[6]}")
            print(f"Status: {item[7]}")

        print("\n------------------------------------")

    except sqlite3.Error as error:
        print(f"\nDatabase error: {error}")

    finally:
        if "connection" in locals():
            connection.close()
