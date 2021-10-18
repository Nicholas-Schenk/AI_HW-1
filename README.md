# AI_HW-1

Generate.py should solve part 0.

Currently generate.py has a main method that I was using for testing it. Obviously, though, in the actual code we will be importing the file and using the function generate, so we will need to get rid it then. 

*Update 10/4*
created runner.py and astar.py. Both are uninfinished in terms of implmentaiton. runner.py only supports displaying generated grids

*Update 10/6*
implemented forward repeated A* search

*_Update 10/13_*
forward a* may have some issues, backward a* may be implemented


*_Update 10/17_*
backward a* implementation that is more consistent with current forward a* implementation added.
the higher g-value bug is still present for grids with blocked off target


*_Update 10/18_*
higher g-value bug fixed for forward A*. fixed runner print outputs
