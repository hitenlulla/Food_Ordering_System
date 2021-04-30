from tkinter import *
from tkinter import messagebox
from datetime import *
from PIL import ImageTk,Image
from tkinter import scrolledtext
from tkinter import messagebox
import os.path
import datetime
import random
import mysql.connector
import smtplib


#Declaring User defined exception
class MyEx(Exception):
	def __init__(self, msg):
		self.msg = msg

#Back-End of TBS
class Product:
	def __init__(self,name,price,qty):
		self.name = name
		self.price = price
		self.qty = qty

	def getName(self):
		return self.name

	def getPrice(self):
		return self.price

	def getQty(self):
		return self.qty

#Database:
veg_burger = Product("Veg Burger",100,1)
chicken_burger = Product("Chicken Burger",150,1)
mutton_burger = Product("Mutton Burger",200,1)

coke_bev = Product("Coke",50,1)
sprite_bev = Product("Sprite",50,1)
fanta_bev = Product("Fanta",50,1)

french_fry = Product("French Fries",75,1)
onion_ring = Product("Onion Rings",75,1)

paneer_bbq = Product("Paneer Bbq",150,1)
chicken_bbq = Product("Chicken Bbq",200,1)
prawns_bbq = Product("Prawns Bbq",200,1)

cheese_des = Product("Cheese Cake",150,1)
choco_des = Product("Chocolate Truffle",150,1)

#Inititalising Billing database
con = None
cursor = None
try:
	con = mysql.connector.connect(user = 'root',password = 'abcd1234',host = 'localhost')
	print("Connected to database")
	cursor = con.cursor()
	sql1 = "create database if not exists bill;"
	cursor.execute(sql1)
	sql3 = "use bill;"
	cursor.execute(sql3)
	sql2 = "create table if not exists bill(name varchar(30), price int, qty int);"
	cursor.execute(sql2)
	print("Table Bill created")
except Exception as e:
	messagebox.showerror(e)
	con.rollback()
finally:
	cursor.close()
	if con is not None:
		con.close()

#Creating and updating the cart list
data = ""
cart_list = []
bill = []
num = random.randrange(100,999)

#Front End of TBS
#Main page of TBS
root = Tk()
root.title("TBS-Online Order System")
root.geometry("640x450+400+200")

canvas = Canvas(root,width = 700, height = 550)
canvas.pack()

bgImage = ImageTk.PhotoImage(Image.open('root/TBS.jpg'))
canvas.create_image(280,150,image = bgImage)

canvas.create_text(450,30,fill="Red",font="Times 35 italic bold",text="The Burger Surfer")

canvas.create_line(300, 42, 436, 42)
canvas.create_line(450, 42, 544, 42)
canvas.create_line(550, 42, 600, 42)

def order():
	root.withdraw()
	order.deiconify()

#Cart Page using scrolled text to display the cart
def cart():
	
	con = None
	cursor = None
	try:
		con = mysql.connector.connect(user = 'root',password = 'abcd1234',host = 'localhost')
		cursor = con.cursor()
		sql = "use bill;"
		cursor.execute(sql)
		for c in cart_list:
			name = c.getName()
			price = c.getPrice()
			qty = c.getQty()
			sql = "insert into bill values('%s','%d','%d')"
			args = (name,price,qty)
			cursor.execute(sql % args)
			con.commit()

		sql = "select * from bill;"
		cursor.execute(sql)
		bill = cursor.fetchall()

		if len(cart_list) == 0:
			raise MyEx("Cart Empty")
		else:
			root.withdraw()
			cart.deiconify()
			foodData.delete('1.0',END)
			msg = "Name of Item            Price     Qty\n" +"---------------------------------------\n"
			for c in cart_list:
				namex = c.getName()
				ls = 25 - len(namex)
				pricex = c.getPrice()
				ls2 = 10 - len(str(pricex))
				qtyx = c.getQty()
				msg += str(namex) + (" " *ls) + str(pricex)+ (" " *ls2) + str(qtyx)+"\n"
			foodData.insert(INSERT,msg)

			total = 0
			for c in cart_list:
				total += c.getPrice() * c.getQty()
			foodData.insert(INSERT,"\n\n")
			totalmsg = "Total Amount:            " + str(total)
			foodData.insert(INSERT,totalmsg)
	except MyEx as e:
		messagebox.showerror("Error",e)
	except Exception as e:
		messagebox.showerror(e)
		con.rollback()
	finally:
		cursor.close()
		if con is not None:
			con.close()

#Check-out Page for bill creation and mailing
def checkout():

	try:
		if len(cart_list) == 0:
			raise MyEx("Cart Empty")	
		else:
			total = 0
			msg = ""
			dt = datetime.datetime.now().date()
			time = datetime.datetime.today().time()
			dt = str(dt)
			day = dt[8:10]
			month = dt[5:7]
			year = dt[0:4]
			dt = day + "-" + month +"-" + year
			date = "Date:" + dt + "\n" +"Time:"+str(time)[0:8]
			msg = "Name of Item            Price     Qty\n" +"---------------------------------------\n"
			for c in cart_list:
				namex = c.getName()
				ls = 25 - len(namex)
				pricex = c.getPrice()
				ls2 = 10 - len(str(pricex))
				qtyx = c.getQty()
				msg += str(namex) + (" " *ls) + str(pricex)+ (" " *ls2) + str(qtyx)+"\n"
			
			for c in cart_list:
				total += c.getPrice() * c.getQty()
			totalmsg = "Total Amount:         Rs." + str(total)

			#Login page for Gmail details
			login.deiconify()

			#File-Handling for Bill
			filename = "bill.txt"
			if os.path.exists(filename):
				f = None
				try:
					f = open(filename,"w")
					data = "Bill no: "+ str(num) +"\n" + msg +"\n\n" + totalmsg + "\n\n" + date
					f.write(data +"\n")					
				except Exception as e:
					messagebox.showerror("Error",e)
				finally:
					f.close()
			else:
				messagebox.showerror("Error","File not found")
	except MyEx as e:
		messagebox.showerror("Error",e)

btnOrder = Button(root,text = 'Order',width = 13, font = ('roman',25,'bold'),command = order)
btnOrderWindow =canvas.create_window(450,90, window = btnOrder)

btnCart = Button(root,text = 'Cart',width = 13, font = ('roman',25,'bold'), command = cart)
btnOrderWindow =canvas.create_window(450,140, window = btnCart)

btnCheckout = Button(root,text = 'Checkout',width = 13, font = ('roman',25,'bold'),command = checkout)
btnOrderWindow =canvas.create_window(450,190, window = btnCheckout)


#Login Page
login = Toplevel(root)
login.title("Login")
login.geometry("300x200+550+300")
login.configure(background = "White")


def loginEmail():
	eid = str(entEmailId.get())
	epd = str(entPwd.get())
	to = 'theburgersurfer@gmail.com'
	subject = "Order no:-" + str(num)

	text = ""
	dt = datetime.datetime.now().date()
	time = datetime.datetime.today().time()
	dt = str(dt)
	day = dt[8:10]
	month = dt[5:7]
	year = dt[0:4]
	dt = day + "-" + month +"-" + year
	date = "Date:" + dt + "\n" +"Time:"+str(time)[0:8]
	text = "Name of item- Qty\n" + ("-" * 25) + "\n" 

	for c in cart_list:
		namex = c.getName()
		qtyx = c.getQty()
		text += str(namex) + "-" + str(qtyx)+"\n"

	total = 0
	for c in cart_list:
		total += c.getPrice() * c.getQty()
	totalmsg = "Total Amount: Rs." + str(total)
	text += "\n\n" + totalmsg + "\n\n" + date

	sender = eid
	password = epd
	message = 'Subject: {}\n\n{}'.format(subject,text)
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.ehlo()
	server.starttls()
	server.login(sender,password)
	print("Logged In")
	try:
		server.sendmail(sender,to,message)
		print("Email Sent")
		login.withdraw()
		messagebox.showinfo("Information","Order confirmed\nBill Ready")
		root.destroy()
	except:
		print("Error in sending Email")
	finally:
		server.quit()

emailId = Label(login,text = "Gmail-Id:",font = ('roman',20,'bold'))
emailId.pack(pady = 5)

entEmailId = Entry(login, bd = 5)
entEmailId.pack(pady = 2)

pwd = Label(login, text = "Password:",font = ('roman',20,'bold'))
pwd.pack(pady = 5)

entPwd = Entry(login,show = "*", bd = 5)
entPwd.pack(pady = 2)

confirmButton = Button(login, text = "Confirm",width = 10, command = loginEmail)
confirmButton.pack(pady = 10)
login.withdraw()

#'Order' Page of TBS

order = Toplevel(root)
order.title("Menu")
order.geometry("650x600+400+150")
order.configure(background = "Black")

def burgersMenu():
	order.withdraw()
	brg.deiconify()

def beveragesMenu():
	order.withdraw()
	bev.deiconify()

def friesMenu():
	order.withdraw()
	fry.deiconify()

def barbequeMenu():
	order.withdraw()
	bbq.deiconify()

def desertsMenu():
	order.withdraw()
	des.deiconify()

def backToRoot():
	order.withdraw()
	root.deiconify()

imgBurger = Image.open('root/Menu/Burgers.jpg')
imgBurger = imgBurger.resize((200,200), Image.ANTIALIAS)
imgBurger = ImageTk.PhotoImage(imgBurger)
lblBurger = Label(order, image = imgBurger)
lblBurger.place(x=60,y=20)
btnBurger = Button(order, text = "Burgers",width = 12,font = ('roman',20),command = burgersMenu)
btnBurger.place(x=85,y=230)

imgBeverages = Image.open('root/Menu/Beverages.jpg')
imgBeverages = imgBeverages.resize((200,200), Image.ANTIALIAS)
imgBeverages = ImageTk.PhotoImage(imgBeverages)
lblBeveragesFries = Label(order, image = imgBeverages)
lblBeveragesFries.place(x=370,y=20)
btnBeverages = Button(order, text = "Beverages",width = 12,font = ('roman',20),command = beveragesMenu)
btnBeverages.place(x=395,y=230)


imgFries = Image.open('root/Menu/Fries.jpg')
imgFries = imgFries.resize((170,170), Image.ANTIALIAS)
imgFries = ImageTk.PhotoImage(imgFries)
lblFries = Label(order, image = imgFries)
lblFries.place(x=30,y=320)
btnFries = Button(order, text = "Fries",width = 10,font = ('roman',20), command = friesMenu)
btnFries.place(x=50,y=500)

imgBarbeque = Image.open('root/Menu/Barbeque.jpg')
imgBarbeque = imgBarbeque.resize((170,170), Image.ANTIALIAS)
imgBarbeque = ImageTk.PhotoImage(imgBarbeque)
lblBarbeque = Label(order, image = imgBarbeque)
lblBarbeque.place(x=240,y=320)
btnBarbeque = Button(order, text = "Barbeque",width = 10,font = ('roman',20), command = barbequeMenu)
btnBarbeque.place(x=260,y=500)

imgDeserts = Image.open('root/Menu/Deserts.jpeg')
imgDeserts = imgDeserts.resize((170,170), Image.ANTIALIAS)
imgDeserts = ImageTk.PhotoImage(imgDeserts)
lblDeserts = Label(order, image = imgDeserts)
lblDeserts.place(x=450,y=320)
btnDeserts = Button(order, text = "Desserts",width = 10,font = ('roman',20), command = desertsMenu)
btnDeserts.place(x=470,y=500)

imgBack = Image.open('root/Back.png')
imgBack = imgBack.resize((10,10), Image.ANTIALIAS)
imgBack = ImageTk.PhotoImage(imgBack)
backBtn = Button(order, text = "Back", width = 5, image = imgBack, compound = LEFT, command = backToRoot)
backBtn.place(x = 590, y = 570)
order.withdraw()

#Burger-Menu

def vBurg():
	x = veg_burger
	if x in cart_list:
		x.qty += 1
	else:
		cart_list.append(veg_burger)

def mBurg():
	x = mutton_burger
	if x in cart_list:
		x.qty += 1
	else:
		cart_list.append(mutton_burger)

def cBurg():
	x = chicken_burger
	if x in cart_list:
		x.qty += 1
	else:
		cart_list.append(chicken_burger)

def backToOrder():
	brg.withdraw()
	fry.withdraw()
	bbq.withdraw()
	des.withdraw()
	bev.withdraw()
	order.deiconify()


def nextToFries():
	brg.withdraw()
	fry.deiconify()

brg = Toplevel(order)
brg.title("Burgers")
brg.geometry("740x310+350+300")
brg.configure(background = "White")

imgBurger1 = Image.open('root/Burgers/VegBurger.jpg')
imgBurger1 = imgBurger1.resize((250,250), Image.ANTIALIAS)
imgBurger1 = ImageTk.PhotoImage(imgBurger1)
lblBurger1 = Label(brg, image = imgBurger1)
lblBurger1.place(x=0,y=0)
btnBurger1 = Button(brg, text = "Veg-Burger",width = 12,font = ('roman',20), command = vBurg)
btnBurger1.place(x=50,y=240)

imgBurger2 = Image.open('root/Burgers/MuttonBurger.jpg')
imgBurger2 = imgBurger2.resize((300,250), Image.ANTIALIAS)
imgBurger2 = ImageTk.PhotoImage(imgBurger2)
lblBurger2 = Label(brg, image = imgBurger2)
lblBurger2.place(x=230,y=0)
btnBurger2 = Button(brg, text = "Mutton-Burger",width = 12,font = ('roman',20), command = mBurg)
btnBurger2.place(x=290,y=240)


imgBurger3 = Image.open('root/Burgers/ChickenBurger.jpg')
imgBurger3 = imgBurger3.resize((250,250), Image.ANTIALIAS)
imgBurger3 = ImageTk.PhotoImage(imgBurger3)
lblBurger3 = Label(brg, image = imgBurger3)
lblBurger3.place(x=480,y=0)
btnBurger3 = Button(brg, text = "Chicken-Burger",width = 12,font = ('roman',20), command = cBurg)
btnBurger3.place(x=530,y=240)

imgBack1 = Image.open('root/Back.png')
imgBack1 = imgBack1.resize((10,10), Image.ANTIALIAS)
imgBack1 = ImageTk.PhotoImage(imgBack1)
backBtn1 = Button(brg, text = "Back", width = 5, image = imgBack1, compound = LEFT, command = backToOrder)
backBtn1.place(x = 10, y = 280)

imgNext1 = Image.open('root/Next.jpg')
imgNext1 = imgNext1.resize((10,10), Image.ANTIALIAS)
imgNext1 = ImageTk.PhotoImage(imgNext1)
NextBtn1 = Button(brg, text = "Next", width = 5, image = imgNext1, compound = RIGHT, command = nextToFries)
NextBtn1.place(x = 680, y = 280)

brg.withdraw()

#Fries-Menu
def fFry():
	x = french_fry
	if x in cart_list:
		x.qty += 1
	else:
		cart_list.append(french_fry)


def oFry():
	x = onion_ring
	if x in cart_list:
		x.qty += 1
	else:
		cart_list.append(onion_ring)


def nextToBBQ():
	fry.withdraw()
	bbq.deiconify()

fry = Toplevel(order)
fry.title("Fries")
fry.geometry("600x330+400+300")
fry.configure(background = "White")

imgFry1 = Image.open('root/Fries/FrenchFries.jpg')
imgFry1 = imgFry1.resize((250,250), Image.ANTIALIAS)
imgFry1 = ImageTk.PhotoImage(imgFry1)
lblFry1 = Label(fry, image = imgFry1)
lblFry1.place(x=30,y=0)
btnFry1 = Button(fry, text = "French-Fries",width = 12,font = ('roman',20), command = fFry)
btnFry1.place(x=80,y=260)

imgFry2 = Image.open('root/Fries/OnionRings.png')
imgFry2 = imgFry2.resize((250,250), Image.ANTIALIAS)
imgFry2 = ImageTk.PhotoImage(imgFry2)
lblFry2 = Label(fry, image = imgFry2)
lblFry2.place(x=300,y=0)
btnFry2 = Button(fry, text = "Onion-Rings",width = 12,font = ('roman',20), command = oFry)
btnFry2.place(x=350,y=260)

imgBack2 = Image.open('root/Back.png')
imgBack2 = imgBack2.resize((10,10), Image.ANTIALIAS)
imgBack2 = ImageTk.PhotoImage(imgBack2)
backBtn2 = Button(fry, text = "Back", width = 5, image = imgBack2, compound = LEFT, command = backToOrder)
backBtn2.place(x = 20, y = 300)

imgNext2 = Image.open('root/Next.jpg')
imgNext2 = imgNext2.resize((10,10), Image.ANTIALIAS)
imgNext2 = ImageTk.PhotoImage(imgNext2)
NextBtn2 = Button(fry, text = "Next", width = 5, image = imgNext2, compound = RIGHT, command = nextToBBQ)
NextBtn2.place(x = 530, y = 300)

fry.withdraw()

#BBQ-Menu

def cBbq():
	x = chicken_bbq
	if x in cart_list:
		x.qty += 1
	else:
		cart_list.append(chicken_bbq)


def paBbq():
	x = paneer_bbq
	if x in cart_list:
		x.qty += 1
	else:
		cart_list.append(paneer_bbq)


def prBbq():
	x = prawns_bbq
	if x in cart_list:
		x.qty += 1
	else:
		cart_list.append(prawns_bbq)


def nextToBev():
	bbq.withdraw()
	bev.deiconify()

bbq = Toplevel(order)
bbq.title("Barbeque")
bbq.geometry("900x340+300+300")
bbq.configure(background = "Black")

imgBbq1 = Image.open('root/Barbeque/Paneer.jpg')
imgBbq1 = imgBbq1.resize((250,250), Image.ANTIALIAS)
imgBbq1 = ImageTk.PhotoImage(imgBbq1)
lblBbq1 = Label(bbq, image = imgBbq1)
lblBbq1.place(x=10,y=10)
btnBbq1 = Button(bbq, text = "BBQ-Paneer",width = 12,font = ('roman',20), command = paBbq)
btnBbq1.place(x=50,y=270)

imgBbq2 = Image.open('root/Barbeque/Chicken.jpg')
imgBbq2 = imgBbq2.resize((250,250), Image.ANTIALIAS)
imgBbq2 = ImageTk.PhotoImage(imgBbq2)
lblBbq2 = Label(bbq, image = imgBbq2)
lblBbq2.place(x=320,y=10)
btnBbq2 = Button(bbq, text = "BBQ-Chicken",width = 12,font = ('roman',20), command = cBbq)
btnBbq2.place(x=380,y=270)

imgBbq3 = Image.open('root/Barbeque/Prawns.jpg')
imgBbq3 = imgBbq3.resize((250,250), Image.ANTIALIAS)
imgBbq3 = ImageTk.PhotoImage(imgBbq3)
lblBbq3 = Label(bbq, image = imgBbq3)
lblBbq3.place(x=630,y=10)
btnBbq3 = Button(bbq, text = "BBQ-Prawns",width = 12,font = ('roman',20), command = prBbq)
btnBbq3.place(x=690,y=270)

imgBack3 = Image.open('root/Back.png')
imgBack3 = imgBack3.resize((10,10), Image.ANTIALIAS)
imgBack3 = ImageTk.PhotoImage(imgBack3)
backBtn3 = Button(bbq, text = "Back", width = 5, image = imgBack3, compound = LEFT, command = backToOrder)
backBtn3.place(x = 20, y = 310)

imgNext3 = Image.open('root/Next.jpg')
imgNext3 = imgNext3.resize((10,10), Image.ANTIALIAS)
imgNext3 = ImageTk.PhotoImage(imgNext3)
NextBtn3 = Button(bbq, text = "Next", width = 5, image = imgNext3, compound = RIGHT, command = nextToBev)
NextBtn3.place(x = 830, y = 310)

bbq.withdraw()

#Beverages-Menu

def coke():
	x = coke_bev
	if x in cart_list:
		x.qty += 1
	else:
		cart_list.append(coke_bev)


def sprite():
	x = sprite_bev
	if x in cart_list:
		x.qty += 1
	else:
		cart_list.append(sprite_bev)


def fanta():
	x = fanta_bev
	if x in cart_list:
		x.qty += 1
	else:
		cart_list.append(fanta_bev)


def nextToDes():
	bev.withdraw()
	des.deiconify()

bev = Toplevel(order)
bev.title("Beverages")
bev.geometry("620x270+400+300")
bev.configure(background = "White")

imgBev1 = Image.open('root/SoftDrinks/Coke.jpg')
imgBev1 = imgBev1.resize((175,175), Image.ANTIALIAS)
imgBev1 = ImageTk.PhotoImage(imgBev1)
lblBev1 = Label(bev, image = imgBev1)
lblBev1.place(x=40,y=0)
btnBev1 = Button(bev, text = "Coke",width = 7,font = ('roman',20), command = coke)
btnBev1.place(x=80,y=200)

imgBev2 = Image.open('root/SoftDrinks/Sprite.jpg')
imgBev2 = imgBev2.resize((175,170), Image.ANTIALIAS)
imgBev2 = ImageTk.PhotoImage(imgBev2)
lblBev2 = Label(bev, image = imgBev2)
lblBev2.place(x=220,y=5)
btnBev2 = Button(bev, text = "Sprite",width = 7,font = ('roman',20), command = sprite)
btnBev2.place(x=260,y=200)

imgBev3 = Image.open('root/SoftDrinks/Fanta.jpg')
imgBev3 = imgBev3.resize((175,170), Image.ANTIALIAS)
imgBev3 = ImageTk.PhotoImage(imgBev3)
lblBev3 = Label(bev, image = imgBev3)
lblBev3.place(x=400,y=5)
btnBev3 = Button(bev, text = "Fanta",width = 7,font = ('roman',20), command = fanta)
btnBev3.place(x=440,y=200)

imgBack4 = Image.open('root/Back.png')
imgBack4 = imgBack4.resize((10,10), Image.ANTIALIAS)
imgBack4 = ImageTk.PhotoImage(imgBack4)
backBtn4 = Button(bev, text = "Back", width = 5, image = imgBack4, compound = LEFT, command = backToOrder)
backBtn4.place(x = 20, y = 240)

imgNext4 = Image.open('root/Next.jpg')
imgNext4 = imgNext4.resize((10,10), Image.ANTIALIAS)
imgNext4 = ImageTk.PhotoImage(imgNext4)
NextBtn4 = Button(bev, text = "Next", width = 5, image = imgNext4, compound = RIGHT, command = nextToDes)
NextBtn4.place(x = 550, y = 240)

bev.withdraw()

#Desserts-Menu

def cheeseCake():
	x = cheese_des
	if x in cart_list:
		x.qty += 1
	else:
		cart_list.append(cheese_des)


def chocoTruffle():
	x = choco_des
	if x in cart_list:
		x.qty += 1
	else:
		cart_list.append(choco_des)


des = Toplevel(order)
des.title("Desserts")
des.geometry("500x270+450+300")
des.configure(background = "Black")

imgDes1 = Image.open('root/Desserts/CheeseCake.jpg')
imgDes1 = imgDes1.resize((175,175), Image.ANTIALIAS)
imgDes1 = ImageTk.PhotoImage(imgDes1)
lblDes1 = Label(des, image = imgDes1)
lblDes1.place(x=40,y=10)
btnDes1 = Button(des, text = "Cheese-Cake",width = 12,font = ('roman',20), command = cheeseCake)
btnDes1.place(x=50,y=200)

imgDes2 = Image.open('root/Desserts/ChocTruffle.jpg')
imgDes2 = imgDes2.resize((175,175), Image.ANTIALIAS)
imgDes2 = ImageTk.PhotoImage(imgDes2)
lblDes2 = Label(des, image = imgDes2)
lblDes2.place(x=280,y=10)
btnDes2 = Button(des, text = "Chocolate-Truffle",width = 12,font = ('roman',20), command = chocoTruffle)
btnDes2.place(x=290,y=200)

imgBack5 = Image.open('root/Back.png')
imgBack5 = imgBack5.resize((10,10), Image.ANTIALIAS)
imgBack5 = ImageTk.PhotoImage(imgBack5)
backBtn5 = Button(des, text = "Back", width = 5, image = imgBack4, compound = LEFT, command = backToOrder)
backBtn5.place(x = 20, y = 240)

des.withdraw()

#Cart-Menu

def addItem():
	cart.withdraw()
	order.deiconify()

def removeItem():
	cart.withdraw()
	remo.deiconify()

def home():
	cart.withdraw()
	root.deiconify()

cart = Toplevel(root)
cart.title("Cart")
cart.geometry("400x400+400+200")
cart.configure(background = "White")

foodData = scrolledtext.ScrolledText(cart, width = 45, height = 20)
foodData.pack(pady = 20)

addBtn = Button(cart,text = "Add-Item",command = addItem,font = ('roman',20))
addBtn.place(x=20,y = 350)

homeBtn = Button(cart,text = "Home",command = home,font = ('roman',20))
homeBtn.place(x=140,y = 350)

remBtn = Button(cart,text = "Remove-Item",command = removeItem,font = ('roman',20))
remBtn.place(x=230,y = 350)
cart.withdraw()

def confirm():
	try:
		flag = False
		entName.focus()
		x = entName.get()
		for c in cart_list:
			y = c.getName()
			if x.lower() == y.lower():
				cart_list.remove(c)
				flag = True
				messagebox.showinfo("Information","Item removed from cart")
				entName.delete(0,END)
				entName.focus()
		if len(cart_list) == 0:
			raise MyEx("Cart Empty")
		if flag:
			pass
		else:
			raise MyEx("Element not present in the cart")
	except MyEx as e:
		messagebox.showerror("Error",str(e))

def cancel():
	remo.withdraw()
	root.deiconify()


remo = Toplevel(cart)
remo.geometry("250x170+400+200")
remo.title("Removing an element")
remo.configure(background = "White")

lblName = Label(remo, text = "Name of item:", font = ('roman',20,'bold'))
lblName.pack(pady = 5)

entName = Entry(remo, bd = 5)
entName.pack()

btnConfirm = Button(remo,text = "Confirm", font= ('roman',20,'bold'), command = confirm)
btnConfirm.pack(pady = 5)

btnCancel = Button(remo,text = "Cancel", font= ('roman',20,'bold'), command = cancel)
btnCancel.pack(pady = 5)
remo.withdraw()

root.mainloop()