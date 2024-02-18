import difflib

from pymongo_get_database import get_database


def main():
    db = get_database()
    betsByDate = db["betsByDate"]
    betsByName = db["betsByName"]

    docData = betsByDate.find({})
    for rowBet in docData:
        print("------------- " + rowBet["timestamp"] + " ---------------")
        betBookieName_dic = getBetsByTeamName(rowBet)
        match_dic = groupBetsByTeamMatch(betBookieName_dic)
        print(match_dic)
        bet_dic = {"timestamp": rowBet["timestamp"], "bets": match_dic}
        betsByName.insert_one(bet_dic)


def getBetsByTeamName(n):
    betBookieName_dic = {}
    for bet in n["bets"]:
        key = bet["bookie"]

        if not key in betBookieName_dic:
            betBookieName_dic[key] = {}

        index = bet["teamA"]["name"] + " vs " + bet["teamB"]["name"]

        betBookieName_dic[key][index] = bet
    return betBookieName_dic


def getClosestMatchComparison(matchX, matchY):
    # print("matchX: " + matchX + " matchY: " + matchY)
    matchListX = matchX.split(" vs ")
    matchListY = matchY.split(" vs ")

    # comparation by team name in the match: A B = C D
    # A C -> A D
    # B C -> B D

    closest_matches = [
        difflib.get_close_matches(matchX, matchListY) for matchX in matchListX
    ]
    return closest_matches


def groupBetsByTeamMatch(n):
    bookie_stop_dic = {}
    match_stop_dic = {}
    match_dic = {}
    for bookieX in n.keys():
        for matchX in n[bookieX].keys():
            for bookieY in n.keys():
                if bookieY == bookieX or bookieY in bookie_stop_dic:
                    continue
                if not bookieY in match_stop_dic:
                    match_stop_dic[bookieY] = {}
                for matchY in n[bookieY].keys():
                    if matchY in match_stop_dic[bookieY]:
                        continue
                    # print("bookieX: " + bookieX + " bookieY: " + bookieY)
                    closest_matches = getClosestMatchComparison(matchX, matchY)

                    if len(closest_matches) > 0 and len(closest_matches[0]) > 0:
                        if not matchX in match_dic:
                            match_dic[matchX] = {}
                            match_dic[matchX][bookieX] = n[bookieX][matchX]

                        match_dic[matchX][bookieY] = n[bookieY][matchY]

                        # stop cycling matchY
                        match_stop_dic[bookieY][matchY] = 1

        # stop cycling bookieX
        bookie_stop_dic[bookieX] = 1
    return match_dic


if __name__ == "__main__":
    main()
