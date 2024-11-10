import numpy as np

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
    # banded_alignment, alignment_cost = banded_algorithm("dog", "cat")
    # unrestricted_alignment, alignment_cost = unrestricted_algorithm("dog", "cat")
    # aligned_a, aligned_b = perform_alignment(unrestricted_alignment,"dog","cat")
    # return alignment_cost, aligned_a, aligned_b
    alignment_cost = unrestricted_algorithm("dog", "cat")
    return alignment_cost, "cat","dog"

def banded_algorithm(str_a,str_b):
    pass

def unrestricted_algorithm(str_a,str_b):

    #create/initialize matrix used to calculate
    matrix = [[row if column == 0 else column for column in range(len(str_a) + 1)] for row in range(len(str_b))]

    #fill in the matrix one block at a time
    for i in range(1, len(str_a) - 1):
        for j in range(1, len(str_b) - 1):
            if str_a[i - 1] == str_b[j-1]:
                # match!
                matrix[i][j] = matrix[i - 1][j - 1]
            else:
                matrix[i][j] = min(matrix[i - 1][j] + 1,
                                   matrix[i][j - 1] + 1,
                                   matrix[i - 1][j - 1] + 1)
    alignment_cost = matrix[-1][-1]


    # return unrestricted_alignment, alignment_cost
    return alignment_cost

def perform_alignment(alignment_path, str_a, str_b):


    return aligned_a, aligned_b

