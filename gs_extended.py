import copy
def gs_extended(mpref, wpref, n):
    curr_match_count = 0
    men_matchings = [-1 for i in range(n)]
    women_matchings = [-1 for i in range(n)]
    mpref_red = copy.deepcopy(mpref)
    wpref_red =copy.deepcopy(wpref)
    # continue until all matches made
    while curr_match_count < n:
        for man in range(n):
            # if man is single
            if men_matchings[man] == -1:
                # get first woman from man's REDUCED preference list
                woman = mpref_red[man][0]
                print(man, woman)

                # if a woman is with someone, assign that man to be free
                if women_matchings[woman] > -1:
                    # create match (man, woman)
                    abandoned_man = women_matchings[woman]
                    men_matchings[abandoned_man] = -1 # assign abandoned man to be free
                    men_matchings[man] = woman #match man and woman together
                    women_matchings[woman] = man
                    man_rank = wpref[woman].index(man)
                    for i in range(man_rank + 1, len(wpref[woman])):
                        successor = wpref[woman][i]
                        wpref_red[woman].remove(successor)
                        mpref_red[successor].remove(woman)
                    # curr_match_count == curr_match_count the number of pairs stays the same

                #
                else:
                    men_matchings[man] = woman  # match man and woman together
                    women_matchings[woman] = man
                    man_rank = wpref[woman].index(man)
                    for i in range(man_rank + 1, len(wpref[woman])):
                        successor = wpref[woman][i]
                        wpref_red[woman].remove(successor)
                        mpref_red[successor].remove(woman)
                    curr_match_count += 1 #the number of pairs stays the same

    return men_matchings, mpref_red, wpref_red
