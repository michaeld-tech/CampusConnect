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
#  SEARCH AND FILTERING
# =====================================================


class SearchItems:
    """Handles searching for lost and found items."""

    def __init__(self, database):
        self.database = database

    def search_items(self):
        """Search for items using name, category or location."""

        print("\n========== SEARCH FOR AN ITEM ==========")

        print("1. Search by item name")
        print("2. Search by category")
        print("3. Search by location")

        choice = input("\nChoose search option (1-3): ").strip()

        if choice not in ["1", "2", "3"]:
            print("\nError: Invalid search option.")
            return

        search_fields = {
            "1": "item_name",
            "2": "category",
            "3": "location"
        }

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
            print(f"\nItem Name: {item['item_name']}")
            print(f"Category: {item['category']}")
            print(f"Description: {item['description']}")
            print(f"Location: {item['location']}")

            if "date_lost" in item:
                print(f"Date Lost: {item['date_lost']}")

            if "date_found" in item:
                print(f"Date Found: {item['date_found']}")

            print("------------------------------------")

        print(f"\nTotal matching items: {len(results)}")
