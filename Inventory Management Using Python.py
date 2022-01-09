#Importing Required Modules

from tkinter import *

import tkinter.messagebox as tm

from tkinter import filedialog

from tkinter import ttk

import random

from datetime import date,datetime

import os

import tempfile

import mysql.connector as sql

#---------------------------------------------------------------------------------------------------------------------------------------------------

#Connecting to mysql

con=sql.connect(host="localhost",user="root",password="root",database="inventory",auth_plugin = 'mysql_native_password')
cursor=con.cursor()    #Creating a cursor 

#---------------------------------------------------------------------------------------------------------------------------------------------------

#Displaying Date

now = date.today()
today = now.strftime("%d/%m/%Y") 

#---------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------Required Functions Definition (For Both Screens or Individual Screens )---------------
def pwd_check(pwd):  
    
    if pwd=="root":      #Checking Password
        return True
    else: 
        return False
 

def data_auth1():

    pwd_var=StringVar()         #Authentication Screen for Resetting Customer Data

    top=Toplevel() 
    top.geometry("400x120")
    top.title("Customer Data Reset")

    top.resizable(False,False)
 
    lbl=Label(top,text="Enter database password: ").grid(row=0,column=0)
    pwd_entry=Entry(top,font=("Times New Roman",10),width=15,show="*",
                    textvariable=pwd_var).grid(row=0,column=1)
    
    lbl_warn=Label(top,text="WARNING!!! CHANGES MADE TO DATABASE CAN'T BE UNDONE",
                   font=("Times new roman",8,"bold"),padx=2,bg="white",fg="black").place(x=0,y=70)


    sub=Button(top,text="SUBMIT",padx=10,pady=5,bd=5,fg="black",bg="white",
               font=("Ariel",8,"bold"),width=5,relief=RAISED,
               command=lambda:reset_cust_data(pwd_var.get(),top))
    sub.grid(row=1,column=1)
    

def data_auth2():

    pwd_var=StringVar()       #Authentication Screen for Resetting Sales Data

    top=Toplevel() 
    top.geometry("400x120")
    top.title("Sales Data Reset")
    
    top.resizable(False,False)

    lbl=Label(top,text="Enter database password: ").grid(row=0,column=0)
    pwd_entry=Entry(top,font=("Times New Roman",10),width=15,
                    show="*",textvariable=pwd_var).grid(row=0,column=1)
    
    lbl_warn=Label(top,text="WARNING!!! CHANGES MADE TO DATABASE CAN'T BE UNDONE",
                   font=("Times new roman",8,"bold"),padx=2,bg="white",fg="black").place(x=0,y=70)

    sub=Button(top,text="SUBMIT",padx=10,pady=5,bd=5,fg="black",bg="white",
               font=("Ariel",8,"bold"),width=5,relief=RAISED,
               command=lambda:reset_sales_data(pwd_var.get(),top))
    sub.grid(row=1,column=1)  


def reset_cust_data(pwd,top):

    #For resetting Customer Details

    if pwd_check(pwd)==True:
        cursor.execute("DELETE FROM customer")
        con.commit()
        tm.showinfo("Data Erased","Customer data has been erased successfully!")
        top.destroy()
        
    else:
        tm.showerror("Incorrect Details",
                     "Invalid password!!! Unable to reset customer data")
        top.destroy()


def reset_sales_data(pwd,top):
 
    #For resetting sales

    if pwd_check(pwd)==True:
        cursor.execute("UPDATE sales set UNIT_SOLD=0")
        con.commit()
        tm.showinfo("Data Erased",
                    "Sales data has been erased successfully!")
        top.destroy()
    else:
        tm.showerror("Incorrect Details",
                     "Invalid password!!! Unable to reset sales data")
        top.destroy()


def reset_stock():

    #For resetting / reordering stock

    cursor.execute("update stock set stock.STOCK=stock.REORDER_LVL;")
    con.commit()


#---------------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------Main Screen------------------------------------------------------------------------------------ 
class Inventory:

    def __init__(self,x):

        self.x=x
        self.x.title("Inventory")
        self.x.geometry("1980x1080+0+0")
        self.x.attributes('-fullscreen',"True")
        self.x.config(bg="honeydew4")
        title=Label(self.x,text="Inventory Management\t\t"+
                    str(today),bd=10,font=("Bahnschrift",30,"bold"),relief=GROOVE,
                    bg="Navy Blue",fg="White").pack(fill=X)

        #-----------------------------------------Required Functions Definition (for Main Screen)--------------------


        def showing_stock():                  #Function For Button 'SHOW STOCK'         
                                              
            frame2=LabelFrame(self.x,relief=RAISED,bd=8,bg="Ivory2")  
            frame2.place(x=770,y=75,height=250,relwidth=0.5)
            label=Label(frame2,text="Stock",font=("Calibri",25,"bold"),
                        bg="Blue",fg="white").pack(fill=X)
            
            cursor.execute("select * from stock;")
            
            row=cursor.fetchall()
            
            
            table=ttk.Treeview(frame2,show="headings",height="7")
            table.pack()

            table['columns']=('S_NO','PROD_CODE','PROD_NAME',
                              'PRICE','STOCK','REORDER_LVL')
            
            table.column('S_NO',width=50,anchor=CENTER)
            table.column('PROD_CODE',width=100,anchor=CENTER)
            table.column('PROD_NAME',width=200,anchor=CENTER)
            table.column('PRICE',width=100,anchor=CENTER)
            table.column('STOCK',width=100,anchor=CENTER)
            table.column('REORDER_LVL',width=100,anchor=CENTER)

            #column headings
            table.heading('S_NO',text="S.No")
            table.heading('PROD_CODE',text="Product Code")
            table.heading('PROD_NAME',text="Product Name")
            table.heading('PRICE',text="Price")
            table.heading('STOCK',text="Stock")
            table.heading('REORDER_LVL',text="Reorder Level")

            style=ttk.Style()
            style.theme_use("alt")
            style.configure("Treeview",background="ivory2",
                            foreground="black",fieldbackground="ivory2")
            style.map("Treeview",background=[('selected','blue')])

            for i in row:                   #Inserting Values
                
                table.insert(parent='',index='end',values=i)
        

        def showing_custdata():               #Function For Button 'SHOW CUSTOMER DATA' 

            frame3=LabelFrame(self.x,relief=RAISED,bd=8,bg="Ivory2")
            frame3.place(x=770,y=325,height=250,relwidth=0.5)
            label=Label(frame3,text="Customer Data",
                        font=("Calibri",25,"bold"),bg="Blue",fg="white").pack(fill=X)

            cursor.execute("select * from customer;")

            row=cursor.fetchall()
            
            
            table=ttk.Treeview(frame3,show="headings",height="7")
            table.pack()

            table['columns']=('Customer_Name','C_ID',
                              'KeyPerson_Name','Mobiles','Tablets',
                              'Laptop','Television','Desktop',
                              'Monitor','Delivery_Date','Total')
            

            table.column('Customer_Name',width=95,anchor=CENTER)
            table.column('C_ID',width=95,anchor=CENTER)
            table.column('KeyPerson_Name',width=100,anchor=CENTER)
            table.column('Mobiles',width=50,anchor=CENTER)
            table.column('Tablets',width=50,anchor=CENTER)
            table.column('Laptop',width=50,anchor=CENTER)
            table.column('Television',width=60,anchor=CENTER)
            table.column('Desktop',width=50,anchor=CENTER)
            table.column('Monitor',width=60,anchor=CENTER)
            table.column('Delivery_Date',width=80,anchor=CENTER)
            table.column('Total',width=60,anchor=CENTER)

            #column headings

            table.heading('Customer_Name',text="Customer Name")
            table.heading('C_ID',text="Customer ID")
            table.heading('KeyPerson_Name',text="ContactPerson")
            table.heading('Mobiles',text="Mobile")
            table.heading('Tablets',text="Tablet")
            table.heading('Laptop',text="Laptop")
            table.heading('Television',text="Television")
            table.heading('Desktop',text="Desktop")
            table.heading('Monitor',text="Monitor")
            table.heading('Delivery_Date',text="Delivery Date")
            table.heading('Total',text="Total")

            style=ttk.Style()
            style.theme_use("alt")
            style.configure("Treeview",background="ivory2",
                            foreground="black",fieldbackground="ivory2")
            style.map("Treeview",background=[('selected','blue')])

            for i in row:
                
                table.insert(parent='',index='end',values=i)

        
        def showing_salesdata():              #Function For Button 'SHOW SALES DATA' 

            frame4=LabelFrame(self.x,relief=RAISED,bd=8,bg="Ivory2")
            frame4.place(x=770,y=575,height=250,relwidth=0.5)
            label=Label(frame4,text="Sales Data",font=("Calibri",25,"bold"),
                        bg="Blue",fg="white").pack(fill=X)
            
            cursor.execute("select * from sales;")
            
            row=cursor.fetchall()
            
            
            table=ttk.Treeview(frame4,show="headings",height="7")
            table.pack()

            table['columns']=('S_NO','PROD_NAME','UNIT_SOLD','PRICE')
            
            table.column('S_NO',width=50,anchor=CENTER)
            table.column('PROD_NAME',width=100,anchor=CENTER)
            table.column('UNIT_SOLD',width=100,anchor=CENTER)
            table.column('PRICE',width=100,anchor=CENTER)


            #column headings
            table.heading('S_NO',text="S.No")
            table.heading('PROD_NAME',text="Product Name")
            table.heading('UNIT_SOLD',text="Units Sold")
            table.heading('PRICE',text="Price")

            style=ttk.Style()
            style.theme_use("alt")
            style.configure("Treeview",background="ivory2",
                            foreground="black",fieldbackground="ivory2")
            style.map("Treeview",background=[('selected','blue')])
           

            for i in row:           
                
                table.insert(parent='',index='end',values=i)


    #-----------------------------Frame 1 Product Detail-----------------------

        frame1=LabelFrame(self.x,relief=RAISED,bd=8,bg="Ivory2")
        frame1.place(x=0,y=75,height=750,relwidth=0.5)
        prod_detail_label=Label(frame1,text="Inventory Functions",
                                font=("Calibri",25,"bold"),bg="Blue",fg="white").pack(fill=X)

        #------------------------Required Buttons for Main Screen--------

        b_showstock=Button(frame1,padx=48,pady=8,bd=8,fg="black",
                           bg="white",font=("Ariel",10,"bold"),width=10,
                           text="SHOW STOCK",command=showing_stock).place(x=320,y=80)

        b_showcust=Button(frame1,padx=48,pady=8,bd=8,fg="black",
                          bg="white",font=("Ariel",10,"bold"),width=10,
                          text="SHOW CUSTOMER DATA",
                          command=showing_custdata).place(x=320,y=160)
        
        b_showsales=Button(frame1,padx=48,pady=8,bd=8,fg="black",
                           bg="white",font=("Ariel",10,"bold"),width=10,
                           text="SHOW SALES DATA",
                           command=showing_salesdata).place(x=320,y=240)

        b_place_order=Button(frame1,padx=48,pady=8,bd=8,fg="black",
                             bg="white",font=("Ariel",10,"bold"),width=10,
                             text="PLACE ORDER",command=self.billing).place(x=320,y=320)

        b_reorder_stock=Button(frame1,padx=48,pady=8,bd=8,fg="black",
                               bg="white",font=("Ariel",10,"bold"),width=10,
                               text="REORDER STOCK",command=reset_stock).place(x=320,y=400)
         
        b_reset_cust_data=Button(frame1,padx=48,pady=8,bd=8,fg="black",
                                 bg="white",font=("Ariel",10,"bold"),width=10,
                                 text="RESET CUSTOMER DATA",command=data_auth1).place(x=320,y=480)
        
        b_reset_sales_data=Button(frame1,padx=48,pady=8,bd=8,fg="black",
                                  bg="white",font=("Ariel",10,"bold"),width=10,
                                  text="RESET SALES DATA",command=data_auth2).place(x=320,y=560)

        b_exit=Button(frame1,padx=48,pady=8,bd=8,fg="black",
                      bg="white",font=("Ariel",10,"bold"),width=10,
                      text="QUIT",command=self.x.destroy).place(x=320,y=640)

    #-----------------------------Frame 2 Stock---------------------------------

        frame2=LabelFrame(self.x,relief=RAISED,bd=8,bg="Ivory2")
        frame2.place(x=770,y=75,height=250,relwidth=0.5)
        label=Label(frame2,text="Stock",font=("Calibri",25,"bold"),
                    bg="Blue",fg="white").pack(fill=X)

    #-----------------------------Frame 3 Customer Data-------------------------

        frame3=LabelFrame(self.x,relief=RAISED,bd=8,bg="Ivory2")
        frame3.place(x=770,y=325,height=250,relwidth=0.5)
        label=Label(frame3,text="Customer Data",font=("Calibri",25,"bold"),
                    bg="Blue",fg="white").pack(fill=X)

    #-----------------------------Frame 4 Sales Data----------------------------

        frame4=LabelFrame(self.x,relief=RAISED,bd=8,bg="Ivory2")
        frame4.place(x=770,y=575,height=250,relwidth=0.5)
        label=Label(frame4,text="Sales Data",font=("Calibri",25,"bold"),
                    bg="Blue",fg="white").pack(fill=X)

    
    def billing(self):
        self.app=Billing(Toplevel(self.x))

#---------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------- Billling Screen----------------------------------------------------------------------------------

class Billing:

    def __init__(self,r):

        r.title("Billing")
        r.geometry("1980x1080+0+0")
        r.attributes('-fullscreen',"True")
        r.config(bg="honeydew4")
        title=Label(r,text="SALES \t\t"+str(today),bd=10,
                    font=("Bahnschrift",30,"bold"),relief=GROOVE,
                    bg="navy blue",fg="white").pack(fill=X)


        #-------------------------------Variables---------------------------------------------------

        #------------------------------Customer Varibles--------------------------------------------
        c_ref_var=StringVar()     #StringVar()used to store a string
        c_name_var=StringVar()
        c_no_var=StringVar()
        c_email_var=StringVar()
        c_kp_var=StringVar()
        c_kpno_var=StringVar()

        #-----------------------------Order Variables------------------------------------------------

        mpvar=StringVar()  
        tabvar=StringVar()
        lapvar=StringVar()
        tvvar=StringVar()
        pcvar=StringVar()
        movar=StringVar()
        stotvar=StringVar()
        totvar=StringVar()

        dateomvar=IntVar()
        monthomvar=IntVar()
        yearomvar=IntVar()

        datelist=[x for x in range(1,32)]
        monthlist=[y for y in range(1,13)]
        yearlist=["2021","2022","2023","2024"]


        mpvar.set("0")
        tabvar.set("0")
        lapvar.set("0")
        tvvar.set("0")
        pcvar.set("0")
        movar.set("0")


        
        #----------------------------Required Functions Definition (For Billing Screen)-------------------------------------------------------------

        def reset():        #For resetting all the particulars
            
            mpvar.set("0")
            tabvar.set("0")
            lapvar.set("0")
            tvvar.set("0")
            pcvar.set("0")
            movar.set("0")

            dateomvar.set("0")
            monthomvar.set("0")
            yearomvar.set("0")

            stotvar.set("")
            totvar.set("")
            gen_id()
            c_name_var.set("")
            c_no_var.set("")
            c_email_var.set("")
            c_kp_var.set("")
            c_kpno_var.set("")  

            txt.delete(1.0,END)


        def c_id():         #For getting all existing Customer ID's from Database

            cursor.execute("select C_ID from customer")
            l=[i[0] for i in cursor]
            return l
        

        def checkdate(year,month,date):         #Checking for Invalid Delivery Date 
            
            try:
                
                datetime(year,month,date)

                return True

            except ValueError:

                tm.showerror("Error ","Please select a valid date")

                return False


        def get_date(year,month,date):          #Getting Date of Delivery and Formatting it to get the required format

            s=str(year)
            if len(str(month))==1:
                s+="/0"+str(month)
            else:
                s+="/"+str(month)

            if len(str(date))==1:
                s+"/0"+str(date)
            else:
                s+="/"+str(date)
            return s


        def tot():                              #For Calculation of Total and Subtotal
            
            mp=float(mpvar.get())
            mobiles=20000

            lap=float(lapvar.get())
            laptops=50000

            tab=float(tabvar.get())
            tablets=30000

            pc=float(pcvar.get())
            pcs=70000

            tv=float(tvvar.get())
            tvs=35000
            
            mo=float(movar.get())
            monitors=10000

            subtot=(mp*mobiles)+(lap*laptops)+(tab*tablets)
            +(pc*pcs)+(tv*tvs)+(mo*monitors)
            stotvar.set(str(subtot))

            tax=18/100

            total=subtot+(tax*subtot)
            totvar.set(str(total))


        def gen_id():                           #For Generating Unique Customer ID everytime
            
            g=''.join(random.choice('0123456789ABCDEFGHIJKLMONPQRSTUVWXYZ')
                      for i in range(7))
            if g not in c_id():
                c_ref_var.set(g)

            else:
                gen_id()

        gen_id()

        def receipt():                           #For Calculating Total and Subtotal, Displaying Receipt and Affecting Database
            global s

            txt.delete(1.0,END)

            mp=float(mpvar.get())
            mobiles=20000

            lap=float(lapvar.get())
            laptops=50000

            tab=float(tabvar.get())
            tablets=30000

            pc=float(pcvar.get())
            pcs=70000

            tv=float(tvvar.get())
            tvs=35000
            
            mo=float(movar.get())
            monitors=10000

            subtot=(mp*mobiles)+(lap*laptops)
            +(tab*tablets)+(pc*pcs)+(tv*tvs)+(mo*monitors)

            tax=18/100
            total=subtot+(tax*subtot)


            s=random.randint(10000,99999)
            if checkdate(yearomvar.get(),monthomvar.get(),
                         dateomvar.get())==True:           #Checking for Valid Date at the time of Generating Bill

                if total!=0 and c_name_var.get()!="" and c_kp_var.get()!='' and c_kpno_var.get()!='' and c_kpno_var.get().isdigit() and c_no_var.get().isdigit():           #Checking for Valid Details at the time of Generating Bill

                    cursor.execute("select STOCK from stock")

                    x=cursor.fetchall()

                    y=(i[0] for i in x)

                    print(y)


                    if min(y)<=0:

                        #Checking for Unavailability of Product

                        tm.showinfo("Reorder",
                                    "Due to unavailabilty of specific products the entire stock has been refilled")       
                        reset_stock()
                    
                    
                    #----------------------------------------Displaying Receipt-----------------------------------

                    txt.insert(END,"\t\t\tGadget Zone\n")

                    txt.insert(END,"Invoice no:"+ str(s)
                               + "\t\t\t\tPhone no. 9898989898\nCustomer Ref No.:"
                               +str(c_ref_var.get())+ "\t\t\t\tDate:"+ str(today))
                    txt.insert(END,"\n-----------------------------------------------------------")
                    txt.insert(END,"\n\n-----------------------------------------------------------\n")

                    txt.insert(END,"Products\t\t\tQty\tPrice\t\tAmount\n\n")

                    if mp!=0:
                        txt.insert(END,"Mobile Phone\t\t\t"+ str(int(mp))
                                   +"\t"+ str(mobiles) +"\t\t"+str(mp*mobiles)+"\n\n")

                    if tab!=0:
                        txt.insert(END,"Tablet\t\t\t"+ str(int(tab))
                                   +"\t"+ str(tablets) +"\t\t"+str(tab*tablets)+"\n\n")

                    if lap!=0:
                        txt.insert(END,"Laptop\t\t\t"+ str(int(lap))
                                   +"\t"+ str(laptops) +"\t\t"+str(lap*laptops)+"\n\n")

                    if pc!=0:
                        txt.insert(END,"Desktop\t\t\t"+ str(int(pc))
                                   +"\t"+ str(pcs) +"\t\t"+str(pc*pcs)+"\n\n")

                    if tv!=0:
                        txt.insert(END,"TV\t\t\t"+ str(int(tv))
                                   +"\t"+ str(tvs) +"\t\t"+str(tv*tvs)+"\n\n")

                    if mo!=0:
                        txt.insert(END,"Monitors\t\t\t"+ str(int(mo))
                                   +"\t"+ str(monitors) +"\t\t"+str(mo*monitors)+"\n\n\n")

                    if checkdate(yearomvar.get(),monthomvar.get(),
                                 dateomvar.get())==True:
                        txt.insert(END,"Delivery Date:"+str(dateomvar.get())
                                   +"/"+str(monthomvar.get())+"/"+str(yearomvar.get())+"\n\n")

                    txt.insert(END,"SUBTOTAL:\t\t\t\t\t\t"+ str(subtot)+"\n\n")
                    txt.insert(END,"Tax (CGST+SGST):  18%\n\n")

                    txt.insert(END,"GRAND TOTAL(Incl of taxes):\t\t\t\t\t\t"+str(total))
                    
                    
                    tm.showinfo("Conifrmation ","Your order has been placed successfully")
                    

                    #--------------------------Database operations--------------------------------------------------
                        
                    
                    #CHANGING FOR MOBILE
                    cursor.execute("UPDATE stock SET STOCK=STOCK-"
                                   +str(int(mp))+" WHERE PROD_CODE='P001'")
                    con.commit()

                    cursor.execute("UPDATE sales SET UNIT_SOLD=UNIT_SOLD+"
                                   +str(int(mp))+" WHERE PROD_NAME='Mobile Phone'")
                    con.commit()

                    #CHANGING FOR TABLETS
                    cursor.execute("UPDATE stock SET STOCK=STOCK-"
                                   +str(int(tab))+" WHERE PROD_CODE='P002'")
                    con.commit()
                    
                    cursor.execute("UPDATE sales SET UNIT_SOLD=UNIT_SOLD+"
                                   +str(int(tab))+" WHERE PROD_NAME='Tablet'")
                    con.commit()

                    #CHANGING FOR LAPTOPS
                    cursor.execute("UPDATE stock SET STOCK=STOCK-"
                                   +str(int(lap))+" WHERE PROD_CODE='P003'")
                    con.commit()

                    cursor.execute("UPDATE sales SET UNIT_SOLD=UNIT_SOLD+"
                                   +str(int(lap))+" WHERE PROD_NAME='Laptop'")
                    con.commit()

                    #CHANGING FOR TV
                    cursor.execute("UPDATE stock SET STOCK=STOCK-"
                                   +str(int(tv))+" WHERE PROD_CODE='P004'")
                    con.commit()

                    cursor.execute("UPDATE sales SET UNIT_SOLD=UNIT_SOLD+"
                                   +str(int(tv))+" WHERE PROD_NAME='Television'")
                    con.commit()

                    #CHANGING FOR PC
                    cursor.execute("UPDATE stock SET STOCK=STOCK-"
                                   +str(int(pc))+" WHERE PROD_CODE='P005'")
                    con.commit()

                    cursor.execute("UPDATE sales SET UNIT_SOLD=UNIT_SOLD+"
                                   +str(int(pc))+" WHERE PROD_NAME='Desktop'")
                    con.commit()

                    #CHANGING FOR MONITOR
                    cursor.execute("UPDATE stock SET STOCK=STOCK-"
                                   +str(int(mo))+" WHERE PROD_CODE='P006'")
                    con.commit()

                    cursor.execute("UPDATE sales SET UNIT_SOLD=UNIT_SOLD+"
                                   +str(int(mo))+" WHERE PROD_NAME='Monitor'")
                    con.commit()

                    gen_id()

                    
                    x="insert into customer(Customer_Name,C_ID,KeyPerson_Name,Mobiles,Tablets,Laptop,Television,Desktop,Monitor,Delivery_Date,Total)values('"+str(c_name_var.get())+"','"+str(c_ref_var.get())+"','"+str(c_kp_var.get())+"',"+str(int(mp))+","+str(int(tab))+","+str(int(lap))+","+str(int(tv))+","+str(int(pc))+","+str(int(mo))+",'"+get_date(yearomvar.get(),monthomvar.get(),dateomvar.get())+"',"+str(int(total))+")"
                    
                    cursor.execute(x)
                    con.commit()

                    #---------------------------------------------------------------------------------------------------

                else:                           #Displaying Error if Invalid Details are Entered

                    tm.showwarning("Inalid Details ","Please check the input details")
                    
        
        def print_bill():                        #For Printing the receipt
            

            t=txt.get("1.0",END)

            printer=Toplevel()
            printer.geometry("600x600")
            printer.resizable(False,False)
            printer.config(bg="ivory3")

            l=Label(printer,relief=RIDGE,
                    bg="ivory3").place(x=0,y=0,height=525)

            txt_box=Text(printer,font=("Courier",12))
            txt_box.pack(fill=BOTH)

            txt_box.insert("1.0",t)

            
            
            def printing():
                
                global z

                txt_box.delete("1.0",END)
                    
                mp=float(mpvar.get())
                mobiles=20000

                lap=float(lapvar.get())
                laptops=50000

                tab=float(tabvar.get())
                tablets=30000

                pc=float(pcvar.get())
                pcs=70000

                tv=float(tvvar.get())
                tvs=35000
                
                mo=float(movar.get())
                monitors=10000

                subtot=(mp*mobiles)+(lap*laptops)
                +(tab*tablets)+(pc*pcs)+(tv*tvs)+(mo*monitors)

                tax=18/100
                total=subtot+(tax*subtot)

                txt_box.insert(END,"\t\t\tGadget Zone\n")

                txt_box.insert(END,"Invoice no:"+ str(s) +
                               "\t\t\t\tPhone no.: 9898989898\nCustomer Ref No.:"+
                               str(c_ref_var.get())+ "\t\t\tDate:"+ str(today))
                txt_box.insert(END,"\n---------------------------------------------------------------------")
                txt_box.insert(END,"\n---------------------------------------------------------------------\n")

                txt_box.insert(END,"Products\t\tQty\tPrice\t\tAmount\n\n")

                if mp!=0:
                    txt_box.insert(END,"Mobile Phone\t\t"+ str(int(mp)) +
                                   "\t"+ str(mobiles) +"\t\t"+str(mp*mobiles)+"\n\n")

                if tab!=0:
                    txt_box.insert(END,"Tablet\t\t\t"+ str(int(tab)) +"\t"
                                   + str(tablets) +"\t\t"+str(tab*tablets)+"\n\n")

                if lap!=0:
                    txt_box.insert(END,"Laptop\t\t\t"+ str(int(lap)) +"\t"
                                   + str(laptops) +"\t\t"+str(lap*laptops)+"\n\n")

                if pc!=0:
                    txt_box.insert(END,"Desktop\t\t\t"+ str(int(pc)) +"\t"
                                   + str(pcs) +"\t\t"+str(pc*pcs)+"\n\n")

                if tv!=0:
                    txt_box.insert(END,"TV\t\t\t"+ str(int(tv)) +"\t"
                                   + str(tvs) +"\t\t"+str(tv*tvs)+"\n\n")

                if mo!=0:
                    txt_box.insert(END,"Monitors\t\t"+ str(int(mo)) +"\t"
                                   + str(monitors) +"\t\t"+str(mo*monitors)+"\n\n\n")

                if checkdate(yearomvar.get(),monthomvar.get(),
                             dateomvar.get())==True:
                    txt_box.insert(END,"Delivery Date:"+str(dateomvar.get())
                                   +"/"+str(monthomvar.get())+"/"
                                   +str(yearomvar.get())+"\n\n")

                txt_box.insert(END,"SUBTOTAL:\t\t\t\t\t"+ str(subtot)+"\n\n")
                txt_box.insert(END,"Tax (CGST+SGST):  18%\n\n")

                txt_box.insert(END,"GRAND TOTAL(Incl of taxes):\t\t\t"
                               +str(total)+'\n\n')
            

                z=txt_box.get("1.0",END)

                p=tempfile.mktemp(".txt")
                open(p,"w").write(z)
                os.startfile(p,"print")

                printer.destroy()

                #Saving the file

                f=filedialog.asksaveasfile(mode="w",defaultextension=".txt ")
                f.write(z)
                f.close()                                
                        
            Print=Button(printer,padx=48,pady=10,bd=8,
                         fg="black",bg="white",font=("Ariel",10,"bold"),
                         width=10,text="PRINT AND SAVE",
                         command=printing).place(x=100,y=500)
            
            Cancel=Button(printer,padx=48,pady=10,bd=8,
                          fg="black",bg="white",font=("Ariel",10,"bold"),
                          width=10,text="CANCEL",
                          command=printer.destroy).place(x=300,y=500)
                

            
        #-------------------------------Frame1 Customer Details-------------------------------------------------------------------------------------


        frame1=LabelFrame(r,relief=RAISED,bd=8,bg="ivory2")
        frame1.place(x=0,y=75,height=750,relwidth=0.3)
        c_info_label=Label(frame1,text="Customer Info",
                           font=("Calibri",25,"bold"),bg="Blue",
                           fg="White").pack(fill=X)

        c_ref_l=Label(frame1,text="Customer ref. no.:",
                      font=("Times new roman",18,"bold"),padx=2,
                      bg="powder blue",fg="black",relief=SUNKEN).place(x=0,y=70)
        c_ref_t=Entry(frame1,font=("Times New Roman",15),
                      width=22,textvariable=c_ref_var).place(x=210,y=70)
        
        c_name_l=Label(frame1,text="Customer name:",
                       font=("Times new roman",18,"bold"),padx=2,
                       bg="powder blue",fg="black",relief=SUNKEN).place(x=0,y=170)
        c_name_t=Entry(frame1,font=("Times New Roman",15),
                       width=22,textvariable=c_name_var).place(x=210,y=170)

        c_no_l=Label(frame1,text="Customer Ph. No.:",
                     font=("Times new roman",18,"bold"),padx=2,
                     bg="powder blue",fg="black",relief=SUNKEN).place(x=0,y=270)
        c_no_t=Entry(frame1,font=("Times New Roman",15),
                     width=22,textvariable=c_no_var).place(x=210,y=270)

        c_email_l=Label(frame1,text="Customer email id:",
                        font=("Times new roman",18,"bold"),padx=2,
                        bg="powder blue",fg="black",relief=SUNKEN).place(x=0,y=370)
        c_email_t=Entry(frame1,font=("Times New Roman",15),
                        width=22,textvariable=c_email_var).place(x=210,y=370)

        c_kp_l=Label(frame1,text="Contact Person:",
                     font=("Times new roman",18,"bold"),padx=2,
                     bg="powder blue",fg="black",relief=SUNKEN).place(x=0,y=470)
        c_kp_t=Entry(frame1,font=("Times New Roman",15),
                     width=22,textvariable=c_kp_var).place(x=210,y=470)

        c_kpno_l=Label(frame1,text="ContactPerson Ph.No:",
                       font=("Times new roman",16,"bold"),padx=2,
                       bg="powder blue",fg="black",relief=SUNKEN).place(x=0,y=570)
        c_kpno_t=Entry(frame1,font=("Times New Roman",15),
                       width=22,textvariable=c_kpno_var).place(x=210,y=570)


        #-------------------------------Frame2 Order Details----------------------------------------------------------------------------------------

        frame2=LabelFrame(r,relief=RAISED,bd=8,bg="ivory2")
        frame2.place(x=462,y=75,relwidth=0.3,height=750)
        order_details_label=Label(frame2,text="Order Details",
                                  font=("Calibri",25,"bold"),bg="Blue",fg="White").pack(fill=X)

        o_mp_l=Label(frame2,text="Mobile Phone:",
                     font=("Times new roman",18,"bold"),padx=2,
                     bg="powder blue",fg="black",relief=SUNKEN).place(x=0,y=70)
        o_mp_t=Entry(frame2,font=("Times New Roman",15),
                     width=10,textvariable=mpvar).place(x=300,y=70)

        o_tab_l=Label(frame2,text="Tablet:",
                      font=("Times new roman",18,"bold"),padx=2,
                      bg="powder blue",fg="black",relief=SUNKEN).place(x=0,y=120)
        o_tab_t=Entry(frame2,font=("Times New Roman",15),
                      width=10,textvariable=tabvar).place(x=300,y=120)

        o_lap_l=Label(frame2,text="Laptop:",
                      font=("Times new roman",18,"bold"),padx=2,
                      bg="powder blue",fg="black",relief=SUNKEN).place(x=0,y=170)
        o_lap_t=Entry(frame2,font=("Times New Roman",15),
                      width=10,textvariable=lapvar).place(x=300,y=170)

        o_tv_l=Label(frame2,text="Television:",
                     font=("Times new roman",18,"bold"),padx=2,
                     bg="powder blue",fg="black",relief=SUNKEN).place(x=0,y=220)
        o_tv_t=Entry(frame2,font=("Times New Roman",15),
                     width=10,textvariable=tvvar).place(x=300,y=220)

        o_pc_l=Label(frame2,text="Desktop:",
                     font=("Times new roman",18,"bold"),padx=2,
                     bg="powder blue",fg="black",relief=SUNKEN).place(x=0,y=270)
        o_pc_t=Entry(frame2,font=("Times New Roman",15),
                     width=10,textvariable=pcvar).place(x=300,y=270)

        o_mo_l=Label(frame2,text="Monitor:",
                     font=("Times new roman",18,"bold"),padx=2,
                     bg="powder blue",fg="black",relief=SUNKEN).place(x=0,y=320)
        o_mo_t=Entry(frame2,font=("Times New Roman",15),
                     width=10,textvariable=movar).place(x=300,y=320)

        o_expdel_l=Label(frame2,text="Delivery Date:",
                         font=("Times new roman",18,"bold"),padx=2,
                         bg="powder blue",fg="black",relief=SUNKEN).place(x=0,y=380)

        o_expdel_date=OptionMenu(frame2,dateomvar,
                                 *datelist).place(x=250,y=380)
        o_expdel_month=OptionMenu(frame2,monthomvar,
                                  *monthlist).place(x=300,y=380)
        o_expdel_year=OptionMenu(frame2,yearomvar,
                                 *yearlist).place(x=350,y=380)

        b=Button(frame2,padx=48,pady=8,bd=8,fg="black",
                 bg="white",font=("Ariel",10,"bold"),width=10,
                 text="RESET",command=reset).place(x=100,y=450)

        tot=Button(frame2,padx=48,pady=8,bd=8,fg="black",
                   bg="white",font=("Ariel",10,"bold"),width=10,
                   text="TOTAL",command=tot).place(x=100,y=520)

        o_stot_l=Label(frame2,text="Subtotal:",
                       font=("Times new roman",18,"bold"),padx=2,
                       bg="powder blue",fg="black",relief=SUNKEN).place(x=0,y=600)
        o_stot_t=Entry(frame2,font=("Times New Roman",15),
                       width=13,textvariable=stotvar).place(x=300,y=600)

        o_tot_l=Label(frame2,text="Total (Incl of Taxes):",
                      font=("Times new roman",18,"bold"),padx=2,
                      bg="powder blue",fg="black",relief=SUNKEN).place(x=0,y=650)
        o_tot_t=Entry(frame2,font=("Times New Roman",15),
                      width=13,textvariable=totvar).place(x=300,y=650)


        #-------------------------------Frame3 Billing ---------------------------------------------------------------------------------------------

        frame3=LabelFrame(r,relief=RAISED,bd=8,bg="ivory2")
        frame3.place(x=923,y=75,relwidth=0.4,height=100)

        billing_label=Label(frame3,text="Billing Area ",
                            font=("Calibri",25,"bold"),bg="Blue",fg="White").pack(fill=X)

        btitle=Label(frame3,text="Invoice",font=("Ariel",20),
                     bd=8,relief=SUNKEN,).pack(fill=X)


        #------------------------------Frame4 Billing Buttons---------------------------------------------------------------------------------------

        frame4=LabelFrame(r,relief=SUNKEN,bd=7.6,bg="ivory2")
        frame4.place(x=923,y=695,height=125,relwidth=0.4)

        b_gbill=Button(frame4,padx=48,pady=10,bd=8,fg="black",
                       bg="white",font=("Ariel",10,"bold"),width=10,
                       text="GENERATE BILL",command=receipt).place(x=0,y=15)
                           
        b_reset=Button(frame4,padx=48,pady=10,bd=8,fg="black",
                       bg="white",font=("Ariel",10,"bold"),width=10,
                       text="PRINT BILL",command=print_bill).place(x=201,y=15)
                           
        b_exit=Button(frame4,padx=48,pady=10,bd=8,fg="black",
                      bg="white",font=("Ariel",10,"bold"),width=10,
                      text="QUIT",command=r.destroy).place(x=402,y=15)

        #------------------------------Frame5 Receipt-----------------------------------------------------------------------------------------------

        frame5=LabelFrame(r,relief=RAISED,bd=7,bg="white")
        frame5.place(x=923,y=170,height=525,relwidth=0.399999999999)

        bill=Label(frame5,text="",font=("Ariel",20,"bold")).pack(fill=X)

        txt=Text(frame5,font=("Courier",12))
        txt.pack(fill=BOTH)
        
#---------------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------Execution-------------------------------------------------------------------------------------
if __name__ =="__main__":
    x=Tk()
    app_=Inventory(x)
    x.mainloop()

#----------------------------------------------------END--OF--PROJECT-------------------------------------------------------------------------------
