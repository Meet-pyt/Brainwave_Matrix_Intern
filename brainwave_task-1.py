balance = 5000

def checkbalance():
    global balance
    balance = 5000
    print("your current balance is : ",balance)

def deposit():
    global depo
    depo = int(input("Entre the amount to be deposited: "))
    global total
    total = depo + balance   
    print("your current balance after deposit is : ",total)

def Withdraw():
    global withd
    withd = int(input("Entre the amount to be Withdraw: "))
    if withd > balance:
        print("Insufficient balance")
    else:
        global widthbalance
        widthbalance = balance - withd
        print("your current balance after Withdrawl is : ",widthbalance)

def atm():
    pin = int(input("Enter pin of your account: "))
    if pin == 123:
        while True:
            select = int(input("Select any one option: \n 1). Check balance \n 2). Deposit \n 3). Withdraw \n 4). Exit \n"))
            if select == 1:
                checkbalance()
            elif select == 2:
                deposit()
            elif select == 3:
                Withdraw()
            elif select == 4:
                exit()
            else:
                print("Invalid option..")
    else:
        print("invalid pin")

atm()