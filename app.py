from pymongo_get_database import get_database

default_bet = 50


def main():
    db = get_database()
    betsByName = db["betsByName"]

    docData = betsByName.find({})
    for rowData in docData:
        print("------------- " + rowData["timestamp"] + " ---------------")
        getBetsResults(rowData)


def getBetsResults(rowData):
    for rowBet in rowData["bets"].values():
        for rowBookie in rowBet.values():
            odds_list = [
                rowBookie["teamA"]["payOffPercent"],
                rowBookie["teamB"]["payOffPercent"],
                rowBookie["payOffDraw"],
            ]
            # min in the list has the best positive EV chances
            to_win = min(odds_list)
            odds_list.remove(to_win)

            odds_win = getProbability(to_win)
            odds_lose = sum(map(getProbability, odds_list))

            print(rowBookie)
            print(
                "("
                + str(getAmountWonPerBet(default_bet, to_win))
                + "*"
                + str(odds_win)
                + ")-("
                + str(default_bet)
                + "*"
                + str(odds_lose)
                + ")"
            )

            result = (getAmountWonPerBet(default_bet, to_win) * odds_win) - (
                default_bet * odds_lose
            )
            print(result)


def getProbability(decimalOdd):
    return 1 / decimalOdd


def getAmountWonPerBet(amountBet, winPayOff):
    return (amountBet * winPayOff) - amountBet


if __name__ == "__main__":
    main()
