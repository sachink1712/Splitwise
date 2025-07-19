# Splitwise self code
class SplitWise:
    def __init__(self):
        self.names = []
        self.expenses = {}
        self.split = {}

    # Getting the names
    def get_people(self, name_list):
        self.names = [name.lower() for name in name_list]

    # Expenses occurred
    def get_expense(self, amount, people):
        people = [person.lower() for person in people if person.lower() in self.names]

        if amount in self.expenses:
            self.expenses[amount] += people
        else:
            self.expenses[amount] = people

    # Split calculation
    def split_calculation(self):
        for amount, name in self.expenses.items():
            split = amount/len(name)
            for each_name in name:
                if each_name in self.split.keys():
                    self.split[each_name] += split
                else:
                    self.split[each_name] = split
        return self.split

    # Run the scripts
    def run(self):
        self.get_people(['sachin','kumar'])
        self.get_expense()
        return self.split_calculation()


if __name__ == "__main__":
    SplitWise = SplitWise()
    split = SplitWise.run()
    print(split)
