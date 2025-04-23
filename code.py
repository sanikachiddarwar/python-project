import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#Reading data from csv file
df = pd.read_csv("C:\\Users\\admin\\Desktop\\PYTHONNN\\dataset.csv")


# Clean column names
df.columns = df.columns.str.strip().str.replace("_", "  ").str.replace("(", "").str.replace(")", "").str.replace(",", "").str.replace("’", "").str.replace("'", "").str.replace(".", "")


#DataSet
print("Dataset Overview: ")
print(df)


#Basic EDA Prints
print("Basic EDA prints: ")
print(df.describe())
print(df.info())
print(df.head())
print(df.tail())
print(df.columns)
print(df.shape)
print(df.isnull().sum())
print(df.columns.tolist())






# List of relevant infrastructure columns
infra_columns = [
    'Electricity',
    'Drinking Water',
    'Library or Reading Corner or Book Bank',
    'Ramps',
    'Playground',
    'Computer Available'
]

# Calculate number of schools with each facility (assume >0 as available)
has_facility = (df[infra_columns] > 0).sum()
percent_facility = has_facility / len(df) * 100

# Create DataFrame
infra_df = pd.DataFrame({
    'Facility': infra_columns,
    'Percentage': percent_facility.values
}).sort_values(by='Percentage')

# Plot
sns.set_style("whitegrid")
plt.figure(figsize=(10, 6))
ax = sns.barplot(data=infra_df, x='Percentage', y='Facility')

# Add percentage labels using Pandas' formatted string
texts = infra_df['Percentage'].map(lambda x: f'{x:.1f}%')
[ax.text(x + 1, y, txt, va='center') for x, y, txt in zip(infra_df['Percentage'], range(len(infra_df)), texts)]

plt.title("Percentage of Schools with Infrastructure Facilities")
plt.xlabel("Percentage of Schools")
plt.ylabel("Facility")
plt.tight_layout()
plt.show()









# Ensure these are numeric (handle possible non-numeric or NaNs)
df[infra_columns] = df[infra_columns].apply(pd.to_numeric, errors='coerce')

# Group by School Management and calculate % availability
grouped = df.groupby('School Management')[infra_columns].apply(
    lambda x: (x > 0).sum() / x.shape[0] * 100
).reset_index()

# Melt for plotting
infra_melted = grouped.melt(id_vars='School Management', var_name='Facility', value_name='Percentage')

# Plot
plt.figure(figsize=(14, 7))
sns.set_style("whitegrid")
sns.barplot(data=infra_melted, x='Facility', y='Percentage', hue='School Management')

plt.title("Infrastructure Availability by School Management Type")
plt.xlabel("Infrastructure Facility")
plt.ylabel("Percentage of Schools with Facility")
plt.xticks(rotation=45)
plt.legend(title='Management Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()



















# Ensure numeric
df[infra_columns] = df[infra_columns].apply(pd.to_numeric, errors='coerce')

# Group by School Category
infra_by_category = df.groupby('School Category')[infra_columns].apply(
    lambda x: (x > 0).sum() / x.shape[0] * 100
).reset_index()

# Melt for Seaborn
infra_cat_melted = infra_by_category.melt(id_vars='School Category', 
                                          var_name='Facility', 
                                          value_name='Percentage')

# Plot
plt.figure(figsize=(14, 7))
sns.set_style("whitegrid")
sns.barplot(data=infra_cat_melted, 
            x='Facility', 
            y='Percentage', 
            hue='School Category')

plt.title("Infrastructure Availability by School Category")
plt.xlabel("Infrastructure Facility")
plt.ylabel("Percentage of Schools with Facility")
plt.xticks(rotation=45)
plt.legend(title='School Level', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()







# Ensure numeric types
df[infra_columns] = df[infra_columns].apply(pd.to_numeric, errors='coerce')

# Check for "Fully Equipped" schools — all facilities > 0
fully_equipped = (df[infra_columns] > 0).all(axis=1)

# Count the categories
coverage_counts = fully_equipped.value_counts().rename(index={True: 'Fully Equipped', False: 'Under-equipped'})

# Plot
plt.figure(figsize=(7, 5))
sns.set_style("whitegrid")
colors = ['#2ecc71', '#e74c3c']
plt.pie(coverage_counts, labels=coverage_counts.index, autopct='%1.1f%%', startangle=140, colors=colors)
plt.title('Distribution of School Facility Coverage')
plt.axis('equal')
plt.tight_layout()
plt.show()



management_map = {
    # Private
    "Private Unaided (Recognized)": "Private",
    "Unrecognized": "Private",
    "Madarsa recognized (by Wakf board/Madarsa Board)": "Private",
    "Madarsa unrecognized": "Private",
    
    # Government
    "Department of Education": "Government",
    "Government Aided": "Government",
    "Tribal Welfare Department": "Government",
    "Local body": "Government",
    "Social welfare Department": "Government",
    "Other Govt. managed schools": "Government",
    "Kendriya Vidyalaya / Central School": "Government",
    "Jawahar Navodaya Vidyalaya": "Government",
    "Other Central Govt. Schools": "Government",
    "Railway School": "Government",
    "Sainik School": "Government",
    "Ministry of Labor": "Government",
    "Central Tibetan School": "Government"
}
df["School_Type_Grouped"] = df["School Management"].map(management_map)
df["School_Type_Grouped"]
rural_infra = df.groupby("Rural/Urban")[[
    "Functional Drinking Water",
    "Functional Electricity",
    "Functional Toilet Facility",
    "Furniture",
    "Handwash",
    "Water Purifier"
]].sum().T
rural_infra.plot(kind="bar", color=["#f1d2cd", "#e15e5e"])
plt.title("Infrastructure Comparison: Rural vs Urban Schools")
plt.ylabel("Number of Schools with Facility")
plt.xlabel("Infrastructure Type")
plt.xticks(rotation=45)
plt.legend(title="Location")
plt.tight_layout()
plt.show()



















