from math import factorial # check

def custom_factorial(number):
    if type(number) is not int:
        raise ValueError("factorial only accepts int arguments")
    if number < 0:
        raise ValueError("cannot calculate factorial of a negative number")
    
    if number == 0:
        return 1
    elif number > 0:
        res = 1
        for i in range(1, number+1): # comeca em 1 e termina no numero do fatorial
            res*=i
        return res
        
    
number = 7
print(custom_factorial(number))
print(factorial(number))