a=0
while a==0:
    c=input("Choice or list? ")
    if c=='Choice' or c=='choice':
        num=int(input("What is your number? "))
        prime=True
        for n in range(2,(round(num/2)+1)):
            if (int(num))%n==0:
                prime=False
                if n<(num/n):
                    print ((n),"*",int(num/n),"=",(num))
                if n>(num/n):
                    break
                if n==(num/n):
                    print ("")
                    print ("PERFECT SQUARE")
                    print (n,"^2","=",(num))
                    print ("PERFECT SQUARE")
                    print ("")
                    break
        if prime==True and num>1:
            print ((num),"is prime")
        else:
            print ((num),"is not prime")
    elif c=='list' or c=='List':
        a=int(input("Where would you like the list to begin? "))
        b=int(input("Where would you like the list to end? "))
        for i in range(a,b+1):
            prime=True
            for n in range(2,(round(int(i)/2)+1)):
                if (int(i))%n==0:
                    prime=False
            if prime==True and i>1:
                print (i)
    elif c=='no' or c=='stop' or c=='No' or c=='Stop':
        a=1
    




