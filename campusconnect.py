# =====================================================
# CAMPUSCONNECT - ALU LOST AND FOUND SYSTEM
#  DATABASE MANAGEMENT
# =====================================================

import sqlite3

class Database:
    """Handles database operations for CampusConnect."""

    def __init__(self, database_name="campusconnect.db"):
        self.database_name = database_name
        self.create_tables()

    def connect(self):
        """Connect to the SQLite database."""
        return sqlite3.connect(self.database_name)

    def create_tables(self):
        """Create the lost and found items tables."""

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lost_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                location TEXT NOT NULL,
                date_lost TEXT NOT NULL,
                contact TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS found_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                location TEXT NOT NULL,
                date_found TEXT NOT NULL,
                contact TEXT NOT NULL,
                status TEXT DEFAULT 'Available',
                claimed_by TEXT
            )
        """)

        connection.commit()
        connection.close()

        print("Database tables created successfully!")

    def insert_lost_item(self, item):
        """Save a reported lost item in the database."""

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO lost_items (
                item_name, category, description,
                location, date_lost, contact
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            item["item_name"],
            item["category"],
            item["description"],
            item["location"],
            item["date_lost"],
            item["contact"]
        ))

        connection.commit()
        item_id = cursor.lastrowid
        connection.close()

        print(f"Lost item recorded successfully! ID: {item_id}")
        return item_id

    def insert_found_item(self, item):
        """Save a found item in the database."""

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO found_items (
                item_name, category, description,
                location, date_found, contact
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            item["item_name"],
            item["category"],
            item["description"],
            item["location"],
            item["date_found"],
            item["contact"]
        ))

        connection.commit()
        item_id = cursor.lastrowid
        connection.close()

        print(f"Found item recorded successfully! ID: {item_id}")
        return item_id

    def fetch_items(self, search_term=None):
        """Retrieve lost and found items from the database."""

        connection = self.connect()
        cursor = connection.cursor()

        if search_term:
            search = f"%{search_term}%"

            cursor.execute("""
                SELECT id, item_name, category, description,
                       location, date_lost, contact, 'Lost' AS item_type
                FROM lost_items
                WHERE item_name LIKE ?
                   OR category LIKE ?
                   OR location LIKE ?

                UNION ALL

                SELECT id, item_name, category, description,
                       location, date_found, contact, 'Found' AS item_type
                FROM found_items
                WHERE item_name LIKE ?
                   OR category LIKE ?
                   OR location LIKE ?
            """, (search, search, search, search, search, search))

        else:
            cursor.execute("""
                SELECT id, item_name, category, description,
                       location, date_lost, contact, 'Lost' AS item_type
                FROM lost_items

                UNION ALL

                SELECT id, item_name, category, description,
                       location, date_found, contact, 'Found' AS item_type
                FROM found_items
            """)

        results = cursor.fetchall()
        connection.close()

        return results

    def search_items(self, field, keyword):
        """Search lost and found items by a specific field."""

        allowed_fields = ["item_name", "category", "location"]

        if field not in allowed_fields:
            print("Invalid search field.")
            return []

        connection = self.connect()
        cursor = connection.cursor()

        search = f"%{keyword}%"

        query = f"""
            SELECT id, item_name, category, description,
                   location, date_lost AS item_date,
                   contact, 'Lost' AS item_type
            FROM lost_items
            WHERE {field} LIKE ?

            UNION ALL

            SELECT id, item_name, category, description,
                   location, date_found AS item_date,
                   contact, 'Found' AS item_type
            FROM found_items
            WHERE {field} LIKE ?
        """

        cursor.execute(query, (search, search))

        columns = [
            description[0]
            for description in cursor.description
        ]

        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        connection.close()

        return results

    def update_item_status(self, item_id, claimant_name):
        """Mark a found item as returned and record who claimed it."""

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE found_items
            SET status = 'Returned',
                claimed_by = ?
            WHERE id = ?
            AND status = 'Available'
        """, (claimant_name, item_id))

        connection.commit()

        updated = cursor.rowcount > 0

        connection.close()

        if updated:
            print("Item successfully marked as returned!")
        else:
            print("Item not found or has already been returned.")

        return updated
# =====================================================
#  LOST ITEM REPORTING
# =====================================================

from datetime import datetime

class LostItem:
    """Handles reporting of lost items."""

    def __init__(self, database):
        self.database = database

    def report_lost_item(self):
        """Collect lost item details and save them."""

        print("\n========== REPORT A LOST ITEM ==========")

        item_name = input("Enter item name: ").strip()
        category = input("Enter item category: ").strip()
        description = input("Describe the item: ").strip()
        location = input("Where did you last see the item? ").strip()
        date_lost = input("Date lost (YYYY-MM-DD): ").strip()
        contact = input("Enter your contact information: ").strip()

         
        if not all([
            item_name,
            category,
            description,
            location,
            date_lost,
            contact
        ]):
            print("\nError: All fields are required.")
            return

      
        try:
            datetime.strptime(date_lost, "%Y-%m-%d")
        except ValueError:
            print("\nError: Invalid date format.")
            print("Please use YYYY-MM-DD.")
            return

        
        item = {
            "item_name": item_name,
            "category": category,
            "description": description,
            "location": location,
            "date_lost": date_lost,
            "contact": contact
        }

      
        self.database.insert_lost_item(item)

        print("\nYour lost item report has been submitted!")
# =====================================================
# MEMBER 3: FOUND ITEM REGISTRATION
# =====================================================

class FoundItem:
    """Handles registration of found items."""

    def __init__(self, database):
        self.database = database

    def register_found_item(self):
        """Collect found item details and save them."""

        print("\n========== REGISTER A FOUND ITEM ==========")

        item_name = input("Enter item name: ").strip()
        category = input("Enter item category: ").strip()
        description = input("Describe the item: ").strip()
        location = input("Where did you find the item? ").strip()
        date_found = input("Date found (YYYY-MM-DD): ").strip()
        contact = input("Enter your contact information: ").strip()

        # Validate required fields
        if not all([
            item_name,
            category,
            description,
            location,
            date_found,
            contact
        ]):
            print("\nError: All fields are required.")
            return

        # Validate date format
        try:
            datetime.strptime(date_found, "%Y-%m-%d")
        except ValueError:
            print("\nError: Invalid date format.")
            print("Please use YYYY-MM-DD.")
            return

        # Organise the information
        item = {
            "item_name": item_name,
            "category": category,
            "description": description,
            "location": location,
            "date_found": date_found,
            "contact": contact
        }

        # Save using Member 1's database function
        self.database.insert_found_item(item)

        print("\nFound item registered successfully!")

# =====================================================
#  SEARCH AND FILTERING
# =====================================================

class SearchItems:
    """Handles searching for lost and found items."""

    def __init__(self, database):
        self.database = database

    def search_items(self):
        """Search lost and found items by name, category or location."""

        print("\n========== SEARCH FOR AN ITEM ==========")
        print("1. Search by item name")
        print("2. Search by category")
        print("3. Search by location")

        choice = input("\nChoose search option (1-3): ").strip()

        search_fields = {
            "1": "item_name",
            "2": "category",
            "3": "location"
        }

        if choice not in search_fields:
            print("\nError: Invalid search option.")
            return

        field = search_fields[choice]
        keyword = input("Enter your search keyword: ").strip()

        if not keyword:
            print("\nError: Search keyword cannot be empty.")
            return

        results = self.database.search_items(field, keyword)

        if not results:
            print("\nNo matching items found.")
            return

        print("\n========== SEARCH RESULTS ==========")

        for item in results:
            print(f"\nItem ID: {item['id']}")
            print(f"Item Name: {item['item_name']}")
            print(f"Category: {item['category']}")
            print(f"Description: {item['description']}")
            print(f"Location: {item['location']}")
            print(f"Date: {item['item_date']}")
            print(f"Contact: {item['contact']}")
            print(f"Item Type: {item['item_type']}")

            if item["item_type"] == "Found":
                print(f"Status: {item['status']}")

            print("------------------------------------")

        print(f"\nTotal matching items: {len(results)}")


import sqlite3


class Database:
    """Database wrapper for searching lost and found items."""

    def __init__(self, db_path="campusconnect.db"):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def search_items(self, field, keyword):
        """Search lost and found items by name, category or location."""

        allowed_fields = ["item_name", "category", "location"]

        if field not in allowed_fields:
            print("Invalid search field.")
            return []

        connection = self.connect()
        cursor = connection.cursor()

        search_value = f"%{keyword}%"

        query = """
            SELECT
                id, item_name, category, description,
                location, date_lost AS item_date,
                contact, 'Lost' AS item_type,
                NULL AS status
            FROM lost_items
            WHERE {field} LIKE ?

            UNION ALL

            SELECT
                id, item_name, category, description,
                location, date_found AS item_date,
                contact, 'Found' AS item_type,
                status
            FROM found_items
            WHERE {field} LIKE ?
        """.format(field=field)

        cursor.execute(query, (search_value, search_value))
        columns = [column[0] for column in cursor.description]

        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        connection.close()
        return results

# =====================================================
# CAMPUSCONNECT - MAIN APPLICATION
# MEMBER 5: SYSTEM INTEGRATION AND CLAIM MANAGEMENT
# =====================================================

class CampusConnect:
    """Main application controller for CampusConnect."""

    def __init__(self, database):
        """Initialize the application."""
        self.database = database
        self.running = True

    def display_menu(self):
        """Display the main application menu."""

        print("\n" + "=" * 50)
        print("          CAMPUSCONNECT")
        print("       LOST AND FOUND SYSTEM")
        print("=" * 50)

        print("1. Report Lost Item")
        print("2. Report Found Item")
        print("3. Search for Items")
        print("4. View Available Items")
        print("5. Claim/Collect Found Item")
        print("6. Exit")

        print("=" * 50)

    def get_input(self, message):
        """Get validated input from the user."""

        while True:
            value = input(message).strip()

            if value:
                return value

            print("Input cannot be empty. Please try again.")

    def get_item_id(self):
        """Get a valid item ID."""

        while True:
            try:
                item_id = int(input("Enter item ID: "))

                if item_id > 0:
                    return item_id

                print("Item ID must be greater than zero.")

            except ValueError:
                print("Please enter a valid numerical ID.")

    def report_lost_item(self):
        """Allow users to report lost items."""

        print("\n========== REPORT LOST ITEM ==========")

        item = (
            self.get_input("Item name: "),
            self.get_input("Category: "),
            self.get_input("Description: "),
            self.get_input("Location lost: "),
            self.get_input("Date lost (YYYY-MM-DD): "),
            self.get_input("Contact information: ")
        )

        try:
            self.database.insert_lost_item(item)

            print("\nLost item reported successfully!")

        except Exception as error:
            print("Unable to report lost item:", error)

    def report_found_item(self):
        """Allow users to report found items."""

        print("\n========== REPORT FOUND ITEM ==========")

        item = (
            self.get_input("Item name: "),
            self.get_input("Category: "),
            self.get_input("Description: "),
            self.get_input("Location found: "),
            self.get_input("Date found (YYYY-MM-DD): "),
            self.get_input("Contact information: ")
        )

        try:
            self.database.insert_found_item(item)

            print("\nFound item reported successfully!")

        except Exception as error:
            print("Unable to report found item:", error)

    def search_items(self):
        """Search for lost and found items."""

        print("\n========== SEARCH ITEMS ==========")

        search_term = self.get_input(
            "Enter item name, category or location: "
        )

        try:
            items = self.database.fetch_items(search_term)

            if not items:
                print("\nNo matching items found.")
                return

            print("\nSearch Results")
            print("-" * 50)

            for item in items:
                print(item)

        except Exception as error:
            print("Search failed:", error)

    def view_available_items(self):
        """Display available found items."""

        print("\n========== AVAILABLE FOUND ITEMS ==========")

        try:
            items = self.database.fetch_items()

            if not items:
                print("No items currently available.")
                return

            available_items = [
                item for item in items
                if len(item) > 8 and item[8] == "Available"
            ]

            if not available_items:
                print("No available found items.")
                return

            for item in available_items:
                print("-" * 50)
                print("Item ID:", item[0])
                print("Item Name:", item[1])
                print("Category:", item[2])
                print("Description:", item[3])
                print("Location:", item[4])
                print("Date Found:", item[5])
                print("Contact:", item[6])
                print("Status:", item[8])

        except Exception as error:
            print("Unable to retrieve available items:", error)

    def claim_found_item(self):
        """Allow users to collect a found item."""

        print("\n========== CLAIM FOUND ITEM ==========")

        try:
            item_id = self.get_item_id()

            claimant_name = self.get_input(
                "Enter your full name: "
            )

            print("\nConfirm that you have verified ownership.")
            confirmation = input(
                "Has the item been successfully handed over? (yes/no): "
            ).strip().lower()

            if confirmation != "yes":
                print("\nCollection not confirmed.")
                return

            self.database.update_item_status(
                item_id,
                claimant_name
            )

            print("\nItem collection recorded successfully!")
            print("The item status has been updated.")

        except Exception as error:
            print("Unable to process item collection:", error)

    def run(self):
        """Run the main application."""

        print("\nWelcome to CampusConnect!")

        while self.running:

            self.display_menu()

            choice = input("Select an option (1-6): ").strip()

            if choice == "1":
                self.report_lost_item()

            elif choice == "2":
                self.report_found_item()

            elif choice == "3":
                self.search_items()

            elif choice == "4":
                self.view_available_items()

            elif choice == "5":
                self.claim_found_item()

            elif choice == "6":
                print("\nThank you for using CampusConnect!")
                print("Goodbye!")
                self.running = False

            else:
                print("\nInvalid choice. Please select 1-6.")


# =====================================================
# APPLICATION ENTRY POINT
# =====================================================

def main():
    """Initialize the database and start CampusConnect."""

    try:
        database = Database()

        application = CampusConnect(database)

        application.run()

    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")

    except Exception as error:
        print("\nApplication error:", error)


if __name__ == "__main__":
    main()
