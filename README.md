Case-Based-Reasoning-8-Puzzle
=============================

Solve 8 Puzzle using Case Based Reasoning

The basic idea is that given a new problem, with start and goal
states (S0,G0), it will:
-Retrieve a similar prior problem (i.e., one with similar initial and final states (S1,G1)).Call the similar problem’s solution path P.
-If P does not exactly solve the problem, adapt P into a solution path, by concatenating it with two new paths:
-Ps, from S0 to S1, and
-Pg, from G1 to G0.
