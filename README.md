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

After you complete the listing process, enter the ID of the item you wish to seize or `0` for reverting back. Enter your full name and confirm that the item has been received. The item now gets the status **Returned**, your name is recorded, and the item will not be shown as available anymore.

### 0. Exit System

Closes the app.

## Starting the Project

You need Python version 3.0. No additional packages necessary.

```
python main.py
```

The SQLite database file named `campusconnect.db` will be created automatically when the app is run for the first time. It will always be taken from this location irrespective of the folder from which you run the command.

## Database

The application keeps its information in two tables:

- **lost_items** which contain the particulars of lost items;
- **found_items** which summarize details of found items, their availability (i.e. `Available` or `Returned`) and name of the person who took them.

## Code Organization

- `main.py` is the entry point of the system, i.e. the file needed to start the app.
- `campusconnect.py` is the file that contains classes of the program.

| Class          | Responsibility                                                  |
| -------------- | --------------------------------------------------------------- |
| `Database`     | Creates the tables and reads and writes item records            |
| `LostItem`     | Collects and validates lost item reports                        |
| `FoundItem`    | Collects and validates found item registrations                 |
| `SearchItems`  | Searches available found items by name, category or location    |
| `CampusConnect`| Shows the main menu and handles the claim process               |
