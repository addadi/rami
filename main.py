import argparse
import random

from family_config import FamilyConfig

__version__ = "0.3"

class Person:
    def __init__(self, name, birth_year):
        self.name = name
        self.birth_year = birth_year
        self.bio_elements = {}


class FamilyMember:
    def __init__(self, name, greeting, relationship):
        self.name = name
        self.greeting = greeting
        self.relationship = relationship


class FamilyBirthdayCard:
    def __init__(self, birthday_person, family_members):
        self.birthday_person = birthday_person
        self.family_members = family_members

    def show_bio_for_year(self, year):
        bio_element = self.birthday_person.bio_elements.get(str(year))
        if bio_element:
            print(
                f"{self.birthday_person.name} was {bio_element['age']} years old at {year}. {bio_element['content']['content']}"
            )
        else:
            last_year = max(int(year) for year in self.birthday_person.bio_elements)
            print(
                f"{self.birthday_person.name} had nothing special at {year} but in {last_year}"
            )

    def show_bio_for_all_years(self):
        for year, bio_element in self.birthday_person.bio_elements.items():
            print(
                f"{self.birthday_person.name} was {bio_element['age']} years old at {year}. {bio_element['content']['content']}"
            )

    def make_wish(self):
        for member in self.family_members:
            print(f"{member.greeting} {self.birthday_person.name}!")

    def birthday_message(self):
        print(f"{self.birthday_person.greeting} {self.birthday_person.name}!")

    def recursive_birthday_greeting(self):
        print(f"Happy Birthday {self.birthday_person.name}!")

    def personalized_greeting(self, name):
        for member in self.family_members:
            if member.name == name:
                print(
                    f"{member.name}, who is the {member.relationship} of {self.birthday_person.name}, is greeting you with: {member.greeting}"
                )
                return
        print(f"No greeting found for {name}.")


def parse_args():
    parser = argparse.ArgumentParser(description="Family Birthday Card Program")
    parser.add_argument(
        "action",
        choices=["rami", "wishes", "greeting", "bio"],
        help="Choose the action to perform",
    )
    parser.add_argument("--year", type=int, help="Specify the year for bio information")
    parser.add_argument("--all", action="store_true", help="Show bio for all years")
    parser.add_argument(
        "--name", help="Specify the name for personalized greeting or bio"
    )
    parser.add_argument(
            "--version", action="version", version=f"%(prog)s {__version__}"
            )
    return parser.parse_args()


def print_with_emoji(data, emoji):
    print(f"{emoji} {data}")


def print_birthday_person_data(birthday_person):
    emojis = ["<F0><9F><8E><89>", "<F0><9F><8E><82>", "<F0><9F><8E><8A>", "<F0><9F><92><96>"]

    for prop, value in birthday_person.__dict__.items():
        print_with_emoji(f"{prop.capitalize()}: {value}", random.choice(emojis))

    # Print bio elements
    for year, bio_element in birthday_person.get("bio_elements", {}).items():
        print_with_emoji(
            f"Year {year} Bio: {bio_element['content']}", random.choice(emojis)
        )


def main():
    args = parse_args()

    # Read family configuration
    family_config_data = FamilyConfig.read_family_config("family_data.json")

    if args.action == "rami":
        # Print only the birthday person's data
        print_birthday_person_data(family_config_data["birthday_person"])
    else:
        # Initialize birthday person object dynamically
        birth_year = family_config_data["birthday_person"]["birth_year"]

        birthday_person = Person(
            name=family_config_data["birthday_person"]["name"], birth_year=birth_year
        )

        for prop, value in family_config_data["birthday_person"].items():
            if prop not in ["name", "birth_year", "bio_elements"]:
                setattr(birthday_person, prop, value)

        # Set bio elements
        birthday_person.bio_elements = {
            str(year): {
                "content": content,
                "age": int(year) - birth_year,
            }
            for year, content in family_config_data["birthday_person"]
            .get("bio_elements", {})
            .items()
        }

        # Initialize family members
        family_members = [
            FamilyMember(
                name=member["name"],
                greeting=member["greeting"],
                relationship=member["relationship"],
            )
            for member in family_config_data["family_members"]
        ]

        family_birthday_card = FamilyBirthdayCard(birthday_person, family_members)

        # Perform the chosen action
        if args.action == "bio":
            if args.all:
                family_birthday_card.show_bio_for_all_years()
            elif args.year:
                family_birthday_card.show_bio_for_year(args.year)
            else:
                print("Please provide a year using the --year parameter.")
        elif args.action == "wishes":
            family_birthday_card.make_wish()
        elif args.action == "greeting":
            if args.name:
                family_birthday_card.personalized_greeting(args.name)
            elif args.all:
                print("List of family members with greetings:")
                for member in family_members:
                    print(member.name)
            else:
                family_birthday_card.birthday_message()
                family_birthday_card.recursive_birthday_greeting()


if __name__ == "__main__":
    main()
