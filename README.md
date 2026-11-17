# CampusConnect – ALU Lost and Found System

CampusConnect is a command-line lost-and-found application designed for the African Leadership University (ALU) community. It provides a central place to report lost belongings, report items that have been found, search item reports, view available found items, and record item collection.

## Features

- **Report a lost item** – record the item's name, category, description, last-seen location, date lost, and contact information.
- **Report a found item** – record details about an item that has been found, including where and when it was found and how to contact the person who reported it.
- **Search item reports** – search lost and found records by item name, category, or location.
- **View available found items** – display found items that are available for collection.
- **Record a claim** – record the claimant's name and update a found item's status to `Returned` after the handover is confirmed.
- **Store records locally** – use an SQLite database, created automatically when the application starts.

## Technology

- **Language:** Python 3
- **Database:** SQLite (`sqlite3`, included with Python)
- **Date validation:** Python `datetime` module

No third-party Python packages are required by the code shown.

## Project structure

The supplied source code contains the application logic in Python. A typical project layout is:

```text
CampusConnect/
├── main.py                 # Application code / entry point
├── campusconnect.db        # Created automatically on first run
└── README.md
```

If your Python source file has a different name, use that filename in the run command below.

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/michaeld-tech/CampusConnect.git
cd CampusConnect
```

### 2. Check Python

Python 3 is required. Check that it is installed:

```bash
python3 --version
```

### 3. Run the application

If the main Python file is named `main.py`, run:

```bash
python3 main.py
```

The application creates `campusconnect.db` and its tables automatically when it starts. The database file is stored in the application's current working directory.

## Using CampusConnect

When the program starts, it displays this menu:

```text
1. Report Lost Item
2. Report Found Item
3. Search for Items
4. View Available Items
5. Claim/Collect Found Item
6. Exit
```

Choose an option by entering its number.

### Reporting an item

Provide the requested item details. Dates are expected in `YYYY-MM-DD` format (for example, `2026-11-17`). The reporting prompts require the item name, category, description, location, date, and contact information.

### Searching

Choose whether to search by item name, category, or location, then enter a keyword. Search matching uses partial text matching.

### Claiming a found item

Enter the found item's ID and your full name. Confirm that ownership has been verified and the item has been handed over. A successful claim changes the item's status from `Available` to `Returned` and records the claimant's name.

## Database design

CampusConnect uses two SQLite tables:

### `lost_items`

| Column | Description |
|---|---|
| `id` | Auto-incrementing primary key |
| `item_name` | Name of the lost item (required) |
| `category` | Item category (required) |
| `description` | Item description |
| `location` | Where the item was last seen (required) |
| `date_lost` | Date the item was lost (required) |
| `contact` | Reporter contact information (required) |

### `found_items`

| Column | Description |
|---|---|
| `id` | Auto-incrementing primary key |
| `item_name` | Name of the found item (required) |
| `category` | Item category (required) |
| `description` | Item description |
| `location` | Where the item was found (required) |
| `date_found` | Date the item was found (required) |
| `contact` | Reporter contact information (required) |
| `status` | Defaults to `Available`; becomes `Returned` after a recorded claim |
| `claimed_by` | Name of the person who collected the item |

## Important implementation notes

The supplied source currently contains inconsistencies between some methods and their callers. In particular:

- The database insertion methods `insert_lost_item()` and `insert_found_item()` access item details using dictionary keys, but the main application's reporting methods currently pass tuples.
- `fetch_items()` returns eight columns, while `view_available_items()` expects a ninth column containing the found-item status. As written, this can prevent the available-items view from identifying available records.
- The source also defines separate `LostItem` and `SearchItems` classes, but the main `CampusConnect` controller handles the menu workflow directly.

These issues should be corrected and tested before relying on all menu options. The README describes the intended workflows and the database structure present in the supplied code; it does not imply that every workflow currently runs successfully.

## Contributing

1. Fork the repository.
2. Create a branch for your change.
3. Make and test your changes.
4. Submit a pull request describing what you changed.

## License

No license information was included in the supplied source. Add a `LICENSE` file and update this section if the project is distributed under a specific license.
