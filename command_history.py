#!/usr/bin/env python3
# coding: utf-8
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2023 Federico Motta    <federico.motta@unimore.it>
#                    Lorenzo  Carletti <lorenzo.carletti@unimore.it>
#                    Matteo   Vanzini  <matteo.vanzini@unimore.it>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
Build a dendrogram by running UPGMA over some language parameters

UPGMA (Unweighted Pair Group Method with Arithmetic mean) is a
simple agglomerative (bottom-up) hierarchical clustering method

Usage:
         coming soon...
"""
import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering


def plot_dendrogram(model, **kwargs):
    """Create linkage matrix and then plot the dendrogram"""

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)


base_folder = "datasets/"
base_file = "preprocessed_inputs_04.xlsx"


dfs = pd.read_excel(base_folder + base_file, sheet_name=None)
dfs.keys()
dfs["boolean_matrix"]
dfs["boolean_matrix"].set_index("parameter").astype(int)
df_bool = dfs["boolean_matrix"].set_index("parameter").astype(int)

AgglomerativeClustering(2, linkage="average", metric="euclidean")
AgglomerativeClustering(2, linkage="average", metric="euclidean").fit(df_bool)
clst = AgglomerativeClustering(2, linkage="average", metric="euclidean")
clst.fit(df_bool)
model = AgglomerativeClustering(2, linkage="average", metric="euclidean")

model = AgglomerativeClustering(
    linkage="average",
    metric="euclidean",
    distance_threshold=0,
    n_clusters=None,
)
model.fit(df_bool.transpose())
plt.clf()
plt.cla()
plt.title("Hierarchical Clustering Dendrogram\n(UPGMA method)")
labels = list(df_bool.columns)
plot_dendrogram(model, labels=labels)
plt.xlabel("32 dialetti, from 'Guardiano_et_al_TableA_2023_Apr3'")
plt.savefig("./plot.svg", dpi=1200)

print(df_bool.to_string())
dfs.keys()
dfs["without_nan"].loc[:, ["FS", "Nic"]]
tmp_df = dfs["without_nan"].loc[:, ["FS", "Nic"]]
tmp_df.loc[~tmp_df["FS"].eq(tmp_df["Nic"]), :]
tmp_df["FS"].eq(tmp_df["Nic"]).all()
df_bool
df_bool.transpose()
df_bool.transpose().sum(axis=0)
df_bool.transpose().sum(axis=0).isin(range(1, 31))
max(range(1, 31))
df_bool

dfs = pd.read_excel(base_folder + base_file, sheet_name=None)
df = dfs["no_all_zero_rules_imputed_PGE_W"]
df
df.astype(str).eq("?").sum().sum()

dfs = pd.read_excel(base_folder + base_file, sheet_name=None)
df.astype(str).eq("?").sum().sum()
dfs = pd.read_excel(base_folder + base_file, sheet_name=None)
df.astype(str).eq("?").sum().sum()
df = dfs["no_all_zero_rules_imputed_PGE_W"]
df.astype(str).eq("?").sum().sum()
df.astype(str).eq("0").sum().sum()

df_t = df.transpose()
df_t
df_t.astype(str).eq("0").sum(axis=0)
df_t.astype(str).eq("0").sum(axis=1)
df_t
df_t
df_t.iloc[0, :]
df_t.iloc[0, :].to_list()
df_t.columns = df_t.iloc[0, :].to_list()
df_t
df_t.iloc[0, :]
df_t.iloc[list(range(1, 33)), :]
df_t = df_t.iloc[list(range(1, 33)), :]
df_t.astype(str).eq("0").sum(axis=0)
df_t.astype(str).eq("0").sum(axis=0).eq(0)
selector = [
    param
    for param, flag in df_t.astype(str)
    .eq("0")
    .sum(axis=0)
    .eq(0)
    .to_dict()
    .items()
    if flag
]
selector
len(selector)
df_t
df_t.loc[:, selector]
df_t.loc[:, selector].replace({"+": True, "-": False}).astype("boolean")
df_bool_imputed = (
    df_t.loc[:, selector].replace({"+": True, "-": False}).astype("boolean")
)

df_clust = df_bool_imputed.astype(int)
model = AgglomerativeClustering(
    linkage="average",
    metric="euclidean",
    distance_threshold=0,
    n_clusters=None,
)
model.fit(df_clust.transpose())
model = AgglomerativeClustering(
    linkage="average",
    metric="euclidean",
    distance_threshold=0,
    n_clusters=None,
)
model.fit(df_bool.transpose())
plt.clf()
plt.cla()
plt.title("Hierarchical Clustering Dendrogram\n(UPGMA method)")


plot_dendrogram(model, labels=list(df_bool.columns))
plt.xlabel("31 dialetti, from 'Guardiano_et_al_TableA_2023_Apr3'")

plt.savefig("./plot.svg", dpi=1200)
model = AgglomerativeClustering(
    linkage="average",
    metric="euclidean",
    distance_threshold=0,
    n_clusters=None,
)
model.fit(df_clust.transpose())
df_clust
plt.clf()
plt.cla()
plt.title("Hierarchical Clustering Dendrogram\n(UPGMA method)")

plot_dendrogram(model, labels=list(df_clust.columns))
plt.xlabel(
    "32 dialetti, from 'Guardiano_et_al_TableA_2023_Apr3' imputed\n(PGE=-, WAP=++-, GFL=-, PGL=+)"
)
plt.savefig("./plot2.svg", dpi=1200)
model.fit(df_clust)
plt.clf()
plt.cla()
plt.title("Hierarchical Clustering Dendrogram\n(UPGMA method)")

plot_dendrogram(model, labels=list(df_clust.transpose().columns))
plt.xlabel(
    "32 dialetti, from 'Guardiano_et_al_TableA_2023_Apr3' imputed\n(PGE=-, WAP=++-, GFL=-, PGL=+)"
)
plt.savefig("./plot2.svg", dpi=1200)
plt.clf()
plt.cla()
plt.title("Hierarchical Clustering Dendrogram\n(UPGMA method)")


plot_dendrogram(model, labels=list(df_clust.transpose().columns))
plt.xlabel(
    "32 dialetti, from 'Guardiano_et_al_TableA_2023_Apr3' imputed\n(PGE=-, WAP=++-, GFL=-, PGL=+)"
)
plt.savefig("./plot2.svg", dpi=1200)
plt.clf()
plt.cla()
plt.title("Hierarchical Clustering Dendrogram\n(UPGMA method)")


plot_dendrogram(model, labels=list(df_clust.transpose().columns))
plt.xlabel(
    "32 dialetti, from 'Guardiano_et_al_TableA_2023_Apr3' imputed (PGE=-, WAP=++-, GFL=-, PGL=+)"
)
plt.savefig("./plot2.svg", dpi=1200)
plt.clf()
plt.cla()
plt.title("Hierarchical Clustering Dendrogram\n(UPGMA method)")


plot_dendrogram(model, labels=list(df_clust.transpose().columns))
plt.xlabel(
    "32 dialetti, from 'TableA 2023', imputed (PGE=-, WAP=++-, GFL=-, PGL=+)"
)
plt.savefig("./plot2.svg", dpi=1200)
