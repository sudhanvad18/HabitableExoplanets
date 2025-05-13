#imports
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px 
import umap.plot
import umap.umap_ as umap

#import dataset (NASA data from April 2023)
#df = pd.read_csv("April_Dataset.csv", skiprows=range(296), low_memory=False)
df = pd.read_csv("July_Dataset.csv", skiprows=range(294), low_memory=False)

# Remove all observations with a controversial flag of 1
df = df.loc[df['pl_controv_flag'] != 1]
df.reset_index(drop=True, inplace=True)
df = df.append({'pl_name':"Earth",'st_lum':1.000, 'st_rad':1.000, 'st_teff':5778, 'pl_orbper':365.25, 'pl_orbsmax':1.0, 'pl_orbeccen':0.025, 'pl_cmasse':1.5}, ignore_index=True)


#features of planets to focus on
features = ["st_lum", "st_rad", "st_teff", "pl_orbper", "pl_orbsmax", "pl_orbeccen","pl_cmasse"]

#dataset with only the selected features
X = df[features]
#drop na values 
X.dropna(inplace=True)

# Drop corresponding rows from df
df = df.loc[X.index]
df = df.reset_index(drop=True)

#use the sklearn to normalize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print(X_scaled)

# Perform K-means clustering
k = 5  # Number of clusters
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(X_scaled)

# Assign cluster labels to the data
df['cluster_label'] = kmeans.labels_

# Explore the clusters
cluster_counts = df['cluster_label'].value_counts()
print("\n\n", cluster_counts, "\n\n")

# Evaluate and analyze the clusters
cluster_stats = df.groupby('cluster_label')[features].mean()
print(cluster_stats, "\n")

#generate a space to visualize the clusters using UMAP
umap_model = umap.UMAP(n_components=3, n_neighbors=15, min_dist=0.3)
#umap_model = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.1)
umap_embeddings = umap_model.fit_transform(X_scaled)

umap_df = pd.DataFrame(data=umap_embeddings, columns=["UMAP1", "UMAP2", "UMAP3"])
umap_df['cluster_label'] = kmeans.labels_
umap_df['Planet'] = df['pl_name']

umap_df.to_csv('Cluster_Data.csv')

def show_past_exoplanets():
    planets = [
        "HD 210277 b", "HD 222582 b", "HD 10697 b", "HD 141937 b", "HD 147513 b",
        "HD 142415 b", "HD 183263 b", "HD 159868 b", "HD 100777 b", "HD 132406 b",
        "HD 16175 b", "HD 73534 b", "BD+14 4559 b", "HD 181720 b", "GJ 876 e",
        "HD 34445 b", "HD 10180 g", "Kepler-16 b", "HD 63765 b", "HD 137388 b",
        "HD 163607 c", "HD 219415 b", "BD-06 1339 c", "Kepler-68 d", "Kepler-309 c",
        "HD 13908 c", "HD 141399 d", "Kapteyn c", "HD 10442 b", "GJ 3293 c",
        "HD 564 b", "HD 1605 c", "WASP-47 c", "KELT-6 c", "WASP-41 c", "KIC 9663113 b",
        "Kepler-454 c", "Kepler-1086 c", "Kepler-553 c", "Kepler-1600 b", "Kepler-1593 b",
        "HD 221585 b", "HD 214823 b", "Kepler-1647 b", "HD 9174 b", "HD 165155 b",
        "HD 128356 b", "HD 17674 b", "GJ 3323 c", "HD 18015 b", "Kepler-1649 c",
        "HD 27969 b", "HD 109286 b", "Kepler-1868 b", "KIC 3526061 b", "TOI-1288 c",
        "Kepler-1649c", "Kepler-174d", "Kepler-62f", "Earth"
    ]

    for i in range(len(planets)):
        planet_info = df.loc[df["pl_name"] == planets[i]]

        if not planet_info.empty:
            print("Planet: ", planets[i], "\n", planet_info)

show_past_exoplanets()


# Plot the 3D UMAP with a legend
fig = px.scatter_3d(
    umap_df,
    x="UMAP1",
    y="UMAP2",
    z="UMAP3",
    color=df["cluster_label"],
    hover_name = "Planet",
    opacity=0.8,
    title="3D UMAP with Cluster Labels",
    labels={"Cluster": "Cluster Label"},
    #color_continuous_scale=px.colors.qualitative.Light24,  # Color scale for the clusters
)

fig.show()
