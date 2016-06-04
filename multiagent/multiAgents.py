# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    actualPosition = currentGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    ghostDistance = []
    for ghostState in newGhostStates:
      ghostDistance += [manhattanDistance(newPos,ghostState.getPosition())]
    
    foodDistance = []
    for food in newFood.asList():
      foodDistance += [manhattanDistance(newPos,food)]

    capsuleDistance = []
    for capsule in successorGameState.getCapsules():
      capsuleDistance += [manhattanDistance(newPos,capsule)]  

    score = successorGameState.getScore()
    ghost = 0    
    if(newScaredTimes[0]>1 and newScaredTimes[0]<26):
      ghost = -sum(ghostDistance)
    else:
      ghost = sum(ghostDistance)

    return ghost-(sum(foodDistance)/(successorGameState.getNumFood()+0.1))-5*successorGameState.getNumFood()+4*score

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    def findMax(gameState,depth):
        depth = depth + 1
        if depth==self.depth or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
        v = -float("inf")
        validActions=[]
        for a in gameState.getLegalActions(0):
          if(a!=Directions.STOP):
            validActions+=[a] 
        for action in validActions:
          v = max(v,findMin(gameState.generateSuccessor(0,action),depth,1))   
        return v
                
    def findMin(gameState,depth,ghost):
        if gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
        v = float("inf")
        
        validActions=gameState.getLegalActions(ghost)
        
        for action in validActions:
          if ghost<gameState.getNumAgents()-1:
            v = min(v,findMin(gameState.generateSuccessor(ghost,action),depth,ghost+1))
          else:
            v = min(v,findMax(gameState.generateSuccessor(ghost,action),depth))

        return v
    pacmanActions = gameState.getLegalActions(0)
    best = -float("inf")
    bestAction = ''
    for action in pacmanActions:
        depth = 0
        tempBest = findMin(gameState.generateSuccessor(0, action), depth,1)
        if tempBest > best:
            best = tempBest
            bestAction = action        
    print best
    return bestAction           
                  
class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    def findMax(gameState,depth,alfa,beta):
        depth = depth + 1
        if depth==self.depth or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
        v = -float("inf")
        validActions=[]
        for a in gameState.getLegalActions(0):
          if(a!=Directions.STOP):
            validActions+=[a] 
        for action in validActions:
          v = max(v,findMin(gameState.generateSuccessor(0,action),depth,alfa,beta,1))
          if(v>= beta):
            return v
          alfa = max(alfa,v)      
        return v
                
    def findMin(gameState,depth,alfa,beta,ghost):
        if gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
        v = float("inf")
        
        validActions=gameState.getLegalActions(ghost)
        
        for action in validActions:
          if(ghost<gameState.getNumAgents()-1):
            v = min(v,findMin(gameState.generateSuccessor(ghost,action),depth,alfa,beta,ghost+1))
          else:
            v = min(v,findMax(gameState.generateSuccessor(ghost,action),depth,alfa,beta))
          if (v<=alfa):
            return v
          beta = min(beta,v)  
        return v
    
    pacmanActions = gameState.getLegalActions(0)
    best = -float("inf")
    alfa = -float("inf")
    beta = float("inf")
    bestAction = ''
    for action in pacmanActions:
        depth = 0
        tempBest = findMin(gameState.generateSuccessor(0, action), depth,alfa,beta,1)
        if tempBest > best:
            best = tempBest
            bestAction = action
    print best                
    return bestAction 

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    def findMax(gameState,depth):
        depth = depth + 1
        if depth==self.depth or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
        v = -float("inf")
        validActions=[]
        for a in gameState.getLegalActions(0):
          if(a!=Directions.STOP):
            validActions+=[a] 
        for action in validActions:
          v = max(v,findRand(gameState.generateSuccessor(0,action),depth,1))   
        return v
                
    def findRand(gameState,depth,ghost):
        if gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
        v = 0
        
        validActions=gameState.getLegalActions(ghost)
        
        for action in validActions:
          if ghost<gameState.getNumAgents()-1:
            v += findRand(gameState.generateSuccessor(ghost,action),depth,ghost+1)
          else:
            v += findMax(gameState.generateSuccessor(ghost,action),depth)

        return v
    pacmanActions = gameState.getLegalActions(0)
    best = -float("inf")
    bestAction = ''
    for action in pacmanActions:
        depth = 0
        tempBest = findRand(gameState.generateSuccessor(0, action), depth,1)
        if tempBest > best:
            best = tempBest
            bestAction = action        
    return bestAction  

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

