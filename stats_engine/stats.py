import numpy as np


def get_overlap(user_one_data, user_two_data):
    overlap = {}

    print(len(user_one_data.keys()))
    print(len(user_two_data.keys()))

    if len(user_one_data.keys()) > len(user_two_data.keys()):
        longest_list = user_one_data
    else:
        longest_list = user_two_data

    for anime in longest_list:
        try:
            overlap[anime] = (user_one_data[anime], user_two_data[anime])
        except KeyError:
            next

    print(len(overlap.keys()))

    return overlap


def calculate_cosine_similarity(overlap):
    dot_product = 0
    n_one = 0
    n_two = 0

    for anime in overlap:
        dot_product += overlap[anime][0] * overlap[anime][1]
        n_one += overlap[anime][0] ** 2
        n_two += overlap[anime][1] ** 2

    return dot_product / (np.sqrt(n_one) * np.sqrt(n_two))


def calculate_affinity(user_one_data, user_two_data):
    overlap = get_overlap(user_one_data, user_two_data)

    output_affinity = []

    # Cosine Similarity
    cosine_similarity = calculate_cosine_similarity(overlap)
    output_affinity.append(('Cosine Similarity', cosine_similarity))

    # Faux MAL
    output_affinity.append(('Faux MAL', 10 * (cosine_similarity - 0.9)))

    return output_affinity
