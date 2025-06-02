import os

v = [5, 3, 2, 4, 7, 1, 0, 6]

def bubble_sort(input):
    v_length = len(input)
    indexed = v_length-1 # controle de indice ja indexado
    for times in range(0, v_length-1): # loop pra organizacao completa
        flag = False # flag pra verificar se ja ta organizado antes do fim da iteracao completa
        for i in range(0, indexed):
            v1, v2 = input[i], input[i+1] # valor original item, valor original par
            if v1 > v2: # swap
                input[i] = v2
                input[i+1] = v1
                flag = True
        indexed-=1
        if not flag:
            print('ja organizamos tudo')
            break
    return input

sorted_list = bubble_sort(v)
print(sorted_list)