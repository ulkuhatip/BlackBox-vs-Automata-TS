from __future__ import annotations


def levenshtein_distance(left: str, right: str) -> int:
    """Compute Levenshtein distance between two strings."""
    if left == right:
        return 0
    if not left:
        return len(right)
    if not right:
        return len(left)

    previous_row = list(range(len(right) + 1))
    for i, left_char in enumerate(left, start=1):
        current_row = [i]
        for j, right_char in enumerate(right, start=1):
            insert_cost = current_row[j - 1] + 1
            delete_cost = previous_row[j] + 1
            replace_cost = previous_row[j - 1] + (left_char != right_char)
            current_row.append(min(insert_cost, delete_cost, replace_cost))
        previous_row = current_row
    return previous_row[-1]


def map_unseen_pattern(pattern: str, vocabulary: set[str]) -> tuple[str, int]:
    """Map an unseen pattern to the closest known pattern."""
    if not vocabulary:
        raise ValueError("vocabulary cannot be empty")

    best_match = min(vocabulary, key=lambda candidate: (levenshtein_distance(pattern, candidate), candidate))
    return best_match, levenshtein_distance(pattern, best_match)
