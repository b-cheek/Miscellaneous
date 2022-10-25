#create a program that will simulate a game of lucky sevens
#the output will say when you went broke, and when you should have stopped
#(and the respective dollar value)

import random
roll=0
sroll=0
##dollar=(int(input("How many dollars do you have? ")))
initialDollar=100
maxstop=0
while 0==0:
    dollar = initialDollar
    stop = dollar
    while dollar>0:
        die1=(random.randint(1,6))
        die2=(random.randint(1,6))
        if (die1)+(die2)==7:
            dollar+=5
            if dollar>stop:
                stop=dollar
                sroll=roll
        dollar-=1
        if stop>maxstop:
            maxstop=stop
            print(maxstop)
    ##    print("---------------------")
    ##    print("Roll# "+str(roll),"Die 1:",str(die1),"   ","Die 2:",str(die2))
    ##    print("")
    ##    print("You have $"+str(dollar))
    ##    print("")
        roll+=1
print ("You are broke after",(roll),"rolls")
print ("You should have quit after",str(sroll),"rolls when you had $"+str(stop))
    
        
