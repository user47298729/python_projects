import csv
from sys import exit as sysexit
import project


def expenses(label="name", backwards="t", show="~", showlabel="name", currency="€") -> list:
    """Returns the expenses of the file filename after filtering it
    through the filter in the parameters

    Args:
        file_ (str): which file?
        label (str, optional): Which label do you want to use to sort. Defaults to "date".
        backwards (str, optional): Sort it backwards or not (t/f). Defaults to "t".
        show (str, optional): Only show specified entries
        ~str: Is str in the value of entrie[showlabel]
        e~str: Does value of entrie[showlabel] end with str
        s~str: Same like e~str just instead of end it is start
        . Defaults to None.
        showlabel (str, optional): show will be filtered in this label. Defaults to "name".
        currency (str, optional): which currency do you want to display. Defaults to "€".

    Returns:
        list: Returns all of the expenses in filename after filtering it through the filters
    """

    entries = list()

    # Appends all of the entries as a dictionary per entrie to the list entries
    with open(f"csvs/expenses.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            entries.append({"date": row["date"], "price": float(row["price"]), "name": row["name"].title(), "place": row["place"], "method": row["method"].title()})

    return sort(entries, label, backwards, show, showlabel, currency)


def sort(list_: list, label: str, backwards: str, show: str, showlabel: str, currency: str) -> list:
    """Expects a list with dictionarys inside of it
    and then filters those through the specified filters

    Returns:
        list_: returns the filtered version of "list"
    """
    sorted_entries = list()

    if backwards == "f":
        backwards = False
    else:
        backwards = True

    # Only shows entries that are supossed to be shown
    if show != "~":
        cutted_entries = cut(list_, show, showlabel)

    else:
        cutted_entries = list_

    # Sorts the entries
    for entrie in sorted(cutted_entries, key = lambda entrie: entrie[label], reverse = backwards):
        # Date and price are brought into "normal" form here so that the programm can use them before as a filter
        y, m, d = entrie["date"].split("-")
        entrie["date"] = f"{d}/{m}/{y}"

        price = project.convert(str(entrie["price"]) + currency)
        entrie["price"] = "{:,.2f}".format(price) + project.symbol(currency)
        entrie["place"] = entrie["place"] if project.website(entrie["place"]) else entrie["place"].title()

        sorted_entries.append(entrie)

    return sorted_entries


def cut(list_: list, show: str, showlabel: str) -> list:
    """Gets a dictionary and two strs.
    It will only return the values that fit show in the label showlabel

    Returns:
        list: Returns "list_" but only with the values that fit the filters
    """
    cutted_entries = list()

    for entrie in list_:
        # e~... means that the entrie should end with the ...
        if show.startswith("e~"):
            checks = show.lstrip("e").lstrip("~").split("/")

            for check in checks:
                value_to_check = str(entrie[showlabel])
                if value_to_check.endswith(check):
                    cutted_entries.append(entrie)
                    break


        # e~... means that the entrie should start with the ...
        elif show.startswith("s~"):
            checks = show.lstrip("s").lstrip("~").split("/")

            for check in checks:
                value_to_check = str(entrie[showlabel])
                if value_to_check.startswith(check):
                    cutted_entries.append(entrie)
                    break


        # ~... means that ... should be in the entrie
        elif show.startswith("~"):
            checks = show.lstrip("~").split("/")

            for check in checks:
                value_to_check = str(entrie[showlabel])
                if check in value_to_check:
                    cutted_entries.append(entrie)
                    break

        # If there isn't a ~, it means that the entrie should be exactly show
        else:
            checks = show.split("/")

            for check in checks:
                value_to_check = str(entrie[showlabel])
                if check == value_to_check:
                    cutted_entries.append(entrie)
                    break

    if len(cutted_entries) == 0:
        sysexit("There isn't an entry matching your filter")

    return cutted_entries


def accounts(cur="€") -> list:
    """
    Same like expenses just with balance
    """

    accounts_ = list()

    # Appends all of the entries as a dictionary per entrie to the list entries
    with open(f"csvs/balance.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            accounts_.append({"name": row["name"], "balance": f"{round(project.convert(row['balance'] + cur), 2):,.2f}{project.symbol(cur)}"})

    return accounts_
