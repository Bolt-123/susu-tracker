import unittest
from decimal import Decimal
from susu import SusuGroup

class TestSusuGroup(unittest.TestCase):

    def setUp(self):
        # Create a group with 50.00 GHS weekly contribution and 3 members
        self.group = SusuGroup("50.00")
        self.group.add_members("M1", "Ama")
        self.group.add_members("M2", "Kofi")
        self.group.add_members("M3", "Esi")

    def test_full_payment_closes_week_and_pays_recipient(self):
        """Test 1: When all members pay in full, week closes, pot pays first member, and week advances."""
        self.group.record_contribution("M1", "50.00")
        self.group.record_contribution("M2", "50.00")
        self.group.record_contribution("M3", "50.00")
        
        self.group.close_week()
        
        self.assertEqual(self.group.current_week, 2)
        self.assertEqual(len(self.group.payout_history), 1)
        self.assertEqual(self.group.payout_history[0]['recipient'], "Ama")
        self.assertEqual(self.group.payout_history[0]['amount'], Decimal("150.00"))

    def test_partial_payment_blocks_week_closure(self):
        """Test 2: Partial payment leaves debt and prevents week closure."""
        self.group.record_contribution("M1", "50.00")
        self.group.record_contribution("M2", "50.00")
        self.group.record_contribution("M3", "30.00")  # Esi pays 30, owes 20
        
        self.group.close_week()
        
        # Week must not advance, no payout created
        self.assertEqual(self.group.current_week, 1)
        self.assertEqual(len(self.group.payout_history), 0)

    def test_reject_unknown_member(self):
        """Test 3: System rejects payments from unregistered member IDs."""
        self.group.record_contribution("M99", "50.00")
        self.assertNotIn("M99", self.group.current_week_contributions)

    def test_reject_zero_or_negative_amount(self):
        """Test 4: System rejects payments of zero or negative amounts."""
        self.group.record_contribution("M1", "0.00")
        self.group.record_contribution("M2", "-10.00")
        self.assertNotIn("M1", self.group.current_week_contributions)
        self.assertNotIn("M2", self.group.current_week_contributions)

    def test_reject_overpayment(self):
        """Test 5: System rejects payments exceeding what a member owes for the week."""
        self.group.record_contribution("M1", "60.00")  # Exceeds weekly target of 50.00
        self.assertNotIn("M1", self.group.current_week_contributions)

    def test_reject_duplicate_member_and_late_additions(self):
        """Test 6: System rejects duplicate member IDs and late additions after week starts."""
        # Test duplicate ID rejection
        self.group.add_members("M1", "Duplicate Ama")
        self.assertEqual(len(self.group.members), 3)

        # Start group by making a payment
        self.group.record_contribution("M1", "50.00")

        # Test late member addition rejection
        self.group.add_members("M4", "Kwame")
        self.assertEqual(len(self.group.members), 3)

if __name__ == '__main__':
    unittest.main()
