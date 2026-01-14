I would like you to make a new function
which should create tasks. A task look like a 

    dict with Task, Start, Finish.
    starttime: string, e.g. '2025-11-04'
    
    Milestone format:
    - duration: minimum calendar duration allowed (days)
    - workdays: total person-days (FTE-days) needed to complete the milestone

The function should take the following parameters:

def saturatedtasks(projectstarttime, systems, systemmilestones, ressources, max_systems_in_progress=3):

The function should start by calculating the FTE's available on any given calendarday since the projectstarttime. Secondly take the systemmilesones and merge them with the systems creating a list of undonetasks. 

For each task set an 'workeddays'= 0 parameter and an 'assigned FTE count'=0 variable. Also keep a list of donetasks as well as a list of opentasks.

Now loop over the calendar where you for each day:
  usedcapacity=0
  loop over all the opentasks:
    update the workeddays with min(capacityof day - usedcapacity,fte's needed for the day) and update usedcapacity accordingly
    if workeddays>=workdays needed & calendartime >= starttime+duration
      close task and add it do donetasks
  if usedcapacity<available capacity of the day:
    transfer a new task from undonetask to opentasks if the number of used dev's is less than the available one
  
  finally export the donetasks  in the same format as createtasks
