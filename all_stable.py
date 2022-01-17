import numpy as np


def find_all_stable(malechoice, femalechoice, n):
    # Output list with all matchings
    res = []
    # Initialization
    unchanged = [True] * n
    marriage = [0] * n
    malecounter = [0] * n
    # Female choice transformation

    fc = np.zeros((n, n), dtype=int)
    for i in range(1, n):
        for j in range(0, n - 1):
            fc[i][femalechoice[i][j]] = j
        fc[i][0] = n
        malecounter[i] = 0
        marriage[i] = 0

    def get_marriage(marriage):
        malematches = [0] * (n - 1)
        for j in range(1, n):
            malematches[marriage[j] - 1] = j
        return(malematches)

    def print_marriage(marriage):
        malematches = [0] * (n - 1)
        for j in range(1, n):
            malematches[marriage[j] - 1] = j
        print(*malematches)

    def proposal(i, malec, marriage, c):
        if i < 0:
            success = True
        elif (i == 0) or malec[i] == (n - 1) or not (unchanged[i]):  # n not (n+1), as we have n equals 5
            success = False
        else:
            c += 1
            j = malec[i]
            malec[i] = j + 1
            success = refusal(i, malechoice[i][j], malec, marriage, c)
        return success

    def refusal(i, j, malec, marriage, c):
        if fc[j][abs(marriage[j])] > fc[j][i]:
            k = marriage[j]
            marriage[j] = i
            success = proposal(k, malec, marriage, c)
        else:
            success = proposal(i, malec, marriage, c)
        return success

    def breakmariage(malecounter, marriage, i, n, count):
        malecounter_ori = malecounter.copy()
        marriage_ori = marriage.copy()
        marriage[malechoice[i][malecounter[i] - 1]] = -i
        success = proposal(i, malecounter, marriage, count)

        if not (success):
            unchanged[i] = False
            malecounter_ref = malecounter_ori.copy()
            marriage_ref = marriage_ori.copy()
            malecounter = malecounter_ref
            marriage = marriage_ref
            return malecounter, marriage

        #print_marriage(marriage)  # marriage[i] means the woman who is married to i man
        new_marriage = get_marriage(marriage)  # convert into female solution
        res.append(new_marriage)
        # establish the relationships between the original and the obtained stable matching

        for j in range(i, n):
            # if i==2 and j==2:
            #     print("This is it")
            malecounter, marriage = breakmariage(malecounter, marriage, j, n, count)

        for j in range((i + 1), n):
            unchanged[j] = True
        # return malecounter_ori, abs(marriage_ori)
        return malecounter_ori, marriage_ori

    count = 0
    for i in range(1, n):
        proposal(i, malecounter, marriage, count)
    #print_marriage(marriage)

    new_marriage = get_marriage(marriage)  # convert into female solution
    res.append(new_marriage)
    # establish the relationships between the original and the obtained stable matching

    M_optimal_marriage = marriage.copy()
    M_optimal_counter = malecounter.copy()
    for i in range(1, n - 1):
        breakmariage(M_optimal_counter.copy(), M_optimal_marriage.copy(), i, n, count)
    return res
