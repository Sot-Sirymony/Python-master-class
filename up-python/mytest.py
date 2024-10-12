#Bitwise Oeprator 
x={1,2,3}
y=1
print("y in x",y in x)
print("y not in x",y not in x)

# i = 101
# if i > 15 and i == 101:
#      if 1 == 1 :
#            print("10 is less than ggytfytfiyiyg15")
# else :
#     print("I am Not in if condition")

# if 1 == 1 : print("i234324") 
# else : print("23")


age = int(input("name is:"))
print("age is ",age,"year old ")

def check_grade(grade):
    if grade == 'A':
        return "Outstanding"
    elif grade == 'B':
        return "Excellent"
    elif grade == 'C':
        return "Very Good"
    elif grade == 'D':
        return "Good"
    elif grade == 'E':
        return "Satisfactory"
    else:
        return "Unrecognized"

# Example usage
grade_input = input("Enter the student's grade (A, B, C, D, E): ").upper()
result = check_grade(grade_input)
print(f"The grade {grade_input} is: {result}")
