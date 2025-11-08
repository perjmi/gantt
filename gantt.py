"""
Gantt Charts Examples using Plotly
Based on examples from https://plotly.com/python/gantt/
"""

import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd

systems = [{'name': 'hac', 'systype': 'policy', 'country': 'se', 'complexity': 'medium', 'quality': 'medium', 'method': 'option1'}]
systems.append({'name': 'sol', 'systype': 'policy', 'country': 'se', 'complexity': 'medium', 'quality': 'medium', 'method': 'option1'})
systems.append({'name':'tosca','systype':'policy','country':'dk','complexity':'hard','quality':'medium','method':'option2'})

systemmilestones = [
    {
        'complexity': 'medium',
        'method':'option1',
        'milestones': [
            {'name': 'T360 2 T360Next', 'duration': 15,'workdays':45,'ftetype':'dev'},
            {'name': 'BI fac 2 T360Next', 'duration': 42,'workdays':210,'ftetype':'dev'},
            {'name': 'Test on SF mock', 'duration': 1,'workdays':5,'ftetype':'test'},
            {'name': 'Real data 2 SF', 'duration': 40,'workdays':200,'ftetype':'dev'}
        ]
    }
]

systemmilestones.append(
    {
        'complexity': 'hard',
        'method':'option2',
        'milestones': [
            {'name': 'milestone1', 'duration': 15,'workdays':45,'ftetype':'dev'},
            {'name': 'milestone2', 'duration': 7,'workdays':14,'ftetype':'test'}
        ]
    }
)

ressources = [
    {'ftetype':'dev','unitcostprday':1000,'availability':0.8,'ressourcename':'Developer1'},
    {'ftetype':'dev','unitcostprday':1000,'availability':1.0,'ressourcename':'Developer2'},
    {'ftetype':'dev','unitcostprday':950,'availability':0.85,'ressourcename':'Developer3'},
    {'ftetype':'dev','unitcostprday':1050,'availability':0.9,'ressourcename':'Developer4'},
    {'ftetype':'dev','unitcostprday':980,'availability':0.95,'ressourcename':'Developer5'},
    {'ftetype':'dev','unitcostprday':1020,'availability':1.0,'ressourcename':'Developer6'},
    {'ftetype':'test','unitcostprday':800,'availability':0.9,'ressourcename':'Tester1'},
    {'ftetype':'test','unitcostprday':820,'availability':0.95,'ressourcename':'Tester2'},
    {'ftetype':'test','unitcostprday':780,'availability':1.0,'ressourcename':'Tester3'}
]

ressources1 = [
    {'ftetype':'dev','unitcostprday':1050,'availability':0.9,'ressourcename':'Developer4'},
    {'ftetype':'dev','unitcostprday':980,'availability':0.95,'ressourcename':'Developer5'},
    {'ftetype':'dev','unitcostprday':1020,'availability':1.0,'ressourcename':'Developer6'},
    {'ftetype':'test','unitcostprday':800,'availability':0.9,'ressourcename':'Tester1'},
    {'ftetype':'test','unitcostprday':820,'availability':0.95,'ressourcename':'Tester2'},
    {'ftetype':'test','unitcostprday':780,'availability':1.0,'ressourcename':'Tester3'}
]

def createtasks(starttime, systems, systemmilestones, ressources):
    """
    Generate tasks for Gantt chart from systems, systemmilestones, and ressources.
    Tries to exhaust resources by issuing as many parallel tasks as possible.
    Returns a list of dicts with Task, Start, Finish.
    starttime: string, e.g. '2025-11-04'
    
    Milestone format:
    - duration: minimum calendar duration allowed (days)
    - workdays: total person-days (FTE-days) needed to complete the milestone
    
    The function assigns resources to meet the workdays requirement while ensuring
    the calendar duration is at least the minimum duration specified.
    """
    import pandas as pd
    from datetime import timedelta
    
    def parse_date(d):
        return pd.to_datetime(d)
    
    # Track when each resource becomes available
    resource_availability = {}
    for res in ressources:
        resource_availability[res['ressourcename']] = parse_date(starttime)
    
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
    
    # Process milestones across all systems, always trying to use available resources
    while True:
        # Find the next milestone that can be started
        # Criteria: has resources available and previous milestone in system is done
        best_candidate = None
        best_start_time = None
        
        for system_name, queue_info in system_queues.items():
            if queue_info['current_index'] >= len(queue_info['milestones']):
                continue  # This system is done
            
            milestone = queue_info['milestones'][queue_info['current_index']]
            ftetype = milestone['ftetype']
            min_duration = milestone['duration']
            workdays = milestone['workdays']
            
            # Get resources of the correct type, sorted by availability time
            available_resources = [r for r in ressources if r['ftetype'] == ftetype]
            available_resources.sort(key=lambda r: resource_availability[r['ressourcename']])
            
            if len(available_resources) == 0:
                continue  # No resources of this type available
            
            # Calculate when this milestone could start
            # It needs: (1) previous milestone in system done, (2) at least one resource available
            prev_milestone_finish = system_milestone_finish[system_name]
            
            # Determine how many resources to assign to meet workdays within min_duration
            # We want to assign enough resources so that the work can be done in min_duration
            # or more if needed
            
            # Calculate how many resources we need at minimum
            # If we use N resources for min_duration days, we get: min_duration * sum(availability)
            # We need this to be >= workdays
            
            assigned = []
            total_availability = 0
            for res in available_resources:
                assigned.append(res)
                total_availability += res['availability']
                # Check if we can meet workdays in min_duration with these resources
                if min_duration * total_availability >= workdays:
                    break
            
            if len(assigned) == 0:
                continue  # Should not happen given the check above
            
            # Calculate when all assigned resources are available
            earliest_resource_time = max([resource_availability[r['ressourcename']] for r in assigned])
            milestone_can_start = max(prev_milestone_finish, earliest_resource_time)
            
            # Choose the milestone that can start earliest
            if best_candidate is None or milestone_can_start < best_start_time:
                best_candidate = (system_name, queue_info, milestone, assigned)
                best_start_time = milestone_can_start
        
        if best_candidate is None:
            break  # No more milestones can be started
        
        # Assign the best candidate milestone
        system_name, queue_info, milestone, assigned = best_candidate
        min_duration = milestone['duration']
        workdays = milestone['workdays']
        
        # All resources on the same milestone must start at the same time
        # This is when ALL required resources are available
        milestone_start = best_start_time
        
        # Calculate total availability of assigned resources
        total_availability = sum(res['availability'] for res in assigned)
        
        # Calculate calendar days needed such that total person-days = workdays
        # Each resource contributes (calendar_days * availability) person-days
        # Total contribution = calendar_days * total_availability
        # We need: calendar_days * total_availability = workdays
        calendar_days_needed = workdays / total_availability if total_availability > 0 else min_duration
        
        # Ensure we respect the minimum duration
        calendar_days = max(calendar_days_needed, min_duration)
        
        milestone_finish_times = []
        for res in assigned:
            # Each resource works for the same calendar_days
            finish = milestone_start + timedelta(days=calendar_days)
            
            taskname = f"{queue_info['system']['name']}-{milestone['name']}-{res['ressourcename']}"
            tasks.append({
                'Task': taskname,
                'Start': milestone_start.strftime('%Y-%m-%d'),
                'Finish': finish.strftime('%Y-%m-%d'),
                'Resource': res['ressourcename'],
                'ResourceType': res['ftetype'],
                'System': queue_info['system']['name'],
                'Milestone': milestone['name'],
                'FTE': 1,
                'EffectivePersonDays': calendar_days * res['availability']  # For verification
            })
            
            # Update when this resource becomes available again
            resource_availability[res['ressourcename']] = finish
            milestone_finish_times.append(finish)
        
        # Mark this milestone as complete for this system
        system_milestone_finish[system_name] = max(milestone_finish_times)
        queue_info['current_index'] += 1
    
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

def basic_gantt_timeline():
    """Basic Gantt chart using plotly.express.timeline (recommended approach)"""
    print("Creating basic Gantt chart with plotly.express.timeline...")
    
    df = pd.DataFrame([
        dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28'),
        dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15'),
        dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30')
    ])

    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
    fig.update_yaxes(autorange="reversed")  # otherwise tasks are listed from the bottom up
    fig.update_layout(title="Basic Gantt Chart with Plotly Express")
    fig.show()

def gantt_with_resources():
    """Gantt chart colored by resource using discrete colors"""
    print("Creating Gantt chart with resource coloring...")
    
    df = pd.DataFrame([
        dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28', Resource="Alex"),
        dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15', Resource="Alex"),
        dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30', Resource="Max")
    ])

    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Resource")
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(title="Gantt Chart Colored by Resource")
    fig.show()

def gantt_with_completion():
    """Gantt chart colored by completion percentage using continuous colors"""
    print("Creating Gantt chart with completion percentage coloring...")
    
    df = pd.DataFrame([
        dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28', Completion_pct=50),
        dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15', Completion_pct=25),
        dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30', Completion_pct=75)
    ])

    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Completion_pct")
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(title="Gantt Chart Colored by Completion Percentage")
    fig.show()

def gantt_by_resource_timeline():
    """Gantt chart showing multiple bars on the same horizontal line by resource"""
    print("Creating Gantt chart organized by resource...")
    
    df = pd.DataFrame([
        dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28', Resource="Alex"),
        dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15', Resource="Alex"),
        dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30', Resource="Max")
    ])

    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Resource", color="Resource", text="Task")
    # Note: When setting color to the same value as y, autorange should not be set to reverse
    fig.update_traces(textposition="middle center", textfont_size=12)
    fig.update_layout(
        title="Gantt Chart Organized by Resource (with text on bars)",
        showlegend=False  # Hide the legend since text is on the bars
    )
    fig.show()

def gantt_with_resources_text_on_bars():
    """Gantt chart colored by resource with resource names displayed on the bars"""
    print("Creating Gantt chart with resource names on bars...")
    
    df = pd.DataFrame([
        dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28', Resource="Alex"),
        dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15', Resource="Alex"),
        dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30', Resource="Max")
    ])

    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Resource", text="Resource")
    fig.update_yaxes(autorange="reversed")
    fig.update_traces(textposition="middle center", textfont_size=12, textfont_color="white")
    fig.update_layout(
        title="Gantt Chart with Resource Names on Bars",
        showlegend=False  # Hide the legend since text is on the bars
    )
    fig.show()

def deprecated_figure_factory_basic():
    """Basic Gantt chart using the deprecated figure factory approach"""
    print("Creating basic Gantt chart with deprecated figure factory...")
    
    df = [dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28'),
          dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15'),
          dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30')]

    fig = ff.create_gantt(df)
    fig.update_layout(title="Basic Gantt Chart with Figure Factory (Deprecated)")
    fig.show()

def figure_factory_grouped_tasks():
    """Gantt chart with grouped tasks using the deprecated figure factory"""
    print("Creating grouped tasks Gantt chart with figure factory...")
    
    df = [dict(Task="Job-1", Start='2017-01-01', Finish='2017-02-02', Resource='Complete'),
          dict(Task="Job-1", Start='2017-02-15', Finish='2017-03-15', Resource='Incomplete'),
          dict(Task="Job-2", Start='2017-01-17', Finish='2017-02-17', Resource='Not Started'),
          dict(Task="Job-2", Start='2017-01-17', Finish='2017-02-17', Resource='Complete'),
          dict(Task="Job-3", Start='2017-03-10', Finish='2017-03-20', Resource='Not Started'),
          dict(Task="Job-3", Start='2017-04-01', Finish='2017-04-20', Resource='Not Started'),
          dict(Task="Job-3", Start='2017-05-18', Finish='2017-06-18', Resource='Not Started'),
          dict(Task="Job-4", Start='2017-01-14', Finish='2017-03-14', Resource='Complete')]

    colors = {'Not Started': 'rgb(220, 0, 0)',
              'Incomplete': (1, 0.9, 0.16),
              'Complete': 'rgb(0, 255, 100)'}

    fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True,
                          group_tasks=True)
    fig.update_layout(title="Gantt Chart with Grouped Tasks and Custom Colors")
    fig.show()

def figure_factory_numeric_color():
    """Gantt chart colored by numeric variable using the deprecated figure factory"""
    print("Creating Gantt chart with numeric coloring using figure factory...")
    
    df = [dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28', Complete=10),
          dict(Task="Job B", Start='2008-12-05', Finish='2009-04-15', Complete=60),
          dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30', Complete=95)]

    fig = ff.create_gantt(df, colors='Viridis', index_col='Complete', show_colorbar=True)
    fig.update_layout(title="Gantt Chart Colored by Numeric Variable (Viridis)")
    fig.show()

def main():
    """Run all Gantt chart examples"""
    print("Running Plotly Gantt Chart Examples")
    print("=" * 50)
    
    # Modern plotly.express examples (recommended)
    basic_gantt_timeline()
    gantt_with_resources()
    gantt_with_resources_text_on_bars()
    gantt_with_completion()
    gantt_by_resource_timeline()
    
    print("\n" + "=" * 50)
    print("Deprecated Figure Factory Examples")
    print("=" * 50)
    
    # Deprecated figure factory examples
    deprecated_figure_factory_basic()
    figure_factory_grouped_tasks()
    figure_factory_numeric_color()
    
    print("\nAll examples completed!")

def plottasksonproject(df):
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
        showlegend=True
    )
    fig.show()

def plot_system_milestones(df):
    """Plot system milestones: bar height (vertical thickness) is proportional to total FTEs working at any one time per system"""
    import pandas as pd

    # Collect all unique dates for time splits
    all_dates = pd.concat([df["Start"], df["Finish"]]).drop_duplicates().sort_values()
    intervals = list(zip(all_dates[:-1], all_dates[1:]))

    rows = []
    # Track first appearance of each milestone per system
    milestone_first_bar = {}
    for (start, end) in intervals:
        active = df[
            (df["Start"] <= start) & (df["Finish"] > start)
        ]
        grouped = active.groupby(["System", "Milestone"]).agg({
            "FTE": "sum"
        }).reset_index()
        for _, row in grouped.iterrows():
            key = (row["System"], row["Milestone"])
            milestone_text = row["Milestone"] if key not in milestone_first_bar else ""
            milestone_first_bar[key] = True
            rows.append({
                "System": row["System"],
                "Start": start,
                "Finish": end,
                "FTE": row["FTE"],
                "Milestone": milestone_text
            })

    interval_df = pd.DataFrame(rows)
    if interval_df.empty or interval_df["FTE"].max() == 0:
        print("No milestones to plot or FTE is zero.")
        return

    # Scale FTE for bar height (vertical thickness)
    max_fte = interval_df["FTE"].max()
    interval_df["FTE_scaled"] = interval_df["FTE"] / max_fte * 0.3

    fig = px.timeline(
        interval_df,
        x_start="Start",
        x_end="Finish",
        y="System",
        color="System",
        text="Milestone"
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_traces(
        textposition="inside",
        insidetextanchor="middle",
        textfont_size=10,
        width=list(interval_df["FTE_scaled"])
    )
    fig.update_layout(
        title="System Milestones (Bar height ∝ total FTEs working at any time)",
        showlegend=True
    )
    fig.show()

def project():
    """Generate and display a Gantt chart for the defined project"""
    print("Creating project Gantt chart...")
    tasks = createtasks('2025-11-04', systems, systemmilestones, ressources)
    df = pd.DataFrame(tasks)
    print("\nOriginal tasks DataFrame:")
    print(df)
    print("\nOriginal FTE values:", df["FTE"].unique())
    
    convert_tasksed = convert_tasks(tasks)
    df_converted = pd.DataFrame(convert_tasksed)
    print("\nConverted tasks DataFrame:")
    print(df_converted)
    print("\nConverted FTE values:", df_converted["FTE"].unique())
    
    plottasksonproject(df_converted)

if __name__ == "__main__":
    project()
