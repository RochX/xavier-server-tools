# dynamically create the "prove" statement in a gsiril file
# for now using the example case of attempting to find an extent of Titanic Doubles using Stedman singles (145 or 345)
import os, subprocess
count = 0

# curr_touch: list of leads, ex [p,b,s,p,p,...]
# leads: what can be placed in the leads
# num_leads: desired length
def find_touches(curr_touch,leads,num_leads):
  if len(curr_touch) > 0 and not prove_touch(curr_touch):
    return

  if len(curr_touch) == num_leads or prove_touch(curr_touch):
    output_touch(curr_touch)
    return

  for l in leads:
    find_touches(curr_touch+[l],leads,num_leads)


def output_touch(touch):
  global count
  count += 1
  print(count, touch, prove_touch(touch))

# returns if touch is true
def prove_touch(touch):
  subprocess.run("cp template.siril titanic.siril", shell=True)
  subprocess.run(f"echo \"\nprove {','.join(touch)}\" >> titanic.siril", shell=True)
  completed = subprocess.run("gsiril < titanic.siril", shell=True, text=True, capture_output=True)
  # print("Touch:", touch)
  # print("Process output:", completed.stdout)
  # print("Process error:", completed.stderr)

  return "Touch is true" in completed.stdout


leads = ["pp","sp","ps","ss"]
lead_length = 4

find_touches([], leads, 5)