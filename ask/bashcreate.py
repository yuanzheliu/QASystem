with open("test.sh",'w') as f: 
    for s in range(1,6): 
        for i in range(1,11):
            print('python3 ask.py ../data/Development_data/set{}/a{}.txt 10 > data/set{}a{}.txt'.format(s,i,s,i),file = f)
    for i in range(1,11):
        print('python3 ask.py ../data/noun_counting_data/a{}.txt'.format(s,i),file = f)
