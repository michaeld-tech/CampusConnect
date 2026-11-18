# =====================================================
# CAMPUSCONNECT - ALU LOST AND FOUND SYSTEM
#  DATABASE MANAGEMENT
# =====================================================

import sqlite3
from datetime import datetime
from pathlib import Path

class Database:
    """Handles database operations for CampusConnect."""

    def __init__(self, database_name=None):
        if database_name is None:
            database_path = Path(__file__).resolve().with_name("campusconnect.db")
        else:
            database_path = Path(database_name).expanduser().resolve()

        self.database_name = str(database_path)
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

    def fetch_available_items(self, field=None, keyword=None):
        """Retrieve found items that are still available.

        Optionally filter by item_name, category or location.
        """
        
        query = """
            SELECT id, item_name, category, description,
                   location, date_found, contact, status
            FROM found_items
            WHERE status = 'Available'
        """
        params = ()

        if field and keyword:
            if field not in ("item_name", "category", "location"):
                print("Invalid search field.")
                return []
            query += f" AND {field} LIKE ?"
            params = (f"%{keyword}%",)

        query += " ORDER BY id"

        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
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
#  FOUND ITEM REGISTRATION
# ============================================================

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

        # Save to the database
        self.database.insert_found_item(item)

        print("\nFound item registered successfully!")

# =====================================================
#  SEARCH AND FILTERING
# =====================================================

class SearchItems:
    """Handles searching for available found items."""

    def __init__(self, database):
        self.database = database

    def search_items(self):
        """Search available found items by name, category or location.

        Returns the list of matching items.
        """

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
            return []

        keyword = input("Enter your search keyword: ").strip()

        if not keyword:
            print("\nError: Search keyword cannot be empty.")
            return []

        return self.database.fetch_available_items(search_fields[choice], keyword)


# =====================================================
# CAMPUSCONNECT - MAIN APPLICATION
#  SYSTEM INTEGRATION AND CLAIM MANAGEMENT
# =====================================================

class CampusConnect:
    """Main application controller for CampusConnect."""

    def __init__(self, database):
        """Initialize the application."""
        self.database = database
        self.lost_items = LostItem(database)
        self.found_items = FoundItem(database)
        self.searcher = SearchItems(database)
        self.running = True

    def display_menu(self):
        """Display the main application menu."""

        print("\n" + "=" * 50)
        print("CAMPUSCONNECT".center(50))
        print("ALU LOST AND FOUND SYSTEM".center(50))
        print("=" * 50)
        print("\nHow may we help you today?\n")
        print("1. Report a Lost Item")
        print("2. Register a Found Item")
        print("3. Claim for an Item")
        print("0. Exit System")

    def get_input(self, message):
        """Get non-empty input from the user."""

        while True:
            value = input(message).strip()

            if value:
                return value

            print("Input cannot be empty. Please try again.")

    def display_items(self, items):
        """Print a list of available found items."""

        if not items:
            print("\nNo matching available items found.")
            return

        for item in items:
            print("-" * 50)
            print("Item ID:", item[0])
            print("Item Name:", item[1])
            print("Category:", item[2])
            print("Description:", item[3])
            print("Location:", item[4])
            print("Date Found:", item[5])
            print("Contact:", item[6])
            print("Status:", item[7])

        print("-" * 50)
        print(f"Total available items: {len(items)}")

    def claim_item(self):
        """View or search available items, then claim one."""

        while True:
            print("\n========== CLAIM FOR AN ITEM ==========")
            print("1. View all available items")
            print("2. Search for an item")
            print("0. Back to main menu")

            choice = input("\nSelect an option: ").strip()

            if choice == "1":
                print("\n========== AVAILABLE FOUND ITEMS ==========")
                items = self.database.fetch_available_items()
            elif choice == "2":
                items = self.searcher.search_items()
            elif choice == "0":
                return
            else:
                print("\nInvalid choice. Please select 1, 2 or 0.")
                continue

            self.display_items(items)

            if items:
                self.collect_item({item[0] for item in items})

    def collect_item(self, valid_ids):
        """Ask which listed item to claim and record the collection."""

        while True:
            value = input("\nEnter the ID of the item to claim (0 to go back): ").strip()

            if value == "0":
                return

            if value.isdigit() and int(value) in valid_ids:
                item_id = int(value)
                break

            print("Please enter one of the item IDs listed above.")

        claimant_name = self.get_input("Enter your full name: ")

        print("\nConfirm that you have verified ownership.")
        confirmation = input(
            "Has the item been successfully handed over? (yes/no): "
        ).strip().lower()

        if confirmation != "yes":
            print("\nCollection not confirmed.")
            return

        try:
            self.database.update_item_status(item_id, claimant_name)
        except Exception as error:
            print("Unable to process item collection:", error)

    def run(self):
        """Run the main application."""

        while self.running:

            self.display_menu()

            choice = input("\nSelect an option: ").strip()

            if choice == "1":
                self.lost_items.report_lost_item()

            elif choice == "2":
                self.found_items.register_found_item()

            elif choice == "3":
                self.claim_item()

            elif choice == "0":
                print("\nThank you for using CampusConnect!")
                print("Goodbye!")
                self.running = False

            else:
                print("\nInvalid choice. Please select 1, 2, 3 or 0.")


