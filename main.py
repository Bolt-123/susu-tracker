from susu import SusuGroup

def main():
    print("SUSU GROUP TRACKER CLI")

    # 1. Setup Group
    while True:
        try:
            weekly_amount = input("Enter fixed weekly contribution amount in GHS (e.g., 50.00): ").strip()
            group = SusuGroup(weekly_amount)
            print(f"Group initialized with a weekly contribution of {group.weekly_contribution} GHS.\n")
            break
        except Exception as e:
            print(f"Invalid amount input. Error: {e}. Please try again.")

    # 2. Interactive Command Menu
    while True:
        print("\n Main Menu")
        print(f"Status: Week {group.current_week} | Members Registered: {len(group.members)}")
        print("1. Add Member")
        print("2. Record Contribution")
        print("3. Close Week")
        print("4. Show Report")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()

        if choice == '1':
            member_id = input("Enter Member ID: ").strip()
            name = input("Enter Member Name: ").strip()
            if member_id and name:
                group.add_members(member_id, name)
            else:
                print("Error: Member ID and Name cannot be empty.")

        elif choice == '2':
            member_id = input("Enter Member ID: ").strip()
            amount = input("Enter Contribution Amount in GHS: ").strip()
            if member_id and amount:
                try:
                    group.record_contribution(member_id, amount)
                except Exception as e:
                    print(f"Error recording contribution: {e}")
            else:
                print("Error: Member ID and Amount are required.")

        elif choice == '3':
            group.close_week()

        elif choice == '4':
            group.show_report()

        elif choice == '5':
            print("Exiting Susu Tracker CLI.")
            break

        else:
            print("Invalid selection. Please choose an option between 1 and 5.")

if __name__ == "__main__":
    main()
