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