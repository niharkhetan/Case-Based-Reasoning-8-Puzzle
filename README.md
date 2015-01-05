Case-Based-Reasoning-8-Puzzle
=============================

Solve 8 Puzzle using Case Based Reasoning

The basic idea is that given a new problem, with start and goal
states (S0,G0), it will:

* Retrieve a similar prior problem (i.e., one with similar initial and final states (S1,G1)).Call the similar problem’s solution    path P.
* If P does not exactly solve the problem, adapt P into a solution path, by concatenating it with two new paths:
* Pg, from G1 to G0.

New Problem = (S0, G0)
Similar Problem = (S1, G1) with solutino path P

So the computed path will look like S0 -> S1 -> -> G1 -> G0

New cases generated are stored for future use.

PLease write to me on nkhetan@indiana.edu if you wish to appreciate/criticize/contribute to the project
