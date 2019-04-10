
def takeSecond(elem):
    return elem[1]

if __name__ == '__main__':
    list = []
    list1 = [1,3]
    list2 = [5,7]
    list3 = [2,1]
    list4 = [4,4]

    list.append(list1)
    list.append(list2)
    list.append(list3)
    list.append(list4)

    list.sort(key=takeSecond)

    print(list)
