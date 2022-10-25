c=str(input("list or choice? "))
if c=='choice':
   a=1
   while a==1:
      num=int(input('Choose a number '))
      if num > 1:
         # check for factors
         for i in range(2,num):
             if (num % i) == 0:
                 print(num,"is not a prime number")
                 print(i,"times",num//i,"is",num)
                 break
         else:
             print(num,"is a prime number")
             
      # if input number is less than
      # or equal to 1, it is not prime
      else:
         print(num,"is not a prime number")
else:
   num=int(input("Where would you like the list to begin? "))
   if num<3:
      num=3
      print ("2")
   if num%2==0:
      num=num+1
   end=int(input("How high do you want the list to go? "))
   while num<end:
      if num > 1:
         # check for factors
         for i in range(2,num):
             if (num % i) == 0:
                 break
         else:
             print(num)
         num+=2
          

