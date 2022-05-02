#This is the send client of clientA

from socket import*
from filelock import Timeout, FileLock
file_path = "balanceB.txt"
lock_path = "balanceB.txt.lock"

lock = FileLock(lock_path, timeout=10)




# this function prints the menu to the user
def print_menu():
    print("Enter a choice:")
    print("1. Enter a new transaction")
    print("2. The current balance for each account.")
    print("3. Print the unconfirmed transactions")
    print("4. Print the last X number of confirmed transactions (either as a Payee or a Payer).")
    print("5. Print the blockchain")
    print("6. Exit")


# function definition for new transaction
def new_transaction():
    #variables that will be used later are initialized
    payer_account = ""
    payer = '3'
    payee_account = ""
    payee = '3'
    transaction_amount_hex=""
    # let the user know that this option was selected
    print("new transaction was selected")
    # ask user to select payer account, loop goes back if user enters an invalid input
    while payer != '1' or payer != '2':
        # prompt user to select account
        print("select payer account:")
        print("1. B0000001")
        print("2. B0000002")

        # take in user input and assign payer account based on it
        payer = input()
        if payer == '1':
            payer_account = "B0000001"
            print("Choice: 1")
            break
        elif payer == '2':
            payer_account = "B0000002"
            print("Choice: 2")
            break
        else:
            # go back to beginning of loop if user inputs invalid entry
            print("invalid entry, enter 1 or 2")
            payer = '3'
    # ask user to select payee account, loop goes back if user enters an invalid input
    while payee != '1' or payee != '2':
        # prompt user to select account
        print("select payee account:")
        print("1. A0000001 ")
        print("2. A0000002 ")
        # take in user input
        payee = input()
        #select account based on user input
        if payee == '1':
            payee_account = "A0000001"
            print("Choice: 1")
            break
        elif payee == '2':
            payee_account = "A0000002"
            print("Choice: 2")
            break
        else:
            # go back to beginning of loop if user inputs invalid entry
            print("invalid entry, enter 1 or 2")
            payee = '3'
    #ask user to enter amount that will for Tx
    transaction_amount = input("Enter the amount of payment in decimal. :")
    transaction_amount_int=int(transaction_amount)

    #get balances, unconfirmed and confirmed from balance.txt
    f = open("balanceB.txt", "r")
    account_1 = f.readline()
    account_2 = f.readline()
    account1_unconfirmed_balance = account_1[9:17]
    account1_confirmed_balance = account_1[18:26]
    account2_unconfirmed_balance = account_2[9:17]
    account2_confirmed_balance = account_2[18:26]

    #transforming the balances from hex to decimal
    account1_balance = int(account1_unconfirmed_balance, 16)
    account2_balance = int(account2_unconfirmed_balance, 16)
    f.close()

    #let the user know if there are not enough funds in the account to complete the transaction
    if(payer == '1' and (transaction_amount_int+2)>account1_balance):
        print("Insufficient funds. ")
    elif (payer == '2' and (transaction_amount_int+2) > account2_balance):
        print("Insufficient funds. ")
    # this else take place if there are enough funds for the transaction
    else:
        # record the transaction in Unconfirmed_TA.txt int the format payer:payee:Tx amount
        #transform the transaction amount to hex so that we can write it on the file
        transaction_amount_hex ='%.8X' %(transaction_amount_int)

        f = open("Unconfirmed_TB.txt", "a")
        #send the transaction to FullNode1
        transaction_text=payer_account + ":" + payee_account + ":" +transaction_amount_hex.upper()
        #let full node 1 the message came from a client
        clientSocket.sendto("clientB".encode(),('localhost',14000))
        #send the transaction to full node 1
        clientSocket.sendto(transaction_text.encode(),('localhost',14000))
        f.write(payer_account + ":" + payee_account + ":" +transaction_amount_hex.upper())
        f.write("\n")
        f.close()
        # print confirmation
        print("Tx: " + payer_account + " pays " + payee_account + " the amount of " + transaction_amount + " BC")

        #subtract the transaction from the balance txt file
        with lock:
            lock.acquire()
        try:
            f = open("balanceB.txt", "w")
            if (payer == '1'):
                #transform from int to hex and pad with 0's so that we can write to file
                account1_unconfirmed_balance = '%.8X' % (account1_balance-transaction_amount_int-2)
                #write to file with the updated numbers
                f.write("B0000001"+":"+account1_unconfirmed_balance+":"+account1_confirmed_balance+"\n")
                f.write("B0000002" + ":" + account2_unconfirmed_balance+ ":" + account2_confirmed_balance+"\n")
                f.close();
                #do the same from above, now assuming the transaction was payed with the second account
            if (payer == '2'):
            # transform from int to hex and pad with 0's so that we can write to file
                account2_unconfirmed_balance = '%.8X' % (account2_balance - transaction_amount_int - 2)
                # write to file with the updated numbers
                f.write("B0000001" + ":" + account1_unconfirmed_balance + ":" + account1_confirmed_balance+"\n")
                f.write("B0000002" + ":" + account2_unconfirmed_balance + ":" + account2_confirmed_balance+"\n")
                f.close()
        finally:
            lock.release()




# function definition for displaying the current balance of each account
def print_balance():
    print("function for displaying balance was selected")
    b = open("BalanceF2.txt", "r")
    f2_balance = b.read()
    print("Full Node 2 Balance: " + f2_balance)
    b.close()
    f = open("balanceB.txt", "r")
    account_1 = f.readline()
    account_2 = f.readline()
    f.close()
    account1_name=account_1[0:8]
    account1_unconfirmed_balance = account_1[9:17]
    account1_confirmed_balance = account_1[18:26]
    account2_name = account_2[0:8]
    account2_unconfirmed_balance = account_2[9:17]
    account2_confirmed_balance = account_2[18:26]
    print("Account: "+ account1_name)
    print("Unconfirmed Balance: "+account1_unconfirmed_balance)
    print("confirmed Balance: "+account1_confirmed_balance)
    print("Account: " + account2_name)
    print("Unconfirmed Balance: " + account2_unconfirmed_balance)
    print("confirmed Balance: " + account2_confirmed_balance)


# function definition for displaying unconfirmed Tx
def print_unconfirmed():

    #display to the user the function they selected
    print("function for displaying unconfirmed transactions was selected")

    #open unconfirmed_TA.txt file
    f = open("unconfirmed_TB.txt", "r")
    #infinite loop reads line by line and displays info until there are no more lines left
    while True:

        account_info = f.readline()
        if not account_info:
            break
        payer_name = account_info[0:8]
        payee_name = account_info[9:17]
        transaction_amount = account_info[18:26]
        transaction_amount = str(int(transaction_amount, 16))
        print("Account :"+ payer_name+" Payed Account :"+ payee_name+" "+"the amount of : "+transaction_amount+" BC")
    #close file
    f.close()


# function definition for displaying confirmed Tx
def print_transactions():
    print("function for displaying last confirmed transactions was selected")
    # display to the user the function they selected
    print("function for displaying unconfirmed transactions was selected")

    # open unconfirmed_TB.txt file
    f = open("Confirmed_TB.txt", "r")
    # infinite loop reads line by line and displays info until there are no more lines left
    while True:

        account_info = f.readline()
        if not account_info:
            break
        payer_name = account_info[0:8]
        payee_name = account_info[9:17]
        transaction_amount = account_info[18:26]
        transaction_amount = str(int(transaction_amount, 16))
        print(
            "Account :" + payer_name + " Payed Account :" + payee_name + " " + "the amount of : " + transaction_amount + " BC")
    # close file
    f.close()


# function definition for displaying the blockchain
def print_blockchain():
    print("function for displaying blockchain was selected")
    # open blockchain.txt file
    f = open("blockchain.txt", "r")
    # infinite loop reads line by line and displays info until there are no more lines left
    while True:

        blockchain_info = f.readline()
        if not blockchain_info:
            break
        nonce = blockchain_info[0:7]
        last_block_hash = blockchain_info[8:71]
        merkle_root = blockchain_info[72:136]
        Tx1 = blockchain_info[136:160]
        Tx2 = blockchain_info[160:184]
        Tx3 = blockchain_info[184:208]
        Tx4 = blockchain_info[208:232]
    print("Nonce: (4-byte)" + nonce)
    print("Last Block Hash(32-byte): " + last_block_hash)
    print("Merkle Root(32-byte) : " + merkle_root)
    print("Tx1 (12-byte): " + Tx1[0:8] + " paid " + Tx1[8:16] + " the amount of " + Tx1[16:24] + " BC")
    print("Tx2 (12-byte): " + Tx2[0:8] + " paid " + Tx2[8:16] + " the amount of " + Tx2[16:24] + " BC")
    print("Tx3 (12-byte): " + Tx3[0:8] + " paid " + Tx3[8:16] + " the amount of " + Tx3[16:24] + " BC")
    print("Tx4 (12-byte): " + Tx4[0:8] + " paid " + Tx4[8:16] + " the amount of " + Tx4[16:24] + " BC")

# function for selecting a function depending on user input
def menu_select(argument):

    if argument == '1':
        return new_transaction()

    elif argument == '2':
        print_balance()
        return
    elif argument == '3':
        print_unconfirmed()
        return
    elif argument == '4':
        print_transactions()
        return
    elif argument == '5':
        print_blockchain()
        return
    else:
        print("invalid selection")
        return




# Press the green button in the gutter to run the script.
if __name__ == '__main__':


    serverName = 'localhost'

    serverPort = 12000

    clientSocket = socket(AF_INET, SOCK_DGRAM)

    clientSocket.connect((serverName, serverPort))

    # infinite loop
    while 1:
        # calls the print_menu function
        print_menu()

        # takes user input and uses it to select an option from the menu
        menu_choice = input()
        if menu_choice == '6':
            clientSocket.close()
            break
        menu_select(menu_choice)



