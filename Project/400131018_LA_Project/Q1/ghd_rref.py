import numpy as np

# Index Finders
def get_left_most_non_zero_column_index(matrix, start_row_index):
    is_col_non_zero_list = [matrix[start_row_index:,i].any() for i in range(matrix.shape[1])]
    if np.any(is_col_non_zero_list):
        return np.argmax(is_col_non_zero_list)
    else:
        return -1

def get_top_most_non_zero_row_index(matrix, start_row_index, pivot_column_index):
    is_row_non_zero_list = [matrix[i,pivot_column_index].any() for i in range(matrix.shape[0])]

    # Ignore the rows before i
    for i in range(start_row_index):
        is_row_non_zero_list[i] = False

    if np.any(is_row_non_zero_list):
        return np.argmax(is_row_non_zero_list)
    else:
        return -1
    
def get_top_most_non_zero_row_index_thats_not_current_row(matrix, current_row_index, start_row_index, pivot_column_index):
    is_row_non_zero_list = [matrix[i,pivot_column_index].any() for i in range(matrix.shape[0])]

    # Ignore the rows before i
    for i in range(start_row_index):
        is_row_non_zero_list[i] = False

    # Ignore the current row even if it's non-zero
    is_row_non_zero_list[current_row_index] = False

    if np.any(is_row_non_zero_list):
        return np.argmax(is_row_non_zero_list)
    else:
        return -1

def row_echelon_form(matrix):
    pivot_positions = []
    # For every row
    for i in range(matrix.shape[0]):
        left_most_non_zero_column_index = get_left_most_non_zero_column_index(matrix, start_row_index=i)
        if left_most_non_zero_column_index == -1:
            break

        # Step 1: try to put a 1 in the 'i'th row of the 'left_most_non_zero_column_index' column (aka pivot position)
        # check if its not non-zero already
        if matrix[i,left_most_non_zero_column_index] == 0:
            # find the top most non zero row below pivot
            top_most_non_zero_row_index = get_top_most_non_zero_row_index(
                matrix,
                start_row_index=i,
                pivot_column_index=left_most_non_zero_column_index)
            if top_most_non_zero_row_index == -1:
                break
            # add the found non-zero row to the 'i'th row (pivots row)
            matrix[i,:] = (matrix[i,:] + matrix[top_most_non_zero_row_index,:])%2
        # divide 'i'th row (pivots row) by the pivots value to get 1 in pivots position
        # matrix[i,:] = matrix[i,:] / matrix[i, left_most_non_zero_column_index]

        # save the pivot positions for styling
        pivot_positions.append((i,left_most_non_zero_column_index))

        # Step 2: make all the other rows below the pivots row zero in the 'left_most_non_zero_column_index' column
        for row_index in range(i+1, matrix.shape[0]):

            # find the top most non zero row below pivot
            top_most_non_zero_row_index_thats_not_current_row = get_top_most_non_zero_row_index_thats_not_current_row(
                matrix,
                current_row_index=row_index,
                start_row_index=i,
                pivot_column_index=left_most_non_zero_column_index)
            
            if top_most_non_zero_row_index_thats_not_current_row == -1:
                break
            
            # add the found non-zero row to the current_row and make it zero in the 'left_most_non_zero_column_index'(pivot_index) column
            # coef = -1.0 * matrix[row_index, left_most_non_zero_column_index] / matrix[top_most_non_zero_row_index_thats_not_current_row, left_most_non_zero_column_index]
            if matrix[row_index, left_most_non_zero_column_index] != 0:
                matrix[row_index,:] = (matrix[row_index,:] + matrix[top_most_non_zero_row_index_thats_not_current_row,:])%2

            # print(i, row_index, top_most_non_zero_row_index_thats_not_current_row)
            # print(matrix)
            # print()
    return matrix, pivot_positions

def reduced_row_echelon_form(matrix, pivot_positions):
    # sort pivots from right to left
    pivot_positions = sorted(pivot_positions, key=lambda x: x[1], reverse=True)

    for pivot in pivot_positions:
        for current_row in range(pivot[0]):
            # add the pivot row to the current_row and make it zero in the pivot column
            # coef = -1.0 * matrix[current_row, pivot[1]] / matrix[pivot[0], pivot[1]]
            if matrix[current_row,pivot[1]] != 0:
                matrix[current_row,:] = (matrix[current_row,:]+matrix[pivot[0],:])%2
            # print(pivot, current_row, (matrix[current_row,:]+matrix[pivot[0],:])%2)
            # print(matrix)
            # print()
    return matrix
    
def rref(A):
    row_echelon_matrix, pivot_positions = row_echelon_form(A)
    rref_A = reduced_row_echelon_form(row_echelon_matrix, pivot_positions)

    return rref_A

