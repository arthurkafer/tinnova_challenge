def mult_checker(div): # funcao dinamica pra checagem de multiplos de x valor
    return lambda x: x % div == 0

def sum_of_multiples(list_until):
    lista = list(range(list_until))
    check_div_3 = mult_checker(3)
    check_div_5 = mult_checker(5)

    sum = 0
    for item in lista:
        if check_div_3(item) or check_div_5(item):
            sum+=item
    return sum

print(sum_of_multiples(10))