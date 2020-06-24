import numpy as np
from anilist_api.anilist import get_users_scores

L1 = get_users_scores("octavius928")
L2 = get_users_scores("NamesAreRubbish")

overlap = {}

for anime in L1:
    try:
        overlap[anime] = (L1[anime], L2[anime])
    except KeyError:
        next

dot_product = 0
n1 = 0
n2 = 0

for anime in overlap:
    dot_product += overlap[anime][0]*overlap[anime][1]
    n1 += overlap[anime][0]**2
    n2 += overlap[anime][1]**2

cos_sim = dot_product / (np.sqrt(n1)*np.sqrt(n2))
print("Cosine similarity:")
print(cos_sim)
mal = 10*(cos_sim-0.9)
print("Something dumb that looks like MAL affinity:")
print(mal)
