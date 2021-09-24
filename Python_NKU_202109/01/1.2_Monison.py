from math import sqrt

def check_prime(i):
    # if i == 2:  # special case
        # return True
    # else:  # i > 2
        # result = True
        # sq = sqrt(i)
        # for a in range(2, i):  # do not use sq here, it is not a integer
            # if a <= sq:
                # if i % a == 0:
                    # result = False
                    # break
            # else:  # a > sq
                # break
        # return result
        
    if i == 1:  # special case
        return False
    n = int(sqrt(i))
    for a in range(2, n + 1):
        if i % a == 0:
            return False
    return True

# for test function
# for i in range(2, 100):
    # if check_prime(i):
        # print(i)

def check_Mns(P):
    if not check_prime(P):
        return False  # P must be a prime first
    else:  # if P is a prime
        M = 2 ** P - 1
        return check_prime(M)

# Prime, start from 2 to save time
order = 1
for P in range(2, 100):
    if check_Mns(P):
        print('No.%d\tP = %d\tM = %d' %(order, P, 2 ** P - 1))
        order += 1

z = input('Press any key to continue...')
