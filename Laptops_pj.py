
# coding: utf-8

# In[266]:


import pandas as pd

laptops = pd.read_csv("laptops.csv",encoding = "Windows-1251")
laptops


# In[267]:


def clean_col(strr):
    strr = strr.strip()
    strr = strr.replace("Operating System","os")
    strr = strr.replace(" ","_")
    strr = strr.replace("(","")
    strr = strr.replace(")","")
    strr = strr.lower()
    return strr

laptops.columns = [clean_col(c) for c in laptops.columns]
laptops


# In[268]:


laptops["screen_size"] = laptops["screen_size"].str.replace('"','').astype(float)
laptops.rename({"screen_size": "screen_size_inches"}, axis=1, inplace=True)

laptops["ram"] = laptops["ram"].str.replace("GB","").astype(int)
laptops.rename({"ram":"ram_gb"}, axis=1, inplace=True)

dtypes = laptops.dtypes
print(dtypes)
laptops


# In[269]:


laptops["weight"] = (laptops["weight"]
                     .str.replace("kg","")
                     .str.replace("s","")
                    )
laptops["weight"] = laptops["weight"].astype(float)
laptops.rename({"weight":"weight_kg"}, axis = 1, inplace=True)
  
    
laptops["price_euros"] = (laptops["price_euros"]
                          .str.replace(",",".")
                          .astype(float)
                         )                       
weight_describe = laptops["weight_kg"].describe()
price_describe = laptops["price_euros"].describe()

print(price_describe)
laptops


# In[270]:


laptops["gpu_manufacturer"] = (laptops["gpu"]
                                    .str.split(n=1,expand=True)
                                    .iloc[:,0]
                               )

laptops["cpu_manufacturer"] = (laptops["cpu"]
                               .str.split(n=1, expand=True)
                               .iloc[:,0])

laptops


# In[271]:


screen_res = laptops["screen"].str.rsplit(n=1, expand=True)
screen_res.columns = ["A", "B"]
screen_res.loc[screen_res["B"].isnull(), "B"] = screen_res["A"]
laptops["screen_resolution"] = (screen_res["B"]
                                    .str.split(n=1,expand=True)
                                    .iloc[:,0]
                                    )

laptops["cpu_speed_ghz"] = (laptops["cpu"]
                            .str.replace("GHz","")
                            .str.rsplit(n=1,expand=True)
                            .iloc[:,1]
                            .astype(float)
                           )

laptops


# In[272]:


mapping_dict = {
    'Android': 'Android',
    'Chrome OS': 'Chrome OS',
    'Linux': 'Linux',
    'Mac OS': 'macOS',
    'No OS': 'No OS',
    'Windows': 'Windows',
    'macOS': 'macOS'
}

laptops["os"] = laptops["os"].map(mapping_dict)

laptops


# In[273]:


value_counts_before = laptops.loc[laptops["os_version"].isnull(), "os"].value_counts()

laptops.loc[laptops["os"] == "macOS", "os_version"] = "X"


laptops.loc[laptops["os"] == "No OS", "os_version"] = "Version Unknown"

value_counts_after = laptops.loc[laptops["os_version"].isnull(), "os"].value_counts()

print(value_counts_before)
print("\n")
print(value_counts_after)
print("\n")
laptops


# In[274]:


# replace 'TB' with 000 and rm 'GB'
laptops["storage"] = (laptops["storage"]
                      .str.replace('GB','')
                      .str.replace('TB','000')
                     )
laptops


# In[275]:


# split out into two columns for storage
laptops[["storage_1", "storage_2"]] = laptops["storage"].str.split("+", expand=True)
laptops


# In[276]:


for s in ["storage_1", "storage_2"]:
    s_capacity = s + "_capacity_gb"
    s_type = s + "_type"
        # create new cols for capacity and type
    laptops[[s_capacity, s_type]] = laptops[s].str.split(n=1,expand=True)
    # make capacity numeric (can't be int because of missing values)
laptops


# In[277]:


laptops[s_capacity] = laptops[s_capacity].astype(float)
# strip extra white space
laptops[s_type] = laptops[s_type].str.strip()

# remove unneeded columns
laptops.drop(["storage", "storage_1", "storage_2"], axis=1, inplace=True)
laptops


# In[278]:


laptops_dtypes = laptops.dtypes
cols = ['manufacturer', 'model_name', 'category', 'screen_size_inches',
        'screen', 'cpu', 'cpu_manufacturer',  'cpu_speed_ghz', 'ram_gb',
        'storage_1_type', 'storage_1_capacity_gb', 'storage_2_type',
        'storage_2_capacity_gb', 'gpu', 'gpu_manufacturer', 'os',
        'os_version', 'weight_kg', 'price_euros']

laptops = laptops[cols]
laptops.to_csv("laptops_cleaned.csv", index = False)

laptops_cleaned = pd.read_csv("laptops_cleaned.csv")
laptops_cleaned_dtypes = laptops_cleaned.dtypes


laptops_cleaned


# In[279]:


#Are laptops made by Apple more expensive than those by other manufacturers?

me_apple_laptop = laptops_cleaned.loc[laptops_cleaned["manufacturer"] == "Apple"].max()
me_apple_laptop_row_display = laptops_cleaned.loc[laptops_cleaned["price_euros"] == me_apple_laptop["price_euros"]]
gt_apple_laptops = laptops_cleaned.loc[laptops_cleaned["price_euros"] > me_apple_laptop["price_euros"]]
gt_apple_laptops_list = gt_apple_laptops["manufacturer"].value_counts()

print(me_apple_laptop_row_display[["manufacturer","model_name","price_euros"]])
print("\n")
print(gt_apple_laptops[["manufacturer","model_name","price_euros"]].sort_values("price_euros", ascending = False))
print("\n")
gt_apple_laptops_list


# In[280]:


#What is the best value laptop with a screen size of 15" or more?

laptops_15in_or_more = laptops_cleaned.loc[laptops_cleaned["screen_size_inches"] >= 15]
best_value_laptops = laptops_15in_or_more.sort_values("price_euros", ascending = True).head()
best_value_laptops


# In[281]:


#Which laptop has the most storage space?

most_storage_lt = (laptops_cleaned
                   .sort_values("storage_1_capacity_gb", ascending = False)
                   .sort_values("storage_2_capacity_gb", ascending = False)
                   .head())
most_storage_lt2 = most_storage_lt.sort_values("storage_1_capacity_gb", ascending = False)
most_storage_lt2

