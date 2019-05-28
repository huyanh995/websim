import random

group = ['market', 'sector', 'industry', 'subindustry']


def get_alphas(data):
    data_mod = [""] + data
    id = random.choice([0, 2, 2, 2, 4])
    alphas = []
    pattern = [
        "group_neutralize(rank( {} / {} ), {},constantCheck=False, tolerance=0.01, scale=1)",
        "group_neutralize(group_rank(( {} / {}), {}, ignoreNanInput=False), {}, constantCheck=False, tolerance=0.01, scale=1)",

        "group_neutralize(rank( ({} - {}) / {} ), {}, constantCheck=False, tolerance=0.01, scale=1)",
        "group_neutralize(group_rank(( ({} - {}) / {}), {}, ignoreNanInput=False), {}, constantCheck=False, tolerance=0.01, scale=1)",

        "group_neutralize(rank( ({} + {}) / {} ), {})",
        "group_neutralize(group_rank(( ({} + {}) / {}), {}, ignoreNanInput=False), {}, constantCheck=False, tolerance=0.01, scale=1)",
    ]

    chosen_ids = random.sample(range(0, len(data_mod)), 3)
    rnd_data1 = data_mod[chosen_ids[0]]
    rnd_data2 = data_mod[chosen_ids[1]]
    rnd_data3 = data_mod[chosen_ids[2]]
    rnd_group = random.choice(group)

    for rndGroupNeutralize in group:
        if id % 2 == 1:
            if id <= 1:
                alpha = pattern[id].format(rnd_data1, rnd_data2, rnd_group, rndGroupNeutralize)
            else:
                alpha = pattern[id].format(rnd_data1, rnd_data2, rnd_data3, rnd_group, rndGroupNeutralize)

        else:
            if id <= 1:
                alpha = pattern[id].format(rnd_data1, rnd_data2, rndGroupNeutralize)
            else:
                alpha = pattern[id].format(rnd_data1, rnd_data2, rnd_data3, rndGroupNeutralize)

        alphas.append(alpha)

    return alphas
