# sum-1 = 'AAA'
# print(sum-1)

# l = {('sum'):'a', 123:'b', 234:'b'}
# for k, v in l.items():
    # print(k, v)

# l.get('B', 2)
# print(l)

# print('')

# bTuple = (1,8,5,7)
# bTuple.sort()

# sorted(bTuple)

# with open('A.txt', 'r+') as f:
    # Read = f.seek(5)

# print(Read)
    
    
    
# with open('test.txt', 'rb+') as fp:
    # fp.readline()
    # fp.seek(10, 1)
    # print(fp.readline())


# prefix = "Py"
# print(prefix + 'thon')

# def ask(prompt = "Do you like Python? ", hint = "yes or no"):
    # while True:
        # answer = input(prompt)
        # if answer.lower() in ('y', 'yes'):
            # print("Thank you")
            # return True
        # if answer.lower() in ('n', 'no'):
            # print("Why not ")
            # return False
        # else:
            # print(hint)

# ask("AAAA")

# l = [1,2,3,4]
# l.remove(2)
# print(l)
# print(l.pop())

# words = ['I', 'I', 'love', 'Python']
# for w in reversed(words):
    # print(w)
# print(words.count('I'))
# print((1,2,3,4)<(1,2,4))


# def ask(prompt, hint = "yes or no", chance = 2):
    # while chance > 0:
        # answer = input(prompt)
        # if answer.lower() in ('y', 'yes'):
            # print("Thank you")
            # return True
        # if answer.lower() in ('n', 'no'):
            # print("Why not ")
            # return False
        # else:
            # chance -= 1
            # print(hint)
    # print("Sorry, you have tried too many times.")

# ask("Do you like SciPy?")

def compute(*numbers):    
    s = 1
    for n in numbers:    
        s = s * n + n    
    return s

print(compute([3,3]))
print(compute([1,2,3]))
print(compute([3,2,1]))

nums = [3,3]
print(compute(*nums))


z = input('Press any key to contimue...')