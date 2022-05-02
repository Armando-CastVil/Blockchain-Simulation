#This is the receive client of clientA

from socket import*
import time

def subtract_balance(amount, account_name):
    time.sleep(3)
    counter=0
    # get balances, unconfirmed and confirmed from balance.txt
    fop = open("balanceA.txt", "r")
    account_1 = fop.readline()
    account_2 = fop.readline()
    account1_unconfirmed_balance = account_1[9:17]
    account1_confirmed_balance = account_1[18:26]
    #print("Account 1:")
    #print(account1_confirmed_balance)
    account2_unconfirmed_balance = account_2[9:17]
    account2_confirmed_balance = account_2[18:26]
    # transforming the balances from hex to decimal
    account1_balance = int(account1_confirmed_balance, 16)
    account2_balance = int(account2_confirmed_balance, 16)
    fop.close()

    transaction_amount_int = int(amount,16)
    if (account_name == "A0000001"):

        # transform from int to hex and pad with 0's so that we can write to file
        account1_confirmed_balance = '%.8X' % (account1_balance - transaction_amount_int)

        # write to file with the updated numbers
        f=open("balanceA.txt","w")
        f.write("A0000001" + ":" + account1_unconfirmed_balance + ":" + account1_confirmed_balance + "\n")
        f.write("A0000002" + ":" + account2_unconfirmed_balance + ":" + account2_confirmed_balance + "\n")
        f.close()
    # do the same from above, now assuming the transaction was payed with the second account
    elif (account_name == "A0000002"):
        # transform from int to hex and pad with 0's so that we can write to file
        account2_confirmed_balance = '%.8X' % (account2_balance - transaction_amount_int)
        # write to file with the updated numbers
        f = open("balanceA.txt", "w")
        f.write("A0000001" + ":" + account1_unconfirmed_balance + ":" + account1_confirmed_balance + "\n")
        f.write("A0000002" + ":" + account2_unconfirmed_balance + ":" + account2_confirmed_balance + "\n")
        f.close()
def add_balance(amount, account_name):
    counter=0
    # get balances, unconfirmed and confirmed from balance.txt
    fop = open("balanceA.txt", "r")
    account_1 = fop.readline()
    account_2 = fop.readline()
    account1_unconfirmed_balance = account_1[9:17]
    account1_confirmed_balance = account_1[18:26]
    #print("Account 1:")
    #print(account1_confirmed_balance)
    account2_unconfirmed_balance = account_2[9:17]
    account2_confirmed_balance = account_2[18:26]
    # transforming the balances from hex to decimal
    account1_confirmed_balance_int = int(account1_confirmed_balance, 16)
    account2_confirmed_balance_int = int(account2_confirmed_balance, 16)
    account1_unconfirmed_balance_int = int(account1_unconfirmed_balance, 16)
    account2_unconfirmed_balance_int = int(account2_unconfirmed_balance, 16)
    fop.close()

    transaction_amount_int = int(amount,16)
    if (account_name == "A0000001"):

        # transform from int to hex and pad with 0's so that we can write to file
        account1_confirmed_balance = '%.8X' % (account1_confirmed_balance_int + transaction_amount_int)
        account1_unconfirmed_balance = '%.8X' % (account1_confirmed_balance_int + transaction_amount_int)

        # write to file with the updated numbers
        f=open("balanceA.txt","w")
        f.write("A0000001" + ":" + account1_unconfirmed_balance + ":" + account1_confirmed_balance + "\n")
        f.write("A0000002" + ":" + account2_unconfirmed_balance + ":" + account2_confirmed_balance + "\n")
        f.close()
    # do the same from above, now assuming the transaction was payed with the second account
    elif (account_name == "A0000002"):
        # transform from int to hex and pad with 0's so that we can write to file
        account2_confirmed_balance = '%.8X' % (account2_confirmed_balance_int + transaction_amount_int)
        account2_unconfirmed_balance = '%.8X' % (account2_confirmed_balance_int + transaction_amount_int)

        # write to file with the updated numbers
        f = open("balanceA.txt", "w")
        f.write("A0000001" + ":" + account1_unconfirmed_balance + ":" + account1_confirmed_balance + "\n")
        f.write("A0000002" + ":" + account2_unconfirmed_balance + ":" + account2_confirmed_balance + "\n")
        f.close()

if __name__ == '__main__':

    #socket setup
    serverPort = 15000
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print("Client A is ready to receive")
    # define an empty list
    unconfirmed_Txs = []

    # open file and read the content in a list
    with open('unconfirmed_TA.txt', 'r') as f:
        for line in f:
            # remove linebreak which is the last character of the string
            currentTx = line[:-1]
            # add item to the list
            unconfirmed_Txs.append(currentTx)
    while 1:
        message, clientAddress = serverSocket.recvfrom(2048)
        received_transaction = message.decode()
        print(received_transaction)
        payer = received_transaction[0:8]
        payee = received_transaction[9:17]
        amount = received_transaction[18:26]

        # if the client account is a payer
        if payer == "A0000001" or payer == "A0000002" :
            f = open("Confirmed_TA.txt", 'a')
            f.write(received_transaction + "\n")
            f.close()
            for x in unconfirmed_Txs:
                #removes transaction from unconfirmed transaction file, but appends it to confirmed transaction file beforehand
                if x == received_transaction:
                    f=open("Confirmed_TA.txt",'a')
                    f.write(received_transaction+"\n")
                    del unconfirmed_Txs[unconfirmed_Txs.index(x)]
                    f.close()
            #calls function to subtract amount from confirmed balance
            subtract_balance(amount, payer)
            #updates the unconfirmed tx file
            with open('Unconfirmed_TA.txt', 'w') as f:
                for item in unconfirmed_Txs:
                    f.write("%s\n" % item)
        #if the client is a payee
        if payee == "A0000001" or payee == "A0000002":
            f = open("Confirmed_TA.txt", 'a')
            f.write(received_transaction + "\n")
            f.close()
            add_balance(amount, payee)
