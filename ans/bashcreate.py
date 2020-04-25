with open("test.sh",'w') as f: 
    for s in range(1,6): 
        for i in range(1,11):
            print('python3 answer.py ../ask/data/set{}/a{}.txt set{}a{}.txt > data/answerset{}a{}.txt'.format(s,i,s,i,s,i),file = f)
    #for i in range(1,11):
        #print('python3 ask.py ../data/noun_counting_data/a{}.txt'.format(s,i),file = f)
