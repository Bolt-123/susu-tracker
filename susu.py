from decimal import Decimal

class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name

class SusuGroup:
    def __init__(self, weekly_contribution):
        self.weekly_contribution = Decimal(str(weekly_contribution))
        self.members = []
        self.current_week = 1
        self.current_week_contributions = {}
        self.payout_history = []
        self.group_started = False

    def add_members(self, member_id, name):
        if self.group_started:
            print('Cannot add member after payments have started.')
            return

        # Confirm duplicates
        for member in self.members:
            if member.member_id == member_id:
                print('Member ID already exists.')
                return

        # Add member if checks pass
        new_member = Member(member_id, name)
        self.members.append(new_member)
        print(f"Member '{name}' ({member_id}) added successfully.")

    def record_contribution(self, member_id, amount):
        # 1. Verify member exists
        member_found = False
        for member in self.members:
            if member.member_id == member_id:
                member_found = True
                break

        if not member_found:
            print('Member not found!')
            return

        # 2. Validate positive amount
        amount_paid = Decimal(str(amount))
        if amount_paid <= Decimal('0.00'):
            print('Payment must be greater than 0!')
            return

        # 3. Calculate remaining amount owed
        already_paid = self.current_week_contributions.get(member_id, Decimal('0.00'))
        owed = self.weekly_contribution - already_paid

        # 4. Prevent overpayment
        if amount_paid > owed:
            print('Payment exceeds the remaining amount owed for this week.')
            return

        # 5. Lock group and save contribution
        self.group_started = True
        self.current_week_contributions[member_id] = already_paid + amount_paid
        print(f"Recorded payment of {amount_paid} GHS for member '{member_id}'.")

    def close_week(self):
        if not self.members:
            print("Cannot close week: No members registered.")
            return

        # 1. Check for unpaid members
        unpaid_members = []
        for member in self.members:
            paid = self.current_week_contributions.get(member.member_id, Decimal('0.00'))
            owed = self.weekly_contribution - paid

            if owed > Decimal('0.00'):
                unpaid_members.append(f"{member.name} ({member.member_id}) owes {owed} GHS")

        # 2. Reject closure if any member still owes
        if unpaid_members:
            print("Cannot close week. The following members still owe:")
            for status in unpaid_members:
                print(f" - {status}")
            return

        # 3. Calculate payout pot and sequential recipient
        pot = self.weekly_contribution * Decimal(str(len(self.members)))
        recipient_index = (self.current_week - 1) % len(self.members)
        recipient = self.members[recipient_index]

        # 4. Record payout
        self.payout_history.append({
            'week': self.current_week,
            'recipient': recipient.name,
            'amount': pot
        })
        print(f"Week {self.current_week} closed! Pot of {pot} GHS paid to {recipient.name}.")

        # 5. Reset weekly ledger and advance week
        self.current_week_contributions = {}
        self.current_week += 1

    def show_report(self):
        print(f"\n=== Status Report: Week {self.current_week} ===")
        print(f"Weekly Required Contribution: {self.weekly_contribution} GHS")
        print("Member Statuses:")
        for member in self.members:
            paid = self.current_week_contributions.get(member.member_id, Decimal('0.00'))
            owed = self.weekly_contribution - paid
            if owed == Decimal('0.00'):
                print(f" - {member.name}: Paid in full ({paid} GHS)")
            else:
                print(f" - {member.name}: Paid {paid} GHS | Owes {owed} GHS")

        print("\nPayout History:")
        if not self.payout_history:
            print(" - No payouts recorded yet.")
        else:
            for payout in self.payout_history:
                print(f" - Week {payout['week']}: {payout['recipient']} received {payout['amount']} GHS")
