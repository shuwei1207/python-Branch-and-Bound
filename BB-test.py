import heapq
from operator import itemgetter
import numpy as np
import sys
import random
import time
import csv
import queue
class Node(object):
    def __init__(self, level=None, sequence=None):
        self.level = level
        self.sequence = sequence
        self.upperBound, self.upperBoundSequence = None, None
        self.lowerBound = self.getLowerBound()
        self.pathCost = 0
        self.currentTime = 0
        # print('node seq=',self.sequence,sep=' ')

    def __lt__(self, other):
        return self.lowerBound < other.lowerBound

    def getUpperBound(self):
        # generate FCFS combine SPT sequence
        # nowT is represent Current time
        # makespan is represent total completion time
        nowT = 0
        makespan = 0
        remainJobs = jobs.copy()
        for i in self.sequence:
            nowT = max(nowT, jobs[i][0])
            nowT += jobs[i][1]
            remainJobs.remove(jobs[i])
            makespan += nowT
        # 計算到目前為止所得到的makespan
        self.pathCost = makespan
        self.currentTime = nowT
        # jobs_FCFS sort all remain jobs by release Date
        jobs_FCFS = sorted(remainJobs, key=itemgetter(0))
        # jobs_SPT sort all remain jobs by processing Date
        jobs_SPT = sorted(remainJobs, key=itemgetter(1))
        seq = self.sequence.copy()
        for i in range(len(remainJobs)):
            # print("FCFS=", jobs_FCFS, sep=' ')
            # print("SPT=", jobs_SPT, sep=' ')
            if nowT < jobs_SPT[0][0]:
                seq.append(jobs.index(jobs_FCFS[0]))
                nowT = max(nowT, jobs_FCFS[0][0])
                nowT += jobs_FCFS[0][1]
                jobs_SPT.remove(jobs_FCFS[0])
                jobs_FCFS.remove(jobs_FCFS[0])
            else:
                nowT = max(nowT, jobs_SPT[0][0])
                nowT += jobs_SPT[0][1]
                seq.append(jobs.index(jobs_SPT[0]))
                jobs_FCFS.remove(jobs_SPT[0])
                jobs_SPT.remove(jobs_SPT[0])
            # print("seq=",seq,sep=' ')
            makespan += nowT
        # print(makespan)
        # print("UB seq=", seq, sep=' ')
        return makespan, seq

    def getLowerBound(self):
        '''
        # lower bound is produce by SPT rule,because SPT in 1||summation C(j) will get optimal value
        nowT = 0
        makespan = 0
        remainJobs = jobs.copy()
        for i in self.sequence:
            nowT = max(nowT, jobs[i][0])
            nowT += jobs[i][1]
            remainJobs.remove(jobs[i])
            makespan += nowT
        jobs_SPT = sorted(remainJobs, key=itemgetter(1))
        seq = self.sequence.copy()
        for i in range(len(remainJobs)):
            nowT += jobs_SPT[0][1]
            seq.append(jobs.index(jobs_SPT[0]))
            jobs_SPT.remove(jobs_SPT[0])
            makespan += nowT
        print("LB seq(SPT)=", seq,'makespan',makespan, sep=' ')
        return  makespan
        '''
        # lower bound is produce by SRPT
        nowT = 0
        makespan = 0
        remainJobs = jobs.copy()
        for i in self.sequence:
            nowT = max(nowT, jobs[i][0])
            nowT += jobs[i][1]
            remainJobs.remove(jobs[i])
            makespan += nowT
        remainTime = []
        for i in range(len(remainJobs)):
            remainTime.append(int(remainJobs[i][1]))

        remain = 0
        time = nowT
        remainTime.append(99999999999)
        while(remain!= len(remainJobs)):
            smallest = len(remainJobs)
            for i in range(len(remainJobs)):
                if remainJobs[i][0] <= time and remainTime[i] < remainTime[smallest] and remainTime[i] > 0 :
                    smallest = i
            remainTime[smallest] -= 1
            if remainTime[smallest] == 0:
                remain+=1
                endTime = time + 1
                makespan+=endTime
            time += 1
        #print("LB seq(SRPT)=", makespan, sep=' ')
        return makespan

    def getChild(self):
        global jobNumber
        availible = set(np.arange(jobNumber))
        subSquence = set(self.sequence)
        remainJobs = list(availible - subSquence)
        tmp_remainJobs = remainJobs.copy()
        for i in range(len(remainJobs)):
            for j in range(i+1,len(remainJobs)):
                pi = jobs[remainJobs[i]][1]
                pj = jobs[remainJobs[j]][1]
                ri = jobs[remainJobs[i]][0]
                rj = jobs[remainJobs[j]][0]
                a = max(self.currentTime, ri) + pi + self.pathCost
                b = max(self.currentTime, rj) + pj + self.pathCost
                if a >= b and a - b >= ((pi-pj)*jobNumber-len(self.sequence)-1):
                    tmp_remainJobs.remove(remainJobs[i])
                    break
                if a <= b and (pi-pj) <= (a-b) * (jobNumber-len(self.sequence)):
                    tmp_remainJobs.remove(remainJobs[i])
                    break
        return tmp_remainJobs


def loadData():
    filepath = 'n100.txt'
    jobs = []
    with open(filepath) as fp:
        line = fp.readline()
        jobNumber = int(line)
        while line:
            try:
                line = fp.readline()
                tmplist= []
                tmplist.append(int(line.split()[0]))
                tmplist.append(int(line.split()[1]))
                jobs.append(tmplist)
            except:
                return jobNumber, jobs

def BnbSlover():

    upperBound = sys.maxsize
    solution = []
    # root is a empty node
    root = Node(level=0, sequence=[])
    heap = []
    heapq.heappush(heap, root)
    totalNode = 0
    while len(heap) != 0:
        minNode = heapq.heappop(heap)
        for i in minNode.getChild():
            a = minNode.sequence.copy()
            a.append(i)
            child = Node(level=minNode.level+1, sequence=a)
            # only if when child's lower bound is better than current bound
            # the child will be push in heap hoping to get a better solution
            if child.lowerBound < upperBound:
                heapq.heappush(heap, child)
                totalNode += 1
                # if child's upper bound is better than current bound
                # update current upper bound and so as the current solution
                child.upperBound, child.upperBoundSequence = child.getUpperBound()
                if child.upperBound < upperBound:
                    upperBound = child.upperBound
                    solution = child.upperBoundSequence.copy()
            #print(solution)
            #print(upperBound)
        #print(len(heap))
    return solution, upperBound, totalNode

if __name__ == '__main__':
    # first for release date ,second for processing time
    jobNumber, AllJobs = loadData()
    with open('n100.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Number of jobs ', 'Solution', 'Objective Value', 'total Nodes pushed in heap', 'processing time'])
        jobNumber = 0
        for i in range(10):
            # 計時開始
            tStart = time.time()
            jobNumber = i*10+10
            jobs = AllJobs[0:jobNumber]
            solution, objectiveValue, totalNode = BnbSlover()
            print('job numbers:', jobNumber, sep=' ')
            print('solution:', solution, sep=' ')
            print('objective Value:', objectiveValue, sep=' ')
            print('total numbers of nodes pushed in heap:', totalNode, sep=' ')
            # 計時結束
            tEnd = time.time()
            # 列印結果
            print("It cost %f sec" % (tEnd - tStart))
            writer.writerow([jobNumber,solution, objectiveValue, totalNode, '%f'% (tEnd - tStart)])
            print()
