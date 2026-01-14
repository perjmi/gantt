"""
Gantt Charts for Project Planning
"""

import plotly.express as px
import pandas as pd

systems = [{'name': 'bif', 'systype': 'general', 'country': 'all', 'complexity': 'hard', 'quality': 'good', 'method': 'option3'}]
systems.append({'name': 'hac', 'systype': 'policy', 'country': 'se', 'complexity': 'small', 'quality': 'good', 'method': 'option1'})
systems.append({'name': 'sol', 'systype': 'policy', 'country': 'se', 'complexity': 'small', 'quality': 'good', 'method': 'option1'})
systems.append({'name': 'prosit', 'systype': 'policy', 'country': 'se', 'complexity': 'small', 'quality': 'good', 'method': 'option1'})
systems.append({'name':'axapta','systype':'policy','country':'dk','complexity':'hard','quality':'medium','method':'option3'})
systems.append({'name': 'grus', 'systype': 'policy', 'country': 'se', 'complexity': 'small', 'quality': 'good', 'method': 'option1'})
systems.append({'name': 'warranty', 'systype': 'policy', 'country': 'se', 'complexity': 'small', 'quality': 'good', 'method': 'option1'})
systems.append({'name': 'motor', 'systype': 'policy', 'country': 'se', 'complexity': 'small', 'quality': 'poor', 'method': 'option1'})
systems.append({'name': 'gwse', 'systype': 'claims', 'country': 'se', 'complexity': 'small', 'quality': 'good', 'method': 'option1'})
systems.append({'name': 'clan', 'systype': 'claims', 'country': 'se', 'complexity': 'small', 'quality': 'good', 'method': 'option1'})
systems.append({'name':'tosca','systype':'policy','country':'dk','complexity':'hard','quality':'medium','method':'option3'})
systems.append({'name': 'mdb', 'systype': 'customer', 'country': 'se', 'complexity': 'small', 'quality': 'good', 'method': 'option1'})
systems.append({'name': 'tia', 'systype': 'policy', 'country': 'dk', 'complexity': 'medium', 'quality': 'medium', 'method': 'option1'})
systems.append({'name': 'fks', 'systype': 'customer', 'country': 'dk', 'complexity': 'small', 'quality': 'good', 'method': 'option1'})
systems.append({'name': 'gwdk', 'systype': 'claims', 'country': 'dk', 'complexity': 'small', 'quality': 'good', 'method': 'option2'})
systems.append({'name':'gwaff','systype':'policy','country':'dk','complexity':'medium','quality':'good','method':'option2'})
systems.append({'name':'pms','systype':'policy','country':'no','complexity':'hard','quality':'medium','method':'option3'})
systems.append({'name': 'gwno', 'systype': 'claims', 'country': 'no', 'complexity': 'small', 'quality': 'good', 'method': 'option2'})
systems.append({'name': 'kn', 'systype': 'customer', 'country': 'no', 'complexity': 'small', 'quality': 'good', 'method': 'option2'})

systemmilestones = [
    {
        'complexity': 'small',
        'method':'option1',
        'milestones': [
            {'name': 'T360 2 T360Next', 'duration': 15,'workdays':20,'ftetype':'dev'},
            {'name': 'BI fac 2 T360Next', 'duration': 42,'workdays':30,'ftetype':'dev'},
            {'name': 'Test on SF mock', 'duration': 1,'workdays':5,'ftetype':'test'},
            {'name': 'Real data 2 SF', 'duration': 40,'workdays':20,'ftetype':'dev'},
            {'name': 'Test of SF', 'duration': 10,'workdays':20,'ftetype':'dev'},
            {'name': 'Test of MM', 'duration': 30,'workdays':20,'ftetype':'dev'},
            {'name': 'Test of other marts', 'duration': 30,'workdays':20,'ftetype':'dev'}
        ]
    }
]
systemmilestones.append(
    {
        'complexity': 'medium',
        'method':'option1',
        'milestones': [
            {'name': 'T360 2 T360Next', 'duration': 15,'workdays':45,'ftetype':'dev'},
            {'name': 'BI fac 2 T360Next', 'duration': 42,'workdays':100,'ftetype':'dev'},
            {'name': 'Test on SF mock', 'duration': 1,'workdays':5,'ftetype':'test'},
            {'name': 'Real data 2 SF', 'duration': 40,'workdays':40,'ftetype':'dev'},
            {'name': 'Test of SF', 'duration': 10,'workdays':50,'ftetype':'dev'},
            {'name': 'Test of MM', 'duration': 30,'workdays':50,'ftetype':'dev'},
            {'name': 'Test of other marts', 'duration': 30,'workdays':50,'ftetype':'dev'}
        ]
    }
)

systemmilestones.append(
   {
        'complexity': 'hard',
        'method':'option1',
        'milestones': [
            {'name': 'T360 2 T360Next', 'duration': 15,'workdays':45,'ftetype':'dev'},
            {'name': 'BI fac 2 T360Next', 'duration': 42,'workdays':100,'ftetype':'dev'},
            {'name': 'Test on SF mock', 'duration': 1,'workdays':5,'ftetype':'test'},
            {'name': 'Real data 2 SF', 'duration': 40,'workdays':40,'ftetype':'dev'},
            {'name': 'Test of SF', 'duration': 10,'workdays':50,'ftetype':'dev'},
            {'name': 'Test of MM', 'duration': 30,'workdays':50,'ftetype':'dev'},
            {'name': 'Test of other marts', 'duration': 30,'workdays':50,'ftetype':'dev'}
        ]
    })

systemmilestones.append(
    {
        'complexity': 'small',
        'method':'option2',
        'milestones': [
            {'name': 'CTM', 'duration': 30,'workdays':150,'ftetype':'dev'},
            {'name': 'CTM to SF', 'duration': 5,'workdays':10,'ftetype':'dev'},
            {'name': 'Test on SF mock', 'duration': 1,'workdays':5,'ftetype':'test'},
            {'name': 'Real data 2 SF', 'duration': 40,'workdays':40,'ftetype':'dev'},
            {'name': 'Test of SF', 'duration': 10,'workdays':30,'ftetype':'dev'},
            {'name': 'Test of MM', 'duration': 30,'workdays':30,'ftetype':'dev'},
            {'name': 'Test of other marts', 'duration': 30,'workdays':30,'ftetype':'dev'}
        ]
    }
)

systemmilestones.append(
    {
        'complexity': 'medium',
        'method':'option2',
        'milestones': [
            {'name': 'CTM', 'duration': 40,'workdays':190,'ftetype':'dev'},
            {'name': 'CTM to SF', 'duration': 5,'workdays':10,'ftetype':'dev'},
            {'name': 'Test on SF mock', 'duration': 1,'workdays':5,'ftetype':'test'},
            {'name': 'Real data 2 SF', 'duration': 40,'workdays':40,'ftetype':'dev'},
            {'name': 'Test of SF', 'duration': 10,'workdays':30,'ftetype':'dev'},
            {'name': 'Test of MM', 'duration': 30,'workdays':30,'ftetype':'dev'},
            {'name': 'Test of other marts', 'duration': 30,'workdays':30,'ftetype':'dev'}
        ]
    }
)

systemmilestones.append(
    {
        'complexity': 'medium',
        'method':'option2',
        'milestones': [
            {'name': 'CTM', 'duration': 40,'workdays':250,'ftetype':'dev'},
            {'name': 'CTM to SF', 'duration': 5,'workdays':10,'ftetype':'dev'},
            {'name': 'Test on SF mock', 'duration': 1,'workdays':5,'ftetype':'test'},
            {'name': 'Real data 2 SF', 'duration': 40,'workdays':40,'ftetype':'dev'},
            {'name': 'Test of SF', 'duration': 10,'workdays':30,'ftetype':'dev'},
            {'name': 'Test of MM', 'duration': 30,'workdays':30,'ftetype':'dev'},
            {'name': 'Test of other marts', 'duration': 30,'workdays':30,'ftetype':'dev'}
        ]
    }
)


systemmilestones.append(
    {
        'complexity': 'hard',
        'method':'option3',
        'milestones': [
            {'name': 'CTM', 'duration': 40,'workdays':90,'ftetype':'dev'},
            {'name': 'CTM to SF', 'duration': 20,'workdays':100,'ftetype':'dev'},
            {'name': 'Test on SF mock', 'duration': 1,'workdays':5,'ftetype':'test'},
            {'name': 'Real data 2 SF', 'duration': 40,'workdays':200,'ftetype':'dev'},
            {'name': 'Test of SF', 'duration': 10,'workdays':50,'ftetype':'dev'},
            {'name': 'Test of MM', 'duration': 30,'workdays':50,'ftetype':'dev'},
            {'name': 'Test of other marts', 'duration': 30,'workdays':50,'ftetype':'dev'}
        ]
    }
)

ressources = [
    {'ftetype':'dev','unitcostprday':1000,'availability':0.6,'ressourcename':'Developer1','onboardingday':0},
    {'ftetype':'dev','unitcostprday':1000,'availability':0.6,'ressourcename':'Developer2','onboardingday':0},
    {'ftetype':'dev','unitcostprday':950,'availability':0.6,'ressourcename':'Developer3','onboardingday':0},
    {'ftetype':'dev','unitcostprday':1050,'availability':0.6,'ressourcename':'Developer4','onboardingday':0},
    {'ftetype':'dev','unitcostprday':980,'availability':0.6,'ressourcename':'Developer5','onboardingday':0},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer6','onboardingday':0},
    {'ftetype':'dev','unitcostprday':980,'availability':0.6,'ressourcename':'Developer7','onboardingday':0},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer8','onboardingday':0},
    {'ftetype':'dev','unitcostprday':980,'availability':0.6,'ressourcename':'Developer9','onboardingday':0},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer10','onboardingday':0},
    {'ftetype':'dev','unitcostprday':980,'availability':0.6,'ressourcename':'Developer11','onboardingday':0},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer12','onboardingday':0},
    {'ftetype':'dev','unitcostprday':980,'availability':0.6,'ressourcename':'Developer13','onboardingday':0},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer14','onboardingday':0},
    {'ftetype':'test','unitcostprday':800,'availability':0.6,'ressourcename':'Tester1','onboardingday':0},
    {'ftetype':'test','unitcostprday':820,'availability':0.6,'ressourcename':'Tester2','onboardingday':0},
    {'ftetype':'test','unitcostprday':780,'availability':0.6,'ressourcename':'Tester3','onboardingday':0}
]

##Adding more resources with onboarding delay
ressources = [
    {'ftetype':'dev','unitcostprday':1000,'availability':0.6,'ressourcename':'Developer1','onboardingday':0},
    {'ftetype':'dev','unitcostprday':1000,'availability':0.6,'ressourcename':'Developer2','onboardingday':0},
    {'ftetype':'dev','unitcostprday':950,'availability':0.6,'ressourcename':'Developer3','onboardingday':0},
    {'ftetype':'dev','unitcostprday':1050,'availability':0.6,'ressourcename':'Developer4','onboardingday':0},
    {'ftetype':'dev','unitcostprday':980,'availability':0.6,'ressourcename':'Developer5','onboardingday':0},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer6','onboardingday':0},
    {'ftetype':'dev','unitcostprday':980,'availability':0.6,'ressourcename':'Developer7','onboardingday':0},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer8','onboardingday':0},
    {'ftetype':'dev','unitcostprday':980,'availability':0.6,'ressourcename':'Developer9','onboardingday':0},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer10','onboardingday':0},
    {'ftetype':'dev','unitcostprday':980,'availability':0.6,'ressourcename':'Developer11','onboardingday':0},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer12','onboardingday':0},
    {'ftetype':'dev','unitcostprday':980,'availability':0.6,'ressourcename':'Developer13','onboardingday':0},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer14','onboardingday':0},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer15','onboardingday':90},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer16','onboardingday':90},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer17','onboardingday':90},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer18','onboardingday':90},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer19','onboardingday':90},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer20','onboardingday':180},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer21','onboardingday':180},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer22','onboardingday':180},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer23','onboardingday':180},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer24','onboardingday':180},
    {'ftetype':'dev','unitcostprday':1020,'availability':0.6,'ressourcename':'Developer25','onboardingday':180},
    {'ftetype':'test','unitcostprday':800,'availability':0.6,'ressourcename':'Tester1','onboardingday':0},
    {'ftetype':'test','unitcostprday':820,'availability':0.6,'ressourcename':'Tester2','onboardingday':0},
    {'ftetype':'test','unitcostprday':780,'availability':0.6,'ressourcename':'Tester3','onboardingday':0},
    {'ftetype':'test','unitcostprday':780,'availability':0.6,'ressourcename':'Tester4','onboardingday':90},
    {'ftetype':'test','unitcostprday':780,'availability':0.6,'ressourcename':'Tester5','onboardingday':90},
    {'ftetype':'test','unitcostprday':780,'availability':0.6,'ressourcename':'Tester6','onboardingday':180}
]

def createtasks(starttime, systems, systemmilestones, ressources, max_systems_in_progress=3):
    """
    Generate tasks for Gantt chart from systems, systemmilestones, and ressources.
    Tries to exhaust resources by issuing as many parallel tasks as possible.
    Limits the number of systems in progress at any time to max_systems_in_progress.
    Ensures that once a system starts, it is continuously worked on until finished.
    Returns a list of dicts with Task, Start, Finish.
    starttime: string, e.g. '2025-11-04'
    
    Milestone format:
    - duration: minimum calendar duration allowed (days)
    - workdays: total person-days (FTE-days) needed to complete the milestone
    
    The function assigns resources to meet the workdays requirement while ensuring
    the calendar duration is at least the minimum duration specified.
    
    Resources are only assigned on workdays (Monday-Friday), excluding weekends.
    """
    import pandas as pd
    from datetime import timedelta
    
    def parse_date(d):
        return pd.to_datetime(d)
    
    def is_workday(date):
        """Check if a date is a workday (Monday=0 to Friday=4)"""
        return date.weekday() < 5
    
    def next_workday(date):
        """Get the next workday from the given date"""
        next_day = date
        while not is_workday(next_day):
            next_day += timedelta(days=1)
        return next_day
    
    def add_workdays(start_date, num_workdays):
        """Add a number of workdays to a date, skipping weekends"""
        current = start_date
        days_added = 0
        while days_added < num_workdays:
            if is_workday(current):
                days_added += 1
            if days_added < num_workdays:
                current += timedelta(days=1)
        return current
    
    # Track when each resource becomes available (ensure start is a workday)
    resource_availability = {}
    project_start_date = parse_date(starttime)

    for res in ressources:
        # Calculate specific start date for this resource based on onboardingday
        onboarding_days = res.get('onboardingday', 0)
        res_start = project_start_date + timedelta(days=onboarding_days)
        resource_availability[res['ressourcename']] = next_workday(res_start)
    
    tasks = []
    
    # Build a queue of (system, milestone_index, milestone) for each system
    # Track current milestone index for each system
    system_queues = {}
    system_milestone_finish = {}  # When the current milestone of each system finished
    
    for system in systems:
        ms_set = None
        for ms in systemmilestones:
            if ms['complexity'] == system['complexity'] and ms['method'] == system['method']:
                ms_set = ms
                break
        if ms_set:
            system_name = system['name']
            system_queues[system_name] = {
                'milestones': ms_set['milestones'],
                'current_index': 0,
                'system': system
            }
            system_milestone_finish[system_name] = parse_date(starttime)
    
    # Track which systems are currently in progress (have started but not finished all milestones)
    systems_in_progress = set()
    systems_completed = set()
    system_start_time = {}  # Track when each system first started

    while True:
        # Find candidate systems for next milestone assignment
        candidate_systems = []
        for system_name, queue_info in system_queues.items():
            if queue_info['current_index'] >= len(queue_info['milestones']):
                systems_completed.add(system_name)
                continue  # This system is done
            candidate_systems.append(system_name)

        # Update systems_in_progress: add any system that has started but not finished
        systems_in_progress = set([
            name for name in system_queues
            if name not in systems_completed and system_queues[name]['current_index'] > 0
        ])

        # If fewer than max_systems_in_progress systems are in progress, allow new systems to start
        available_slots = max_systems_in_progress - len(systems_in_progress)
        # Prioritize continuing work on systems already in progress, ordered by start time (oldest first)
        prioritized_systems = sorted(
            systems_in_progress, 
            key=lambda name: system_start_time.get(name, parse_date(starttime))
        )
        # If slots remain, add systems that have not started yet
        not_started = [name for name in candidate_systems if name not in systems_in_progress and name not in systems_completed]
        prioritized_systems += not_started[:available_slots]

        # Try to assign milestones for all prioritized systems
        # Track which resources have been used in this iteration
        used_resources = set()
        assigned_any = False
        
        for idx, system_name in enumerate(prioritized_systems):
            queue_info = system_queues[system_name]
            if queue_info['current_index'] >= len(queue_info['milestones']):
                continue  # This system is done

            milestone = queue_info['milestones'][queue_info['current_index']]
            ftetype = milestone['ftetype']
            min_duration = milestone['duration']
            workdays = milestone['workdays']

            # Get resources of the correct type that haven't been used in this iteration
            available_resources = [r for r in ressources if r['ftetype'] == ftetype and r['ressourcename'] not in used_resources]
            available_resources.sort(key=lambda r: resource_availability[r['ressourcename']])

            if len(available_resources) == 0:
                continue  # No resources of this type available

            # Calculate when this milestone could start
            prev_milestone_finish = system_milestone_finish[system_name]

            assigned = []
            total_availability = 0
            for res in available_resources:
                assigned.append(res)
                total_availability += res['availability']
                if min_duration * total_availability >= workdays:
                    break

            if len(assigned) == 0:
                continue

            earliest_resource_time = max([resource_availability[r['ressourcename']] for r in assigned])
            milestone_can_start = max(prev_milestone_finish, earliest_resource_time)
            
            # Ensure milestone starts on a workday
            milestone_start = next_workday(milestone_can_start)

            # Calculate how many workdays are needed based on availability
            total_availability = sum(res['availability'] for res in assigned)
            workdays_needed = workdays / total_availability if total_availability > 0 else min_duration
            
            # Calculate calendar duration considering only workdays
            # We need at least min_duration calendar days, and enough workdays to complete the work
            calendar_days_for_workdays = 0
            temp_date = milestone_start
            workdays_counted = 0
            while workdays_counted < workdays_needed:
                if is_workday(temp_date):
                    workdays_counted += 1
                temp_date += timedelta(days=1)
                calendar_days_for_workdays += 1
            
            # Ensure we meet the minimum duration requirement
            calendar_days = max(calendar_days_for_workdays, min_duration)
            
            # Calculate the finish date by adding calendar days
            milestone_finish = milestone_start + timedelta(days=calendar_days)
            
            # Count actual workdays in the span for effective person-days calculation
            actual_workdays = 0
            check_date = milestone_start
            while check_date < milestone_finish:
                if is_workday(check_date):
                    actual_workdays += 1
                check_date += timedelta(days=1)

            milestone_finish_times = []
            for res in assigned:
                taskname = f"{queue_info['system']['name']}-{milestone['name']}-{res['ressourcename']}"
                tasks.append({
                    'Task': taskname,
                    'Start': milestone_start.strftime('%Y-%m-%d'),
                    'Finish': milestone_finish.strftime('%Y-%m-%d'),
                    'Resource': res['ressourcename'],
                    'ResourceType': res['ftetype'],
                    'System': queue_info['system']['name'],
                    'Milestone': milestone['name'],
                    'FTE': 1,
                    'EffectivePersonDays': actual_workdays * res['availability']
                })
                resource_availability[res['ressourcename']] = milestone_finish
                milestone_finish_times.append(milestone_finish)
                used_resources.add(res['ressourcename'])

            system_milestone_finish[system_name] = max(milestone_finish_times)
            
            # Track system start time if this is its first milestone
            if queue_info['current_index'] == 0:
                system_start_time[system_name] = milestone_start
            
            queue_info['current_index'] += 1
            assigned_any = True
        
        if not assigned_any:
            break  # No more milestones can be started

    return tasks

def convert_tasks(tasks):
    """
    Convert tasks into intervals grouped by System, ResourceType, and Milestone.
    For each interval, calculate total FTE count.
    Output is in the same task format as createtasks().
    """
    import pandas as pd

    # Collect all unique time boundaries
    dates = set()
    for t in tasks:
        dates.add(t['Start'])
        dates.add(t['Finish'])
    dates = sorted(pd.to_datetime(list(dates)))
    intervals = list(zip(dates[:-1], dates[1:]))

    result = []
    for start, end in intervals:
        # Find tasks active in this interval
        active = [t for t in tasks if pd.to_datetime(t['Start']) <= start and pd.to_datetime(t['Finish']) > start]
        # Group by System, ResourceType, Milestone
        groups = {}
        for t in active:
            key = (t['System'], t['ResourceType'], t['Milestone'])
            groups.setdefault(key, 0)
            groups[key] += t['FTE']
        for (system, res_type, milestone), fte_sum in groups.items():
            result.append({
                'Task': f'{system}-{milestone}-{res_type}',
                'Start': start.strftime('%Y-%m-%d'),
                'Finish': end.strftime('%Y-%m-%d'),
                'Resource': f'{res_type}',
                'ResourceType': res_type,
                'System': system,
                'Milestone': milestone,
                'FTE': fte_sum
            })
    return result

def plottasksonproject(df, save_as_png=False, filename="gantt_project_tasks.png", xaxis_range=None):
    """Plot the Gantt chart for the project tasks DataFrame"""
    # Scale FTE so bars have height proportional to FTE
    max_fte = df["FTE"].max()
    if max_fte > 0:
        df["FTE_scaled"] = df["FTE"] / max_fte * 0.8
    else:
        df["FTE_scaled"] = 0.5
    
    print("\nFTE scaling for plottasksonproject:")
    print(df[["Task", "Start", "Finish", "FTE", "FTE_scaled"]])

    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="System", text="Milestone")
    fig.update_yaxes(autorange="reversed")
    
    # Set bar widths (vertical thickness) based on FTE_scaled
    # We need to map each bar to its corresponding FTE_scaled value
    fte_scaled_values = df["FTE_scaled"].tolist()
    
    # For each trace (grouped by System), we need to assign widths based on the data points
    bar_index = 0
    for trace in fig.data:
        num_bars = len(trace.x)
        trace.width = fte_scaled_values[bar_index:bar_index + num_bars]
        bar_index += num_bars
    
    fig.update_traces(textposition="inside", insidetextanchor="middle", textfont_size=10, textfont_color="white")
    fig.update_layout(
        title="Project Gantt Chart (Bar height ∝ FTE)",
        showlegend=True,
        width=1200,
        height=800
    )

    if xaxis_range:
        fig.update_xaxes(range=xaxis_range)
    
    if save_as_png:
        fig.write_image(filename)
        print(f"Saved project tasks chart as {filename}")
    else:
        fig.show()

def plot_system_summary(df, save_as_png=False, filename="gantt_system_summary.png", xaxis_range=None):
    """
    Plot simplified Gantt chart: one box per system from start to finish.
    Box height × length represents total workdays.
    Height is proportional to workdays, so height × length = workdays.
    """
    import pandas as pd
    
    # Calculate start, end, and total workdays for each system
    system_summary = df.groupby('System').agg({
        'Start': 'min',
        'Finish': 'max',
        'EffectivePersonDays': 'sum'
    }).reset_index()
    
    system_summary.columns = ['System', 'Start', 'Finish', 'TotalWorkdays']
    
    # Calculate calendar days for each system
    system_summary['Start'] = pd.to_datetime(system_summary['Start'])
    system_summary['Finish'] = pd.to_datetime(system_summary['Finish'])
    system_summary['CalendarDays'] = (system_summary['Finish'] - system_summary['Start']).dt.days
    
    # Calculate box height: height = workdays / calendar_days
    # So height × length = workdays / calendar_days × calendar_days = workdays
    system_summary['BoxHeight'] = system_summary['TotalWorkdays'] / system_summary['CalendarDays']
    
    # Scale heights for visualization
    max_height = system_summary['BoxHeight'].max()
    if max_height > 0:
        system_summary['BoxHeight_scaled'] = system_summary['BoxHeight'] / max_height * 0.8
    else:
        system_summary['BoxHeight_scaled'] = 0.5
    
    print("\nSystem Summary:")
    print(system_summary[['System', 'Start', 'Finish', 'CalendarDays', 'TotalWorkdays', 'BoxHeight']])
    
    # Create text showing workdays
    system_summary['Text'] = system_summary['TotalWorkdays'].apply(lambda x: f'{x:.0f} wd')
    
    # Map systems to countries
    system_country_map = {s['name']: s['country'] for s in systems}
    system_summary['Country'] = system_summary['System'].map(system_country_map)
    
    # Define flag URLs and colors
    flag_urls = {
        'dk': 'https://flagcdn.com/w320/dk.png',
        'se': 'https://flagcdn.com/w320/se.png',
        'no': 'https://flagcdn.com/w320/no.png'
    }
    
    # Set colors: transparent for countries with flags (to show flag), default for others
    country_colors = {
        'dk': 'rgba(0,0,0,0)',
        'se': 'rgba(0,0,0,0)',
        'no': 'rgba(0,0,0,0)',
        'all': '#636EFA'
    }

    fig = px.timeline(
        system_summary,
        x_start="Start",
        x_end="Finish",
        y="System",
        color="Country",
        color_discrete_map=country_colors,
        text="Text"
    )
    
    # Add flag images
    for i, row in system_summary.iterrows():
        country = row.get('Country')
        if country in flag_urls:
            # Calculate duration in milliseconds for sizex
            duration_ms = (row['Finish'] - row['Start']).total_seconds() * 1000
            
            fig.add_layout_image(
                dict(
                    source=flag_urls[country],
                    xref="x",
                    yref="y",
                    x=row['Start'],
                    y=row['System'],
                    sizex=duration_ms,
                    sizey=row['BoxHeight_scaled'],
                    sizing="stretch",
                    opacity=1.0,
                    layer="below",
                    xanchor="left",
                    yanchor="middle"
                )
            )

    fig.update_yaxes(autorange="reversed")
    fig.update_traces(
        textposition="inside",
        insidetextanchor="middle",
        textfont_size=12,
        textfont_color="white",
        width=list(system_summary['BoxHeight_scaled'])
    )
    fig.update_layout(
        title="System Summary (Box height × length ∝ total workdays)",
        showlegend=True,
        xaxis_title="Timeline",
        yaxis_title="System",
        width=1200,
        height=800
    )

    if xaxis_range:
        fig.update_xaxes(range=xaxis_range)
    
    if save_as_png:
        fig.write_image(filename)
        print(f"Saved system summary chart as {filename}")
    else:
        fig.show()

def plot_milestone_progress(df, save_as_png=False, filename="gantt_milestone_progress.png", xaxis_range=None):
    """
    Plot a line chart showing cumulative number of milestones completed over time.
    A milestone is considered complete when it finishes.
    """
    import pandas as pd
    import plotly.graph_objects as go
    
    # Get unique milestone completions (system + milestone combination)
    # Group by System and Milestone to get finish times
    milestone_completions = df.groupby(['System', 'Milestone']).agg({
        'Finish': 'max'
    }).reset_index()
    
    milestone_completions['Finish'] = pd.to_datetime(milestone_completions['Finish'])
    milestone_completions = milestone_completions.sort_values('Finish')
    
    # Create cumulative count
    milestone_completions['CumulativeMilestones'] = range(1, len(milestone_completions) + 1)
    
    print("\nMilestone Completions:")
    print(milestone_completions)
    
    # Create line chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=milestone_completions['Finish'],
        y=milestone_completions['CumulativeMilestones'],
        mode='lines+markers',
        name='Milestones Completed',
        line=dict(color='blue', width=2),
        marker=dict(size=6),
        hovertemplate='<b>Date:</b> %{x}<br><b>Milestones:</b> %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Cumulative Milestones Completed Over Time',
        xaxis_title='Date',
        yaxis_title='Number of Milestones Completed',
        hovermode='closest',
        showlegend=True,
        width=1200,
        height=800
    )

    if xaxis_range:
        fig.update_xaxes(range=xaxis_range)
    
    if save_as_png:
        fig.write_image(filename)
        print(f"Saved milestone progress chart as {filename}")
    else:
        fig.show()

def project(xaxis_range=None):
    """Generate and display a Gantt chart for the defined project"""
    print("Creating project Gantt chart...")
    # Limit to 3 systems in progress at any time
    tasks = createtasks('2025-11-04', systems, systemmilestones, ressources, max_systems_in_progress=7)
    df = pd.DataFrame(tasks)
    print("\nOriginal tasks DataFrame:")
    print(df)
    print("\nOriginal FTE values:", df["FTE"].unique())
    for i in range(df.shape[0]):
        print(f"Row {i} - Task: {df.at[i, 'Task']}, FTE: {df.at[i, 'FTE']}")
        
    convert_tasksed = convert_tasks(tasks)
    df_converted = pd.DataFrame(convert_tasksed)
    print("\nConverted tasks DataFrame:")
    print(df_converted)
    print("\nConverted FTE values:", df_converted["FTE"].unique())
    
    # Save task lists to CSV files
    df.to_csv('tasks_detailed.csv', index=False)
    df_converted.to_csv('tasks_converted.csv', index=False)
    print("\nTask lists saved to CSV files:")
    print("1. tasks_detailed.csv - Detailed individual tasks with resource assignments")
    print("2. tasks_converted.csv - Converted tasks grouped by System/ResourceType/Milestone")
    
    # Save all three charts as PNG files
    plottasksonproject(df_converted, save_as_png=True, filename="gantt_project_tasks.png", xaxis_range=xaxis_range)
    plot_system_summary(df, save_as_png=True, filename="gantt_system_summary.png", xaxis_range=xaxis_range)
    plot_milestone_progress(df, save_as_png=True, filename="gantt_milestone_progress.png", xaxis_range=xaxis_range)
    
    print("\nAll three Gantt charts have been saved as PNG files:")
    print("1. gantt_project_tasks.png - Detailed project tasks with milestones")
    print("2. gantt_system_summary.png - System summary with total workdays")
    print("3. gantt_milestone_progress.png - Cumulative milestone progress over time")

if __name__ == "__main__":
    project()
