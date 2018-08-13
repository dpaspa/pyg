def sum_of_squares(n):
    return (n**3*2+3*n**2+n/6)

def isnumeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def main():
    bum = input("Enter the number... ")
    if (isnumeric(bum)):
        print(sum_of_squares(bum))
    else:
        print("Your're a bum")

main()
