#Solve the Matrix
MATRIX_STR = '''
7ii
Tsx
h%?
i #
sM 
$a 
#t%''' 

# Step 1: Convert matrix_string to a 2D list (matrix)
matrix = []
for line in MATRIX_STR.strip().split('\n'):
    matrix.append(list(line))
print("Matrix:")
for row in matrix:
    print(row)
# Step 2: Iterate through columns
# Step 3: Filter alpha characters
# Step 4: Replace symbols with spaces
# Step 5: Print the decoded message
str=""
for col in range(len(matrix[0])):
    for row in range(len(matrix)):
        char = matrix[row][col]
        if char.isalpha():
            str+=char
        else:
            str+=" "
    


print(str)