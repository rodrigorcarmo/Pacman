# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    stack = util.Stack()
    visited = []
    stack.push((problem.getStartState(), []))
    while not stack.isEmpty():
        estado, caminho = stack.pop()

        if problem.isGoalState(estado):
            return caminho

        if not estado in visited:
            visited.append(estado)
            proximos = problem.getSuccessors(estado)
            for item in proximos:
                stack.push((item[0], caminho + [item[1]]))
    return []


def breadthFirstSearch(problem):
    "Search the shallowest nodes in the search tree first. [p 81]"
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    visited = []
    queue.push((problem.getStartState(), []))
    while not queue.isEmpty():
        estado, caminho = queue.pop()

        if problem.isGoalState(estado):
            return caminho

        if not estado in visited:
            visited.append(estado)
            proximos = problem.getSuccessors(estado)
            for item in proximos:
                queue.push((item[0], caminho + [item[1]]))
    return []

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    queue = util.PriorityQueue()
    visited = []
    queue.push((problem.getStartState(), []), 0)
    while not queue.isEmpty():
        estado, caminho = queue.pop()

        if problem.isGoalState(estado):
            return caminho

        if not estado in visited:
            visited.append(estado)
            proximos = problem.getSuccessors(estado)
            for item in proximos:
                queue.push((item[0], caminho + [item[1]]), problem.getCostOfActions(caminho + [item[1]]))
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    queue = util.PriorityQueue()
    visited = []
    queue.push((problem.getStartState(), []), heuristic(problem.getStartState(), problem))
    while not queue.isEmpty():
        estado, caminho = queue.pop()

        if problem.isGoalState(estado):
            return caminho

        if not estado in visited:
            visited.append(estado)
            proximos = problem.getSuccessors(estado)
            for item in proximos:
                queue.push((item[0], caminho + [item[1]]),
                           problem.getCostOfActions(caminho + [item[1]]) + heuristic(item[0], problem))
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
