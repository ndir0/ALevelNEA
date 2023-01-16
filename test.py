"""
classes = [["firstClass", "a", "b", "c"],
           ["secondClass", "b", "a", "c"],
           ["thirdClass", "b", "c", "a"]]

people = [["a", "firstClass", "secondClass", "thirdClass"],
          ["b", "secondClass", "thirdClass", "firstClass"],
          ["c", "thirdClass", "firstClass", "secondClass"]]

matches = []
matches2 = []
matched = False

for i in classes:
    classes2 = []
    classes2.append(i[0])
    classes2.append("")
    matches.append(classes2)

for i in people:
    people2 = []
    people2.append(i[0])
    people2.append("")
    matches2.append(people2)

print(matches)
print(matches2)
print()

while matched != True:
    for i in matches:
        for j in classes:
            if i[0] == j[0]:
                person = j[1]
        for x in matches2:
            if x[0] == person and x[1] == "":
                matches3 = []
                matches3.append(i[0])
                matches3.append(person)
                matches.remove(i)
                matches.append(matches3)
                matches2.remove(x)
                matches2.append(matches3[::-1])
                print(matches)
                print(matches2)
                print()
            elif len(x[1]) > 1:
                for z in people:
                    if z[0] == x[0]:
                        preference1 = (z.index(x[1]))
                        preference2 = (z.index(i[0]))
                        if preference2 < preference1:
                            for c in matches:
                                if c == i:
                                    matches.remove(c)
                                    matches3 = []
                                    matches3.append(x[1])
                                    matches3.append(z[0])
                                    matches.append(matches3)

print(matches)
"""
 
N = 3

def personPrefers(prefer, person, class1, class2):
    for i in range(N):
        if prefer[person][i] == class1: 
            return False
        if prefer[person][i] == class2: 
            return True
        
def GaleShapley(prefer):
    freeCount = N
    classFree = [False for i in range(N)]
    personClass = [-1 for i in range(N)] 
    while freeCount > 0:
        class1 = 0
        while class1 < N: 
            if classFree[class1] == False: 
                break
            class1 += 1
        i = 0
        while i < N and classFree[class1] == False: 
            person = prefer[class1][i]
            if personClass[person - N] == -1: 
                personClass[person - N] = class1 
                classFree[class1] = True
                freeCount -= 1
            else:
                class2 = personClass[person - N]
                if personPrefers(prefer, person, class1, class2) == False: 
                    personClass[person - N] = class1 
                    classFree[class1] = True
                    classFree[class2] = False
            i += 1
    print("Person ", " Class") 
    for i in range(N): 
        print(i + N, "\t", personClass[i]) 

prefer = [[3, 4, 5], [3, 4, 5], [3, 4, 5],
          [0, 1, 2], [2, 1, 0], [2, 0, 1]] 
  
GaleShapley(prefer)
