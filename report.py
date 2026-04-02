# BH AI Analyst Project
# Aaliyah Orloff
# Automated Property Performance Report using AI

import openai
import pandas as pd

# ── Configuration ──────────────────────────────────────────
API_KEY = "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"
client = openai.OpenAI(api_key=API_KEY)

# ── Step 1: Extract and Transform Data ─────────────────────
print("Loading property data...")
df = pd.read_csv("data.csv")

# Clean the data
df["occupancy_rate"] = pd.to_numeric(df["occupancy_rate"], errors="coerce")
df["delinquency_rate"] = pd.to_numeric(df["delinquency_rate"], errors="coerce")
df = df.dropna()

print(f"Loaded {len(df)} properties successfully.")
print(df.to_string(index=False))
print()

# ── Step 2: Format Data for AI ─────────────────────────────
data_text = df.to_string(index=False)

# ── Step 3: Build the Prompt Framework ─────────────────────
# Role, Context, Task, Format, Constraints
system_prompt = """
You are a senior property management analyst at a multifamily 
real estate company. You specialize in summarizing operational 
performance data clearly for executive audiences.
"""

user_prompt = f"""
Below is this week's performance data for our apartment portfolio.

{data_text}

Columns:
- occupancy_rate: percentage of units currently occupied
- new_leases: number of new leases signed this month
- maintenance_tickets: number of open maintenance requests
- delinquency_rate: percentage of residents behind on rent

Your task is to summarize this data into a brief executive report.

Format your response in exactly three sections:
1. HIGHLIGHTS - what is performing well (3 bullet points max)
2. CONCERNS - what needs immediate attention (3 bullet points max)
3. TRENDS TO WATCH - patterns worth monitoring (3 bullet points max)

Use plain business language. No technical jargon.
Do not make up data. Only reference what is in the table above.
If something is unclear, flag it rather than assume.
"""

# ── Step 4: Send to AI and Get Response ────────────────────
print("Sending data to AI for analysis...")
print()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.2
)

# ── Step 5: Display and Save Output ────────────────────────
report = response.choices[0].message.content

print("=" * 60)
print("WEEKLY PROPERTY PERFORMANCE REPORT")
print("=" * 60)
print(report)
print("=" * 60)

# Save to file
with open("report_output.txt", "w") as f:
    f.write("WEEKLY PROPERTY PERFORMANCE REPORT\n")
    f.write("=" * 60 + "\n")
    f.write(report)

print()
print("Report saved to report_output.txt")