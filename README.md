# python-Branch-and-Bound

We need to solve  1 | 𝑟_𝑗 | ∑▒𝐶_𝑗  with branch and bound algorithm and its method is best first search.
Level : the tree’s height.
Pathcost : the sequence’s cost.
currentTime : the execution time.
Upper bound and Lower bound.

(1) Upper Bound
For example, we have three jobs.
Job 1 :  r=0 , p=4
Job 2 :  r=2 , p=3
Job 3 :  r=4 , p=1

If we use
1. SPT:  3 → 2 → 1
2. FCFS :  1 → 2 → 3 
3. This algo :  0 → 2 →  1


(2) Lower Bound
[Method 1] We use SPT to get lower bound and assume that all job’s release time is zero. Complexity = O(n).
[Method ２] We use SRPT to get lower bound and assume that it allows preemption. Complexity =pseudo polynomial.
However, the bound of SRPT is much better than SPT, which can be seen from the number of nodes that push into the heap.


(3) Dominance rule 
It is from the paper, ON A DOMINANCE TEST FOR THE SINGLE MACHINE SCHEDULING PROBLEM WITH RELEASE DATES TO MINIMIZE TOTAL FLOW TIME.
Journal of the Operations Research, Society of Japan, 2004, Vol. 47, No. 2, 96-111.
Theorem 3.1 and 3.2


(4) Branch and Bound
We create a heap to put the possible solution into it.  The root of the heap means the best solution in that heap.
Therefore we pop the root successively until there are no nodes. 
Finally, we get a sequence.

