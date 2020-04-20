'''
@author: mroch
'''

# Game representation and mechanics
import checkerboard

# tonto - Professor Roch's not too smart strategy
# You are not given source code to this, but compiled .pyc files
# are available for Python 3.7 and 3.8 (fails otherwise).
# This will let you test some of your game logic without having to worry
# about whether or not your AI is working and let you pit your player
# against another computer player.
#
# Decompilation is cheating, don't do it.  Big sister is watching you :-)

# Python cand load compiled modules using the imp module (deprecated)
# We'll format the path to the tonto module based on the
# release of Python.  Note that we provided tonto compilations for Python 3.7
# and 3.8.  If you're not using one of these, it won't work.
import imp
import ai
import sys
major = sys.version_info[0]
minor = sys.version_info[1]
modpath = "__pycache__/tonto.cpython-{}{}.pyc".format(major, minor)
tonto = imp.load_compiled("tonto", modpath)


# human - human player, prompts for input    
import human
import boardlibrary # might be useful for debugging

from timer import Timer
from statistics import mean
        


#Where does the checkers strategy come into play

def Game(red=ai.Strategy, black=tonto.Strategy, 
         maxplies=1, init=None, verbose=True, firstmove=0):
    """Game(red, black, maxplies, init, verbose, turn)
    Start a game of checkers
    red,black - Strategy classes (not instances)
    maxplies - # of turns to explore (default 10)
    init - Start with given board (default None uses a brand new game)
    verbose - Show messages (default True)
    firstmove - Player N starts 0 (red) or 1 (black).  Default 0. 
    """

    # Don't forget to create instances of your strategy,
    # e.g. black('b', checkerboard.CheckerBoard, maxplies)
     
    "Define board and instances of the strategy"
    board = checkerboard.CheckerBoard()
    redplayer = red('r',board, maxplies)
    blackplayer = black('b', board, maxplies)
    maxp1 = redplayer.maxplayer
    minp2 = redplayer.minplayer
    
    "Initialize variables and data structures"
    moveNum = 0
    lastCap = 0
    captures = 0
    moveTimesp1 = []
    moveTimesp2 = []
    
    #print out games initial information
    print("Invoked Game(","red=", red,",","black=", black,",", "maxplies =", maxplies,")\n\n")
    print("How about a nice game of checkers?")
    finished = False
    
    "Determine which player starts the game"
    if firstmove == 1:
        maxplayer = False
    
    #Begin loop for game
    tm = Timer()  
    while finished == False: 
        minplayer = True
        maxplayer = True  
        #Red players moves
        while maxplayer == True:
            terminal, winner = board.is_terminal()
            if terminal:
                print("The game is finished")
                if winner != None:
                    print("player", winner, "wins") 
                else: 
                    print("The game is a draw")
                    print("r average move time", mean(moveTimesp1))
                    print("b average move time", mean(moveTimesp2)) 
                    finished = True
                    return
            print("Player r turn")
            print(board)
            t = Timer()

            move = redplayer.play(board)  
            
            moves_ = board.get_actions(maxp1)
            for a in moves_:
                cap = len(a[1]) > 2
                if cap:
                    captures += 1 
                    lastCap = 0
                    break
                else: 
                    lastCap += 1
                    break
            if cap:
                print("move", moveNum, "by", maxp1, ":", "from", move[1][0], "to", \
                      move[1][1][0:2],"capturing", move[1][1][2], " Result:")      
            else:
                print("move", moveNum, "by", maxp1, ":", "from", move[1][0], "to", \
                      move[1][1], " Result:")  
            board = board.move(move[1])
            moveNum += 1
            ts = round(t.elapsed_s(),2)
            moveTimesp1.append(ts)
            time_min = round(tm.elapsed_min(),2)             
            
            print(board)
            print("Pawn/King count: r", board.get_pawnsN()[0], "R", board.get_kingsN()[0], \
                  "b", board.get_pawnsN()[1], "B", board.get_kingsN()[1], "Time - move:", \
                  ts, "s", "game", time_min, "m")
            print("Moves since last capture", lastCap, "last pawn advance", 0,"\n")
            maxplayer = False
        #Black players moves  
        while minplayer == True:
            terminal, winner = board.is_terminal()
            if terminal:
                print("The game is finished")
                if winner != None:
                    print("player", winner, "wins") 
                else: 
                    print("The game is a draw")
                    print("r average move time", mean(moveTimesp1))
                    print("b average move time", mean(moveTimesp2))
                    finished = True
                    return 
            print("Player b turn")
            print(board)
            t2 = Timer()

            move = blackplayer.play(board)     
            moves_ = board.get_actions(maxp1)
            for a in moves_:
                cap = len(a[1]) > 2
                if cap:
                    captures += 1 
                    lastCap = 0
                    break
                else: 
                    lastCap += 1
                    break                 
            if cap:
                print("move", moveNum, "by", minp2, ":", "from", move[1][0], "to", \
                      move[1][1][0:2],"capturing", move[1][1][2], " Result:")      
            else:
                print("move", moveNum, "by", minp2, ":", "from", move[1][0], "to", \
                      move[1][1], " Result:")  
    
            board = board.move(move[1])
            moveNum += 1
            ts = round(t2.elapsed_s(),2)
            moveTimesp2.append(ts)
            time_min = round(tm.elapsed_min(),2)
            
            "Print out board and results from the turn"
            print(board)
            print("Pawn/King count: r", board.get_pawnsN()[0], "R", \
                  board.get_kingsN()[0], "b", board.get_pawnsN()[1], "B", \
                  board.get_kingsN()[1], "Time - move:", ts, "s", "game", time_min, "m")
            print("Moves since last capture", lastCap, "last pawn advance", captures, "\n")  
            minplayer = False
     

            
if __name__ == "__main__":
    #Game(init=boardlibrary.boards["multihop"])
    #Game(init=boardlibrary.boards["StrategyTest1"])
    #Game(init=boardlibrary.boards["EndGame1"], firstmove = 1)
    Game()
        
        
#Questions:
#1. why does tonto work with move[1] and not ai?
    #2. plies acting weird
    #3. accessing the action that corresponds to the utulity
        
                    
            
        

    
    
