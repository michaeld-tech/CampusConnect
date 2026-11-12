from database import initialize_database

from services.lost_items import report_lost_item
from services.found_items import register_found_item, claim_item
from services.search import search_items


def display_menu():
    

    print("\n========================================")
    print("             CAMPUSCONNECT")
    print("       STUDENT LOST AND FOUND SYSTEM")
    print("========================================")
    print("1. Report a Lost Item")
    print("2. Register a Found Item")
    print("3. Search for an Item")
    print("4. Claim or Return an Item")
    print("0. Exit")
    print("========================================")


def main():
    

    initialize_database()

    print("\nWelcome to CampusConnect!")
    print("Helping ALU students reconnect with lost belongings.")

    while True:
        display_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            report_lost_item()

        elif choice == "2":
            register_found_item()

        elif choice == "3":
            search_items()

        elif choice == "4":
            claim_item()

        elif choice == "0":
            print("\nThank you for using CampusConnect!")
            print("Goodbye!")
            break

        else:
            print("\nInvalid choice. Please select an option from the menu.")


if __name__ == "__main__":
    main()
