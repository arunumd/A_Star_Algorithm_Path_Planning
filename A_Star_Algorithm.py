from __future__ import print_function
from itertools import groupby
from operator import itemgetter
import math
import timeit
import csv
import random

class Move:

    """Eight directional movement"""
    def __init__(self,vertexStart,vertexFinish):
        self.costgLinear = 10
        self.costgDiagonal = 14
        self.vertexStart = vertexStart
        self.vertexFinish = vertexFinish

    def setstartpoint(self,vertexStart):
        self.vertexStart = vertexStart

    def distance(self):
        return ((self.vertexFinish[0] - self.vertexStart[0]) + (self.vertexFinish[1] - self.vertexStart[1]))
        #return math.sqrt(math.pow(((float(self.vertexStart[0]) - float(self.vertexFinish[0]))*10),2) + math.pow(((float(self.vertexStart[1]) - float(self.vertexFinish[1]))*10),2))

    def East(self):
        """Moves one step in East"""
        self.output = [(self.vertexStart[0] + 1), self.vertexStart[1], self.costgLinear, self.distance()]
        return self.output

    def West(self):
        """Moves one step West"""
        self.output = [(self.vertexStart[0] - 1), self.vertexStart[1], self.costgLinear, self.distance()]
        return self.output

    def North(self):
        """Moves one step North"""
        self.output = [self.vertexStart[0], (self.vertexStart[1] + 1), self.costgLinear, self.distance()]
        return self.output

    def South(self):
        """Moves one step South"""
        self.output = [self.vertexStart[0], (self.vertexStart[1] - 1), self.costgLinear, self.distance()]
        return self.output

    def Northeast(self):
        """Moves one step Northeast"""
        self.output = [(self.vertexStart[0] + 1), (self.vertexStart[1] + 1), self.costgDiagonal, self.distance()]
        return self.output

    def Southeast(self):
        """Moves one step Southeast"""
        self.output = [(self.vertexStart[0] + 1), (self.vertexStart[1] - 1), self.costgDiagonal, self.distance()]
        return self.output

    def Northwest(self):
        """Moves one step Northwest"""
        self.output = [(self.vertexStart[0] - 1), (self.vertexStart[1] + 1), self.costgDiagonal, self.distance()]
        return self.output

    def Southwest(self):
        """Moves one step Southwest"""
        self.output = [(self.vertexStart[0] - 1), (self.vertexStart[1] - 1), self.costgDiagonal, self.distance()]
        return self.output


class Obstacles:

    def __init__(self,testpoint):
        self.testpoint = testpoint

    def circle(self):
        self.cright = math.pow(15, 2)
        self.cleft = math.pow((self.testpoint[0] - 180), 2) + math.pow((self.testpoint[1] - 120), 2)
        if self.cleft <= self.cright:
            return True
        else:
            return False

    def square(self):
        if self.testpoint[0] >= 55 and self.testpoint[0] <= 155 and self.testpoint[1] >= 67.5 and self.testpoint[1] <= 112.5:
            return True
        else:
            return False

    def polygon(self):
        self.lines = [[[188.0,51.0],[168.0,14.0]],[[165.0,89.0],[188.0,51.0]],[[158.0,51.0],[165.0,89.0]],[[120.0,55.0],[158.0,51.0]],[[145.0,14.0],[120.0,55.0]],[[168,14],[158,51]]]
        slopes = []
        y_intercepts = []
        m_and_b = []
        for each in self.lines:
            numerator = each[1][1] - each[0][1]
            denominator = each[1][0] - each[0][0]
            slope = numerator / denominator
            slopes.append(slope)
            y_intercept = (each[0][1] - (slope * each[0][0]))
            y_intercepts.append(y_intercept)
            m_and_b.append([slope, y_intercept])
        RHS_Set = []
        for slope_intercept in m_and_b:
            RHS = ((float(slope_intercept[0]) * float(self.testpoint[0])) + float(slope_intercept[1]))
            RHS_Set.append(RHS)

        if self.testpoint[1] >= RHS_Set[0] and self.testpoint[1] <= RHS_Set[1] and self.testpoint[1] <= RHS_Set[2] and self.testpoint[1] >= RHS_Set[5]:
            return True
        elif self.testpoint[1] <= RHS_Set[3] and self.testpoint[1] >= RHS_Set[4] and self.testpoint[1] <= RHS_Set[5] and self.testpoint[1] >= 14.0:
            return True
        else:
            return False

    def scope(self):
        if self.testpoint[0] >= 0 and self.testpoint[0] <= 250 and self.testpoint[1] >= 0 and self.testpoint[1] <= 150:
            return True
        else:
            return False

    def clearance(self):
        if self.scope() == True and self.polygon() == False and self.square() == False and self.circle() == False:
            return True
        else:
            return False

def user_input():
    cond = False
    while cond is False:
        x = input("Please enter the x-coordinate : ")
        y = input("Please enter the y-coordinate : ")
        points = [x,y]
        if type(x) != int:
            print("The x co-ordinate you have entered is not an integer. Please try again !")
            cond = False
        elif type(y) != int:
            print("The y co-ordinate you have entered is not an integer. Please try again !")
            cond = False
        else:
            cond = True
    return points



#-----------------------------------------------------------------

#location_info = iterpoint; passed_list = openlist; passed_dict = storage; lastpoint = end; nodeNr = ?;

def core(location_info, passed_list, passed_dict, lastpoint, nodeNr, epctr):
    """Then we extract our interested node for exploration"""
    #print("the new dict is : ",passed_dict)
    grabbeditem = location_info
    print(location_info)
    #print("The grabbed node is : ",grabbeditem, "of type ",type(grabbeditem))
    iternode = [grabbeditem[0],grabbeditem[1]]
    #print("the iternode is : ",iternode, " and iternode[0] is :",iternode[0], " is of type ", type(iternode[0]))
    """We first copy our current node to closed dictionary"""
    dictleft = tuple(iternode)
    dictright = list(grabbeditem[2:7])
    if dictleft not in passed_dict.keys():
        passed_dict.update({dictleft: dictright})
    #print(passed_dict)
    """We also grab the node number before killing it from our open list"""
    parent_node_no = int(grabbeditem[2])
    #print("parent no is : ", parent_node_no)
    """We grab the Cost G which is already present in current node and use this for further increments"""
    Gcost = int(grabbeditem[4])
    #print("Gcost is : ", Gcost)
    """After copying our current node, we delete the current node from openlist"""
    #print("passed list is : ", passed_list)
    passed_list.remove(grabbeditem)
    #print (passed_list)
    """We grab our current node for creating daughters"""
    currentnode = list(iternode)
    #print(currentnode)
    """Creating an empty swap list"""
    swaplist = []

    mover = Move(currentnode,lastpoint)

    Nop = mover.North()
    if Obstacles([Nop[0],Nop[1]]).clearance():
        swaplist.append(Nop)
    else:
        pass

    mover.setstartpoint(currentnode)
    Sop = mover.South()
    if Obstacles([Sop[0], Sop[1]]).clearance():
        swaplist.append(Sop)
    else:
        pass

    mover.setstartpoint(currentnode)
    Eop = mover.East()
    if Obstacles([Eop[0], Sop[1]]).clearance():
        swaplist.append(Eop)
    else:
        pass

    mover.setstartpoint(currentnode)
    Wop = mover.West()
    if Obstacles([Wop[0], Wop[1]]).clearance():
        swaplist.append(Wop)
    else:
        pass

    mover.setstartpoint(currentnode)
    NEop = mover.Northeast()
    if Obstacles([NEop[0], NEop[1]]).clearance():
        swaplist.append(NEop)
    else:
        pass

    mover.setstartpoint(currentnode)
    NWop = mover.Northwest()
    if Obstacles([NWop[0], NWop[1]]).clearance():
        swaplist.append(NWop)
    else:
        pass

    mover.setstartpoint(currentnode)
    SEop = mover.Southeast()
    if Obstacles([SEop[0], SEop[1]]).clearance():
        swaplist.append(SEop)
    else:
        pass

    mover.setstartpoint(currentnode)
    SWop = mover.Southwest()
    if Obstacles([SWop[0], SWop[1]]).clearance():
        swaplist.append(SWop)
    else:
        pass


    #print("the swaplist after actions is : ",swaplist)
    counter = 0

    for daughters in swaplist:
        totalcostG = int(daughters[2] + Gcost)
        totalcostF = float(totalcostG + daughters[3])
        common = [item for item in passed_list if (item[0] == daughters[0] and item[1] == daughters[1])] #Filter the common elements in openlist
        if len(common) >=1:
            for each in common:
                if float(each[6]) < totalcostF:
                    counter+=1
                    if counter >= 1:
                        break
                    else:
                        nodeNr+=1
                        appendmember = [daughters[0],daughters[1],nodeNr, parent_node_no, totalcostG, daughters[3],totalcostF]
                        passed_list.append(appendmember)
                else:
                    pass

        elif len(common) == 0:
            nodeNr += 1
            appendmember = [daughters[0], daughters[1], nodeNr, parent_node_no, totalcostG, daughters[3], totalcostF]
            passed_list.append(appendmember)

        else:
            pass

    for each in swaplist:
        if (each[0],each[1]) == tuple(lastpoint):
            epctr+=1
            left = (each[0],each[1])
            nodeNr +=1
            totalcostG = int(each[2]+Gcost)
            costH = float(each[3])
            totalcostF = float(totalcostG + each[3])
            right = [nodeNr, parent_node_no, totalcostG, costH, totalcostF]
            passed_dict.update({left:right})
        totalcostG = int(each[2] + Gcost)
        checker = (each[0],each[1])
        if checker in passed_dict.keys():
            value = list(passed_dict.get(checker))
            if totalcostG < value[2]:
                value[1] = int(parent_node_no)
                value = tuple(value)
                passed_dict.update({checker:value})
            else:
                pass
        else:
            pass


    return nodeNr, epctr, passed_dict, passed_list

def main():
    start = timeit.default_timer()
    print("Please enter the start points")
    start = user_input()
    startObst = Obstacles(start)
    while startObst.clearance() == False:
        start = user_input()
        startObst = Obstacles(start)
    print("Please enter the end points")
    end = user_input()
    endObst = Obstacles(end)
    while endObst.clearance() == False:
        end = user_input()
        endObst = Obstacles(end)
    movement = Move(start,end)
    max_costh = movement.distance()
    first_key = (start[0],start[1])
    first_value = [1,0,0,max_costh,max_costh]
    storage = {first_key:first_value}
    openlist = [[start[0],start[1],1,0,0,max_costh,max_costh]]
    counter = 2
    node_no = 1
    end_counter = 0
    while end_counter <= 2:

        if end_counter == 2:
            #print(storage)
            publish = {}
            point_counter = 1
            consideration = tuple(end)
            publish.update({consideration:point_counter})
            terminator = 0
            parentno = 0
            while terminator < 1:
                parentno = int(storage.get(consideration)[1])
                for key,value in storage.items():
                    if value[0] == parentno:
                        consideration = key
                        point_counter +=1
                        publish.update({consideration:point_counter})
                        if consideration == tuple(start):
                            # Reference: https://stackoverflow.com/questions/8023306/get-key-by-value-in-dictionary?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
                            terminator = 2
            print("**** Pulling out the embedded viper from Tail to Head now ****")
            for key, value in sorted(publish.iteritems(), key=lambda (k, v): (v, k)):
                print("%s: %s" % (value, key))



            print("the publish is", publish)
            w = csv.writer(open("A_Star_Algorithm_Nodes.csv", "w"))
            for key, val in publish.iteritems():
                w.writerow([val, key])

            break

        """Select the minimum of cost f column(index 6)"""
        templist1 = [min(openlist, key=itemgetter(6))]
        #print(templist1)
        # print("the open list inside filter 1 is ",openlist)

        if len(templist1) > 1:
            templist2 = [min(templist1, key=itemgetter(5))]
            iterpoint = templist2[0]
            #print("the open list in filter 2 is : ",openlist," the iterpoint is :",iterpoint)
            # location_info = iterpoint; passed_list = openlist; passed_dict = storage; lastpoint = end; nodeNr = ?;
            node_no, end_counter, storage, openlist = core(iterpoint, openlist, storage, end, node_no, end_counter)


        elif len(templist1) == 1:
            templist2 = templist1[0]
            #print("the transfer node is :",transfernode)
            #print("the lowest h cost is :    ",transfernode[5])
            node_no, end_counter, storage, openlist = core(templist2, openlist, storage, end, node_no, end_counter)


        else:
            pass


main()
