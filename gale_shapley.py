import copy
def gale_shapley(mpref, wpref, n, F):
    ### returns men's matchings or proposers' matchings i.e. men_matchings[i] is a partner of proposer i
    curr_match_count = 0
    last_rejected_by_rank_what = [0 for i in range(n)]
    men_matchings = [0 for i in range(n)]
    women_matchings = [0 for i in range(n)]

    # continue until all matches made
    while curr_match_count < n:
        for man in range(n):
            # if man is single
            if men_matchings[man] == 0:
                # get first non-rejecting woman from man's preference list
                woman = mpref[man][last_rejected_by_rank_what[man]] - 1
                # both man and woman are single
                if women_matchings[woman] == 0:
                    # create match (man, woman)
                    men_matchings[man] = woman + 1
                    women_matchings[woman] = man + 1
                    curr_match_count += 1

                # woman is with someone
                else:
                    # find ranks of curr_partner and man given woman's preference list
                    curr_partner = women_matchings[woman]
                    curr_partner_rank = wpref[woman].index(curr_partner)
                    man_rank = wpref[woman].index(man + 1)

                    # woman prefers curr_partner over man
                    if curr_partner_rank < man_rank:
                        last_rejected_by_rank_what[man] = mpref[man].index(woman + 1) + 1

                    # woman prefers man over curr_partner
                    else:
                        men_matchings[curr_partner - 1] = 0
                        last_rejected_by_rank_what[curr_partner - 1] = mpref[curr_partner - 1].index(woman + 1) + 1
                        men_matchings[man] = woman + 1
                        women_matchings[woman] = man + 1
    if F:
        men_matchings = women_matchings
    for x in range(n):
        men_matchings[x] -= 1
    return men_matchings

def get_reduced(mpref, wpref, matches, n):
    # matches is an output of GS, ie. a vector of proposers' partners
    mpref_red = copy.deepcopy(mpref)
    wpref_red =copy.deepcopy(wpref)
    for i in range(n):
        woman = i
        man = matches.index(woman)
        man_rank = wpref[woman].index(man)
        for i in range(man_rank + 1, len(wpref[woman])):
            successor = wpref[woman][i]
            wpref_red[woman].remove(successor)
            # print("removing {0} from {1} list".format(woman, successor))
            mpref_red[successor].remove(woman)
    return mpref_red, wpref_red
