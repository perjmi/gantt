I would like to build a function, which takes tasks as produced by createtasks() and convert them into another set of tasks. This other set of tasks should be cut pr system, pr ressourceType and pr milestone. You might need to slice the times on the original tasks, because I would for each of these new task like to have the total FTE count too. 


I have changed the format of the milestones so that it now has a duration and a workdays field. The duration is the minimum calendar duration allowed and the workdays is the number of full FTE days which one need to assign in order to complete the milestone.

Can you change the logic of createtasks() accordingly 