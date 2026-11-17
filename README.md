# CampusConnect – ALU Lost and Found System

CampusConnect is a simple lost-and-found system for the African Leadership University community. It helps students report belongings they have lost or found, search for items, and record when an item has been collected.

## What the System Does

- **Report lost items:** Add the item's name, category, description, last known location, date it was lost, and contact details.
- **Report found items:** Share details about an item that has been found so its owner can identify and collect it.
- **Search for items:** Find reports using an item's name, category, or location.
- **View available items:** See found items that have not yet been collected.
- **Record item collection:** Confirm that an item has been handed back and record the name of the person who collected it.

## How It Works

The application runs in a terminal and guides the user through a simple menu. Users choose the action they want to complete and provide the requested information. Item records are saved in a local SQLite database, which is created automatically when the application first runs.

When reporting an item, users provide the relevant details and the date in year-month-day format. When collecting a found item, the user provides the item ID and their name, then confirms that the item has been handed over.

## Technology Used

The project is built with Python and uses SQLite to store item records. It uses Python's built-in date and database tools, so no additional packages are needed for the code provided.

## Database

The system stores information in two tables:

- **Lost items:** Keeps the details of items reported missing.
- **Found items:** Keeps the details of items reported found, including whether they are still available or have been returned, and who collected them.

## Running the Project

Make sure Python 3 is installed on your computer. Open the project folder in a terminal and run the main Python file. The database and its tables will be created automatically when the application starts.

## Notes

Some parts of the current source code need to be aligned and tested, particularly the way item details are passed to the database and how available found items are retrieved. These should be fixed to ensure all menu options work as expected.
