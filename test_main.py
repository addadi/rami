import unittest
from unittest.mock import patch
from io import StringIO
from main import FamilyBirthdayCard, Person, FamilyMember, parse_args, main

class TestFamilyBirthdayCard(unittest.TestCase):

    def setUp(self):
        # Set up test data
        birthday_person_data = {
            "name": "rami",
            "birth_year": 1963,
            "bio_elements": {"1963": {"content": "Born!"}},
        }
        family_members_data = [
            {"name": "lidia", "greeting": "Sending warm wishes to {name}!", "relationship": "ima"},
            {"name": "itzhak", "greeting": "Happy birthday, {name}!", "relationship": "aba zal"},
        ]
        self.family_config_data = {
            "family_name": "addady",
            "birthday_person": birthday_person_data,
            "family_members": family_members_data,
        }

    def test_show_bio_for_year(self):
        birthday_person = Person(**self.family_config_data["birthday_person"])
        family_members = [FamilyMember(**data) for data in self.family_config_data["family_members"]]
        family_birthday_card = FamilyBirthdayCard(birthday_person, family_members)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            family_birthday_card.show_bio_for_year(1963)
            output = mock_stdout.getvalue().strip()

        expected_output = "rami was 0 years old at 1963. Born!"
        self.assertEqual(output, expected_output)

    def test_make_wish(self):
        birthday_person = Person(**self.family_config_data["birthday_person"])
        family_members = [FamilyMember(**data) for data in self.family_config_data["family_members"]]
        family_birthday_card = FamilyBirthdayCard(birthday_person, family_members)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            family_birthday_card.make_wish()
            output = mock_stdout.getvalue().strip()

        expected_output = "Sending warm wishes to rami!\nHappy birthday, rami!"
        self.assertEqual(output, expected_output)

    # Add more test methods for other functionalities

class TestMain(unittest.TestCase):

    def test_parse_args(self):
        with patch("sys.argv", ["main.py", "rami", "--year", "1963"]):
            args = parse_args()
        self.assertEqual(args.action, "rami")
        self.assertEqual(args.year, 1963)

    def test_main(self):
        # Add tests for the main function

if __name__ == "__main__":
    unittest.main()
