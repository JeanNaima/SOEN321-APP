import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

RESULTS_CSV = "video_link_results.csv"

# Basic load + cleanup
if not os.path.exists(RESULTS_CSV):
    raise FileNotFoundError(f"{RESULTS_CSV} not found. Run search_and_analyse.py first.")

df = pd.read_csv(RESULTS_CSV)
df["CONTENT"] = df["CONTENT"].astype(str).fillna("")
df["HAS_LINK"] = df["HAS_LINK"].astype(bool)
df["LINK_CATEGORY"] = df["LINK_CATEGORY"].fillna("no_link")
df["subject"] = df["subject"].fillna("unknown")
df["video_url"] = df["video_url"].fillna("unknown")

df.drop_duplicates(inplace=True)

sns.set_theme(style="whitegrid")

#Overall link vs no-link distribution
plt.figure(figsize=(6, 4))
link_counts = df["HAS_LINK"].value_counts()
sns.barplot(x=link_counts.index.map({True: "Has Link", False: "No Link"}), y=link_counts.values, palette="Set2")
plt.title("Comments With vs Without Links")
plt.xlabel("")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

#Link categories (only comments with links)
link_df = df[df["HAS_LINK"]]
if not link_df.empty:
    plt.figure(figsize=(8, 5))
    cat_counts = link_df["LINK_CATEGORY"].value_counts()
    sns.barplot(y=cat_counts.index, x=cat_counts.values, palette="viridis")
    plt.title("Link Category Counts")
    plt.xlabel("Count")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.show()

    #Top domains
    top_domains = link_df["LINK_DOMAIN"].fillna("").replace("", "unknown").value_counts().head(15)
    plt.figure(figsize=(8, 5))
    sns.barplot(y=top_domains.index, x=top_domains.values, palette="magma")
    plt.title("Top 15 Link Domains")
    plt.xlabel("Count")
    plt.ylabel("Domain")
    plt.tight_layout()
    plt.show()

    #Links per subject by category (stacked)
    subject_cat = (
        link_df.groupby(["subject", "LINK_CATEGORY"])
        .size()
        .unstack(fill_value=0)
        .sort_index()
    )
    if not subject_cat.empty:
        subject_cat.plot(kind="bar", stacked=True, figsize=(10, 6), colormap="tab20")
        plt.title("Link Categories by Subject")
        plt.xlabel("Subject")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.xticks(rotation=45, ha="right")
        plt.show()

    #Links per video
    video_counts = link_df.groupby("video_url").size().sort_values(ascending=False).head(20)
    plt.figure(figsize=(10, 6))
    sns.barplot(y=video_counts.index, x=video_counts.values, palette="coolwarm")
    plt.title("Top 20 Videos by Link Volume")
    plt.xlabel("Count")
    plt.ylabel("Video URL")
    plt.tight_layout()
    plt.show()