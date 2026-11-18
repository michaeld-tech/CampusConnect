# CampusConnect - ALU Lost and Found System

CampusConnect is a simple lost-and-found system for the African Leadership University community. Students can report belongings they have lost, register items they have found, and claim found items that belong to them.

## Main Menu

```
==================================================
                  CAMPUSCONNECT
            ALU LOST AND FOUND SYSTEM
==================================================

How may we help you today?

1. Report a Lost Item
2. Register a Found Item
3. Claim for an Item
0. Exit System
```

### 1. Report a Lost Item

Enter the item's name, category, description, where you last saw it, the date it was lost (YYYY-MM-DD) and your contact details. All fields are required.

### 2. Register a Found Item

Enter the item's name, category, description, where you found it, the date it was found (YYYY-MM-DD) and your contact details. The item is saved as **Available** so its owner can claim it.

### 3. Claim for an Item

This option opens a smaller menu:

```
1. View all available items
2. Search for an item
0. Back to main menu
```

- **View all available items** lists every found item that has not been collected yet.
- **Search for an item** finds available items by name, category or location.

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
