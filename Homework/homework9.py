# Homework Completion Tracker
 
# PART 1: Set today's total number of homework tasks
total_homework = 4
original_count = total_homework
print(f"You have {original_count} homework tasks to finish today!\n")
 
# PART 2: Keep a counter for completed homework and the current task number
completed_count = 0
task_num = 1
 
# PART 3: Repeat while there are still homework tasks left
while task_num <= total_homework:
 
    # PART 4: Work out the current homework task from its number
    if task_num == 1:
        next_task = "Math worksheet"
    elif task_num == 2:
        next_task = "Science reading"
    elif task_num == 3:
        next_task = "English writing"
    else:
        next_task = "Coding practice"
 
    answer = input(f"Have you finished: {next_task}? (yes/no): ")
 
    # PART 5: Only move on once the task is marked done
    if answer == "yes":
        completed_count += 1
        task_num += 1
        print("Great job! Homework task completed.")
    else:
        print("Okay, finish it and check again!")
 
    # PART 6: Print how many homework tasks remain
    print("Homework tasks remaining:", total_homework - completed_count)
    print()
 
# PART 7: This only prints once every homework task is marked done
print("===== ALL HOMEWORK COMPLETE! =====")
print("Great work finishing your homework today!\n")
 
# PART 8: A safe look at what an infinite loop would look like
print("Now let's safely peek at an infinite loop...")
test_value = 0
safety_counter = 0
 
while test_value <= 0:
    print("This condition never changes, so this would run forever!")
    safety_counter += 1
 
    if safety_counter == 3:
        print("(Stopping here on purpose - a real infinite loop never stops on its own!)")
        break
 
# PART 9: Print the final homework checklist summary
print("\n===== HOMEWORK COMPLETION SUMMARY =====")
print("Homework Assigned Today:", original_count)
print("Homework Completed:", completed_count)
print("Homework Remaining:", total_homework - completed_count)
print("=======================================")
