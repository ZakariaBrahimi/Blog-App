""" 
s = "descognail" 
sizes = [3, 2, 3, 1, 1]
the output should be concatSwaps ===>> (s, sizes) = "codesignal"
"""

result = list()

def concatSwaps(s, sizes):
    start = 0
    end = 0
    for num in sizes:
        #print(num)
        end += num # 3+2 = 5
        result.append(s[start:end]) # [0:3] ==> des // [3:5] ==>> co // 
        #print(s[start:num])
        start += num # start=3+2=5
    s = 0
    #print(result) # ['des', 'co', 'gna', 'i', 'l']
    for i in range(0,len(result)-1,2): # 0==>>4 ==>1
        s = result[i] # s=des // co
        result[i] = result[i+1] #result[0] = co
        result[i+1] = s #result[1] = des
    m = ''.join(result)
    return m
s = "descognail" 
sizes = [3, 2, 3, 1, 1]
print(concatSwaps(s, sizes))
