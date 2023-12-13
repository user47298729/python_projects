import csv
import project
from sys import exit as sysexit
from datetime import date


def w_transfer(t):
    for _ in range(t):
        amount = project.convert(input("How much: "))
        from_ = input("From: ")
        to = input("To: ")
        check_method(from_, amount)
        check_method(to, -amount)



def writeto(filename: str, dict_: dict) -> bool:
    with open(filename, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[key for key in dict_])
        writer.writerow(dict_)

    #Exit code
    return True


def w_balance(t=1, name=None) -> bool:
    """
    Write a new payment method to balance.csv
    """

    for _ in range(t):
        if not name:
            name = input("Name of payment method: ").lower()

        with open("csvs/balance.csv", "r") as file:
            reader = csv.DictReader(file)
            names = [row["name"] for row in reader]

        if name in names:
            sysexit("The payment method already exists")

        writeto("csvs/balance.csv", {"name": name, "balance": project.convert(input(f"Balance of {name}: "), False)})

    return True


def w_expenses(t: int) -> bool:
    """
    Write a new expense to expenses.csv
    """
    for _ in range(t):
        entrie: dict = new_entry()
        writeto("csvs/expenses.csv", entrie)


def new_entry():
    """Gets a new expense (entry) and returns it.
    The expense contains a name,price,date,place where you bought it and a payment method (x)

    Returns:
        dict: Returns a dictionary with this structure {name of x: value of x}
    """
    try:
        name = input("Name: ")
        price: float = project.convert(input("Price: "), False)
        input_date = get_date()
        place = input("Place: ")
        method = input("Payment method: ")

        is_sure = input(f'Is this right: "{name}, {price}€, {input_date}, {place}, {method}" [y]: ')

    except KeyboardInterrupt:
        sysexit("\n\nExited programm via Ctrl+C")

    print()
    if is_sure.lower() == "y":
        return {
            "name": name,
            "price": price,
            "date": input_date,
            "place": place,
            "method": check_method(method, price)
        }

    # If the user wants to redo it
    return new_entry()


def check_method(method: str, price=0) -> str:
    """Checks if the payment method exists and if it does,
    it removes price amount of money from it. If it doesn't it will ask the user to create a new one and
    enter the balance
    NOTE: It won't subsct price from a new created account so enter the balance of the account after the expense

    Args:
        method (str): the payment method
        price (str, optional): the programm will remove this much money from the account. Defaults to 0.

    Returns:
        str: Just returns the method name again, it's so that you can access it in a variable
    """
    with open("csvs/balance.csv", "r") as file:
        reader = csv.DictReader(file)
        if method.lower() not in [row["name"].lower() for row in reader]:
            print("As the payment method you entered does not exist, it will be added! Press CTRL+C to exit")
            w_balance(1, method)

        else:
            change_balance(method, price)

    return method


def change_balance(method: str, price: float) -> bool:
    """Changes the balance of an account

    Args:
        method (str): The payment method
        price (float): The amount of money, you want to substract from the account (If it is negative, it will be added)
    """
    accounts_ = []

    with open(f"csvs/balance.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            accounts_.append({"name": row["name"], "balance": row["balance"]})

    with open("csvs/balance.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "balance"])
        file.write("name,balance\n")
        for account in accounts_:
            if account["name"] == method:
                new_balance = float(account["balance"]) - price
                if new_balance < 0:
                    print("Attention! Your account is in debt")
                writer.writerow({"name": account["name"], "balance": new_balance})
            else:
                writer.writerow({"name": account["name"], "balance": account["balance"]})

    return True


def get_date() -> str or date:
    """Gets a date from the user but in a specified way.
    If the user only inputs one value, it will just take the actual date and only change the day.
    Same with two values, it will just change the day and month.
    If the user just skips the input, it returns the actual date

    Returns:
        str: Returns a date as a str in the format y-m-d
    """

    input_date = input(f"Date: ")
    heute = date.today()

    if input_date == "":
        return heute

    y, m, d = str(heute).split("-")

    input_array = input_date.split("/")

    # If only one value was entered (day)
    if len(input_array) == 1:
        d = input_date

    # If two values were entered (day and month)
    elif len(input_array) == 2:
        d = input_array[0]
        m = input_array[1]

    # If all values were entered
    elif len(input_array) == 3:
        d, m, y = input_array

    else:
        sysexit("Invalid date")

    if project.validate_date(f"{y}-{int(m):02d}-{int(d):02d}"):
        return f"{y}-{int(m):02d}-{int(d):02d}"

    # If the given date is invalid, exit the programm
    sysexit("Invalid date")
