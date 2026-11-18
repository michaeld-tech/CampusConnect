# CampusConnect - ALU Lost and Found System

CampusConnect is a straightforward system that helps the African Leadership University students handle lost and found items.

## Main Menu

```
==================================================
                  CAMPUSCONNECT
            ALU LOST AND FOUND SYSTEM
==================================================

How may we assist you today?

1. Report a Lost Item
2. Register a Found Item
3. Claim for an Item
0. Exit System
```

### 1. Report a Lost Item

In this section, you need to enter the lost item’s name, category, description, location where it was last however, seen and date of loss (YYYY-MM-DD). Contact information is mandatory.

### 2. Register a Found Item

To register a found item, you must enter the name of the item, its category, description, location where it was found, date of finding the item and your contact details. The item is listed as “Available”.

### 3. Claim for an Item

Upon selecting this option, you will see the following submenu.

```
1. View all available items
2. Search for an item
0. Back to main menu
```

- **View all available items** option gives a list of all lost items that are still as unclaimed.
- **Search for an item** helps find lost items by name, category or location.

After the items are listed, enter the ID of the item you want to claim, or `0` to go back. Then enter your full name and confirm that the item has been handed over. The item is marked as **Returned**, your name is recorded, and the item no longer appears as available.

### 0. Exit System

Closes the application.

## Running the Project

You need Python 3. No extra packages are required.

```
python main.py
```

The SQLite database (`campusconnect.db`) is created automatically in the project folder the first time the application runs. It is always used from that location, no matter which folder you run the command from.

## Database

The system stores information in two tables:

- **lost_items** holds the details of items reported missing.
- **found_items** holds the details of items reported found, their status (`Available` or `Returned`) and the name of the person who collected them.

## Code Structure

- `main.py` is the entry point. Run this file to start the application.
- `campusconnect.py` contains the application classes:

| Class          | Responsibility                                                  |
| -------------- | --------------------------------------------------------------- |
| `Database`     | Creates the tables and reads and writes item records            |
| `LostItem`     | Collects and validates lost item reports                        |
| `FoundItem`    | Collects and validates found item registrations                 |
| `SearchItems`  | Searches available found items by name, category or location    |
| `CampusConnect`| Shows the main menu and handles the claim process               |
