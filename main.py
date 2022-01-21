# SETTINGS

min_dealer_cards = 18

#-----

import time
import random

card_suits = ["Clubs", "Spades", "Diamonds", "Hearts"]

cards = {
    'Ace': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'Jack': 10,
    'Queen': 10,
    'King': 10,
}

print("Welcome to the Casino")

def calculateTotalValue(_cards):
    totalValue = 0
    containsAce = 0
    for card in _cards:
        if card == "Ace":
            containsAce += 1
        else:
            totalValue += cards[card]

    for i in range(0, containsAce):
        if (totalValue + 11) <= 21:
            totalValue += 11
        else:
            totalValue += 1
    return totalValue

def rollCard():
    suit = random.choice(card_suits)
    card_name, value = random.choice(list(cards.items()))
    return [card_name, f"{card_name} of {suit}"]

def getCurrentTokens():
    tokenFile = open("tokens.txt", "r")
    return tokenFile.read()

def setTokens(to):
    tokenFile = open("tokens.txt", "w")
    tokenFile.truncate()
    tokenFile.write(str(to))
    tokenFile.close()

global dealers_cards
dealers_cards = []
global your_cards
your_cards = []

print("Press ENTER to continue.")
input()

currentTokens = getCurrentTokens()

print(f"How many tokens would you like to bet? (Tokens Available: {currentTokens})")
valid = False
global bet
while valid == False:
    bet = input("> ")
    if int(bet):
        if int(bet) > int(currentTokens):
            print("You don't have enough tokens for that.")
        else:
            print(f"Betting {bet} tokens.")
            bet = int(bet)
            valid = True
    elif bet == "0":
        print("Damn you broke as hell.")
        time.sleep(1)
        print("I'll let it slide.")
        time.sleep(1)
        print(f"Betting {bet} tokens.")
        bet = 0
        valid = True
    else:
        print("Invalid input.")

newTokenCount = int(currentTokens) - bet
setTokens(newTokenCount)

global your_turn
your_turn = True
global dealer_turn
dealer_turn = False
global winner
winner = None

print("It's your turn to play.")
print("")
time.sleep(1)

def endGame():
    currentTokens = getCurrentTokens()
    if winner == "dealer":
        print("The dealer wins.")
        print(f"(-{bet} Tokens)")
    elif winner == "player":
        print("You win.")
        print(f"(+{bet*2} Tokens)")
        newTokenCount = int(currentTokens) + (bet*2)
        setTokens(newTokenCount)
    else:
        print("Nobody won?")
        print("(+0 Tokens)")
        newTokenCount = int(currentTokens) + bet
        setTokens(newTokenCount)
    currentTokens = getCurrentTokens()
    print(f"Balance: {currentTokens} Tokens")
    exit(0)

cardGot = rollCard()
your_cards.append(cardGot[0])
yourTotalCards = calculateTotalValue(your_cards)
print(f"You got a {cardGot[1]}. [TOTAL: {yourTotalCards}]")
print()
time.sleep(1)

while your_turn == True:
    cardGot = rollCard()
    your_cards.append(cardGot[0])
    yourTotalCards = calculateTotalValue(your_cards)
    print(f"You got a {cardGot[1]}. [TOTAL: {yourTotalCards}]")
    if yourTotalCards > 21:
        print("Bust.")
        print()
        your_cards = []
        your_turn = False
    elif yourTotalCards == 21:
        print("Blackjack!")
        print()
        winner = "player"
        endGame()
    else:
        print("""
Would you like to hit or stand?
    [hit]: Hit
    [stand]: Stand
        """)
        valid = False
        while valid == False:
            choice = input("> ")
            if choice == "hit":
                valid = True
                print("You ask for another card.")
            elif choice == "stand":
                valid = True
                print("You keep with your current cards.")
                your_turn = False
            else:
                print("Invalid choice.")

print("It's now the Dealer's turn.")
print()

time.sleep(0.2)
dealer_turn = True

cardGot = rollCard()
dealers_cards.append(cardGot[0])
dealerTotal = calculateTotalValue(dealers_cards)
playerTotal = calculateTotalValue(your_cards)
print(f"The dealer got a {cardGot[1]}. [TOTAL: {dealerTotal}]")
print()

while dealer_turn == True:
    time.sleep(1)
    cardGot = rollCard()
    dealers_cards.append(cardGot[0])
    dealerTotal = calculateTotalValue(dealers_cards)
    playerTotal = calculateTotalValue(your_cards)
    print(f"The dealer got a {cardGot[1]}. [TOTAL: {dealerTotal}]")
    time.sleep(1)
    if dealerTotal > 21:
        print("Dealer has gone bust.")
        print("")
        dealers_cards = []
        dealer_turn = False
    elif dealerTotal == 21:
        print("The dealer has blackjack.")
        print("")
        winner = "dealer"
        endGame()
    elif dealerTotal > playerTotal:
        print("The dealer stands.")
        print("")
        dealer_turn = False
    elif dealerTotal >= min_dealer_cards:
        print("The dealer stands.")
        print("")
        dealer_turn = False
    else:
        print("The dealer hits.")
        print("")

dealerTotal = calculateTotalValue(dealers_cards)
playerTotal = calculateTotalValue(your_cards)
if dealerTotal > playerTotal:
    winner = "dealer"
elif playerTotal > dealerTotal:
    winner = "player"
endGame()
