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
