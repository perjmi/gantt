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
            {'name': 'milestone1', 'duration': 10,'fte':2,'ftetype':'dev'},
            {'name': 'milestone2', 'duration': 5,'fte':1,'ftetype':'test'}
        ]
    }
]

systemmilestones.append(
    {
        'complexity': 'hard',
        'method':'option2',
        'milestones': [
            {'name': 'milestone1', 'duration': 15,'fte':3,'ftetype':'dev'},
            {'name': 'milestone2', 'duration': 7,'fte':2,'ftetype':'test'}
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

def createtasks(starttime, systems, systemmilestones, ressources):
    """
    Generate tasks for Gantt chart from systems, systemmilestones, and ressources.
    Tries to exhaust resources by issuing as many parallel tasks as possible.
    Returns a list of dicts with Task, Start, Finish.
    starttime: string, e.g. '2025-11-04'
    """
    import pandas as pd
    from datetime import timedelta
    
    def get_available_resources(ftetype):
        return [r for r in ressources if r['ftetype'] == ftetype]
    
    def parse_date(d):
        return pd.to_datetime(d)
    
    current_time = parse_date(starttime)
    tasks = []
    
    for system in systems:
        ms_set = None
        for ms in systemmilestones:
            if ms['complexity'] == system['complexity'] and ms['method'] == system['method']:
                ms_set = ms
                break
        if not ms_set:
            continue
        for milestone in ms_set['milestones']:
            available = get_available_resources(milestone['ftetype'])
            n_needed = milestone['fte']
            duration = milestone['duration']
            assigned = available[:n_needed]
            if not assigned:
                continue
            for res in assigned:
                eff_duration = duration / res['availability']
                start = current_time
                finish = start + timedelta(days=eff_duration)
                taskname = f"{system['name']}-{milestone['name']}-{res['ressourcename']}"
                tasks.append({
                    'Task': taskname,
                    'Start': start.strftime('%Y-%m-%d'),
                    'Finish': finish.strftime('%Y-%m-%d'),
                    'Resource': res['ressourcename'],
                    'ResourceType': res['ftetype'],
                    'System': system['name'],
                    'Milestone': milestone['name'],
                    'FTE': 1
                })
            current_time = max([parse_date(t['Finish']) for t in tasks if t['Milestone'] == milestone['name'] and t['System'] == system['name']])
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
