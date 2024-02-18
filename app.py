from pymongo_get_database import get_database


def main():
    db = get_database()
    betsByName = db["betsByName"]

    docData = betsByName.find({})
    for rowBet in docData:
        print(rowBet)


if __name__ == "__main__":
    main()
