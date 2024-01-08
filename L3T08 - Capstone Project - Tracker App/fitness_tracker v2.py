##------------------Fitness Tracker Program-----------------

import sqlite3
db = sqlite3.connect('tracker')
cursor = db.cursor()

print("------------------\n")
print("\nWelcome to The Fitness Tracker!\n")

##-----------------Creating tables-----------------

#Creating a 'category' table that will list each category with an ID
cursor.execute(''' CREATE TABLE IF NOT EXISTS categories (ID INTEGER
PRIMARY KEY, Name TEXT)''')

id1 = 1
name1 = 'Upper Body'

id2 = 2
name2 = 'Lower Body'

id3 = 3
name3 = 'Swimming'

cat_entries = [
    (id1, name1),
    (id2, name2),
    (id3, name3),
]

# insert the above list into the table
cursor.executemany('''INSERT OR REPLACE INTO categories(id,Name) VALUES(?,?)''',
                cat_entries)

db.commit()

# Creating the exercise table and populating it.  This table will includ
# all of the exercises, and include a category column
cursor.execute('''
    CREATE TABLE IF NOT EXISTS 'exercises'(ID INTEGER PRIMARY KEY, Name TEXT ,
Units TEXT, Completed_Units INTEGER NOT NULL, category INTEGER)''')

id1 = 1
name1 = 'Shoulder Press'
units1 = 'sets 4x8'
completed_units1 = 2
category1 = 1

id2 = 2
name2 = 'Squats'
units2 = 'sets 3x8'
completed_units2 = 4
category2 = 2

id3 = 3
name3 = 'Tricep Curls'
units3 = 'sets 4x12'
completed_units3 = 5
category3 = 1

id4 = 4
name4 = 'Breast Stroke'
units4 = '4 lengths'
completed_units4 = 2
category4 = 3

exercise_entries = [
                (id1,name1,units1,completed_units1,category1),
                (id2,name2,units2,completed_units2,category2),
                (id3,name3,units3,completed_units3,category3),
                (id4,name4,units4,completed_units4,category4),
                ]       

# insert the above list into the table
cursor.executemany('''INSERT OR REPLACE INTO exercises(id,Name,Units,Completed_Units,
                   Category) VALUES(?,?,?,?,?)''',
                exercise_entries)


# creating a routines table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Routines(ID INTEGER PRIMARY KEY, Name TEXT,
Exercise1 TEXT, Exercise2 TEXT, Exercise3 TEXT, Exercise4 TEXT,
Exercise5 TEXT)''')
db.commit()

# creating a goals table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS goals(ID INTEGER PRIMARY KEY, Category INTEGER ,
Type TEXT, Target INTEGER NOT NULL)''')

#------------------Creating the user menu------------------
# I have made some amendments to the given menu. I wanted to add features that allowed
# the user to add a specific exercise, and for them to update their progress.

while True:
    print("\n***Fitness Tracker User Menu***")
    print('''\n1. Add exercise or category\n2. View exercise by category
3. Delete exercise by category
4. Create Workout Routine\n5. View Workout Routine\n6. View Exercise Progress
7. Set Fitness Goals\n8. View Progress Towards Fitness Goals\n9. Enter a Completed Workout
10. Quit''')
    menu_choice = input("\nWhat would you like to do?: ")


#------------------Menu Choice 1------------------
# allowing user to enter a new exercise category

    if menu_choice == '1':
        choice = input('''\nEnter the relevant number. Would you like to enter a
1. New Category\n2. New Exercise\n:''')
        if choice == '1':
            new_category = input("Enter the name of the new category: ")
            print("\nNew Exercise Category Entry\n")
            cursor.execute(f'''INSERT INTO categories (Name)
                                VALUES('{new_category}') ''')
            print("\nNew category has been created!")
            db.commit()

        elif choice == '2':
            new_exercise = input("\nEnter the name of the new exercise: ")
            new_units = input('''\nHow will you measure this exercise?
Type sets 4x8, km etc: ''')
            new_completed = int(input('''\nHave you completed a workout of this
exercise yet? If so enter how many units were completed: '''))
            
            cursor.execute('''SELECT ID, name FROM categories''')
            show_categories = cursor.fetchall()

            # displaying the categories so the user can see what ID to assign
            # their new exercise to
            for row in show_categories:    
                print(f"{row[0]} - {row[1]}")

            category = int(input('''Enter the category ID of the exercise: '''))
            cursor.execute(f'''INSERT INTO exercises (Name, Units, 
Completed_Units, Category) VALUES(?,?,?,?) ''',(new_exercise,new_units,new_completed,category))
            print("\nNew exercise has been created!")
            db.commit()


#------------------Menu Choice 2------------------
#Viewing categories and exercises in those categories

    elif menu_choice == '2':
        
        print("\nYour exercise categories:\n")
        cursor.execute('''SELECT ID, name FROM  categories''')
        show_categories = cursor.fetchall()
        for row in show_categories:    
            print(f"{row[0]} - {row[1]}")
        print("0 - Back to main menu")
            
        view_choice = input("\nWhich exercise category would you like to view?: ")
        if view_choice == '0':
            continue
        else:
            cursor.execute('''SELECT name, Units, 'Completed_Units'
                            from exercises WHERE category = ? ''', (view_choice,))
            show_exercises = cursor.fetchall()
            for row in show_exercises: 
                #I had to use this if statement to get round potential NULL value
                #in 'Completed Sets'
                if row[2] == 'Completed_Units':
                    print(f'''\nExercise - \t\t{row[0]} 
Units - \t\t{row[1]} \nUnits Completed - \t0''')
                else:
                    print(f'''\nExercise - \t\t{row[0]} 
Units - \t\t{row[1]} \nUnits Completed - \t\t{row[2]}''')
            
    
#------------------Menu Choice 3------------------
#allowing the user to delete a category

    elif menu_choice == '3':
        delete_choice = int(input("Enter the ID of the category you'd like to delete: "))
        cursor.execute('''DELETE FROM categories WHERE id = ? ''', (delete_choice,))
        print(f"Category {delete_choice} has been deleted!")


#------------------Menu Choice 4------------------
# Creating a workout routine. I have set a routine as having to include five
# exercises.  I take each exercise as an input and then put that into a 
# separate table called 'Routines'.

    elif menu_choice == '4':
       
        routine_name = input("What is the name of your new routine?: ")
        ex1 = input("First exercise name: ")
        ex2 = input("Second exercise name: ")
        ex3 = input("Third exercise name: ")
        ex4 = input("Fourth exercise name: ")
        ex5 = input("Fifth exercise name: ")

        cursor.execute(''' INSERT INTO Routines (Name, Exercise1,
Exercise2, Exercise3, Exercise4, Exercise5) VALUES(?, ?, ?, ?, ?, ?)''',
        (routine_name,ex1,ex2,ex3,ex4,ex5))
        db.commit()
        

#------------------Menu Choice 5------------------
# viewing all of the routines in the database
    elif menu_choice == '5':
        print("Here is a list of your routines: \n")
        cursor.execute('''SELECT ID, Name from Routines''') 
        show = cursor.fetchall()
        for row in show:
            print(row[0],row[1])

        view = int(input('''\nPlease enter the ID number of the 
routine you would like to view: ''' ))
        cursor.execute(f'''SELECT * from Routines WHERE ID = {view}''')
        show = cursor.fetchall()
        for row in show:
            print(f'''\nRoutine {row[0]} - {row[1]}\n{row[2]}\n{row[3]}\n{row[4]}
{row[5]}\n{row[6]}''')
        db.commit()


#------------------Menu Choice 6------------------
# Viewing exercise progress. I have chosen to show the user how many units they
# have completed in their chosen category as a way to show their progress. I used
# the SUM statement.

    elif menu_choice == '6':
        print("\nLet's check out your progress!")
        cursor.execute('''SELECT ID, name FROM  categories''')
        show_categories = cursor.fetchall()
        for row in show_categories:    
            print(f"{row[0]} - {row[1]}")
        choice = int(input("\nWhich category would you like to see your progress in?: "))
        cursor.execute(f''' SELECT SUM(Completed_Units) FROM exercises WHERE category = {choice}''')
        show = cursor.fetchall()
        #***I'm not sure why I had to use strip in the next line when I haven't in others***
        show_string = str(show[0]).strip("(),")
        print("You have completed", show_string, "units in this category. Well done!")
        

#------------------Menu Choice 7------------------
# Notes for self - goal categories could be number of completed units, number of custom routines
# number of exercises

    elif menu_choice == '7':
        while True:
            print("\nSet Fitness Goals\n")
            print('''1. Number of total completed units\n2. Number of exercises
3. Number of custom routines\n4. Back to main menu''')
            goal_cat_choice = int(input('''\nWhich category of goal would you like to set?: '''))
            if goal_cat_choice == 1:
                units_target = int(input("What is your target?: "))
                print(f'''Goal of {units_target} completed units has been set!''')
                cursor.execute('''INSERT INTO Goals (category, type, target) VALUES
(?,?,?)''',(goal_cat_choice,"Total Units",units_target))
                db.commit()
            
            elif goal_cat_choice == 2:
                ex_target = int(input("What is your target?: "))
                print(f'''Goal of {ex_target} total exercises has been set!''')
                cursor.execute('''INSERT INTO Goals (category, type, target) VALUES
(?,?,?)''',(goal_cat_choice,"Total exercises",ex_target))
                db.commit()

            elif goal_cat_choice == 3:
                rou_target = int(input("What is your target?: "))
                print(f'''Goal of {rou_target} custom routines has been set!''')
                cursor.execute('''INSERT INTO Goals (category, type, target) VALUES
(?,?,?)''',(goal_cat_choice,"Custom Routines",rou_target))
                db.commit()

            elif goal_cat_choice == 4:
                break

            else:
                print("Please check your input.")


#------------------Menu Choice 8------------------
# viewing progress towards fitness goals
# I will allow the user to view their fitness goals, and then compare the relevant
# values in the goals table and the categories or exercises table. I have relied
# on using for loops and then using the values at particular indexes to act as the
# values by which I determine whether a goal has been met or not.

    elif menu_choice == '8':
        print("Here are your current goals:\n")
        # I want the goals to be displayed differently to the user, depending on
        # their category.
        cursor.execute('''SELECT ID, Type, Target FROM goals WHERE category = 1''')
        show = cursor.fetchall()
        for row in show:
            print(f'''{row[0]}. Complete {row[2]} {row[1]}''')
            cursor.execute('''SELECT SUM(Completed_Units) from exercises''')
            a = cursor.fetchone()
            cursor.execute(f'''SELECT Target FROM goals WHERE ID = {row[0]}''')
            b = cursor.fetchone()
            # I want to display 'a' cleanly. Is there a better way to do it than
            # what I have done below?
            strip_a = str(a).strip("(),")
            if a>=b:
                print(f'''Congratulations! You have completed {strip_a} units and
so have met your goal!''')
            else:
                print(f'''You have only completed {strip_a} units. Still some more
work to do!\n''')

# Displaying the goals and progress of goals in category 2 - amount of exercises
        cursor.execute('''SELECT ID, Type, Target FROM goals WHERE category = 2''')
        show = cursor.fetchall()
        for row in show:
            print(f'''{row[0]}. Enter {row[2]} {row[1]}''')
            cursor.execute('''SELECT COUNT(ID) from exercises''')
            a = cursor.fetchone()
            cursor.execute(f'''SELECT Target FROM goals WHERE ID = {row[0]}''')
            b = cursor.fetchone()
            strip_a = str(a).strip("(),")
            if a>=b:
                print(f'''Congratulations! You have entered {strip_a} exercises and
so have met your goal!''')
            else:
                print(f'''You have only entered {strip_a} exercises. Still some more
work to do!\n''')


# Displaying the goals and progress of goals in category 3 - number of custom routines
        cursor.execute('''SELECT ID, Type, Target FROM goals WHERE category = 3''')
        show = cursor.fetchall()
        for row in show:
            print(f'''{row[0]}. Compile {row[2]} {row[1]}''')
            cursor.execute('''SELECT COUNT(ID) from Routines''')
            a = cursor.fetchone()
            cursor.execute(f'''SELECT Target FROM goals WHERE ID = {row[0]}''')
            b = cursor.fetchone()
            strip_a = str(a).strip("(),")
            if a>=b:
                print(f'''Congratulations! You have compiled {strip_a} routines and
so have met your goal!''')
            else:
                print(f'''You have only compiled {strip_a} routines. Still some more
work to do!\n''')


#------------------Menu Choice 9------------------
# Allowing the user to enter a completed workout. I will display all exercises
# to the user, and then allow them to add to the completed units column.

    elif menu_choice == '9':
        while True:
            print('''\nLet's update your progress! Choose a category, and then
an exercise to update.\n''')
            cursor.execute('''SELECT ID, name FROM  categories''')
            show_categories = cursor.fetchall()
            for row in show_categories:    
                print(f"{row[0]} - {row[1]}")
            print("0 - Back to main menu")
                
            view_choice = input("\nWhat category of exercise did you do?: ")
            if view_choice == '0':
                break
            else:
                cursor.execute('''SELECT ID, name, Units
                                from exercises WHERE category = ? ''', (view_choice,))
                show_exercises = cursor.fetchall()
                for row in show_exercises: 
                    print(f'''\nID - \t\t{row[0]} \nName - \t\t{row[1]} \nUnits - \t{row[2]}''')
                ex_choice = input('''Enter the ID of the exercise you completed: ''')
                add_to = int(input("How many units (sets,km etc.) did you complete?: "))
                cursor.execute(f'''UPDATE exercises 
                            SET Completed_Units = Completed_Units + ?
                WHERE ID = ?''', (add_to,ex_choice))
                db.commit()
                print("Exercise udpated!")

#------------------Menu Choice 10------------------
# Allowing the user to quit

    elif menu_choice == '10':
        exit

    else:
        print("Please check your input.")




    
 
     


    
