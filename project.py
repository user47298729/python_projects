import argparse
from sys import exit as sysexit
from datetime import date
import do
import reads
from tabulate import tabulate
from re import search


def main():
    v = read_args()
    type_ = v["type"].lower()

    try:
        if type_ == "w":
            do.w_expenses(v["times"])

        elif type_ == "br":
            accounts = reads.accounts(v["currency"])
            total_ = total(accounts, "balance", v["currency"])
            print(tabulate(accounts, headers ="keys", tablefmt="rounded_grid"))
            print("Total:", total_)

        elif type_ == "bw":
            do.w_balance(v["times"])

        elif type_ == "t":
            do.w_transfer(v["times"])

        else:
            expenses = reads.expenses(v["label"], v["reversed"], v["show"], v["show_label"], v["currency"])
            total_ = total(expenses, "price", v["currency"])
            print(tabulate(expenses, headers ="keys", tablefmt="rounded_grid"))
            print("Total:", total_)
    #If the user entered a wrong sorting label
    except KeyError:
        sysexit(f"Invalid label {v['label']}")


def total(list_: list, key: str, cur: str) -> str:
    """Calculates the total of all values

    Args:
        list_ (list): A list with similar dictionaries inside (only the values are different, the keys are the same)
        key (str): Which value of the dics do you want to add together
        cur (str): In which currency do you want it outputted

    Returns:
        str: Returns the total rounded to two decimal points + the currency symbol
    """
    sum_ = 0
    for dict_ in list_:
        try:
            add = convert(str(dict_[key])+cur, True)
            sum_ += float(add)
        except ValueError:
            sysexit(f"Error: not all values of {key} are floats + currency")

    return f"{round(sum_, 2):,.2f}{symbol(cur)}"


def symbol(cur: str, reverse=False) -> str:
    """
    Gives back the currencycode as a symbol
    but if reverse, it gives back the symbol as a currencycode
    """
    codes = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "AUD": "A$",
    "CAD": "C$",
    "CHF": "Fr",
    "CNY": "¥",
    "INR": "₹",
    "MXN": "Mex$",
    "RUB": "₽",
    "": "€"
    }
    for code in codes:
        if reverse:
            if cur.upper() == codes[code]:
                return code.lower()
        else:
            if cur.upper() == code:
                return codes[code]

    return cur


def validate_date(date_: str) -> bool:
    """Just validates the date

    Args:
        date_ (str): The date, that is hopefully in this format (YYYY-MM-DD)

    Returns:
        bool: True if it is a valid date, False when it isn't
    """
    try:
        date.fromisoformat(date_)
        return True
    except ValueError:
        return False


def convert(money: str or float, to=True) -> float:
    """Gets money and returns it as euro

    Args:
        money (str): The money you want to convert into euro
        to (bool): convert the currency to euro or euro to the currency
    Returns:
        converted (float): Returns your money in euros
    """
    # I did not use as an API as I could've only had a specific amount of requests
    converted = 0
    currencies = {"€": 1, "$": 1.06, "£": .87, "usd": 1.06, "gbp": 0.87, "eur": 1, "jpy": 157.88, "aud": 1.64, "cad": 1.44, "chf": .97,
    "cny": 7.7, "inr": 87.92, "mxn": 18.4, "rub": 103.564, "": 1}
    money = money.replace(",","")

    for c in currencies:
        if str(money).lower().endswith(c):
            converted = money.rstrip(symbol(c, False)+symbol(c, True))
            currencie = c
            break

    try:
        if not to:
            converted = float(converted) * (1 /currencies[currencie])
        else:
            converted = float(converted) * currencies[currencie]
    except ValueError:
        sysexit(f"ValueError: {money} isn't a float")

    return round(converted, 2)


def read_args() -> dict:
    """reads out the command lines argument
    and checks whether they are useful or not

    Returns:
        dict: Returns a dictionary with values from the command line. If they weren't given in the command line, it uses default values
    """
    parser = argparse.ArgumentParser(description="cmd based expense tracker. Use the cmd line args to specify what you want to do and show")

    possible_args = {
        # arg name: [description, default_value]
        "-type": ["read or write (w)? Balance read or write (bw, br)", "r"],
        "-times": ["How many expenses do you want to add", 1],
        "-lab": ["The label you use to filter the output", "name"],
        "-rev": ["Defines whether you want to show the filtered expenses in reverse (t for True and f for False)", "f"],
        "-show": ["Only show expenses that fit this filter (-s = show)", "~"],
        "-slab": ["Only show expenses that fit the filter -s filter but only in the specified label", "name"],
        "-cur": ["Which currency are the outputted expenses supossed to be", "€"],
    }

    for arg in possible_args:
        default_value = possible_args[arg][1]
        parser.add_argument(arg, default=default_value, help=possible_args[arg][0], type=type(default_value))

    args = parser.parse_args()

    # w = write bw = balance write and t = transfer
    if args.type == "w" or args.type == "bw" or args.type == "t":
        return {"type": args.type, "times": args.times}

    elif args.type == "br" or args.type == "r":
        return {
            "type": args.type,
            "label": args.lab,
            "reversed": args.rev,
            "show": args.show,
            "show_label": args.slab,
            "currency": args.cur
        }

    else:
        sysexit("Invalid args")


def website(word: str) -> bool:
    """Website or not?

    Args:
        word (str): The programm will check whether this is a website or not

    Returns:
        bool: True if website else False
    """
    word = word.lower()
    if search(r"(http(s)?://)?([\w*]+\.)+[\w*]+(/[\w*s ;,./?%&=]*)?", word):
        return True
    else:
        return False


if __name__ == "__main__":
    main()
