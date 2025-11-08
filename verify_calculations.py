"""
Verification script to confirm that time*FTE sums match duration*FTE targets
"""
import pandas as pd
from gantt import createtasks, systems, systemmilestones, ressources

# Create tasks
tasks = createtasks('2025-11-04', systems, systemmilestones, ressources)
df = pd.DataFrame(tasks)

print("=" * 80)
print("VERIFICATION: Checking that time*FTE sums match duration*FTE targets")
print("=" * 80)

# Group by system and milestone to calculate totals
grouped = df.groupby(['System', 'Milestone'])

for (system, milestone), group in grouped:
    # Find the milestone definition
    milestone_def = None
    for sys in systems:
        if sys['name'] == system:
            for ms_set in systemmilestones:
                if ms_set['complexity'] == sys['complexity'] and ms_set['method'] == sys['method']:
                    for ms in ms_set['milestones']:
                        if ms['name'] == milestone:
                            milestone_def = ms
                            break
                    break
            break
    
    if milestone_def:
        # Calculate expected target
        target_person_days = milestone_def['duration'] * milestone_def['fte']
        
        # Calculate actual from tasks (sum of EffectivePersonDays)
        actual_person_days = group['EffectivePersonDays'].sum()
        
        # Calculate difference
        difference = abs(actual_person_days - target_person_days)
        status = "✓ PASS" if difference < 0.01 else "✗ FAIL"
        
        print(f"\n{status} System: {system}, Milestone: {milestone}")
        print(f"  Target (duration * FTE): {milestone_def['duration']} days * {milestone_def['fte']} FTE = {target_person_days:.2f} person-days")
        print(f"  Actual (sum of time*FTE): {actual_person_days:.2f} person-days")
        print(f"  Difference: {difference:.6f} person-days")
        print(f"  Resources assigned: {len(group)} resources")
        
        # Show individual resource contributions
        print(f"  Resource breakdown:")
        for _, row in group.iterrows():
            res_name = row['Resource']
            eff_days = row['EffectivePersonDays']
            print(f"    - {res_name}: {eff_days:.2f} person-days")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

# Overall summary
all_match = True
for (system, milestone), group in grouped:
    milestone_def = None
    for sys in systems:
        if sys['name'] == system:
            for ms_set in systemmilestones:
                if ms_set['complexity'] == sys['complexity'] and ms_set['method'] == sys['method']:
                    for ms in ms_set['milestones']:
                        if ms['name'] == milestone:
                            milestone_def = ms
                            break
                    break
            break
    
    if milestone_def:
        target = milestone_def['duration'] * milestone_def['fte']
        actual = group['EffectivePersonDays'].sum()
        if abs(actual - target) >= 0.01:
            all_match = False
            break

if all_match:
    print("✓ All milestones have matching time*FTE sums! Implementation is correct.")
else:
    print("✗ Some milestones have mismatched time*FTE sums. Please review.")

print("=" * 80)
