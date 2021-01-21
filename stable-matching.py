# Given a list of men and women, as well as their preference lists of the opposite gender, return a list of stable matchings.

# Time complexity: O(n^2)

# initialize equally sized lists of men and women

men = {'Alex', 'Ben', 'Carter', 'Daniel', 'Ethan', 'Francisco', 'Gabriel', 'Henry', 
       'Isaac', 'Jacob', 'Kevin', 'Liam', 'Mason', 'Noah', 'Oliver', 'Parker', 'Quinn',
       'Ryan', 'Samuel', 'Thomas'}
women = {'Ava', 'Brooklyn', 'Charlotte', 'Delilah', 'Emma', 'Faith', 'Grace', 'Harper', 
        'Isabella', 'Julia', 'Kaylee', 'Lillian', 'Mia', 'Natalie', 'Olivia', 'Penelope', 'Quinn',
        'Riley', 'Sophia', 'Taylor'}
men_list = list(men)
women_list = list(women)

# randomly generate preference lists for each man and woman

import random

men_pref = dict()
women_pref = dict()

for m in men:
    men_pref[m] = random.sample(women_list, len(women_list))
for w in women:
    women_pref[w] = random.sample(men_list, len(men_list))

# Gale-Shapley Algorithm

def gale_shapley(men=men, women=women, men_pref=men_pref, women_pref=women_pref):
    
    hasnt_proposed = dict(zip([m for m in men], [women for w in women])) # set of women that a man hasn't proposed to
    some_man_hasnt_proposed_to_all_woman = True # loop stop condition
    fiances = dict(zip([w for w in women], [None for m in men])) # engaged woman-man mappings for fast query
    engaged_pairs = set() # engaged pairs as tuples

    # While there is a man m who is free and hasn’t proposed to every woman
    while len(men) > 0 and some_man_hasnt_proposed_to_all_woman:
        m = men.pop() # Consider a free man m
        w = None # Let w be the highest-ranked woman in m’s preference list to which m has not yet proposed
        for wo in men_pref[m]:
            if wo in hasnt_proposed[m]:
                w = wo
                hasnt_proposed[m].remove(w) # mark the w as visited by removing her from m's to-propose list
                break
        if fiances[w] == None: # If w is free then
            engaged_pairs.add((m, w)) # (m,w) become engaged
            fiances[w] = m
        else: # w is currently engaged to m’
            mp = fiances[w]
            if women_pref[w].index(mp) < women_pref[w].index(m): # If w prefers m’ to m then
                men.add(m) # m remains free
            else: # Else w prefers m to m’
                engaged_pairs.remove((mp, w))
                men.add(mp) # m' becomes free
                engaged_pairs.add((m, w)) # (m,w) become engaged
                fiances[w] = m
        if sum([len(hasnt_proposed[m]) for m in hasnt_proposed]) == 0:
            some_man_hasnt_proposed_to_all_woman = False

    return engaged_pairs

gale_shapley()