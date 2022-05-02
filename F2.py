from socket import *
import time
import os
import hashlib
# turn variable is global
turn = 2


# function increases turn by 1, used to avoid clutter
def turn_upper():
    global turn
    turn = turn + 1
    print("turn is:")
    print(turn)


# updates balance when the node is done mining a block
def update_balance_block():
    print("Full Node 2 is mining a block")

    balance = 0;
    f = open("BalanceF2.txt", "r")
    # 30 from mining a block
    balance = int(f.readline())
    f.close()
    balance = balance + 38
    f = open("BalanceF2.txt", "w")
    f.write(str(balance) + "\n")
    f.close()


# this functions sends the now confirmed transactions to its client
def read_temp(list):
    counter = 0;
    # loop reads line by line and sends them to clientB_receive until there are no more lines left
    for x in list:
        clientSocket.sendto(list[counter].encode(), ('localhost', 16000))
        counter = counter + 1
    open('Tempt_T.txt', 'w').close()

def lastBlockHash():
    fw = open('Blockchain.txt', 'a')
    firstBlock = os.stat('Blockchain.txt').st_size == 0
    fw.close()
    # check to see if there is any block in the blockChain to find the last block hash
    if firstBlock == True:
        lastBlockHash = "0" * 64

    else:
        with open('Blockchain.txt') as f:
            for line in f:
                pass
        last_line = line
        hashHandler = hashlib.sha256()
        hashHandler.update(last_line[0:136].encode("utf-8"))
        lastBlockHash = hashHandler.hexdigest()

    return lastBlockHash

def merkle():
    with open('Tempt_T.txt') as f:
        hashList = f.readlines()
    f.close()

    hashList[0] = hashList[0].replace(':', '')
    hashList[0] = hashList[0].replace('\n', '')
    hashList[0] = hashList[1].replace(':', '')
    hashList[0] = hashList[1].replace('\n', '')
    hashList[0] = hashList[2].replace(':', '')
    hashList[0] = hashList[2].replace('\n', '')
    hashList[0] = hashList[3].replace(':', '')
    hashList[0] = hashList[3].replace('\n', '')

    hashAB = hashList[0] + hashList[1]
    hashHandler = hashlib.sha256()
    hashHandler.update(hashAB.encode("utf-8"))
    hashValue = hashHandler.hexdigest()
    hashAB = hashValue

    hashCD = hashList[2] + hashList[3]
    hashHandler = hashlib.sha256()
    hashHandler.update(hashCD.encode("utf-8"))
    hashValue = hashHandler.hexdigest()
    hashCD = hashValue

    hashABCD = hashAB + hashCD
    hashHandler = hashlib.sha256()
    hashHandler.update(hashABCD.encode("utf-8"))
    hashValue = hashHandler.hexdigest()
    merkle = hashValue

    return merkle

# gets the nonce of the block and sends it to blockChain
def getNonce():
    hashHandler = hashlib.sha256()
    nonce = 0
    lastBlock = lastBlockHash()
    newMerkle = merkle()
    while True:
        block_header = str(nonce) + str(lastBlock) + str(newMerkle)
        hashHandler.update(block_header.encode("utf-8"))
        hashValue = hashHandler.hexdigest()
        nonceFound = True
        for i in range(4):
            if hashValue[i] != '0':
                nonceFound = False
        if nonceFound:
            break
        else:
            nonce = nonce + 1
    nonce = str(nonce)
    nonce = nonce.zfill(8)
    return nonce


# makes the block chain and puts it into the file
def blockChain():
    transList = []
    # Makes the body by concatenating four transactions
    nonce = getNonce()
    lastBlock = lastBlockHash()
    newMerkle = merkle()
    blockHeader = nonce + str(lastBlock) + str(newMerkle)

    # gets transactions and add them to the block
    with open('Tempt_T.txt') as f:
        transList = [line.rstrip() for line in f]

    transList[0] = transList[0].replace(':', '')
    transList[1] = transList[1].replace(':', '')
    transList[2] = transList[2].replace(':', '')
    transList[3] = transList[3].replace(':', '')

    body = ""
    for x in transList:
        body = body + x

    wholeBlock = blockHeader + body

    fw = open('Blockchain.txt', 'a')
    fw.write(wholeBlock)
    fw.write('\n')
    fw.close()

    # send block to server F1
    clientSocket.sendto("F2Block".encode(), ('localhost', 13000))
    clientSocket.sendto(wholeBlock.encode(), ('localhost', 13000))


# will mine the block
def mineBlock():
    print("Full Node 2 is mining a block")
    blockChain()
    update_balance_block()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # socket setup
    serverName = 'localhost'
    serverPort = 14000
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.connect((serverName, serverPort))
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print("Full Node 2 is ready to receive")

    while 1:

        message, clientAddress = serverSocket.recvfrom(2048)
        received_transaction = message.decode()
        print("Sender is: " + received_transaction)
        # performs instructions if clientA send the message
        if received_transaction == "clientB":
            # send tx to  F2 and append the transaction to Tempt_T.txt and check if it's its 4th transaction, mine block if so.
            message, clientAddress = serverSocket.recvfrom(2048)
            received_transaction = message.decode()

            # the received transaction is stored in received_transaction in the format payer:payee:amount, all in hex
            print(received_transaction)
            # send the transaction to F2
            clientSocket.sendto("F2".encode(), ('localhost', 13000))
            clientSocket.sendto(received_transaction.encode(), ('localhost', 13000))



        # performs instructions if F1 sent the message
        elif received_transaction == "F1":
            message, clientAddress = serverSocket.recvfrom(2048)
            received_message = message.decode()
            print(received_message)

        # performs instructions if F1 sent the message
        elif received_transaction == "F1Block":
            message, clientAddress = serverSocket.recvfrom(2048)
            received_message = message.decode()
            print("Full Node 1 sent blockchain: ")
            print(received_message)
            blockchain_info = received_message
            Tx1 = blockchain_info[136:160]
            Tx2 = blockchain_info[160:184]
            Tx3 = blockchain_info[184:208]
            Tx4 = blockchain_info[208:232]
            transaction_info = Tx1[0:8] + ":" + Tx1[8:16] + ":" + Tx1[16:24]
            clientSocket.sendto(transaction_info.encode(), ('localhost', 16000))
            transaction_info = Tx2[0:8] + ":" + Tx2[8:16] + ":" + Tx2[16:24]
            clientSocket.sendto(transaction_info.encode(), ('localhost', 16000))
            transaction_info = Tx3[0:8] + ":" + Tx3[8:16] + ":" + Tx3[16:24]
            clientSocket.sendto(transaction_info.encode(), ('localhost', 16000))
            transaction_info = Tx4[0:8] + ":" + Tx4[8:16] + ":" + Tx4[16:24]
            clientSocket.sendto(transaction_info.encode(), ('localhost', 16000))


        time.sleep(3)
        list = []
        with open('Tempt_T.txt', 'r') as f:

            for line in f:
                # remove linebreak which is the last character of the string
                temp_transaction = line[:-1]
                # add item to the list
                list.append(temp_transaction)

        print("There are :")
        print(len(list))
        print("elements in Tempt_T")
        # if it's its turn to mine,mine the block and update the balance, otherwise skip.
        if (turn % 2 == 0 and len(list) == 4):
            turn_upper()


        elif (turn % 2 == 1 and len(list) == 4):
            mineBlock()
            turn_upper()
            read_temp(list)


