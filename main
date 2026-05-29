try:
    import mysql.connector as mys
    print("""
---------------------------------------------------
WELCOME TO SAEDAN's GROCERY STORE MANAGEMENT SYSTEM
---------------------------------------------------""")
    mycon=mys.connect(host="localhost",user="root", passwd="Password")
    mycursor=mycon.cursor()
    mycursor.execute("create database if not exists project_computer")
    mycursor.execute("use project_computer")
    mycursor.execute("create table if not exists login(username varchar(25) not null,password varchar(25) not null)")
    mycursor.execute("create table if not exists purchase(Odate date not null,Name varchar(25) not null, Pcode int not null,Amount int not null)")
    mycursor.execute("create table if not exists stock(Pcode int not null,Pname varchar(25) not null,Quantity int not null,Price int not null)")
    mycon.commit()
    z=0
    mycursor.execute("select * from login")
    for i in mycursor:
        z+=1
    if z==0:
        mycursor.execute("insert into login values('username','ng')")
        mycon.commit()
    while True:
        print("""
1. Admin
2. Customer
3. Exit
""")
        person=int(input("Enter your choice:"))
        if person==1:
            Pass=input("Enter Password")
            mycursor.execute("select * from login")
            for i in mycursor:
                username,password=i
            if Pass==password:
                p="y"
                print("Welcome")
                while p=="y":
                    print("""1. Add new item
2. Updating price
3. Deleting item
4. Display all items
5. To change the password
6. Log out""")
                    ch=int(input("Enter your choice:"))
                    if ch==1:
                        pcode=int(input("Enter product code:"))
                        pname=input("Enter product name:")
                        quantity=int(input("Enter product quantity:"))
                        price=int(input("Enter Product price:"))
                        mycursor.execute("insert into stock values({},'{}',{},{})".format(pcode,pname,quantity,price))
                        mycon.commit()
                        print("Record successfully inserted")
                    if ch==2:
                        pcode=int(input("Enter product code of the item to update the price:"))
                        price=int(input("Enter updated price:"))
                        mycursor.execute("update stock set Price=%s where Pcode=%s",(price,pcode))
                        mycon.commit()
                    if ch==3:
                        pcode=int(input("Enter Pcode of item to delete:"))
                        mycursor.execute("delete from stock where pcode=%s",(pcode,))
                        print("Item deleted succesfully")
                        mycon.commit()
                    if ch==4:
                        mycursor.execute("select * from stock")
                        d=mycursor.fetchall()
                        for i in d:
                            print(i)
                    if ch==5:
                        password=input("Enter the new password:")
                        mycursor.execute("update login set password=%s",(password,))
                        mycon.commit()
                        print("Password succesfully updated")
                    if ch==6:
                        p="n"
            else:
                print("Wrong password")
        if person==2:
            L=[]
            mycursor.execute("select * from stock")
            d=mycursor.fetchall()
            print("[Pcode,Item,Quantity,Price]")
            for i in d:
                print(i)
            yn=input("Do you wish to buy an item? y/n:")
            while yn=="y":
                pcode=int(input("Enter the pcode of item wished to be brought:"))
                quantity=int(input("Enter amout of item to be brought:"))
                for i in d:
                    if i[0]==pcode:
                        if quantity<=i[2]:
                            print("cost=",quantity*i[3])
                            mycursor.execute("update stock set Quantity=Quantity-%s where Pcode=%s",(quantity,pcode))
                            mycon.commit()
                            L=L+[(pcode,i[1],quantity,i[3],quantity*i[3])]
                        else:
                            print("Insufficient stock, Quantity exceeds stock")
                yn=input("Do you wish to purchase more items? y/n:")
            print()
            print("RECEIPT-")
            print("PCODE      ITEM       QUANTITY   PRICE      COST")
            c=0
            for k in L:
                for j in k:
                    print(j,' '*(10-len(str(j))),end='')
                c=c+k[4]
                print()
            print("TOTAL-",c)
              
        if person==3:
            break
    print("Exited successfully, thanks for visiting SAEDAN's Grocery Store")
    mycon.close()
except Exception as e:
    print("Error:",e)
