def match_words(words):
    count_words = 0
    lst=[]
    for i in words:
        if len(i)>1 and i[0]==i[-1]:
            lst.append(i)
            count_words+=1
    print("The list which satisfys both of the conditions: ", lst)
    return count_words
count=match_words(["131", "abc", "aba", "1221", "142"])
print(count)