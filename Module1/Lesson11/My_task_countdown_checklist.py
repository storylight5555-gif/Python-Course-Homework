total_task=4
original_count=total_task
print("You have ", original_count, "Task to finish today")

task_num=1
completed_task=0
while task_num<=total_task:
    if task_num==1:
        next_task="Make your bed"
    elif task_num==2:
        next_task="Feed your pet"
    elif task_num==3:
        next_task="Take out the trash"
    else:
        next_task="Wash the dishes"
    answer=input( f"Have you finished {next_task} Yes, No?")
    if answer=="Yes":
        completed_task+=1
        task_num+=1
        print("Great job, task completed")
    else:
        print("Ok finish the task and check again")
    print("Task remaining: ", total_task-completed_task)
print("--------------------------")
print("    All Tasks Completed   ")
print("--------------------------")
print()
print("Now safely peak at infinite loops")
test_value=0
safe_counter=0
while test_value<=0:
    print("This condition never changes so this wold run forever")
    safe_counter+=1
    if safe_counter==3:
        print("Stoping here on purpose otherwise this would run forever")
        break