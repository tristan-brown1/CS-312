import numpy as np
from numpy.matrixlib.defmatrix import matrix


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
        Align seq1 against seq2 using Needleman-Wunsch
        Put seq1 on left (j) and seq2 on top (i)
        => matrix[i][j]
        :param seq1: the first sequence to align; should be on the "left" of the matrix
        :param seq2: the second sequence to align; should be on the "top" of the matrix
        :param match_award: how many points to award a match
        :param indel_penalty: how many points to award a gap in either sequence
        :param sub_penalty: how many points to award a substitution
        :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
        :param gap: the character to use to represent gaps in the alignment strings
        :return: alignment cost, alignment 1, alignment 2
    """
    completed_matrix, alignment_cost = unrestricted_algorithm(seq1, seq2,banded_width,match_award,indel_penalty,sub_penalty)
    aligned_a, aligned_b = perform_alignment(completed_matrix, seq1, seq2, match_award, indel_penalty, sub_penalty, gap)
    return alignment_cost, aligned_a, aligned_b

def unrestricted_algorithm(str_a,str_b,banded_width,match_award,indel_penalty,sub_penalty):

    a_length = len(str_a)
    b_length = len(str_b)

    #setup matrix dimensions and initialize with starting row and column
    matrix = [[float('inf')] * (b_length + 1) for _ in range(a_length + 1)]
    for i in range(0, a_length + 1):
        matrix[i][0] = i * 5
    for j in range(0, b_length + 1):
        matrix[0][j] = j * 5

    #main filling of the matrix
    for i in range(1, a_length + 1):
        #check to apply requested banded_width
        if banded_width == -1:
            j_min = 1
            j_max = b_length
        else:
            j_min = max(1, i - banded_width)
            j_max = min(b_length, i + banded_width)

        for j in range(j_min, j_max + 1):
            if str_a[i - 1] == str_b[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1] + match_award
            else:
                insert = matrix[i][j - 1] + indel_penalty
                delete = matrix[i - 1][j] + indel_penalty
                substitute = matrix[i - 1][j - 1] + sub_penalty

                min_value = min(substitute,insert,delete)

                if min_value == substitute:
                    matrix[i][j] = substitute
                elif min_value == insert:
                    matrix[i][j] = insert
                elif min_value == delete:
                    matrix[i][j] = delete

    #grab cost from the end of the matrix
    alignment_cost = matrix[-1][-1]
    return matrix, alignment_cost



def perform_alignment(completed_matrix, str_a, str_b, match_award, indel_penalty, sub_penalty, gap):
    aligned_a = []
    aligned_b = []

    a_length = len(str_a)
    b_length = len(str_b)

    while a_length > 0 or b_length > 0:
        # check if match or substitution
        if (str_a[a_length - 1] == str_b[b_length - 1] and completed_matrix[a_length][b_length] == completed_matrix[a_length - 1][b_length - 1] + match_award or
                str_a[a_length - 1] != str_b[b_length - 1] and completed_matrix[a_length][b_length] == completed_matrix[a_length - 1][b_length - 1] + sub_penalty):

            aligned_a.append(str_a[a_length - 1])
            aligned_b.append(str_b[b_length - 1])
            a_length -= 1
            b_length -= 1

        # check if insertion
        elif completed_matrix[a_length][b_length] == completed_matrix[a_length][b_length - 1] + indel_penalty:

            aligned_a.append(gap)
            aligned_b.append(str_b[b_length - 1])
            b_length -= 1

        # check if deletion
        elif completed_matrix[a_length][b_length] == completed_matrix[a_length - 1][b_length] + indel_penalty:

            aligned_a.append(str_a[a_length - 1])
            aligned_b.append(gap)
            a_length -= 1

    #create properly aligned strings from reverse lists
    aligned_a_str = "".join(aligned_a[::-1])
    aligned_b_str = "".join(aligned_b[::-1])

    return aligned_a_str, aligned_b_str

