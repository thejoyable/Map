import pandas as pd

# Load your CSV
df = pd.read_csv("test_data.csv")  # change path if needed

# Change this to your label column name
label_col = "label"

# Count values
counts = df[label_col].value_counts()
print("Original counts:\n", counts)

# Separate classes
df_0 = df[df[label_col] == 0]
df_1 = df[df[label_col] == 1]

# Downsample logic
if len(df_0) < len(df_1):
    df_1_downsampled = df_1.sample(n=len(df_0), random_state=42)
    df_balanced = pd.concat([df_0, df_1_downsampled])
elif len(df_1) < len(df_0):
    df_0_downsampled = df_0.sample(n=len(df_1), random_state=42)
    df_balanced = pd.concat([df_0_downsampled, df_1])
else:
    df_balanced = df  # already balanced

# Shuffle final dataset
df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

# Check new counts
print("Balanced counts:\n", df_balanced[label_col].value_counts())

# Save if needed
df_balanced.to_csv("balanced_data.csv", index=False)