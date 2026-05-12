import sys
import getpass
from vault import (
    create_vault, unlock_vault,
    add_generated_entry, add_stored_entry,
    get_password, list_entries, delete_entry
)

def main():

    if "--init" in sys.argv:
        print("=== Creating New Vault ===")

        while True:
            pw1 = getpass.getpass("Choose a master password: ")
            if len(pw1) < 8:
                print("Password must be at least 8 characters! Try again.")
                continue
            pw2 = getpass.getpass("Confirm master password : ")
            if pw1 != pw2:
                print("Passwords don't match! Try again.")
                continue
            break

        create_vault(pw1)
        print("Vault created! Run the program again without --init to log in.")
        return


    print("=== Password Manager ===")
    master_pw = getpass.getpass("Master password: ")
    key, vault_data = unlock_vault(master_pw)

    if key is None:
        return

    print("Vault unlocked!\n")


    while True:
        print("\nWhat would you like to do?")
        print("1. Get a password")
        print("2. Add new entry (generated password)")
        print("3. Add new entry (your own password)")
        print("4. List all entries")
        print("5. Delete an entry")
        print("6. Exit")

        choice = input("\nEnter number: ").strip()

        if choice == "1":
            site     = input("Site name: ").strip()
            username = input("Username : ").strip()
            password = get_password(vault_data, key, site, username)
            if password:
                print(f"\nPassword: {password}\n")
            else:
                print("No entry found for that site/username.")

        elif choice == "2":
            site       = input("Site name    : ").strip()
            username   = input("Username     : ").strip()
            length_str = input("Length [20]  : ").strip()
            length     = int(length_str) if length_str.isdigit() else 20
            password   = add_generated_entry(vault_data, key, site, username, length)
            print(f"\nGenerated password: {password}")
            print("Entry saved!\n")

        elif choice == "3":
            site     = input("Site name: ").strip()
            username = input("Username : ").strip()
            pw1      = getpass.getpass("Password : ")
            pw2      = getpass.getpass("Confirm  : ")
            if pw1 != pw2:
                print("Passwords don't match!")
                continue
            add_stored_entry(vault_data, key, site, username, pw1)
            print("Entry saved!")

        elif choice == "4":
            entries = list_entries(vault_data)
            if not entries:
                print("Vault is empty.")
            else:
                print(f"\n{'Site':<30} {'Username':<25} {'Type'}")
                print("-" * 65)
                for e in entries:
                    print(f"{e['site']:<30} {e['username']:<25} {e['type']}")

        elif choice == "5":
            site     = input("Site name: ").strip()
            username = input("Username : ").strip()
            confirm  = input(f"Delete {site}/{username}? [y/N]: ").strip().lower()
            if confirm == "y":
                if delete_entry(vault_data, site, username):
                    print("Deleted.")
                else:
                    print("Entry not found.")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()