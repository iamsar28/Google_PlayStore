#!/usr/bin/env python
# coding: utf-8

# # Market Analysis of Popular App Categories on the Google Play Store
# In this project, we want to find out which types of apps are popular on the Google Play Store. We work for a company that makes free apps and earns money from ads. By knowing which kinds of apps people like, we can help our developers create apps that more people will want to use, and that means more money for us. We'll look at the information from the Google Play Store to see what apps people like the most. This will help us decide what kinds of apps to make in the future.

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


android_df = pd.read_csv("googleplaystore.csv")


# In[3]:


android_df.head()


# In[4]:


android_df[android_df["Category"]=="1.9"]


# In[5]:


android_df[android_df["Category"]=="1.9"].values 


# In[ ]:


# claen_1st = ['Life Made WI-Fi Touchscreen Photo Frame','LIFESTYLE', '1.9', 19.0, '3.0M',
        '1,000+', 'Free', '0', 'Everyone', "LIFESTYLE" , 'February 11, 2018',
        '1.0.19', '4.0 and up']
claen_1st


# In[10]:


android_df[android_df["Category"]=="1.9"] = claen_1st


# In[12]:


android_Category= android_df["Category"].value_counts()
android_Category


# In[16]:


app_count = android_df["App"].value_counts()
app_count


# In[17]:


app_count[app_count > 1]


# In[18]:


"Instagram" in app_count[app_count >1].index


# In[19]:


android_df[android_df["App"]=="Instagram"]


# In[20]:


duplicate_apps_df = android_df[android_df.duplicated(subset = ["App"],keep = "first")]
duplicate_apps_df[duplicate_apps_df["App"]=="Instagram"]


# In[21]:


duplicate_apps_df = android_df[android_df.duplicated(subset = ["App"],keep = False)]
duplicate_apps_df[duplicate_apps_df["App"]=="Instagram"]


# In[22]:


num_duplicate_apps = duplicate_apps_df["App"].nunique()
num_duplicate_apps


# In[23]:


duplicate_apps_df.shape


# In[24]:


android_df.shape[0]


# In[27]:


10841-1181


# In[35]:


reviews_max = android_df.groupby("App")["Reviews"].max()


# In[36]:


reviews_max["Instagram"]


# In[37]:


duplicate_apps_df[duplicate_apps_df["App"]== "Instagram"]


# In[38]:


android_clean = []
already_added= []
for index, row in android_df.iterrows():
    name = row["App"]
    n_reviews = row["Reviews"]
    if (reviews_max[name]== n_reviews) and (name not in already_added):
        android_clean.append(row) # Add the app to the cleaned list
        already_added.append(name) # Add the app name to the list of already added apps


# In[39]:


len(android_clean)


# In[40]:


android_clean = pd.DataFrame(android_clean)


# In[41]:


android_clean


# # Removing Non English Apps
# NOTE: We'll not remove the apps which have 3 or less non-ASCII Characters

# In[45]:


def is_english(app_name):
    lst=[]
    for i in app_name:
        if ord(i) > 127:
            lst.append(False)
        else:
            lst.append(True)
    
    non_ascii = 0
    for j in lst:
        if j == False:
            non_ascii += 1
    
    if non_ascii > 3:
        return False
    else:
        return True


# In[46]:


is_english("Facebook😀😀😀😀")


# In[47]:


android_english = android_clean[android_clean["App"].apply(is_english)]
android_english


# # Filtering Free Apps
# Given that our company specializes in developing free apps monetized through advertisements, we will focus our analysis solely on data pertaining to free apps.

# In[48]:


android_english["Price"].unique()


# In[49]:


android_final = android_english[android_english["Price"] == "0"]


# In[50]:


android_final.shape


# # Visualization Phase
# Identifying Dominant App Genres

# In[51]:


android_final["Category"].value_counts(normalize=True)*100


# In[52]:


# Data
categories = android_final["Category"].value_counts().index[:15]
counts = android_final["Category"].value_counts().values[:15]
percentage = round(android_final["Category"].value_counts(normalize=True)*100, 1)[:15]

# create bar chart
plt.figure(figsize=(12,8))
bars = plt.bar(categories, counts, color="lightgray", alpha=0.75, edgecolor="black", linewidth= 1.5)
plt.xticks(rotation=90, fontsize=12)
plt.grid(axis="y", linestyle = "--", alpha = 0.7)
plt.grid(axis="x", linestyle = "")
plt.yticks(range(0, 3000, 500),[], fontsize=12) #customize tick labels and ranges
plt.tick_params(bottom=0, left=0, right=0)

#Find category with highest count
max_count_category = categories[counts.argmax()]

# Highlight the bar for the category with highest count
max_count_index = list(categories).index(max_count_category)
bars[max_count_index].set_color("Orange")
bars[max_count_index].set_edgecolor("black")

#Adding Data labels and percentage inside each bar
for bar, perc in zip(bars, percentage):
    height = bar.get_height()
    plt.text(bar.get_x() +bar.get_width()/2, height +20, "%d" % int(height), ha="center", va="bottom", fontsize=10)
    plt.text(bar.get_x() +bar.get_width()/2, height/2, f"{perc}%", ha="center", va="center", fontsize=10, color="black")

# Adding a background color
ax= plt.gca()
ax.set_facecolor("#f7f7f7")

# Adding chart title inside plot
plt.text(0.5,0.95, 'Top Android App Categories', horizontalalignment='center', fontsize=16, transform=plt.gca().transAxes,
         color= 'gray', fontweight='bold')

# Adding Conclusion in the chart
plt.text(0.5, 0.86, 'The "FAMILY" category stands out as the most prevalent among the top android app categories, \n showcasing a considerable demand for family-oriented applications',
         horizontalalignment="center", fontsize=14, transform=plt.gca().transAxes, color='gray' )

# Remove Spines
for i in ['top', "right", "left"]:
    plt.gca().spines[i].set_visible(False)
# ax.set_yticklabels([])
plt.tight_layout()

# plt.show()
plt.savefig("Top Android App Categories.png")


# In[53]:


android_final[android_final["Category"]=="FAMILY"]


# # Most Popular App by Installation on Google Play

# In[54]:


android_final["Installs"].value_counts(normalize=True)*100


# In[55]:


android_final["Installs_int"] = android_final["Installs"].str.replace(",","").str.replace("+","").astype(int)


# In[56]:


install_frq = android_final["Installs_int"].value_counts().sort_index()
install_frq =install_frq[install_frq.index > 500] 
install_frq


# In[57]:


install_frq_1 = round(android_final["Installs_int"].value_counts(normalize=True)*100, 2).sort_index()
install_frq_1 =install_frq_1[install_frq_1.index > 500] 
install_frq_1


# In[58]:


# alphanumeric units
def alphanumeric_units(value):
    if value>= 1e9:
        return f'{value / 1e9:.0f}B'
    elif value>= 1e6:
        return f'{value / 1e6:.0f}M'
    elif value>= 1e3:
        return f'{value / 1e3:.0f}K'
    else:
        return f'{value:.0f}'


# In[59]:


alphanumeric_units(100000000)


# In[60]:


install_frq.index


# In[61]:


install_frq.index = install_frq.index.map(alphanumeric_units)
install_frq


# In[62]:


# Data
categories = install_frq.index
counts = install_frq.values
percentage = install_frq_1.values

# create bar chart
plt.figure(figsize=(12,8))
bars = plt.bar(categories, counts, color="lightgray", alpha=0.75, edgecolor="black", linewidth= 1.5)
plt.xticks(rotation=90, fontsize=12)
plt.grid(axis="y", linestyle = "--", alpha = 0.7)
plt.grid(axis="x", linestyle = "")
plt.yticks(range(0, 2500, 500),[], fontsize=12) #customize tick labels and ranges
plt.tick_params(bottom=0, left=0, right=0)

#Find category with highest count
max_count_category = categories[counts.argmax()]

# Highlight the bar for the category with highest count
max_count_index = list(categories).index(max_count_category)
bars[max_count_index].set_color("Orange")
bars[max_count_index].set_edgecolor("black")

#Adding Data labels and percentage inside each bar
for bar, perc in zip(bars, percentage):
    height = bar.get_height()
    plt.text(bar.get_x() +bar.get_width()/2, height +20, "%d" % int(height), ha="center", va="bottom", fontsize=10)
    plt.text(bar.get_x() +bar.get_width()/2, height/2, f"{perc}%", ha="center", va="center", fontsize=10, color="black")

# Adding a background color
ax= plt.gca()
ax.set_facecolor("#f7f7f7")

# Adding chart title inside plot
plt.text(0.5,0.94, 'Distribution of Android Apps Installations', horizontalalignment='center', fontsize=16, transform=plt.gca().transAxes,
         color= 'gray', fontweight='bold')

# Adding Conclusion in the chart
plt.text(0.5, -0.25, '''From the data provided, it's evident that the majority of Android Apps falls within the lower range, \n with the highest number of installations being in 1k to 10M range, \n Specifically, the 1M install range stands out with 1395 apps, indicating a significant number of apps falling in this category. \n As the number of installations increase, the count of apps decreases, \n with only a few apps reaching the installations count of 500M and 1B''',
         horizontalalignment="center", fontsize=11, transform=plt.gca().transAxes, color='gray' )

# Remove Spines
for i in ['top', "right", "left"]:
    plt.gca().spines[i].set_visible(False)
# ax.set_yticklabels([])
plt.tight_layout()

# plt.show()
plt.savefig("Distribution of Android Apps Installations.png")


# In[63]:


categories_android = android_final["Category"].unique()
categories_android


# In[64]:


pd.pivot_table(android_final, values="Installs_int", index="Category", aggfunc="mean")


# In[65]:


# Display Dataframe without scientific notation
pd.options.display.float_format = '{:.0f}'.format


# In[66]:


category_installs = pd.pivot_table(android_final, values="Installs_int", index="Category", aggfunc="mean")
category_installs = category_installs.sort_values(by="Installs_int", ascending=False)
category_installs = category_installs["Installs_int"]
category_installs


# In[67]:


# alphanumeric units
def alphanumeric_units_1(value):
    if value>= 1e9:
        return f'{value / 1e9:.1f}B'
    elif value>= 1e6:
        return f'{value / 1e6:.1f}M'
    elif value>= 1e3:
        return f'{value / 1e3:.1f}K'
    else:
        return f'{value:.1f}'


# In[68]:


category_installs_unit = category_installs.map(alphanumeric_units_1)
category_installs_unit


# In[69]:


# Data
categories = category_installs.index[:15]
counts = category_installs.values[:15]

# create bar chart
plt.figure(figsize=(12,7))
bars = plt.bar(categories, counts, color="lightgray", alpha=0.75, edgecolor="black", linewidth= 1.5)
plt.xticks(rotation=90, fontsize=12)
plt.grid(axis="y", linestyle = "--", alpha = 0.7)
plt.grid(axis="x", linestyle = "")
plt.yticks(range(0, 60000000, 10000000),[], fontsize=12) #customize tick labels and ranges
plt.tick_params(bottom=0, left=0, right=0)

#Find category with highest count
max_count_category = categories[counts.argmax()]

# Highlight the bar for the category with highest count
max_count_index = list(categories).index(max_count_category)
bars[max_count_index].set_color("Orange")
bars[max_count_index].set_edgecolor("black")

#Adding Data labels and percentage inside each bar
for bar, units in zip(bars, category_installs_unit.values):
    height = bar.get_height()
    plt.text(bar.get_x() +bar.get_width()/2, height +25, units, ha="center", va="bottom", fontsize=10)
    
# Adding a background color
ax= plt.gca()
ax.set_facecolor("#f7f7f7")

# Adding chart title inside plot
plt.text(0.5,0.94, 'Average Distribution of Android Apps Installations by Category', horizontalalignment='center', fontsize=16, transform=plt.gca().transAxes,
         color= 'gray', fontweight='bold')

# Adding Conclusion in the chart
plt.text(0.5, 0.77, '''Communication apps lead the pack with an stagering 38.5 million installations, \n followed closely by Video Player at 24.7 million and Social apps at 23.3 million. \n These categories demonstrate significant popularity among Android users, \n showcasing the prominence of communications and media consumptions in the mobile app landscape.''',
         horizontalalignment="center", fontsize=11, transform=plt.gca().transAxes, color='gray' )

# Remove Spines
for i in ['top', "right", "left"]:
    plt.gca().spines[i].set_visible(False)
# ax.set_yticklabels([])
plt.tight_layout()

# plt.show()
plt.savefig("Average Distribution of Android Apps Installations by Category.png")


# In[70]:


category_group = android_final.groupby("Category")


# In[71]:


COMMUNICATION = category_group.get_group("COMMUNICATION").sort_values(by="Installs_int", ascending=False)
COMMUNICATION


# In[72]:


category_installs.index[:15]


# In[73]:


df= COMMUNICATION[["App","Installs_int"]].head(15)
df["Installs_int_unit"]= df["Installs_int"].map(alphanumeric_units)
df


# In[74]:


df = category_group.get_group("VIDEO_PLAYERS").sort_values(by="Installs_int", ascending=False)
df= df[["App","Installs_int"]].head(15)
df["Installs_int_unit"]= df["Installs_int"].map(alphanumeric_units)
df


# In[75]:


df = category_group.get_group("SOCIAL").sort_values(by="Installs_int", ascending=False)
df= df[["App","Installs_int"]].head(15)
df["Installs_int_unit"]= df["Installs_int"].map(alphanumeric_units)
df


# In[76]:


df = category_group.get_group("PHOTOGRAPHY").sort_values(by="Installs_int", ascending=False)
df= df[["App","Installs_int"]].head(15)
df["Installs_int_unit"]= df["Installs_int"].map(alphanumeric_units)
df


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




