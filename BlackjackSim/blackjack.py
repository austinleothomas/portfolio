# Python Black Jack Game
#
## -----------------------------------------------------------------------------------
# CONFIGURATIONS
# -----------------------------------------------------------------------------------
# We import modules.
import random
import tkinter as tk
from PIL import ImageTk,Image
# -----------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------
# Necessary additions.
# -----------------------------------------------------------------------------------
# -> shuffling animation
# -> condition for if bet size exceeds bank amount
# -----------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------
# We define a function to generate a new shoe as needed.
# -----------------------------------------------------------------------------------
def DeckGenerator(DeckCount):
    Shoe = []
    NumDeck = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    SuitDeck = ['-S','-C','-H','-D']

    for i in range(DeckCount):
        for currSuit in SuitDeck:
            for currNum in NumDeck:
                Shoe.append(currNum + currSuit)
    
    random.shuffle(Shoe)
    return(Shoe)
# -----------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------
# We creat the card value dictionary.
# -----------------------------------------------------------------------------------
CardVal = {'2-S':(2,2),'3-S':(3,3),'4-S':(4,4),'5-S':(5,5),'6-S':(6,6),'7-S':(7,7),
               '8-S':(8,8),'9-S':(9,9),'10-S':(10,10),'J-S':(10,10),'Q-S':(10,10),
               'K-S':(10,10),'A-S':(1,11),'2-C':(2,2),'3-C':(3,3),'4-C':(4,4),
               '5-C':(5,5),'6-C':(6,6),'7-C':(7,7),'8-C':(8,8),'9-C':(9,9),
               '10-C':(10,10),'J-C':(10,10),'Q-C':(10,10),'K-C':(10,10),'A-C':(1,11),
               '2-D':(2,2),'3-D':(3,3),'4-D':(4,4),'5-D':(5,5),'6-D':(6,6),'7-D':(7,7),
               '8-D':(8,8),'9-D':(9,9),'10-D':(10,10),'J-D':(10,10),'Q-D':(10,10),
               'K-D':(10,10),'A-D':(1,11),'2-H':(2,2),'3-H':(3,3),'4-H':(4,4),
               '5-H':(5,5),'6-H':(6,6),'7-H':(7,7),'8-H':(8,8),'9-H':(9,9),
               '10-H':(10,10),'J-H':(10,10),'Q-H':(10,10),'K-H':(10,10),'A-H':(1,11)}
# -----------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------
# We write a class to generate GUI windows.
# -----------------------------------------------------------------------------------
class WindowGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        WindowIcon = tk.PhotoImage(file = '.\\Icons\\WindowIcon.png')
        self.iconphoto(True,WindowIcon)
# -----------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------
# We define button click functions for the launch page.
# -----------------------------------------------------------------------------------
def StartClick():
    global isLaunch
    global DeckCount
    global HandCount
    isLaunch = True
    DeckCount = DeckCountVar.get()
    HandCount = HandCountVar.get()
    LaunchPage.destroy()

# def DeckSelect():
#     global DeckCount
#     DeckCount = DeckCountVar.get()

# def HandSelect():
#     global HandCount
#     HandCount = HandCountVar.get()  
# -----------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------
# We generate the launch page GUI.
# -----------------------------------------------------------------------------------
# We call on the window generator class.
LaunchPage = WindowGenerator()

# We define the hex code for the launch page color scheme.
LaunchHexCode = '#094f04'

# We configure the window.
LaunchPage.geometry('1000x500')
LaunchPage.title('Black Jack Simulator')
LaunchPage.config(background = LaunchHexCode)

# We prepare for grid configuration.
LaunchPageColumns = range(2)
LaunchRowCount = 0

# We configure the title text.
LaunchTitle = tk.Label(LaunchPage,
                       text = 'Black Jack Simulator',
                       font = ('Cambria',40,'bold'),
                       bg = LaunchHexCode
                       )
LaunchTitle.grid(row = LaunchRowCount,columnspan = len(LaunchPageColumns))
LaunchRowCount += 1

# We configure the first separator line.
LaunchFirstSeparator = tk.Label(LaunchPage,
                                 text = '____________________________________________________________' \
                                 '__________________________________________',
                                 font = ('Cambria',18,'bold'),
                                 bg = LaunchHexCode
                                 )
LaunchFirstSeparator.grid(row = LaunchRowCount,columnspan = len(LaunchPageColumns))
LaunchRowCount += 1

# We configure the player count button label.
DeckCountLabel = tk.Label(LaunchPage,
                          text = 'Number of Simultaneous Player Hands',
                          font = ('Cambria',18,'bold'),
                          bg = LaunchHexCode
                          )
DeckCountLabel.grid(row = LaunchRowCount,column = LaunchPageColumns[1])

# We configure the deck count button label.
HandCountLabel = tk.Label(LaunchPage,
                          text = 'Number of Decks in Shoe',
                          font = ('Cambria',18,'bold'),
                          bg = LaunchHexCode
                          )
HandCountLabel.grid(row = LaunchRowCount,column = LaunchPageColumns[0])
LaunchRowCount += 1

# We configure the deck count button.
DeckCountOptions = [1,2,4,6,8]
DeckCountVar = tk.IntVar()
DeckCountVar.set(1)

for DeckCount in DeckCountOptions:
    DeckCountButtons = tk.Radiobutton(LaunchPage,
                                      text = str(DeckCount),
                                      variable = DeckCountVar,
                                      value = DeckCount,
                                      padx = 25,
                                      font = ('Cambria',18),
                                      bg = LaunchHexCode,
                                      activebackground = LaunchHexCode,
                                    #   command = DeckSelect
                                      )
    DeckCountButtons.grid(row = LaunchRowCount + DeckCountOptions.index(DeckCount),column = 0)

# We configure the hand count button.
HandCountOptions = [1,2,3]
HandCountVar = tk.IntVar()
HandCountVar.set(1)

for HandCount in HandCountOptions:
    HandCountButtons = tk.Radiobutton(LaunchPage,
                                      text = str(HandCount),
                                      variable = HandCountVar,
                                      value = HandCount,
                                      padx = 25,
                                      font = ('Cambria',18),
                                      bg = LaunchHexCode,
                                      activebackground = LaunchHexCode,
                                    #   command = HandSelect
                                      )
    HandCountButtons.grid(row = LaunchRowCount + HandCountOptions.index(HandCount),column = 1)
LaunchRowCount += len(max(DeckCountOptions,HandCountOptions))

# We configure the second separator line.
LaunchSecondSeparator = tk.Label(LaunchPage,
                                 text = '____________________________________________________________' \
                                 '__________________________________________',
                                 font = ('Cambria',18,'bold'),
                                 bg = LaunchHexCode
                                 )
LaunchSecondSeparator.grid(row = LaunchRowCount,columnspan = len(LaunchPageColumns))
LaunchRowCount += 1

   
# We configure the start button.
StartButton = tk.Button(LaunchPage,
                        text = 'Play!',
                        font = ('Camrbia',18,'bold'),
                        command = StartClick
                        )
StartButton.grid(row = LaunchRowCount,columnspan = len(LaunchPageColumns),pady = 20)
LaunchRowCount += 1

# We configure the grid.
for i in range(LaunchRowCount):
    LaunchPage.grid_rowconfigure(i,weight = 1)
for i in LaunchPageColumns:
    LaunchPage.grid_columnconfigure(i,weight = 1)

# We generate the launch page.
LaunchPage.mainloop()
# -----------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------
# We define main page widgets.
# -----------------------------------------------------------------------------------
def LeftHandWidgets():
    global LeftInput
    global PileImg
    global LeftLabels
    LeftHitButton = tk.Button(MainPage,
                              text = 'Hit',
                              font = ('Cambria',14),
                              command = HitLeftHand,
                              bg = MainHexCode_Btn,
                              fg = 'white'
                              )
    LeftStandButton = tk.Button(MainPage,
                                text = 'Stand',
                                font = ('Cambria',14),
                                command = StandLeftHand,
                                bg = MainHexCode_Btn,
                                fg = 'white'
                                )
    LeftDoubleButton = tk.Button(MainPage,
                                 text = 'Double',
                                 font = ('Cambria',14),
                                 command = DoubleLeftHand,
                                 bg = MainHexCode_Btn,
                                 fg = 'white'
                                 )
    LeftInput = tk.Entry(MainPage,
                         font = ('Cambria',14),
                         width = 5,
                         insertontime = 0
                         )
    LeftInput.insert(1,'1')
    LeftLabel = tk.Label(MainPage,
                         text = 'Bet Size $',
                         font = ('Cambria',14,'bold'),
                         bg = MainHexCode_Prim
                         )
    LeftStack = tk.Label(MainPage,
                         image = PileImg,
                         bg = MainHexCode_Prim
                         )
    LeftHitButton.grid(row = 10,column = 1,pady = 10,padx = 10)
    LeftStandButton.grid(row = 10,column = 2,pady = 10)
    LeftDoubleButton.grid(row = 10,column = 3,pady = 10)
    LeftInput.grid(row = 9,column = 2,padx = 10)
    LeftLabel.grid(row = 9,column = 1)
    LeftStack.grid(row = 9,column = 3)
    LeftLabels = [LeftLabel,LeftStack]

def CenterHandWidgets():
    global CenterInput
    global PileImg
    global CenterLabels
    CenterHitButton = tk.Button(MainPage,
                                text = 'Hit',
                                font = ('Cambria',14),
                                command = HitCenterHand,
                                bg = MainHexCode_Btn,
                                fg = 'white'
                                )
    CenterStandButton = tk.Button(MainPage,
                                  text = 'Stand',
                                  font = ('Cambria',14),
                                  command = StandCenterHand,
                                  bg = MainHexCode_Btn,
                                  fg = 'white'
                                  )
    CenterDoubleButton = tk.Button(MainPage,
                                   text = 'Double',
                                   font = ('Cambria',14),
                                   command = DoubleCenterHand,
                                   bg = MainHexCode_Btn,
                                   fg = 'white'
                                   )
    CenterInput = tk.Entry(MainPage,
                          font = ('Cambria',14),
                          width = 5,
                          insertontime = 0
                          )
    CenterInput.insert(1,'1')
    CenterLabel = tk.Label(MainPage,
                         text = 'Bet Size $',
                         font = ('Cambria',14,'bold'),
                         bg = MainHexCode_Prim
                         )
    CenterStack = tk.Label(MainPage,
                         image = PileImg,
                         bg = MainHexCode_Prim
                         )
    CenterHitButton.grid(row = 10,column = 5,pady = 10)
    CenterStandButton.grid(row = 10,column = 6,pady = 10)
    CenterDoubleButton.grid(row = 10,column = 7,pady = 10)
    CenterInput.grid(row = 9,column = 6,padx = 10)
    CenterLabel.grid(row = 9,column = 5)
    CenterStack.grid(row = 9,column = 7)
    CenterLabels = [CenterLabel,CenterStack]

def RightHandWidgets():
    global RightInput
    global PileImg
    global RightLabels
    RightHitButton = tk.Button(MainPage,
                               text = 'Hit',
                               font = ('Cambria',14),
                               command = HitRightHand,
                               bg = MainHexCode_Btn,
                               fg = 'white'
                               )
    RightStandButton = tk.Button(MainPage,
                                 text = 'Stand',
                                 font = ('Cambria',14),
                                 command = StandRightHand,
                                 bg = MainHexCode_Btn,
                                 fg = 'white'
                                 )
    RightDoubleButton = tk.Button(MainPage,
                                  text = 'Double',
                                  font = ('Cambria',14),
                                  command = DoubleRightHand,
                                  bg = MainHexCode_Btn,
                                  fg = 'white'
                                  )
    RightInput = tk.Entry(MainPage,
                          font = ('Cambria',14),
                          width = 5,
                          insertontime = 0
                          )
    RightInput.insert(1,'1')
    RightLabel = tk.Label(MainPage,
                         text = 'Bet Size $',
                         font = ('Cambria',14,'bold'),
                         bg = MainHexCode_Prim
                         )
    RightStack = tk.Label(MainPage,
                         image = PileImg,
                         bg = MainHexCode_Prim
                         )
    RightHitButton.grid(row = 10,column = 9,pady = 10)
    RightStandButton.grid(row = 10,column = 10,pady = 10)
    RightDoubleButton.grid(row = 10,column = 11,pady = 10,padx = 10)
    RightInput.grid(row = 9,column = 10,padx = 10)
    RightLabel.grid(row = 9,column = 9)
    RightStack.grid(row = 9,column = 11)
    RightLabels = [RightLabel,RightStack]

def PermanentWidgets():
    global BankImg
    global currBank
    global PermLabels
    PermLabels = []
    CloseButton = tk.Button(MainPage,
                            text = 'Quit',
                            font = ('Cambria',14),
                            command = CloseCommand,
                            bg = MainHexCode_Btn,
                            fg = 'white'
                            )
    RunButton = tk.Button(MainPage,
                          text = 'Deal',
                          font = ('Cambria',27,'bold'),
                          command = RunGame,
                          bg = MainHexCode_Btn,
                          fg = 'white'
                          )
    Buffer1 = tk.Label(MainPage,
                       text = '                                            ',
                       bg = MainHexCode_Prim
                       )
    Buffer2 = tk.Label(MainPage,
                       text = '                                            ',
                       bg = MainHexCode_Prim
                       )
    BankStack = tk.Label(MainPage,
                        image = BankImg,
                        bg = MainHexCode_Prim
                        )
    BankLabel = tk.Label(MainPage,
                         text = 'Amount Behind',
                         font = ('Cambria',24,'bold'),
                         bg = MainHexCode_Prim
                         )
    CloseButton.grid(row = 0,column = 1,columnspan = 2)
    RunButton.grid(row = 1,column = 1,rowspan = 2,columnspan = 2)
    Buffer1.grid(row = 10,column = 4)
    Buffer2.grid(row = 10,column = 8)
    BankStack.grid(row = 1,column = 11)
    BankLabel.grid(row = 0,column = 10,columnspan = 2)
    PermLabels = [Buffer1,Buffer2,BankStack,BankLabel]
# -----------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------
# We define main page widget command functions (except for game play function).
# -----------------------------------------------------------------------------------
def HitLeftHand():
    UserCmd = 'HitLeftHand'
    LoopGame(UserCmd)
def StandLeftHand():
    UserCmd = 'StandLeftHand'
    LoopGame(UserCmd)
def DoubleLeftHand():
    UserCmd = 'DoubleLeftHand'
    LoopGame(UserCmd)
def HitCenterHand():
    UserCmd = 'HitCenterHand'
    LoopGame(UserCmd)
def StandCenterHand():
    UserCmd = 'StandCenterHand'
    LoopGame(UserCmd)
def DoubleCenterHand():
    UserCmd = 'DoubleCenterHand'
    LoopGame(UserCmd)
def HitRightHand():
    UserCmd = 'HitRightHand'
    LoopGame(UserCmd)
def StandRightHand():
    UserCmd = 'StandRightHand'
    LoopGame(UserCmd)
def DoubleRightHand():
    UserCmd = 'DoubleRightHand'
    LoopGame(UserCmd)
def CloseCommand():
    MainPage.destroy()
# -----------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------
# We define sub-functions of the gameplay loop.
# -----------------------------------------------------------------------------------
def DealerAction(DealerZero,DealerOne):

    # We pull and establish global variables.
    global currDeck
    global DealerSum

    # We reveal the dealer face-down card.
    global DealerZeroImg
    DealerZeroImg = CardImgGen(DealerZero)
    DealerZeroCard = tk.Label(MainPage,image = DealerZeroImg)
    DealerZeroCard.grid(row = 0,column = 4)
    
    # First draw opportunity logic.
    DealerSum = SumEval(DealerZero,DealerOne)
    for i in range(18,22):
        if i in DealerSum:
            return i
    if 17 in DealerSum and 'A' not in DealerZero and 'A' not in DealerOne:
        return 17
    else:
        DealerThree = PullCard(currDeck)
        global DealerThreeImg
        DealerThreeImg = CardImgGen(DealerThree)
        DealerThreeCard = tk.Label(MainPage,image = DealerThreeImg)
        DealerThreeCard.grid(row = 0,column = 6)
    
    # Next draw opportunity.
    DealerSum = SumEval(DealerZero,DealerOne,DealerThree)
    for i in range(17,22):
        if i in DealerSum:
            return i
        elif DealerSum[0] > 21 and DealerSum[1] > 21:
            return DealerSum[0]
    DealerFour = PullCard(currDeck)
    global DealerFourImg
    DealerFourImg = CardImgGen(DealerFour)
    DealerFourCard = tk.Label(MainPage,image = DealerFourImg)
    DealerFourCard.grid(row = 0,column = 7)

    # Next draw opportunity.
    DealerSum = SumEval(DealerZero,DealerOne,DealerThree,DealerFour)
    for i in range(17,22):
        if i in DealerSum:
            return i
        elif DealerSum[0] > 21 and DealerSum[1] > 21:
            return DealerSum[0]
    DealerFive = PullCard(currDeck)
    global DealerFiveImg
    DealerFiveImg = CardImgGen(DealerFive)
    DealerFiveCard = tk.Label(MainPage,image = DealerFiveImg)
    DealerFiveCard.grid(row = 0,column = 8)

    # Next draw opportunity.
    DealerSum = SumEval(DealerZero,DealerOne,DealerThree,DealerFour,DealerFive)
    for i in range(17,22):
        if i in DealerSum:
            return i
        elif DealerSum[0] > 21 and DealerSum[1] > 21:
            return DealerSum[0]
    DealerSix = PullCard(currDeck)
    global DealerSixImg
    DealerSixImg = CardImgGen(DealerSix)
    DealerSixCard = tk.Label(MainPage,image = DealerSixImg)
    DealerSixCard.grid(row = 1,column = 4)

    # Next draw opportunity.
    DealerSum = SumEval(DealerZero,DealerOne,DealerThree,DealerFour,DealerFive,DealerSix)
    for i in range(17,22):
        if i in DealerSum:
            return i
        elif DealerSum[0] > 21 and DealerSum[1] > 21:
            return DealerSum[0]
    DealerSeven = PullCard(currDeck)
    global DealerSevenImg
    DealerSevenImg = CardImgGen(DealerSeven)
    DealerSevenCard = tk.Label(MainPage,image = DealerSevenImg)
    DealerSevenCard.grid(row = 1,column = 5)

    # Next draw opportunity.
    DealerSum = SumEval(DealerZero,DealerOne,DealerThree,DealerFour,DealerFive,DealerSix,
                        DealerSeven)
    for i in range(17,22):
        if i in DealerSum:
            return i
        elif DealerSum[0] > 21 and DealerSum[1] > 21:
            return DealerSum[0]
    DealerEight = PullCard(currDeck)
    global DealerEightImg
    DealerEightImg = CardImgGen(DealerEight)
    DealerEightCard = tk.Label(MainPage,image = DealerEightImg)
    DealerEightCard.grid(row = 1,column = 6)

    # Next draw opportunity.
    DealerSum = SumEval(DealerZero,DealerOne,DealerThree,DealerFour,DealerFive,DealerSix,
                        DealerSeven,DealerEight)
    for i in range(17,22):
        if i in DealerSum:
            return i
        elif DealerSum[0] > 21 and DealerSum[1] > 21:
            return DealerSum[0]
    DealerNine = PullCard(currDeck)
    global DealerNineImg
    DealerNineImg = CardImgGen(DealerNine)
    DealerNineCard = tk.Label(MainPage,image = DealerNineImg)
    DealerNineCard.grid(row = 1,column = 7)

    # Next draw opportunity.
    DealerSum = SumEval(DealerZero,DealerOne,DealerThree,DealerFour,DealerFive,DealerSix,
                        DealerSeven,DealerEight,DealerNine)
    for i in range(17,22):
        if i in DealerSum:
            return i
        elif DealerSum[0] > 21 and DealerSum[1] > 21:
            return DealerSum[0]
    DealerTen = PullCard(currDeck)
    global DealerTenImg
    DealerTenImg = CardImgGen(DealerTen)
    DealerTenCard = tk.Label(MainPage,image = DealerTenImg)
    DealerTenCard.grid(row = 1,column = 8)

    # Next draw opportunity.
    DealerSum = SumEval(DealerZero,DealerOne,DealerThree,DealerFour,DealerFive,DealerSix,
                        DealerSeven,DealerEight,DealerNine,DealerTen)
    for i in range(17,22):
        if i in DealerSum:
            return i
        elif DealerSum[0] > 21 and DealerSum[1] > 21:
            return DealerSum[0]
    DealerEleven = PullCard(currDeck)
    global DealerElevenImg
    DealerElevenImg = CardImgGen(DealerEleven)
    DealerElevenCard = tk.Label(MainPage,image = DealerElevenImg)
    DealerElevenCard.grid(row = 1,column = 9)

    # Next draw opportunity.
    DealerSum = SumEval(DealerZero,DealerOne,DealerThree,DealerFour,DealerFive,DealerSix,
                        DealerSeven,DealerEight,DealerNine,DealerTen,DealerEleven)
    for i in range(17,22):
        if i in DealerSum:
            return i
        elif DealerSum[0] > 21 and DealerSum[1] > 21:
            return DealerSum[0]

def Shuffling():
    place = 0

def PullCard(currDeck):
    Card = currDeck[0]
    currDeck.remove(currDeck[0])
    return Card

def CardImgGen(CardName):
    CardImage = Image.open('.\\Icons\\Cards\\' + CardName + '.png')
    CardImage = CardImage.resize((75,125))
    CardImage = ImageTk.PhotoImage(CardImage)
    return CardImage

def Deal(currDeck):

    # Pulling values for the dealer's cards.
    DealerZero = PullCard(currDeck)
    DealerOne = PullCard(currDeck)

    # Pulling values for the player cards.
    if HandCount >= 1:
        CenterZero = PullCard(currDeck)
        CenterOne = PullCard(currDeck)
    if HandCount >= 2:
        LeftZero = PullCard(currDeck)
        LeftOne = PullCard(currDeck)
    if HandCount == 3:
        RightZero = PullCard(currDeck)
        RightOne = PullCard(currDeck)

    global DealerZeroImg
    DealerZeroImg = CardImgGen('CardBack')
    DealerZeroCard = tk.Label(MainPage,image = DealerZeroImg)
    DealerZeroCard.grid(row = 0,column = 4)

    global DealerOneImg
    DealerOneImg = CardImgGen(DealerOne)
    DealerOneCard = tk.Label(MainPage,image = DealerOneImg)
    DealerOneCard.grid(row = 0,column = 5)

    # Placing the player cards.
    if HandCount >= 1:
        global CenterZeroImg
        CenterZeroImg = CardImgGen(CenterZero)
        CenterZeroCard = tk.Label(MainPage,image = CenterZeroImg)
        CenterZeroCard.grid(row = 6,column = 5)
        global CenterOneImg
        CenterOneImg = CardImgGen(CenterOne)
        CenterOneCard = tk.Label(MainPage,image = CenterOneImg)
        CenterOneCard.grid(row = 6,column = 6)
    if HandCount >= 2:
        global LeftZeroImg
        LeftZeroImg = CardImgGen(LeftZero)
        LeftZeroCard = tk.Label(MainPage,image = LeftZeroImg)
        LeftZeroCard.grid(row = 6,column = 2)
        global LeftOneImg
        LeftOneImg = CardImgGen(LeftOne)
        LeftOneCard = tk.Label(MainPage,image = LeftOneImg)
        LeftOneCard.grid(row = 6,column = 1)
    if HandCount == 3:
        global RightZeroImg
        RightZeroImg = CardImgGen(RightZero)
        RightZeroCard = tk.Label(MainPage,image = RightZeroImg)
        RightZeroCard.grid(row = 6,column = 9)
        global RightOneImg
        RightOneImg = CardImgGen(RightOne)
        RightOneCard = tk.Label(MainPage,image = RightOneImg)
        RightOneCard.grid(row = 6,column = 10)
     
    # Returning card values.
    if HandCount == 1:
        return (DealerZero,DealerOne,CenterZero,CenterOne)
    if HandCount == 2:
        return (DealerZero,DealerOne,CenterZero,CenterOne,LeftZero,LeftOne)
    if HandCount == 3:
        return (DealerZero,DealerOne,CenterZero,CenterOne,LeftZero,LeftOne,RightZero,RightOne)

def SumEval(*Cards):
    SumVal = [0,0]
    AceCount = 0
    for Card in Cards:
        if 'A' in Card:
            AceCount += 1
        if AceCount <= 1:
            SumVal[0] += min(CardVal[Card])
            SumVal[1] += max(CardVal[Card])
        elif AceCount == 2:
            SumVal[0] += max(CardVal[Card])
            SumVal[1] += min(CardVal[Card])
        else:
            SumVal[0] += min(CardVal[Card])
            SumVal[1] += min(CardVal[Card])
    return SumVal
    
# -----------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------
# We define the gameplay loop functions.
# -----------------------------------------------------------------------------------
# Function ran on initialization (pressing of Play! button).
def RunGame():

    # We pull global variables.
    global currDeck
    global currBank
    global HandCount
    global isReady

    # We verify that we are ready for a new hand.
    if not isReady:
        return
    else:
        isReady = False

    # We clear the field.
    global PermLabels
    if HandCount >= 1:
        global CenterLabels
        PermLabels += CenterLabels
    if HandCount >= 2:
        global LeftLabels
        PermLabels += LeftLabels
    if HandCount == 3:
        global RightLabels
        PermLabels += RightLabels
    for widget in MainPage.winfo_children():
        if isinstance(widget,tk.Label) and widget not in PermLabels:
            widget.destroy()
    
    # We update the bank amount label.
    BankStatement = tk.Label(MainPage,
                             text = '$' + str(round(currBank,2)),
                             font = ('Cambria',20),
                             bg = MainHexCode_Prim
                             )
    BankStatement.grid(row = 1,column = 10)

    # We establish game states.
    global isCenterClosed
    global isLeftClosed
    global isRightClosed
    isCenterClosed = False
    isLeftClosed = False
    isRightClosed = False

    # We store bet amounts.
    global CenterBet
    global RightBet
    global LeftBet
    CenterBet = 0
    RightBet = 0
    LeftBet = 0
    if HandCount >= 1:
        try:
            CenterBet = int(round(float(CenterInput.get())))
        except:
            CenterBet = 1
    if HandCount >= 2:
        try:
            LeftBet = int(round(float(LeftInput.get())))
        except:
            LeftBet = 1
    if HandCount == 3:
        try:
            RightBet = int(round(float(CenterInput.get())))
        except:
            RightBet = 1
    
    # We establish the payout.
    global Pay
    Pay = -(CenterBet + LeftBet + RightBet)

    # We check that deck has enough cards.
    if len(currDeck) < 11*(HandCount + 1):
        Shuffling()
        currDeck = DeckGenerator(DeckCount)
    
    # We deal cards.
    global DealerZero
    global DealerOne
    global CenterZero
    global CenterOne
    global LeftZero
    global LeftOne
    global RightZero
    global RightOne
    if HandCount == 1:
        (DealerZero,DealerOne,CenterZero,CenterOne) = Deal(currDeck)
    if HandCount == 2:
        (DealerZero,DealerOne,CenterZero,CenterOne,LeftZero,LeftOne) = Deal(currDeck)
    if HandCount == 3:
        (DealerZero,DealerOne,CenterZero,CenterOne,LeftZero,LeftOne,RightZero,RightOne) = Deal(currDeck)

    # We check for dealer blackjack.
    DealerSum = SumEval(DealerZero,DealerOne)
    if 21 in DealerSum:
        DealerAction(DealerZero,DealerOne)
        Result = tk.Label(MainPage,text = 'Dealer Blackjack',font = ('Cambria',14,'bold'))
        Result.grid(row = 1,column = 4,rowspan = 3,columnspan = 6)
        if HandCount >= 1:
            CenterSum = SumEval(CenterZero,CenterOne)
            if 21 in CenterSum:
                Pay += CenterBet
        if HandCount >= 2:
            LeftSum = SumEval(LeftZero,LeftOne)
            if 21 in LeftSum:
                Pay += LeftSum
        if HandCount == 3:
            RightSum = SumEval(RightZero,RightOne)
            if 21 in RightSum:
                Pay += RightSum
        isCenterClosed = True
        isLeftClosed = True
        isRightClosed = True
        currBank += Pay
        isReady = True

    # We check for player blackjack.
    if HandCount >= 1:
        CenterSum = SumEval(CenterZero,CenterOne)
        global CenterResult
        if 21 in CenterSum and 21 not in DealerSum:
            CenterResult = tk.Label(MainPage,
                                    text = 'Blackjack!',
                                    font = ('Cambria',14,'bold')
                                    )
            CenterResult.grid(row = 5,column = 5,columnspan = 3)
            Pay += 2.5 * CenterBet
            isCenterClosed = True
        elif 21 in CenterSum and 21 in DealerSum:
            CenterResult = tk.Label(MainPage,
                                    text = 'Push',
                                    font = ('Cambria',14,'bold')
                                    )
            CenterResult.grid(row = 5,column = 5,columnspan = 3)
    if HandCount >= 2:
        LeftSum = SumEval(LeftZero,LeftOne)
        global LeftResult
        if 21 in LeftSum and 21 not in DealerSum:
            LeftResult = tk.Label(MainPage,
                                  text = 'Blackjack!',
                                  font = ('Cambria',14,'bold')
                                  )
            LeftResult.grid(row = 5,column = 1,columnspan = 3)
            Pay += 2.5 * LeftBet
            isLeftClosed = True
        elif 21 in LeftSum and 21 in DealerSum:
            LeftResult = tk.Label(MainPage,
                                  text = 'Push',
                                  font = ('Cambria',14,'bold')
                                  )
            LeftResult.grid(row = 5,column = 1,columnspan = 3)
    if HandCount == 3 and 21:
        RightSum = SumEval(RightZero,RightOne)
        global RightResult
        if 21 in RightSum not in DealerSum:
            RightResult = tk.Label(MainPage,
                                   text = 'Blackjack!',
                                   font = ('Cambria',14,'bold')
                                   )
            RightResult.grid(row = 5,column = 9,columnspan = 3)
            Pay += 2.5 * RightBet
            isRightClosed = True
        elif 21 in RightSum and 21 in DealerSum:
            RightResult = tk.Label(MainPage,
                                   text = 'Push',
                                   font = ('Cambria',14,'bold')
                                   )
            RightResult.grid(row = 5,column = 9,columnspan = 3)
    
    # We assign card count values and set them as global.
    global DealerCardCount
    DealerCardCount = 3
    if HandCount >= 1:
        global CenterCardCount
        CenterCardCount = 2
    if HandCount >= 2:
        global LeftCardCount
        LeftCardCount = 2
    if HandCount == 3:
        global RightCardCount
        RightCardCount = 2

    # If all games are closed, we initialize gampeplay loop automatically.
    if HandCount == 1 and isCenterClosed:
        LoopGame('Pass')
    elif HandCount == 2 and isCenterClosed and isLeftClosed:
        LoopGame('Pass')
    elif HandCount == 3 and isCenterClosed and isLeftClosed and isRightClosed:
        LoopGame('Pass')        

# We define the loop function (run every time a button is pressed until stop condition).
def LoopGame(UserCmd):

    # We pull global values.
    global currDeck
    global currBank
    global Pay
    global isReady
    global CenterResult
    global LeftResult
    global RightResult
    global DealerCardCount
    if HandCount >= 1:
        global CenterCardCount
        global isCenterClosed
        global CenterBet
        global CenterZero
        global CenterOne
    if HandCount >= 2:
        global LeftCardCount
        global isLeftClosed
        global LeftBet
        global LeftZero
        global LeftOne
    if HandCount == 3:
        global RightCardCount
        global isRightClosed
        global RightBet
        global RightZero
        global RightOne
    
    # We respond to possible user inputs.
    if HandCount >= 1 and isCenterClosed == False:
        if UserCmd == 'HitCenterHand':
            CenterCardCount += 1
            if CenterCardCount == 3:
                global CenterThree
                CenterThree = PullCard(currDeck)
                global CenterThreeImg
                CenterThreeImg = CardImgGen(CenterThree)
                CenterThreeCard = tk.Label(MainPage,image = CenterThreeImg)
                CenterThreeCard.grid(row = 6,column = 7)
            elif CenterCardCount == 4:
                global CenterFour
                CenterFour = PullCard(currDeck)
                global CenterFourImg
                CenterFourImg = CardImgGen(CenterFour)
                CenterFourCard = tk.Label(MainPage,image = CenterFourImg)
                CenterFourCard.grid(row = 5,column = 5)
            elif CenterCardCount == 5:
                global CenterFive
                CenterFive = PullCard(currDeck)
                global CenterFiveImg
                CenterFiveImg = CardImgGen(CenterFive)
                CenterFiveCard = tk.Label(MainPage,image = CenterFiveImg)
                CenterFiveCard.grid(row = 5,column = 6)
            elif CenterCardCount == 6:
                global CenterSix
                CenterSix = PullCard(currDeck)
                global CenterSixImg
                CenterSixImg = CardImgGen(CenterSix)
                CenterSixCard = tk.Label(MainPage,image = CenterSixImg)
                CenterSixCard.grid(row = 5,column = 7)
            elif CenterCardCount == 7:
                global CenterSeven
                CenterSeven = PullCard(currDeck)
                global CenterSevenImg
                CenterSevenImg = CardImgGen(CenterSeven)
                CenterSevenCard = tk.Label(MainPage,image = CenterSevenImg)
                CenterSevenCard.grid(row = 4,column = 5)
            elif CenterCardCount == 8:
                global CenterEight
                CenterEight = PullCard(currDeck)
                global CenterEightImg
                CenterEightImg = CardImgGen(CenterEight)
                CenterEightCard = tk.Label(MainPage,image = CenterEightImg)
                CenterEightCard.grid(row = 4,column = 6)
            elif CenterCardCount == 9:
                global CenterNine
                CenterNine = PullCard(currDeck)
                global CenterNineImg
                CenterNineImg = CardImgGen(CenterNine)
                CenterNineCard = tk.Label(MainPage,image = CenterNineImg)
                CenterNineCard.grid(row = 4,column = 7)
            elif CenterCardCount == 10:
                global CenterTen
                CenterTen = PullCard(currDeck)
                global CenterTenImg
                CenterTenImg = CardImgGen(CenterTen)
                CenterTenCard = tk.Label(MainPage,image = CenterTenImg)
                CenterTenCard.grid(row = 3,column = 5)
            elif CenterCardCount == 11:
                global CenterEleven
                CenterEleven = PullCard(currDeck)
                global CenterElevenImg
                CenterElevenImg = CardImgGen(CenterEleven)
                CenterElevenCard = tk.Label(MainPage,image = CenterElevenImg)
                CenterElevenCard.grid(row = 3,column = 6)
        elif UserCmd == 'StandCenterHand':
            if CenterCardCount <= 3:
                CenterResultRow = 5
            elif CenterCardCount <= 6:
                CenterResultRow = 4
            elif CenterCardCount <= 9:
                CenterResultRow = 3
            elif CenterCardCount <= 11:
                CenterResultRow = 2
            CenterResult = tk.Label(MainPage,
                                    text = 'Stand',
                                    font = ('Cambria',14,'bold')
                                    )
            CenterResult.grid(row = CenterResultRow,column = 5,columnspan = 3)
            isCenterClosed = True
        elif UserCmd == 'DoubleCenterHand':
            if CenterCardCount <= 3:
                CenterResultRow = 5
            elif CenterCardCount <= 6:
                CenterResultRow = 4
            elif CenterCardCount <= 9:
                CenterResultRow = 3
            elif CenterCardCount <= 11:
                CenterResultRow = 2
            CenterDouble = PullCard(currDeck)
            global CenterDoubleImg
            CenterDoubleImg = CardImgGen(CenterDouble)
            CenterDoubleCard = tk.Label(MainPage,image = CenterDoubleImg)
            CenterDoubleCard.grid(row = 6,column = 7)
            Pay -= CenterBet
            CenterBet = 2 * CenterBet
            CenterResult = tk.Label(MainPage,
                                    text = 'Double',
                                    font = ('Cambria',14,'bold')
                                    )
            CenterResult.grid(row = CenterResultRow,column = 5,columnspan = 3)
            isCenterClosed = True
    if HandCount >= 2 and isLeftClosed == False:
        if UserCmd == 'HitLeftHand':
            LeftCardCount += 1
            if LeftCardCount == 3:
                global LeftThree
                LeftThree = PullCard(currDeck)
                global LeftThreeImg
                LeftThreeImg = CardImgGen(LeftThree)
                LeftThreeCard = tk.Label(MainPage,image = LeftThreeImg)
                LeftThreeCard.grid(row = 6,column = 3)
            elif LeftCardCount == 4:
                global LeftFour
                LeftFour = PullCard(currDeck)
                global LeftFourImg
                LeftFourImg = CardImgGen(LeftFour)
                LeftFourCard = tk.Label(MainPage,image = LeftFourImg)
                LeftFourCard.grid(row = 5,column = 1)
            elif LeftCardCount == 5:
                global LeftFive
                LeftFive = PullCard(currDeck)
                global LeftFiveImg
                LeftFiveImg = CardImgGen(LeftFive)
                LeftFiveCard = tk.Label(MainPage,image = LeftFiveImg)
                LeftFiveCard.grid(row = 5,column = 2)
            elif LeftCardCount == 6:
                global LeftSix
                LeftSix = PullCard(currDeck)
                global LeftSixImg
                LeftSixImg = CardImgGen(LeftSix)
                LeftSixCard = tk.Label(MainPage,image = LeftSixImg)
                LeftSixCard.grid(row = 5,column = 3)
            elif LeftCardCount == 7:
                global LeftSeven
                LeftSeven = PullCard(currDeck)
                global LeftSevenImg
                LeftSevenImg = CardImgGen(LeftSeven)
                LeftSevenCard = tk.Label(MainPage,image = LeftSevenImg)
                LeftSevenCard.grid(row = 4,column = 1)
            elif LeftCardCount == 8:
                global LeftEight
                LeftEight = PullCard(currDeck)
                global LeftEightImg
                LeftEightImg = CardImgGen(LeftEight)
                LeftEightCard = tk.Label(MainPage,image = LeftEightImg)
                LeftEightCard.grid(row = 4,column = 2)
            elif LeftCardCount == 9:
                global LeftNine
                LeftNine = PullCard(currDeck)
                global LeftNineImg
                LeftNineImg = CardImgGen(LeftNine)
                LeftNineCard = tk.Label(MainPage,image = LeftNineImg)
                LeftNineCard.grid(row = 4,column = 3)
            elif LeftCardCount == 10:
                global LeftTen
                LeftTen = PullCard(currDeck)
                global LeftTenImg
                LeftTenImg = CardImgGen(LeftTen)
                LeftTenCard = tk.Label(MainPage,image = LeftTenImg)
                LeftTenCard.grid(row = 3,column = 1)
            elif LeftCardCount == 11:
                global LeftEleven
                LeftEleven = PullCard(currDeck)
                global LeftElevenImg
                LeftElevenImg = CardImgGen(LeftEleven)
                LeftElevenCard = tk.Label(MainPage,image = LeftElevenImg)
                LeftElevenCard.grid(row = 3,column = 2)
        elif UserCmd == 'StandLeftHand':
            if LeftCardCount <= 3:
                LeftResultRow = 5
            elif LeftCardCount <= 6:
                LeftResultRow = 4
            elif LeftCardCount <= 9:
                LeftResultRow = 3
            elif LeftCardCount <= 11:
                LeftResultRow = 2
            LeftResult = tk.Label(MainPage,
                                  text = 'Stand',
                                  font = ('Cambria',14,'bold')
                                  )
            LeftResult.grid(row = LeftResultRow,column = 1,columnspan = 3)
            isLeftClosed = True
        elif UserCmd == 'DoubleLeftHand':
            if LeftCardCount <= 3:
                LeftResultRow = 5
            elif LeftCardCount <= 6:
                LeftResultRow = 4
            elif LeftCardCount <= 9:
                LeftResultRow = 3
            elif LeftCardCount <= 11:
                LeftResultRow = 2
            LeftDouble = PullCard(currDeck)
            global LeftDoubleImg
            LeftDoubleImg = CardImgGen(LeftDouble)
            LeftDoubleCard = tk.Label(MainPage,image = LeftDoubleImg)
            LeftDoubleCard.grid(row = 6,column = 3)
            Pay -= LeftBet
            LeftBet = 2 * LeftBet
            LeftResult = tk.Label(MainPage,
                                  text = 'Double',
                                  font = ('Cambria',14,'bold')
                                  )
            LeftResult.grid(row = LeftResultRow,column = 1,columnspan = 3)
            isLeftClosed = True
    if HandCount >= 3 and isRightClosed == False:
        if UserCmd == 'HitRightHand':
            RightCardCount += 1
            if RightCardCount == 3:
                global RightThree
                RightThree = PullCard(currDeck)
                global RightThreeImg
                RightThreeImg = CardImgGen(RightThree)
                RightThreeCard = tk.Label(MainPage,image = RightThreeImg)
                RightThreeCard.grid(row = 6,column = 11)
            elif RightCardCount == 4:
                global RightFour
                RightFour = PullCard(currDeck)
                global RightFourImg
                RightFourImg = CardImgGen(RightFour)
                RightFourCard = tk.Label(MainPage,image = RightFourImg)
                RightFourCard.grid(row = 5,column = 9)
            elif RightCardCount == 5:
                global RightFive
                RightFive = PullCard(currDeck)
                global RightFiveImg
                RightFiveImg = CardImgGen(RightFive)
                RightFiveCard = tk.Label(MainPage,image = RightFiveImg)
                RightFiveCard.grid(row = 5,column = 10)
            elif RightCardCount == 6:
                global RightSix
                RightSix = PullCard(currDeck)
                global RightSixImg
                RightSixImg = CardImgGen(RightSix)
                RightSixCard = tk.Label(MainPage,image = RightSixImg)
                RightSixCard.grid(row = 5,column = 11)
            elif RightCardCount == 7:
                global RightSeven
                RightSeven = PullCard(currDeck)
                global RightSevenImg
                RightSevenImg = CardImgGen(RightSeven)
                RightSevenCard = tk.Label(MainPage,image = RightSevenImg)
                RightSevenCard.grid(row = 4,column = 9)
            elif RightCardCount == 8:
                global RightEight
                RightEight = PullCard(currDeck)
                global RightEightImg
                RightEightImg = CardImgGen(RightEight)
                RightEightCard = tk.Label(MainPage,image = RightEightImg)
                RightEightCard.grid(row = 4,column = 10)
            elif RightCardCount == 9:
                global RightNine
                RightNine = PullCard(currDeck)
                global RightNineImg
                RightNineImg = CardImgGen(RightNine)
                RightNineCard = tk.Label(MainPage,image = RightNineImg)
                RightNineCard.grid(row = 4,column = 11)
            elif RightCardCount == 10:
                global RightTen
                RightTen = PullCard(currDeck)
                global RightTenImg
                RightTenImg = CardImgGen(RightTen)
                RightTenCard = tk.Label(MainPage,image = RightTenImg)
                RightTenCard.grid(row = 3,column = 9)
            elif RightCardCount == 11:
                global RightEleven
                RightEleven = PullCard(currDeck)
                global RightElevenImg
                RightElevenImg = CardImgGen(RightEleven)
                RightElevenCard = tk.Label(MainPage,image = RightElevenImg)
                RightElevenCard.grid(row = 3,column = 10)
        elif UserCmd == 'StandRightHand':
            if RightCardCount <= 3:
                RightResultRow = 5
            elif RightCardCount <= 6:
                RightResultRow = 4
            elif RightCardCount <= 9:
                RightResultRow = 3
            elif RightCardCount <= 11:
                RightResultRow = 2
            RightResult = tk.Label(MainPage,
                                   text = 'Double',
                                   font = ('Cambria',14,'bold')
                                   )
            RightResult.grid(row = RightResultRow,column = 9,columnspan = 3)
            isRightClosed = True
        elif UserCmd == 'DoubleRightHand':
            if RightCardCount <= 3:
                RightResultRow = 5
            elif RightCardCount <= 6:
                RightResultRow = 4
            elif RightCardCount <= 9:
                RightResultRow = 3
            elif RightCardCount <= 11:
                RightResultRow = 2
            RightDouble = PullCard(currDeck)
            global RightDoubleImg
            RightDoubleImg = CardImgGen(RightDouble)
            RightDoubleCard = tk.Label(MainPage,image = RightDoubleImg)
            RightDoubleCard.grid(row = 6,column = 11)
            Pay -= RightBet
            RightBet = 2 * RightBet
            RightResult = tk.Label(MainPage,
                                   text = 'Double',
                                   font = ('Cambria',14,'bold')
                                   )
            RightResult.grid(row = RightResultRow,column = 9,columnspan = 3)
            isRightClosed = True
        
    # We look for busts.
    if HandCount >= 1:
        if CenterCardCount == 2:
            CenterSum = SumEval(CenterZero,CenterOne)
        elif CenterCardCount == 3:
            CenterSum = SumEval(CenterZero,CenterOne,CenterThree)
        elif CenterCardCount == 4:
            CenterSum = SumEval(CenterZero,CenterOne,CenterThree,CenterFour)
        elif CenterCardCount == 5:
            CenterSum = SumEval(CenterZero,CenterOne,CenterThree,CenterFour,CenterFive)
        elif CenterCardCount == 6:
            CenterSum = SumEval(CenterZero,CenterOne,CenterThree,CenterFour,CenterFive,CenterSix)
        elif CenterCardCount == 7:
            CenterSum = SumEval(CenterZero,CenterOne,CenterThree,CenterFour,CenterFive,CenterSix,
                                CenterSeven)
        elif CenterCardCount == 8:
            CenterSum = SumEval(CenterZero,CenterOne,CenterThree,CenterFour,CenterFive,CenterSix,
                                CenterSeven,CenterEight)
        elif CenterCardCount == 9:
            CenterSum = SumEval(CenterZero,CenterOne,CenterThree,CenterFour,CenterFive,CenterSix,
                                CenterSeven,CenterEight,CenterNine)
        elif CenterCardCount == 10:
            CenterSum = SumEval(CenterZero,CenterOne,CenterThree,CenterFour,CenterFive,CenterSix,
                                CenterSeven,CenterEight,CenterNine,CenterTen)
        elif CenterCardCount == 11:
            CenterSum = SumEval(CenterZero,CenterOne,CenterThree,CenterFour,CenterFive,CenterSix,
                                CenterSeven,CenterEight,CenterNine,CenterTen,CenterEleven)
        if CenterSum[0] > 21 and CenterSum[1] > 21 and not isCenterClosed:
            if CenterCardCount <= 3:
                CenterResultRow = 5
            elif CenterCardCount <= 6:
                CenterResultRow = 4
            elif CenterCardCount <= 9:
                CenterResultRow = 3
            elif CenterCardCount <= 11:
                CenterResultRow = 2
            CenterResult = tk.Label(MainPage,
                                    text = 'Bust',
                                    font = ('Cambria',14,'bold')
                                    )
            CenterResult.grid(row = CenterResultRow,column = 5,columnspan = 3)
            isCenterClosed = True
    if HandCount >= 2:
        if LeftCardCount == 2:
            LeftSum = SumEval(LeftZero,LeftOne)
        elif LeftCardCount == 3:
            LeftSum = SumEval(LeftZero,LeftOne,LeftThree)
        elif LeftCardCount == 4:
            LeftSum = SumEval(LeftZero,LeftOne,LeftThree,LeftFour)
        elif LeftCardCount == 5:
            LeftSum = SumEval(LeftZero,LeftOne,LeftThree,LeftFour,LeftFive)
        elif LeftCardCount == 6:
            LeftSum = SumEval(LeftZero,LeftOne,LeftThree,LeftFour,LeftFive,LeftSix)
        elif LeftCardCount == 7:
            LeftSum = SumEval(LeftZero,LeftOne,LeftThree,LeftFour,LeftFive,LeftSix,
                                LeftSeven)
        elif LeftCardCount == 8:
            LeftSum = SumEval(LeftZero,LeftOne,LeftThree,LeftFour,LeftFive,LeftSix,
                                LeftSeven,LeftEight)
        elif LeftCardCount == 9:
            LeftSum = SumEval(LeftZero,LeftOne,LeftThree,LeftFour,LeftFive,LeftSix,
                                LeftSeven,LeftEight,LeftNine)
        elif LeftCardCount == 10:
            LeftSum = SumEval(LeftZero,LeftOne,LeftThree,LeftFour,LeftFive,LeftSix,
                                LeftSeven,LeftEight,LeftNine,LeftTen)
        elif LeftCardCount == 11:
            LeftSum = SumEval(LeftZero,LeftOne,LeftThree,LeftFour,LeftFive,LeftSix,
                                LeftSeven,LeftEight,LeftNine,LeftTen,LeftEleven)
        if LeftSum[0] > 21 and LeftSum[1] > 21 and not isLeftClosed:
            if LeftCardCount <= 3:
                LeftResultRow = 5
            elif LeftCardCount <= 6:
                LeftResultRow = 4
            elif LeftCardCount <= 9:
                LeftResultRow = 3
            elif LeftCardCount <= 11:
                LeftResultRow = 2
            LeftResult = tk.Label(MainPage,
                                  text = 'Bust',
                                  font = ('Cambria',14,'bold')
                                  )
            LeftResult.grid(row = LeftResultRow,column = 1,columnspan = 3)
            isLeftClosed = True
    if HandCount == 3:
        if RightCardCount == 2:
            RightSum = SumEval(RightZero,RightOne)
        elif RightCardCount == 3:
            RightSum = SumEval(RightZero,RightOne,RightThree)
        elif RightCardCount == 4:
            RightSum = SumEval(RightZero,RightOne,RightThree,RightFour)
        elif RightCardCount == 5:
            RightSum = SumEval(RightZero,RightOne,RightThree,RightFour,RightFive)
        elif RightCardCount == 6:
            RightSum = SumEval(RightZero,RightOne,RightThree,RightFour,RightFive,RightSix)
        elif RightCardCount == 7:
            RightSum = SumEval(RightZero,RightOne,RightThree,RightFour,RightFive,RightSix,
                                RightSeven)
        elif RightCardCount == 8:
            RightSum = SumEval(RightZero,RightOne,RightThree,RightFour,RightFive,RightSix,
                                RightSeven,RightEight)
        elif RightCardCount == 9:
            RightSum = SumEval(RightZero,RightOne,RightThree,RightFour,RightFive,RightSix,
                                RightSeven,RightEight,RightNine)
        elif RightCardCount == 10:
            RightSum = SumEval(RightZero,RightOne,RightThree,RightFour,RightFive,RightSix,
                                RightSeven,RightEight,RightNine,RightTen)
        elif RightCardCount == 11:
            RightSum = SumEval(RightZero,RightOne,RightThree,RightFour,RightFive,RightSix,
                                RightSeven,RightEight,RightNine,RightTen,RightEleven)
        if RightSum[0] > 21 and RightSum[1] > 21 and not isRightClosed:
            if RightCardCount <= 3:
                RightResultRow = 5
            elif RightCardCount <= 6:
                RightResultRow = 4
            elif RightCardCount <= 9:
                RightResultRow = 3
            elif RightCardCount <= 11:
                RightResultRow = 2
            RightResult = tk.Label(MainPage,
                                   text = 'Bust',
                                   font = ('Cambria',14,'bold')
                                   )
            RightResult.grid(row = RightResultRow,column = 9,columnspan = 3)
            isRightClosed = True
    
    # We evaluate if all games are closed.
    isGameClosed = False
    if HandCount == 1 and isCenterClosed:
        isGameClosed = True
    elif HandCount == 2 and isCenterClosed and isLeftClosed:
        isGameClosed = True
    elif HandCount == 3 and isCenterClosed and isLeftClosed and isRightClosed:
        isGameClosed = True
    
    # If all games are closed, we finish the hand.
    if isGameClosed and not isReady:
        if HandCount >= 1:
            if CenterSum[0] > 21 and CenterSum[1] <= 21:
                CenterVal = CenterSum[1]
            elif CenterSum[1] > 21 and CenterSum[0] <= 21:
                CenterVal = CenterSum[0]
            else:
                CenterVal = max(CenterSum)
        if HandCount >= 2:
            if LeftSum[0] > 21 and LeftSum[1] <= 21:
                LeftVal = LeftSum[1]
            elif LeftSum[1] > 21 and LeftSum[0] <= 21:
                LeftVal = LeftSum[0]
            else:
                LeftVal = max(LeftSum)
        if HandCount >= 3:
            if RightSum[0] > 21 and RightSum[1] <= 21:
                RightVal = RightSum[1]
            elif RightSum[1] > 21 and RightSum[0] <= 21:
                RightVal = RightSum[0]
            else:
                RightVal = max(RightSum)
        if HandCount == 1 and CenterVal == 21:
            DealerSum = max(SumEval(DealerOne,DealerZero))
        elif HandCount == 2 and CenterVal == 21 and LeftVal == 21:
            DealerSum = max(SumEval(DealerOne,DealerZero))
        elif HandCount == 3 and CenterVal == 21 and LeftVal == 21 and RightVal == 21:
            DealerSum = max(SumEval(DealerOne,DealerZero))
        else:
            DealerSum = DealerAction(DealerZero,DealerOne)
        if DealerSum > 21:
            isDealerBust = True
            Result = tk.Label(MainPage,text = 'Dealer Bust!',font = ('Cambria',14,'bold'))
            Result.grid(row = 1,column = 4,rowspan = 3,columnspan = 6)
            if HandCount >= 1:
                Pay += 2 * CenterBet
            if HandCount >= 2:
                Pay += 2 * LeftBet
            if HandCount >= 3:
                Pay += 2 * RightBet
        else:
            isDealerBust = False
        if HandCount >= 1:
            CenterResult.destroy()
            if CenterCardCount <= 3:
                CenterResultRow = 5
            elif CenterCardCount <= 6:
                CenterResultRow = 4
            elif CenterCardCount <= 9:
                CenterResultRow = 3
            elif CenterCardCount <= 11:
                CenterResultRow = 2
            if CenterVal == 21 and CenterCardCount == 2:
                pass
            elif DealerSum == CenterVal and CenterVal <= 21:
                Pay += CenterBet
                CenterResult = tk.Label(MainPage,
                                        text = 'Push',
                                        font = ('Cambria',14,'bold')
                                        )
                CenterResult.grid(row = CenterResultRow,column = 5,columnspan = 3)
            elif (DealerSum < CenterVal and CenterVal <= 21) or isDealerBust:
                Pay += 2 * CenterBet
                CenterResult = tk.Label(MainPage,
                                        text = 'Win',
                                        font = ('Cambria',14,'bold')
                                        )
                CenterResult.grid(row = CenterResultRow,column = 5,columnspan = 3)
            elif DealerSum > CenterVal or CenterVal > 21:
                CenterResult = tk.Label(MainPage,
                                        text = 'Loss',
                                        font = ('Cambria',14,'bold')
                                        )
                CenterResult.grid(row = CenterResultRow,column = 5,columnspan = 3)
        if HandCount >= 2:
            LeftResult.destroy()
            if LeftCardCount <= 3:
                LeftResultRow = 5
            elif LeftCardCount <= 6:
                LeftResultRow = 4
            elif LeftCardCount <= 9:
                LeftResultRow = 3
            elif LeftCardCount <= 11:
                LeftResultRow = 2
            if LeftVal == 21 and LeftCardCount == 2:
                pass
            elif DealerSum == LeftVal and LeftVal <= 21:
                Pay += LeftBet
                LeftResult = tk.Label(MainPage,text = 'Push',font = ('Cambria',14,'bold'))
                LeftResult.grid(row = LeftResultRow,column = 1,columnspan = 3)
            elif (DealerSum < LeftVal and LeftVal <= 21) or isDealerBust:
                Pay += 2 * LeftBet
                LeftResult = tk.Label(MainPage,text = 'Win',font = ('Cambria',14,'bold'))
                LeftResult.grid(row = LeftResultRow,column = 1,columnspan = 3)
            elif DealerSum > LeftVal or LeftVal > 21:
                LeftResult = tk.Label(MainPage,text = 'Loss',font = ('Cambria',14,'bold'))
                LeftResult.grid(row = LeftResultRow,column = 1,columnspan = 3)
        if HandCount == 3:
            RightResult.destroy()
            if RightCardCount <= 3:
                RightResultRow = 5
            elif RightCardCount <= 6:
                RightResultRow = 4
            elif RightCardCount <= 9:
                RightResultRow = 3
            elif RightCardCount <= 11:
                RightResultRow = 2
            if RightVal == 21 and RightCardCount == 2:
                pass
            elif DealerSum == RightVal and RightVal <= 21:
                Pay += RightBet
                RightResult = tk.Label(MainPage,
                                       text = 'Push',
                                       font = ('Cambria',14,'bold')
                                       )
                RightResult.grid(row = RightResultRow,column = 9,columnspan = 3)
            elif (DealerSum < RightVal and RightVal <= 21) or isDealerBust:
                Pay += 2 * RightBet
                RightResult = tk.Label(MainPage,
                                       text = 'Win',
                                       font = ('Cambria',14,'bold')
                                       )
                RightResult.grid(row = RightResultRow,column = 9,columnspan = 3)
            elif DealerSum > RightVal or RightVal > 21:
                RightResult = tk.Label(MainPage,
                                       text = 'Loss',
                                       font = ('Cambria',14,'bold')
                                       )
                RightResult.grid(row = RightResultRow,column = 9,columnspan = 3)
        currBank += Pay
        isReady = True
# -----------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------
# We generate the main page.
# -----------------------------------------------------------------------------------
# We call on the window generator class.
if isLaunch:
    MainPage = WindowGenerator()
    global currDeck
    currDeck = DeckGenerator(DeckCount)
    global currBank
    currBank = 100
    isLaunch = False
    global isReady
    isReady = True

# We define hex codes.
MainHexCode_Prim = '#094f04'
MainHexCode_Btn = '#a11212'

# We configure the window.
MainPage.geometry('1300x900')
MainPage.title('Black Jack Simulator')
MainPage.config(background = MainHexCode_Prim)

# We configure the grid.
for i in range(11):
    MainPage.grid_rowconfigure(i,weight = 1)
for i in range(13):
    MainPage.grid_columnconfigure(i,weight = 1)

# We define relevant icons.
global PileImg
PileImg = Image.open('.\\Icons\\BetStack.png')
PileImg = PileImg.resize((60,60))
PileImg = ImageTk.PhotoImage(PileImg)
global BankImg
BankImg = Image.open('.\\Icons\\BankStack.png')
BankImg = BankImg.resize((75,75))
BankImg = ImageTk.PhotoImage(BankImg)

# We generate permanent fixtures.
PermanentWidgets()

# We configure player button placement.
if HandCount >= 1:
    CenterHandWidgets()
if HandCount >= 2:
    LeftHandWidgets()
if HandCount == 3:
    RightHandWidgets()

# We generate the main page.
MainPage.mainloop()
# -----------------------------------------------------------------------------------