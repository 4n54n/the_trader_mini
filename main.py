

# import custom modules
from trades import tradeList
import config as configs
api = configs.api


import tkinter as tk


import threading
from time import sleep
from playsound import playsound



height = 33* (len(tradeList)+1)


win = tk.Tk()
win.attributes('-topmost', True)
win.geometry("500x"+str(height))



canvas = tk.Canvas(win, width=500, height=height)

win.title("THE TRADER MINI")



# FUNCTIONS



def resetDefault(symbol):
    stockQuanPlacedButDict[symbol].configure(bg= "yellow", text=0)


def do_beep(beep):

    def make_beep_sound():
        try:
            playsound("alerts/beeps/"+beep)
        except:
            pass

    thread_of_beep = threading.Thread(target=make_beep_sound)
    thread_of_beep.start()


def update_status(orderno):
    def update_title():
        win.title(f"order ID : {orderno}")
        sleep(10)
        win.title("THE TRADER MINI")

    thread_of_update_title = threading.Thread(target=update_title)
    thread_of_update_title.start()


def orderExec(symbol, quantity, rule):
    try:
        if configs.test_mode != 1:

            place_order = api.place_order(buy_or_sell = rule.upper()[0], product_type='I',
            exchange='NSE', tradingsymbol = symbol, 
            quantity= quantity, discloseqty=0,price_type='MKT', price=0, 
            trigger_price=None,
            retention='DAY', remarks='001')

            update_status(place_order["norenordno"])

    except:
        print("order not executed")



def stockExec(symbol, quantity):
    print(symbol, quantity, rule)

    symbol = str(symbol)
    quantity = int(quantity)

    orderExec(symbol, quantity, rule)




    #update stock quantity
    stockQuantity = int(stockQuanPlacedButDict[symbol]['text'])


    if rule == "buy":
        stockQuantity += quantity
        stockQuanPlacedButDict[symbol].configure(text = stockQuantity)

    if rule == "sell":
        stockQuantity -= quantity
        stockQuanPlacedButDict[symbol].configure(text = stockQuantity)



    if stockQuantity < 0:
        stockQuanPlacedButDict[symbol].configure(bg= "#ff6600")
    
    elif stockQuantity > 0:
        stockQuanPlacedButDict[symbol].configure(bg= "#39e75f")

    else:
        stockQuanPlacedButDict[symbol].configure(bg= "yellow")






# change button color, swap buy or sell (right click)


rule = "buy"
buttonBack = "green"
buttonFor = "white"


def on_right_click(event):
    global rule, buttonBack

    if buttonBack == "green":
        rule = "sell"
        for i in quantityButtonNameList:
            i.configure(bg = "red")
        buttonBack = "red"

    elif buttonBack == "red":
        rule = "buy"
        for i in quantityButtonNameList:
            i.configure(bg = "green")
        buttonBack = "green"



canvas.bind("<Button-3>", on_right_click) #Button-3 is mouse right click

canvas.pack()
canvas.focus_set()





#RENDER AREA START





tradingbuttonX = 120
tradingsymbolY = 50
stockQuantity = [5,10,30,50,100,200,300,400,500]

quantityButtonNameList = []  # stock quantity buttons

stockQuanPlacedButDict = {}  # stock quantity placed buttons







# SECTION FOR CUSTOM TRADE START

custom_symbol = tk.Entry(font=("Helvetica 8 bold"), width=10)
custom_symbol.place(x=20, y=20)
custom_symbol.bind("<Button-3>", on_right_click)



def customExec(quantity):
    symbol = str( custom_symbol.get() ).upper()
    if symbol == "":
        return None
    symbol += "-EQ"

    quantity = int(quantity)

    print(symbol, quantity, rule)

    orderExec(symbol, quantity, rule)



    #update stock quantity

    stockQuantity = int(customStockQuanPlacedButName['text'])


    if rule == "buy":
        stockQuantity += quantity
        customStockQuanPlacedButName.configure(text = stockQuantity)

    if rule == "sell":
        stockQuantity -= quantity
        customStockQuanPlacedButName.configure(text = stockQuantity)



    if stockQuantity < 0:
        customStockQuanPlacedButName.configure(bg= "#ff6600")
    
    elif stockQuantity > 0:
        customStockQuanPlacedButName.configure(bg= "#39e75f")

    else:
        customStockQuanPlacedButName.configure(bg= "yellow")




def customResetDefault():
    customStockQuanPlacedButName.configure(bg= "yellow", text=0)


#render stock quantity buttons

posx = 120
for stock in stockQuantity:

    customStockButtonName = tk.Button(win, font=("Helvetica 8"), background= buttonBack, foreground= buttonFor, text= stock, height= 1, command= lambda stock= stock : customExec(stock))
    customStockButtonName.pack()
    customStockButtonName.place(x= posx, y= 20-5)

    posx += 35
    quantityButtonNameList.append(customStockButtonName)
    customStockButtonName.bind("<Enter>", func=lambda e:do_beep("beep-1.mp3"))
    customStockButtonName.bind("<Button-3>", on_right_click)



#render stock quantity placed button

customStockQuanPlacedButName = tk.Button(win, font=("Helvetica 8"), background= "yellow", foreground= "black", text= 0, height= 1, command= lambda : customResetDefault())
customStockQuanPlacedButName.pack()
customStockQuanPlacedButName.place(x= posx + 10, y= 20-5)

customStockQuanPlacedButName.bind("<Enter>", func=lambda e:do_beep("beep-1.mp3"))
customStockQuanPlacedButName.bind("<Button-3>", on_right_click)



# SECTION FOR CUSTOM TRADE END





for tradingsymbol, amount100 in tradeList.items():


    #render trading symbol
    symbols_name_label = tk.Label( font=("Helvetica 8 bold"), text=tradingsymbol[:-3])
    symbols_name_label.place(x=20, y=tradingsymbolY-8 )
    symbols_name_label.bind("<Button-3>", on_right_click)

    symbols_amount_label = tk.Label( font=("Helvetica 6 bold"), fg="red", text=amount100)
    symbols_amount_label.place(x=20, y=tradingsymbolY+8 )
    symbols_amount_label.bind("<Button-3>", on_right_click)



    for stock in stockQuantity:
        
        #render stock quantity buttons

        stockButtonName = tk.Button(win, font=("Helvetica 8"), background= buttonBack, foreground= buttonFor, text= stock, height= 1, command= lambda symbol= tradingsymbol, stock= stock : stockExec(symbol, stock))
        stockButtonName.pack()
        stockButtonName.place(x= tradingbuttonX, y= tradingsymbolY-5)

        tradingbuttonX += 35
        quantityButtonNameList.append(stockButtonName)
        stockButtonName.bind("<Enter>", func=lambda e:do_beep("beep-1.mp3"))
        stockButtonName.bind("<Button-3>", on_right_click)

    #render stock quantity placed button
    stockQuanPlacedButName = tk.Button(win, font=("Helvetica 8"), background= "yellow", foreground= "black", text= 0, height= 1, command= lambda symbol= tradingsymbol : resetDefault(symbol))
    stockQuanPlacedButName.pack()
    stockQuanPlacedButName.place(x= tradingbuttonX + 10, y= tradingsymbolY-5)
    stockQuanPlacedButDict[tradingsymbol] = stockQuanPlacedButName
    
    stockQuanPlacedButName.bind("<Enter>", func=lambda e:do_beep("beep-1.mp3"))
    stockQuanPlacedButName.bind("<Button-3>", on_right_click)

    tradingsymbolY += 30
    tradingbuttonX = 120





win.mainloop()
