# Task 1: Diary
# Change to the assignment2 folder of your python_homework folder.  You create your programs for the assignment in this folder.

# Create a program called diary.py. Add code to do the following:

# Open a file called diary.txt for appending.
# In a loop, prompt the user for a line of input. The first prompt should say, "What happened today? ". All subsequent prompts should say "What else? "
# As each line is received, write it to diary.txt, with a newline (\n) at the end.
# When the special line "done for now" is received, write that to diary.txt. Then close the file and exit the program (you just exit the loop).
# Wrap all of this in a try block. If an exception occurs, catch the exception and print out "An exception occurred." followed by the name of the exception itself. Now, normally, you catch specific types of exceptions, and handle each according to program logic. In this case, you can catch any non-fatal exceptions via an except for Exception, and then display the information from the exception and exit the program. The traceback module provides a way to include function traceback information in your error message, which will make it easier to find the error. You can use the following code to handle exceptions using the traceback module.

# import traceback

# ...

# except Exception as e:
#    trace_back = traceback.extract_tb(e.__traceback__)
#    stack_trace = list()
#    for trace in trace_back:
#       stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
#    print(f"Exception type: {type(e).__name__}")
#    message = str(e)
#    if message:
#       print(f"Exception message: {message}")
#    print(f"Stack trace: {stack_trace}")

# Open the file using a with statement (inside the try block), and rely on that statement to handle the file close.
# The input statement should be inside the loop inside the with block.
# Test the program.

# Run it a couple of times to create diary entries. (python diary.py)
# Have a look at diary.txt to make sure it appears correct. Warning: diary.txt will end up in GitHub when you submit your homework, so don't put in anything personal.
# Trigger an exception while running the program: When it prompts you for input, press Ctrl-D. You may need to type Ctrl-C and newline to trigger an exception if Ctrl-D doesn't work. Check to see that the exception is handled.

import traceback

try:
    with open('diary.txt', 'a') as file:
        greeting = input("What happened today?")

        while True:
           file.write(greeting + "\n")
           greeting = input("What else? ")

except Exception as e:
   trace_back = traceback.extract_tb(e.__traceback__)
   stack_trace = list()
   for trace in trace_back:
      stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
   print(f"Exception type: {type(e).__name__}")
   message = str(e)
   if message:
      print(f"Exception message: {message}")
   print(f"Stack trace: {stack_trace}")

