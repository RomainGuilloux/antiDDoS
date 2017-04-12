import datetime
blacklist_table=[]
print blacklist_table
def darth(ip):
    finder=-1
    for i in blacklist_table:
        if ip in i:
            finder= blacklist_table.index(i)
    if (finder==-1):
        print ('%s not in BlackList Table.. Adding it!'%ip)
        now= datetime.datetime.now()
        timeout= now + datetime.timedelta(minutes = 15)
        temparray=[ip,1,1,now]
        blacklist_table.append(temparray)
        #ban_ip(ip)
    elif(finder!=-1):
        print ('%s found in BlackList history. Increasing timeout!'%ip)
        blacklist_table[finder][1]=1
        blacklist_table[finder][2]+=1
        now= datetime.datetime.now()
        timeout=blacklist_table[finder][3]
        if timeout < now:
            timeout=now + datetime.timedelta(minutes = 5*blacklist_table[finder][2])
        if timeout > now:
            timeout=timeout + datetime.timedelta(minutes = 5*blacklist_table[finder][2])
        blacklist_table[finder][3]=timeout
darth(123)
print blacklist_table

darth(123)
print blacklist_table


def release_manager():
    for i in blacklist_table:
        if i[3] > now:
            blacklist_table[1]=0
            Print ("Releasing %s"%i[0])
            # unblock_ip(i[0])
