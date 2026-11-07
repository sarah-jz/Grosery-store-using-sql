try:
    import mysql.connector as mys
    def setup_database():
        mycon=mys.connect(host="localhost",user="root", passwd="Password")
        mycursor=mycon.cursor()
        mycursor.execute("create database if not exists project_computer")
        mycursor.execute("use project_computer")
        mycursor.execute("create table if not exists login(username varchar(25) not null,password varchar(25) not null)")
        mycursor.execute("create table if not exists purchase(Odate date not null,Name varchar(25) not null, Pcode int not null,Quantity int not null,Total_Cost int not null)")
        mycursor.execute("create table if not exists stock(Pcode int not null,Pname varchar(25) not null,Available_Quantity int not null,Price int not null)")
        mycon.commit()
        ensure_default_login(mycon, mycursor)
        return mycon, mycursor

    def header(title):
        print("\n" + "-"*50)
        print(title.center(50))
        print("-"*50)
            
    def ensure_default_login(mycon, mycursor):
        mycursor.execute("SELECT COUNT(*) FROM login")
        count = mycursor.fetchone()[0]
        if count == 0:
            mycursor.execute("INSERT INTO login VALUES (%s,%s)", ("admin", "ng"))
            mycon.commit()
        
    def admin_login():
        Pass=input("Enter Password")
        mycursor.execute("select password from login where username='admin'")
        r=mycursor.fetchone()
        if r and Pass==r[0]:
            return True
        return False

    def Admin_menu():
        print(""" 1. Add new item\n 2. Updating price\n 3. Deleting item\n 4. Display items\n 5. Change password\n 6. View Analytics\n 7. Logout""")

    def Check_if_product_exists(pcode):
        mycursor.execute("SELECT * FROM stock WHERE Pcode=%s",(pcode,))
        if mycursor.fetchone():
            print("Product code already exists")
            return True
        else:
            return False
    
    def Add_item():
        pcode=int(input("Enter product code:"))
        pname=input("Enter product name:")
        quantity=int(input("Enter product quantity:"))
        price=int(input("Enter Product price:"))
        if Check_if_product_exists(pcode):
            return
        mycursor.execute("insert into stock values(%s,%s,%s,%s)",(pcode,pname,quantity,price))
        mycon.commit()
        print("Record successfully inserted")

    def Update_Price():
        pcode=int(input("Enter product code of the item to update the price:"))
        price=int(input("Enter updated price:"))
        mycursor.execute("update stock set Price=%s where Pcode=%s",(price,pcode))
        mycon.commit()

    def Delete_Item():
        pcode=int(input("Enter Pcode of item to delete:"))
        mycursor.execute("delete from stock where pcode=%s",(pcode,))
        print("Item deleted succesfully")
        mycon.commit()

    def Display_Items():
        mycursor.execute("select * from stock")
        d=mycursor.fetchall()
        for i in d:
            print(i)

    def Change_Password():
        password=input("Enter the new password:")
        mycursor.execute("update login set password=%s",(password,))
        mycon.commit()
        print("Password succesfully updated")

    def View_Analytics():
        print("1. Total Revenue \n2. Today's Revenue \n3. Best Selling Products \n4. Search Sales By Date \n5. Low Stock Alert \n6. Most Profitable Products \n7. Total Orders \n8. Average Order Value")
        a=int(input("Enter choice:"))
        return a

    def Customer_menu():
        print("1.display items \n2.purchase items \n3.search item \n4.view cart \n5.remove item from cart \n6.receipt")
        a=int(input("Enter choice:"))
        return a

    def get_stock():
        mycursor.execute("SELECT Pcode, Pname, Available_Quantity, Price FROM stock")
        return mycursor.fetchall()

    def Print_stock():
        d=get_stock()
        print("[Pcode,Item,Quantity,Price]")
        for i in d:
            print(i)

    def Purchase_Item(Cart):
        pcode=int(input("Enter the pcode of item wished to be brought:"))
        quantity=int(input("Enter amout of item to be brought:"))
        mycursor.execute("SELECT * FROM stock WHERE Pcode=%s",(pcode,))
        d= mycursor.fetchone()
        if d:
            if quantity<=d[2]:
                print("cost=",quantity*d[3])
                mycursor.execute("update stock set Available_Quantity=Available_Quantity-%s where Pcode=%s",(quantity,pcode))
                mycon.commit()
                a=1
                for j in Cart:
                    if j[0]==pcode:
                        j[2]+=quantity
                        j[4]=j[2]*j[3]
                        a=2
                if a==1:
                    Cart.append([pcode,d[1],quantity,d[3],quantity*d[3]])
            else:
                print("Insufficient stock, Quantity exceeds stock")
        else:
             print("Product not found")

    def Remove_from_cart(Cart):
        Print_Cart(Cart)
        pcode=int(input("Enter pcode of item to remove:"))
        quantity=int(input("Enter Quantity of item to remove:"))
        for i in Cart[:]:
            if pcode==i[0]:
                if quantity==i[2]:
                    mycursor.execute("update stock set Available_Quantity=Available_Quantity+%s where Pcode=%s",(quantity,pcode))
                    mycon.commit()
                    Cart[:]=[i for i in Cart if i[0]!=pcode]
                elif quantity<i[2]:
                    i[2]-=quantity
                    i[4]=i[2]*i[3]
                    mycursor.execute("update stock set Available_Quantity=Available_Quantity+%s where Pcode=%s",(quantity,pcode))
                    mycon.commit()
                else:
                    print("Quantity wished to return exceeds quantity in Cart.")
                break

    def Search_Item():
        d=get_stock()
        search=input("Enter item name to search:")
        f=False
        for i in d:
            if search.lower() in i[1].lower():
                print(i)
                f=True
        if f==False:
            print("No matching items found")

    def Print_Cart(Cart):
        print("PCODE      ITEM       QUANTITY   PRICE      COST")
        c=0
        for k in Cart:
            for j in k:
                print(j,' '*(10-len(str(j))),end='')
            c=c+k[4]
            print()
        print("TOTAL-",c)
        
    def print_receipt(Cart):
        print()
        print("RECEIPT-")
        Print_Cart(Cart)
        for i in Cart:
            mycursor.execute("Insert into purchase values (CURDATE(),%s,%s,%s,%s)",(i[1],i[0],i[2],i[4]))
        mycon.commit()

    def Total_Revenue():
        mycursor.execute("select sum(Total_Cost) from purchase")
        revenue=mycursor.fetchone()[0]
        if revenue is not None:
            print("Total Revenue=",revenue)
        else:
            print("No sales yet.")

    def Todays_Revenue():
        mycursor.execute("Select sum(Quantity),sum(Total_Cost) from purchase where Odate=curdate()")
        r= mycursor.fetchone()
        if r and r[1] is not None:
            i,j=r
            print("Todays Revenue=",j,"\n Items sold today=",i)
        else:
            print("No sales yet today.")

    def Best_Seller():
        n=int(input("Enter number of top products wished to display:"))
        mycursor.execute("select Name, sum(Quantity) from purchase Group by Pcode order by sum(Quantity) desc limit %s",(n,))
        d=mycursor.fetchall()
        if d:
            for p,s in d:
                  print(p,"-",s)
        else:
            print("No data available")

    def Low_Stock():
        mycursor.execute("Select * from stock where Available_Quantity<10")
        d=mycursor.fetchall()
        if d:
            for i in d:
                  print(i)
        else:
            print("No stock is low")

    def Most_Profitable_Product():
        n=int(input("Enter number of top products wished to display:"))
        mycursor.execute("select Name, sum(Total_Cost)from purchase group by Pcode order by sum(Total_Cost) desc limit %s",(n,))
        d=mycursor.fetchall()
        if d:
            for p,s in d:
                  print(p,"-",s)
        else:
            print("No data available")

    def Sales_By_Date():
        date=input("Enter date (YYYY-MM-DD):")
        mycursor.execute("SELECT SUM(Total_Cost) FROM purchase WHERE Odate=%s",(date,))
        d=mycursor.fetchone()[0]
        if d is not None:
            print(date,"-",d)
        else:
            print("No purchases on given date recorded.")

    def Total_Orders():
        mycursor.execute("SELECT COUNT(*) FROM purchase")
        print("Total Orders =", mycursor.fetchone()[0])

    def Average_Order_Value():
        mycursor.execute("SELECT AVG(Total_Cost) FROM purchase")
        avg = mycursor.fetchone()[0]
        if avg:
            print("Average Order Value =", round(avg, 2))
        else:
            print("No sales yet.")
        
#main code
    mycon,mycursor= setup_database()
    header("WELCOME TO SEDAN's STORE MANAGEMENT SYSTEM")
    while True:
        print("""
1. Admin
2. Customer
3. Exit
""")
        person=int(input("Enter your choice:"))
        if person==1:
            if admin_login():
                    print("Welcome")
                    while True:
                        Admin_menu()
                        ch=int(input("Enter your choice:"))
                        if ch==1:
                            Add_item()
                        elif ch==2:
                            Update_Price()
                        elif ch==3:
                            Delete_Item()
                        elif ch==4:
                            Display_Items()
                        elif ch==5:
                            Change_Password()
                        elif ch==6:
                            a=View_Analytics()
                            if a==1:
                                Total_Revenue()
                            elif a==2:
                                Todays_Revenue()
                            elif a==3:
                                Best_Seller()
                            elif a==4:
                                Sales_By_Date()
                            elif a==5:
                                Low_Stock()
                            elif a==6:
                                Most_Profitable_Product()
                            elif a==7:
                                Total_Orders()
                            elif a==8:
                                Average_Order_Value()
                            else:
                                print("Invalid choice.")
                        elif ch==7:
                            break
                        else:
                            print("Invalid choice")
            else:
                print("Wrong password")
        if person==2:
            Cart=[]
            while True:
                a= Customer_menu()
                if a==1: 
                    Print_stock()
                elif a==2:
                    Purchase_Item(Cart)
                elif a==3:
                    Search_Item()
                elif a==4:
                    Print_Cart(Cart)
                elif a==5:
                    Remove_from_cart(Cart)
                elif a==6:
                    print_receipt(Cart)
                    break
                else:
                    print("Invalid choice")
        if person==3:
            break
    print("Exited successfully, thanks for visiting SAEDAN's Grocery Store")
    mycon.close()
except Exception as e:
    print("Error:",e)
