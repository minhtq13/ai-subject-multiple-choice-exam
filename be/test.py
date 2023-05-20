data2 = [(13, '299', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'C', 'B', 'A', 
'B', 'C', 'D', 'D', 'B', 'A', 'C', 'B', 'A', 'D', 'C', 'A', 'C', 'B', 'D', 'C', 'B', 'C', 'A', 'B', 'A', 'D', 'C', 'B', 'D', 'B', 'C', 'D', 'A', 'B', 'D', 'B', 'A', 'B', 'C', 'C', 'A', 'D', 'B', 'C', 'B', 'A', 'D', 'A', 'C', 'D', 'B', 'A', 'C', 'A', 'B', 'A', 'C', 'B', 'C', 'B', 'C', 'D', 'A', 'C', 'A', 'D', 'A', 'C', 'B', 'C', 'C', 'A', 
'D', 'D', 'B', 'A', 'C', 'A', 'C', 'B', 'D', 'A', 'C', 'A', 'B', 'B', 'D', 'B', 'B', 'A', 'B', 'C', 'D', 'B', 'A', 'B', 'C', 'D', 'B', 'A', 'C', 'C', 'D', 'B', 'B', 'A', 'D', 'C', 'A', 'A', 'B', 'C', 'D', '20_05_2023_16_18_33f13.jpg')] 
data1 = [(9, '0', '299', 'A', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, '0.0833333333333333', None), (10, '1', '299', 'A', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, '0.0833333333333333', None), (12, '235790', '299', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'C', 'B', 'A', 'B', 'C', 'D', 'D', 'B', 'A', 'C', 'B', 'A', 'D', 'C', 'A', 'C', 'B', 'D', 'C', 'B', 'C', 'A', 'B', 'A', 'D', 'C', 'B', 'D', 'B', 'C', 'D', 'A', 'B', 'D', 'B', 'A', 'B', 'C', 'C', 'A', 'D', 'B', 'C', 'B', 'A', 'D', 'A', 'C', 'D', 'B', 'A', 'C', 'A', 'B', 'A', 'C', 
'B', 'C', 'B', 'C', 'D', 'A', 'C', 'A', 'D', 'A', 'C', 'B', 'C', 'C', 'A', 'D', 'D', 'B', 'A', 'C', 'A', 'C', 'B', 'D', 'A', 'C', 'A', 'B', 'B', 'D', 'B', 'B', 'A', 'B', 'C', 'D', 'B', 'A', 'B', 'C', 'D', 'B', 'A', 'C', 'C', 'D', 'B', 'B', 'A', 'D', 'C', 'A', 'A', 'B', 'C', 'D', '10.0', '20_05_2023_18_15_38_f13.jpg')]

def check(data1, data2):
    dung = []
    j = 0
    for data in data2:
        dung.append([])
        for i in range(1, 121):
            print(data1[0][i + 1])
            if data1[len(data1) - 1][i + 1] == data[i + 1] or data1[len(data1) - 1][i + 1] == '':
                dung[j].append(True)
            else:
                dung[j].append(False)
        j = j + 1
    return dung

print(check(data1, data2))