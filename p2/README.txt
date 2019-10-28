###-FUTOSHIKI-###

The futoshiki.py python program has a futoshiki() definition

When user run futoshiki.py in terminal, futoshiki_input.txt file that placed current directory opened.

Then all lines will be read from futoshiki_input.txt line by line with a loop.

Then they organized in two arrays named equality and biggerThan to be used by model in futoshiki() definition.

Then futoshiki(equality, biggerThan) definition will be called with two parameters.

Then futoshiki() opens a cp_model then the equality and biggerThan taken two parameters are used as constraint in the model

Then the model is solved by CpSolver() and a file named futoshiki_output.txt is opened to write solutions in order.

###-KAKURO-###

The kakuros.py python program has a Kakuro() definition

When user run kakuros.py in terminal, kakuro_input.txt file that placed current directory opened.

Also kakuro_output.txt file is opened to organize and to print solutions in.

Then all lines will be read from kakuro_input.txt line by line with a loop.

Then they organized in lineInt array to be used by model in Kakuros() definition.

Then Kakuro(lineInt, outputFile) definition will be called with two parameters.

Then Kakuro() opens a cp_model then the lineInt is used as constraint in the model

Then the model is solved by CpSolver() and all solution values print in outputFile in a design

######################################

Both programs just need a txt file that specifies constraints and need to run in terminal by the name

Then they give a output file in same directory.
