
def align(
        seq1: str,
        seq2: str,
        match_award=-3,
        indel_penalty=5,
        sub_penalty=1,
        banded_width=-1,
        gap='-'
) -> tuple[float, str | None, str | None]:
    """
#         Align seq1 against seq2 using Needleman-Wunsch
#         Put seq1 on left (j) and seq2 on top (i)
#         => matrix[i][j]
#         :param seq1: the first sequence to align; should be on the "left" of the matrix
#         :param seq2: the second sequence to align; should be on the "top" of the matrix
#         :param match_award: how many points to award a match
#         :param indel_penalty: how many points to award a gap in either sequence
#         :param sub_penalty: how many points to award a substitution
#         :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
#         :param gap: the character to use to represent gaps in the alignment strings
#         :return: alignment cost, alignment 1, alignment 2
#     """
    if banded_width != -1:
        a_length = len(seq1)
        b_length = len(seq2)
        if a_length > b_length:
            seq1, seq2 = seq2, seq1

    completed_matrix, alignment_cost = edit_distance_algorithm(seq1, seq2, banded_width, match_award, indel_penalty, sub_penalty)
    aligned_a, aligned_b = perform_alignment(completed_matrix, seq1, seq2, match_award, indel_penalty, sub_penalty, gap)
    return alignment_cost, aligned_a, aligned_b


def edit_distance_algorithm(str_a, str_b, banded_width, match_award, indel_penalty, sub_penalty):
    a_length = len(str_a)
    b_length = len(str_b)

    matrix = {}

    if banded_width == -1:
        for i in range(a_length + 1):
            matrix[(i, 0)] = i * indel_penalty
        for j in range(b_length + 1):
            matrix[(0, j)] = j * indel_penalty
    else:
        for i in range(banded_width + 1):
            matrix[(i, 0)] = i * indel_penalty
        for j in range(banded_width + 1):
            matrix[(0, j)] = j * indel_penalty

    # main filling of the matrix
    for i in range(1, a_length + 1):
        # check to apply requested banded_width
        if banded_width == -1:
            j_min = 1
            j_max = b_length
        else:
            j_min = max(1, i - banded_width)
            j_max = min(b_length, i + banded_width)

        for j in range(j_min, j_max + 1):
            #check for match
            if str_a[i - 1] == str_b[j - 1]:
                matrix[(i, j)] = matrix[(i - 1, j - 1)] + match_award
            else:
            #check to see if value is within banded_width and assign it 'inf' if it is not
                if (i, j - 1) not in matrix:
                    insert = float('inf')
                else:
                    insert = matrix[(i, j - 1)] + indel_penalty

                if (i - 1, j) not in matrix:
                    delete = float('inf')
                else:
                    delete = matrix[(i - 1, j)] + indel_penalty

                if (i - 1, j - 1) not in matrix:
                    substitute = float('inf')
                else:
                    substitute = matrix[(i - 1, j - 1)] + sub_penalty

                matrix[(i, j)] = min(insert, delete, substitute)

    # grab cost from the end of the matrix
    alignment_cost = matrix[(a_length, b_length)]
    return matrix, alignment_cost


def perform_alignment(completed_matrix, str_a, str_b, match_award, indel_penalty, sub_penalty, gap):
    aligned_a = []
    aligned_b = []

    a_length = len(str_a)
    b_length = len(str_b)

    while a_length > 0 or b_length > 0:
    #backtrack through completed_matrix in order to properly align strings

        # check if match or substitute
        if (a_length > 0 and b_length > 0 and ((str_a[a_length - 1] == str_b[b_length - 1] and completed_matrix.get((a_length, b_length)) ==
              completed_matrix.get((a_length - 1, b_length - 1), float('inf')) + match_award) or
             (str_a[a_length - 1] != str_b[b_length - 1] and completed_matrix.get((a_length, b_length)) ==
              completed_matrix.get((a_length - 1, b_length - 1), float('inf')) + sub_penalty))):

            aligned_a.append(str_a[a_length - 1])
            aligned_b.append(str_b[b_length - 1])
            a_length -= 1
            b_length -= 1

        # check if insert
        elif (b_length > 0 and completed_matrix.get((a_length, b_length)) ==
              completed_matrix.get((a_length, b_length - 1), float('inf')) + indel_penalty):

            aligned_a.append(gap)
            aligned_b.append(str_b[b_length - 1])
            b_length -= 1

        # check if delete
        elif (a_length > 0 and completed_matrix.get((a_length, b_length)) ==
              completed_matrix.get((a_length - 1, b_length), float('inf')) + indel_penalty):

            aligned_a.append(str_a[a_length - 1])
            aligned_b.append(gap)
            a_length -= 1

        # otherwise move on
        else:
            break

    # create properly aligned strings from reverse lists
    aligned_a_str = "".join(aligned_a[::-1])
    aligned_b_str = "".join(aligned_b[::-1])

    return aligned_a_str, aligned_b_str
