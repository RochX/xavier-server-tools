# dynamically create the "prove" statement in a gsiril file
# for now using the example case of attempting to find an extent of Titanic Doubles using Stedman singles (145 or 345)
import os, subprocess
count = 0

# curr_touch: list of leads, ex [p,b,s,p,p,...]
# lead_types: what can be placed in the leads
# num_leads: desired length
def find_touches(curr_touch,lead_types,desired_changes):
  length, status = prove_touch(curr_touch)

  # touch is false, adding on anything would not change that fact
  if status == False and not REPEAT_MODE:
    return
  
  # in this combination of modes: check if adding actually changed the result
  if REPEAT_MODE and CALLING_POSITIONS_MODE and curr_touch != []:
    if prove_touch(curr_touch[:-1]) == prove_touch(curr_touch):
      return
    
  if REPEAT_MODE and CALLING_POSITIONS_MODE and length > desired_changes + 200:
    return
  
  # touch is true, adding on anything would break this fact
  if status == True:
    output_touch(curr_touch)
    if not REPEAT_MODE:
      return
    
    if REPEAT_MODE and CALLING_POSITIONS_MODE:
      return

  if not REPEAT_MODE and length >= desired_changes:
    return
  
  if REPEAT_MODE and not CALLING_POSITIONS_MODE and len(curr_touch)*LEAD_LENGTH >= desired_changes:
    return

  for l in lead_types:
    find_touches(curr_touch+[l],lead_types,desired_changes)


def output_touch(touch):
  global count
  count += 1
  outstr = ','.join(touch)

  if REPEAT_MODE:
    outstr = f"repeat({outstr}, {{/12345678/: break}})"

  with open("output.txt", "a") as f:
    length, _ = prove_touch(touch)
    print(count, f"Outputted touch of length {length} to file.")
    print(count, f"Touch is {length} changes:", outstr, file=f)

# returns if touch is true
def prove_touch(touch):
  if touch == []:
    return (0, None)

  subprocess.run(f"cp {method_name}_template.siril {method_name}.siril", shell=True)
  if REPEAT_MODE:
    subprocess.run(f"echo \"\nprove repeat({','.join(touch)},{{/12345678/:break}})\" >> {method_name}.siril", shell=True)
  else:
    subprocess.run(f"echo \"\nprove {','.join(touch)}\" >> {method_name}.siril", shell=True)
  
  completed = subprocess.run(f"gsiril < {method_name}.siril", shell=True, text=True, capture_output=True)
  num_changes = int(completed.stdout.split()[0])
  if "Touch is true" in completed.stdout:
    return (num_changes, True)
  if "Is this OK?" in completed.stdout:
    return (num_changes, "Incomplete")
  if "Touch not completed due to false row" in completed.stdout:
    return (num_changes, False)
  
  raise RuntimeError(f"Error: {completed.stdout}, {completed.stderr}")

method_name = "twinimus"
subprocess.run("mv output.txt prev_output.txt", shell=True)
lead_types = ["pl","hu","sn"]
LEAD_LENGTH = 8
REPEAT_MODE = True
CALLING_POSITIONS_MODE = True
# 1250/8 = 156.25, so 157 leads needed

if CALLING_POSITIONS_MODE:
  lead_types = ["hM","hW","hH","eW"]
else:
  lead_types = ["pl","hu","sn"]

find_touches([], lead_types, 1250)
