

def get_unique_items(big_set):
    items_set = set()
    for items in big_set:
        for item in items:
            items_set.update({item})
    return [{x} for x in items_set]


def brute_force(trans_set_list, min_supp_count):
    combinations = get_unique_items(trans_set_list)
    freq_counts = []
    freq_subsets = []
    done = False
    k = 1

    while not done:
        size = len(freq_counts)
        candidates = permute(combinations, k)
        counts = gen_support_count(candidates, trans_set_list)
        for idx in counts.keys():
            if counts[idx] >= min_supp_count:
                freq_counts.append(counts[idx])
                freq_subsets.append(candidates[idx])
        if size == len(freq_counts):
            break
        k = k + 1
    return [*zip(freq_subsets, freq_counts)]


def apriori(trans_set_list, min_supp_count):
    combinations = get_unique_items(trans_set_list)
    combinations.sort(key=sorted)
    candidates = permute(combinations, 1)
    counts = gen_support_count(candidates, trans_set_list)
    freq_idx = [*filter(lambda x: counts[x] >= min_supp_count, counts)]
    freq_counts = [counts[x] for x in freq_idx]
    freq_subsets = [candidates[i] for i in freq_idx]
    candidates = freq_subsets.copy()
    done = False
    k = 2

    while not done:
        candidates.sort(key=sorted)
        candidates = permute(candidates, k)
        candidates = prune(candidates, freq_subsets)
        counts = gen_support_count(candidates, trans_set_list)
        freq_idx = [*filter(lambda x: counts[x] >= min_supp_count, counts)]
        candidates = [candidates[i] for i in freq_idx]
        for i in freq_idx:
            freq_counts.append(counts[i])
        if len(candidates) == 0:
            break
        for candidate in candidates:
            freq_subsets.append(candidate)
        k = k + 1
    return [*zip(freq_subsets, freq_counts)]


def permute(trans_set_list, size):
    def generate_permutations(current, start):
        if len(current) == size:
            unique_perm.append(current.copy())
            return

        for i in range(start, len(trans_set_list)):
            current_set = trans_set_list[i]
            if i == start or not current_set & current:
                current.update(current_set)
                generate_permutations(current, i + 1)
                current.difference_update(current_set)

    if size > len(trans_set_list) or size <= 0:
        return []

    unique_perm = []
    generate_permutations(set(), 0)

    return unique_perm

# def permute(trans_set_list, size):
#     def generate_permutations(current, start):
#         if len(current) == size:
#             unique_perm.append(current.copy())
#             return
#
#         for i in range(start, len(trans_set_list)):
#             current_set = trans_set_list[i]
#             current = current.union(current_set)
#             generate_permutations(current, i + 1)
#             current.pop()
#
#     if size > len(trans_set_list) or size <= 0:
#         return []
#
#     unique_perm = []
#     generate_permutations(set(), 0)
#
#     return unique_perm


def prune(candidates, freq_subsets):
    pruned_candidates = []
    for candidate in candidates:
        valid = True
        for item in candidate:
            subset = candidate - {item}
            if subset not in freq_subsets:
                valid = False
                break
        if valid:
            pruned_candidates.append(candidate)
    return pruned_candidates


def gen_support_count(combinations, db):
    counts = {}
    for idx, combination in enumerate(combinations):
        count = sum(combination.issubset(set(x)) for x in db)
        counts[idx] = count
    return counts


def generate_association_rules(zipped_counts, min_confidence, total_transactions):
    association_rules = []

    for subset, counts in zipped_counts:
        if len(subset) > 1:
            for item in subset:
                numerator = {item}
                denominator = subset.difference(numerator)
                support = round((counts / total_transactions) * 100)
                confidence = round((counts / get_item_support(numerator, zipped_counts)) * 100)
                if confidence >= min_confidence:
                    association_rules.append((numerator, denominator, support, confidence))
    return association_rules


def get_item_support(target_item, zipped_list):
    for item, count in zipped_list:
        if item == target_item:
            return count

