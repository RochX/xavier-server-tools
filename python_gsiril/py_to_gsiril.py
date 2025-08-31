# dynamically create the "prove" statement in a gsiril file
# for now using the example case of attempting to find an extent of Titanic Doubles using Stedman singles (145 or 345)
import os, subprocess
count = 0

# curr_touch: list of leads, ex [p,b,s,p,p,...]
# lead_types: what can be placed in the leads
# num_leads: desired length
def find_touches(curr_touch,lead_types,num_leads):
  if len(curr_touch) > 0 and not prove_touch(curr_touch, allow_incomplete=True):
    return

  if prove_touch(curr_touch):
    output_touch(curr_touch)
    return

  if len(curr_touch) >= num_leads:
    return

  for l in lead_types:
    find_touches(curr_touch+[l],lead_types,num_leads)


def output_touch(touch):
  global count
  count += 1
  outstr = ','.join(touch)
  with open("output.txt", "a") as f:
    print(count, f"Outputted touch of length {len(touch)*lead_length} to file.")
    print(count, prove_touch(touch), f"Touch is {len(touch)*lead_length} changes:", outstr, file=f)

# returns if touch is true
def prove_touch(touch, allow_incomplete=False):
  subprocess.run(f"cp {method_name}_template.siril {method_name}.siril", shell=True)
  subprocess.run(f"echo \"\nprove {','.join(touch)}\" >> {method_name}.siril", shell=True)
  completed = subprocess.run(f"gsiril < {method_name}.siril", shell=True, text=True, capture_output=True)
  # print("Touch:", touch)
  # print("Process output:", completed.stdout)
  # print("Process error:", completed.stderr)

  return "Touch is true" in completed.stdout or (allow_incomplete and "Is this OK?" in completed.stdout)


method_name = "twinimus"
subprocess.run("mv output.txt prev_output.txt", shell=True)
lead_types = ["pl","hu"]
lead_length = 8
# 1250/8 = 156.25, so 157 leads needed
find_touches(["hu"], lead_types, 1250/lead_length)
