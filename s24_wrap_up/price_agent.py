"""Price an agent service from real running costs. Costs below were measured in this course; the rates are sample numbers."""
RUN_COST = 0.30            # dollars per night: the Shop Ops night shift in project 9 cost 0.23 to 0.40
RUNS_PER_MONTH = 30
SAFETY = 3                 # bad nights, retries and growth: plan for three times the normal cost
SETUP_HOURS = 12           # build, test and hand over
HOURLY = 60                # your rate, sample
SUPPORT_HOURS = 1          # checking logs and small fixes each month
HOURS_SAVED = 20           # Sara's evening hour, about 20 working days a month

model_cost = RUN_COST * RUNS_PER_MONTH
budget = model_cost * SAFETY
monthly = budget + SUPPORT_HOURS * HOURLY
print(f"model cost per month:   ${model_cost:7.2f}   (budget with safety: ${budget:.2f})")
print(f"support per month:      ${SUPPORT_HOURS * HOURLY:7.2f}")
print(f"your cost per month:    ${monthly:7.2f}")
print(f"setup fee:              ${SETUP_HOURS * HOURLY:7.2f}")
print(f"suggested monthly fee:  ${round(monthly * 2, -1):7.2f}   (twice your cost)")
print(f"client saves:           {HOURS_SAVED} hours a month")
