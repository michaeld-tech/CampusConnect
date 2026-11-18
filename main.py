# =====================================================
# CAMPUSCONNECT - ALU LOST AND FOUND SYSTEM
#  APPLICATION ENTRY POINT

# =====================================================

from campusconnect import CampusConnect, Database


def main():
    """Initialize the database and start CampusConnect."""

    try:
        database = Database()

        application = CampusConnect(database)

        application.run()

    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")

    except Exception as error:
        print("\nApplication error:", error)


if __name__ == "__main__":
    main()
