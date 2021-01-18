This is a solver for a puzzle called Shirokuro using a SAT solver.
We're given a grid, in our case always n × n, containing white and black circles. 
The goal is to connect each white circle with a black circle by a straight horizontal or vertical line. 
Moreover, it holds that

• in each circle exactly one line ends,

• lines do not pass through other circles,

• lines do not cross other lines, and

• not necessarily each cell is visited by a line. 

Input

Is a string of length n × n. For example, it is "w0bwb0wbww000bw0bbbww0w0w000b0bbb0w00wbw0w0b0b0wb"
where
• w is a white circle,

• b is a black circle, and

• 0 (zero) is an empty cell.

The (i, j) cell is described by the character at the position (n · i) + j in the string; we start counting from zero.


Output

Is a string of length n × n. It could be "EHWSEHWEWSV00SS0NNEWNVS0S000NVSNEHW0VNEW0S0N0EHWN"

where

• 0 (zero) is an empty cell,

• H is an originally empty cell that now contains a horizontal line 

• V is an originally empty cell that now contains a vertical line 

• N is a circle that is connected from north 

• E is a circle that is connected from east 

• S is a circle that is connected from south

• W is a circle that is connected from west
 
 If no solution is possible, then "X" is the output.
