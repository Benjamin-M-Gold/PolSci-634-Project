import math
import numpy as np
from os.path import exists
import pandas as pd

def mean(bill):
    mean = 0
    if len(bill[3]) == 0:
        return bill[1][1]
    for i in bill[3]:
        mean = mean + i[1]
    return mean/(len(bill[3]))

def propEndorse(bill, legislator):
    if len(bill[3]) == 0:
        return bill[1][1]
    candidate = legislator[4]
    number = 0
    for i in bill[3]:
        if i[4] == candidate:
            number = number + 1
    return number/len(bill[3])

# Initializes legislators
def addInitialNodes(N, meanDifference): 		#Initialize Population

	#lists of agents
    agentList = list()		#List of all people

    #initialize internal variables for each run
    

	#Create list of individuals
    personcounter=0 		#counter for setting personNum
    #Create lists
    while personcounter<N:
        #Set node properties
        #A node is a list of properties: personcounter, b, c, rev, lastrev
        #Could also do this with objects but that slows down code somewhat
        w = np.random.normal(.5,1, size = None)
        partisanship =w*np.random.normal(loc= 20, scale=10, size=None) + (1-w)*np.random.normal(loc= 20+meanDifference, scale=10, size=None) #set partisanship
        district_lean = np.random.randint(-3, 20) #set district lean (decoded not to test changes to this to keep parameters small, but kept it in so indexing wouldn't change)
        if partisanship < 50: 
            party = "R"
        elif partisanship > 50:
            party = "D"
        else:
            e = np.randint(0,1)
            if e == 0:
                party = "R"
            else:
                party = "D"
        endorsed_cand = np.random.randint(0,9) #Pick endorsed candidate
        endorsed_bill = list()
        cosponsors = list()


        #create node with those properties
        node = [personcounter, partisanship, party, district_lean, endorsed_cand, endorsed_bill, cosponsors]
        #add to lists
        agentList.append(node)

        personcounter+=1
    return [agentList]
    
# defines how utility is calculated
def utility(bill, legislator, strength):
    return 0 - abs(bill[2] - legislator[1]) - abs(mean(bill) -  legislator[1]) +  strength * propEndorse(bill, legislator)

# defines how to create a bill
def createBill(number, listz):
    sponsor = np.random.randint(0, len(listz[0])-1)
    for person in listz[0]:
        if person[0] == sponsor:
            mean = person[1]
            break
    ideology = np.random.normal(loc = mean, scale = 1, size = None)
    sponsors = list()
    sponsors.append(listz[0][sponsor])
    bill = [number, listz[0][sponsor], ideology, sponsors]
    listz[0][sponsor][5].append(bill)
    return bill

# checks when the simulation should end.
def checkcondition(time, changes, lastChanges): # Keeps track of how many iterations you/ve already gone over and how many people changed their minds in the last period
    if time > 500 or changes - lastChanges <= 5:
        return True
    else:
        return False

# simple function to check if a list has an object
def contains(listerz, objectz):
    for i in range(len(listerz)):
        if listerz[i] == objectz:
            return i
    return -1

#inputs all the bills and turns them into an adjacenty matrix of who has ties. 
def collectAdjData (bills, legislators): # inputs legislators so it can be applicable to different sized legislatures
    adj_matrix = np.zeros((len(legislators[0]), len(legislators[0])))
    for bill in bills:
        for i in range(len(bill[3])):
            for j in range(len(bill[3])):
                if i != j:
                    adj_matrix[bill[3][i][0]][bill[3][j][0]] = adj_matrix[bill[3][i][0]][bill[3][j][0]] + 1
    return adj_matrix

#creates a matrix where each entry is the ideological distance of every pair of legislators
def collectDistances(legislators):
    dist_matrix = np.zeros((len(legislators[0]), len(legislators[0])))
    for i in range(len(legislators[0])):
        for j in range(len(legislators[0])):
            if i != j:
                dist_matrix[i][j] = abs(legislators[0][i][1] - legislators[0][j][1])
    return dist_matrix

#creates a matrix with a 1 if two legislators endorsed the same candidate and a 0 otherwise
def endorseMatrix(legislators):
    endorse_matrix = np.zeros((len(legislators[0]), len(legislators[0])))
    for i in range(len(legislators[0])):
        for j in range(len(legislators[0])):
            if i != j:
                if legislators[0][i][4] == legislators[0][j][4]:
                    endorse_matrix[i][j] = 1
    return endorse_matrix


################# defines the actual model #################
# each time t legislators will make a probbalistic decision about whether to sponsor a bill or not
# this decision comes based on the utility funciton defined in a previous function
# new legislation is created over the first 100 periods so any legislative sessiion will last at least t periods
# the simulation ends when either a certain amount of time has passed without it reaching a steady state or when it reaches a steady state
# because actors make probabalistic decisions this model will never reach a purely steady state
# I define this model to be in steady state when fewer than 5 binary "cosponsor or don't consponsor" are made in an iteration
#43,500 of these decisions are made each run of the model so if less than 5 of these decisions change than I would argue the model is fairly stable
def modelRun(strength, meanDifference):
    meanDiff = meanDifference
    utilityStrength = strength
    legislators = addInitialNodes(435, meanDiff)
    numLegislators = len(legislators[0])
    endCondition = False
    bills = list()
    t = 1 #tracks time
    n = 0 #tracks how many people change cosponsorship at any time period
    lastN = 0 #tracks n at the last time step
    bills.append(createBill(0, legislators))
    while(endCondition == False): #runs model until certain state is met
        if(t <= 10): # new bills are only drafted in the first 100 time periods
            bills.append(createBill(t, legislators)) #creates a new bill according to previous function
            for legislator in legislators[0]:
                bill_num = 0
                for bill in bills: # nested loops have each legislator condsider each bill
                    if bill[1] != legislator[0]: #ensures original sponsor can't leave bill
                        utilProp = 100/(1+math.exp(utility(bill, legislator, utilityStrength)))
                        threshold = np.random.uniform(0,100)
                        if threshold > utilProp:
                            if contains(bill[3], legislator) == -1:
                                bill[3].append(legislator)
                                n = n +1
                            if contains(legislator[5], bill) == -1:
                                legislator[5].append(bill)
                                n = n +1
                        else:
                            if contains(bill[3], legislator) != -1:
                                bill[3].remove(legislator)
                                n = n +1
                            if contains(legislator[5], bill) != -1:
                                legislator[5].remove(bill) 
                                n = n +1
            t = t + 1
            endCondition = checkcondition(t, n, lastN)
            lastN = n
        else:
            for legislator in legislators[0]:
                bill_num = 0
                for bill in bills: # nested loops have each legislator condsider each bill
                    if bill[1] != legislator[0]: #ensures original sponsor can't leave bill
                        utilProp = 100/(1+math.exp(utility(bill, legislator, utilityStrength)))
                        threshold = np.random.uniform(0,100)
                        if threshold > utilProp:
                            if contains(bill[3], legislator) == -1:
                                bill[3].append(legislator)
                                n = n +1
                            if contains(legislator[5], bill) == -1:
                                legislator[5].append(bill)
                                n = n +1
                        else:
                            if contains(bill[3], legislator) != -1:
                                bill[3].remove(legislator)
                                n = n +1
                            if contains(legislator[5], bill) != -1:
                                legislator[5].remove(bill) 
                                n = n +1
            t = t + 1
            endCondition = checkcondition(t, n, lastN)
            lastN = n
    edge_list = collectAdjData(bills, legislators)
    distances = collectDistances(legislators)
    endorsement_matrix = endorseMatrix(legislators)
    return edge_list, distances, endorsement_matrix, meanDiff, utilityStrength, numLegislators
        

def writeData(edge_list, distances, endorsement_matrix, numLegislators, spread, strength):
    for i in range(numLegislators):
        for j in range(numLegislators):
            if j > i:
                df.loc[len(df.index)] = [spread, strength, distances[i][j], edge_list[i][j], endorsement_matrix[i][j]]

#tester, tester2, tester3, t = modelRun()
#for bill in tester:
#print(tester, tester2, tester3)

## ACTUALLY RUNS MY TESTS ##

#Creates DataFrame where I'll store my information
dict = {'Spread': [], 'Cosponsorship Strength': [], 'ideology':[], 'BIlls Cosponsored': [], 'Co-Endorsement':[]}
df = pd.DataFrame(dict)
print(df)
ideologyDifferences = [0, 10, 40, 50]
endorcementImportance = [50, 100, 200]
t = 0
for difference in ideologyDifferences:
    for importance in endorcementImportance:
        t = t +1
        edge_list, distances, endorsement_matrix, meanDiff, utilityStrength, numLegislators = modelRun(importance, difference)
        writeData(edge_list, distances, endorsement_matrix, numLegislators, meanDiff, utilityStrength)
        print(t)
print(df)
df.to_csv("DataTrial3.csv")
