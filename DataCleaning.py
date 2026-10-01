import pandas as pd
import csv


entry_columns = [
    "EntryID", # None-nullable, No missing values
    "PostedBy", # None-nullable, No missing values
    "SourceName", #Nullable, May be missing
    "SourceURL", #Nullable, May be missing
    "GeoX", #Nullable, Almost entirely missing
    "GeoY", #Nullable, Almost entirely missing
    "Timestamp", #Nullable, A few missing values
    "Text", #Nullable, A few missing values
    "Numlmg", #Nullable, A few missing values
    "ImgURL", #Nullable, Mostly missing
    "NumVideo", #Nullable, A few missing values
    "VideoURL" #Nullable, Mostly missing
]

comment_columns = [
    "CommentID",
    "EntryID",
    "PostedBy",
    "SourceName",
    "SourceURL",
    "GeoX",
    "GeoY",
    "Timestamp",
    "Text",
    #"NumImg",
    #"ImgURL",
    #"NumImg",
    #"ImgURL"
]

likes_columns = [
    "UserID",
    "EntryID",
    "Timestamp"
]


users_columns = [
    "ID",
    "Type",
    "Name",
    "Reserved field",
    "Description"
]

following_columns = [
    "FollowedID",
    "FollowerID",
    "Timestamp" #This field is not mentioned in the readme.
]

services_columns = [
    "UserID",
    "ServiceID",
    "ServiceName",
    "ServiceURL",
    "UserNameOnService",
    "UserURLOnService"
] 

keys = {
   "Entries" : ["EntryID"],
   "Comments": ["PostID"],
   "Likes": ["userID", "PostID"],
   "Users": ["ID"],
   "Following": ["FollowedID", "FollowerID"],
   "Services": ["UserID", "ServiceID"]
}

entries1 = pd.read_csv(
    "entries1.csv",
    sep="\t",
    header=None,
    na_values=r"\N"
)

entries2 = pd.read_csv(
    "entries2.csv",
    sep="\t",
    header=None,
    na_values=r"\N"
)

entries3 = pd.read_csv(
    "entries3.csv",
    sep="\t",
    header=None,
    na_values=r"\N"
)

entries = pd.concat(
    [entries1, entries2, entries3],
    ignore_index=True
)
entries.columns = entry_columns
entries.drop(columns=["GeoX", "GeoY", "Timestamp"], inplace=True)

comments = pd.read_csv(
    "commentAugSept.csv",
    sep="\t",
    header=None,
    na_values=r"\N"
)
comments.columns = comment_columns
comments.drop(columns=["GeoX", "GeoY", "Timestamp"], inplace=True)


likes = pd.read_csv(
    "likes.csv",
    sep="\t",
    header=None,
    na_values=r"\N"
)
likes.columns = likes_columns
likes.drop(columns=["Timestamp"], inplace=True)

users = pd.read_csv(
    "users.csv",
    sep="|",
    header=None,
    na_values="null",
    quoting=csv.QUOTE_NONE
)
users.columns = users_columns
users.drop(columns=["Reserved field", "Description"], inplace=True)

following = pd.read_csv(
    "followingAugSept.csv",
    sep="\t",
    header=None,
    na_values=r"\N"
)
following.columns = following_columns
following.drop(columns=["Timestamp"], inplace=True)


#services = pd.read_csv(
#    "services.csv",
#    sep="|",
#    header=None,
#    na_values="null"
#)
#services.columns = services_columns

#subscriptions = pd.read_csv(
#    "subscriptions.csv",
#    sep="\t",
#    header=None,
#    na_values=r"\N"
#)

#datasets = {
#    "Entries" : entries,
#    "Comments" : comments,
#    "Likes" : likes,
#    "Users" : users,
#    "Following" : following,
    #"Services" : services
    #"Subscriptions" : subscriptions
#}



# Remove entries referencing nonexistent users
#before = len(entries)

#entries = entries[
#    entries["PostedBy"].isin(users["ID"])
#].copy()

#print(f"Removed entries: {before - len(entries):,}")
#print(f"Remaining entries: {len(entries):,}")

# Save cleaned entries
#entries.to_csv(
#    "entries_cleaned.csv",
#    sep="\t",
#    header=False,
#    index=False,
#    na_rep=r"\N"
#)


# Remove comments with invalid references
#before = len(comments)

#comments = comments[
#    comments["EntryID"].isin(entries["EntryID"]) &
#    comments["PostedBy"].isin(users["ID"])
#].copy()

#print(f"Removed comments: {before - len(comments):,}")
#print(f"Remaining comments: {len(comments):,}")

# Save cleaned comments
#comments.to_csv(
#    "comments_cleaned.csv",
#    sep="\t",
#    header=False,
#    index=False,
#    na_rep=r"\N"
#)



# Remove likes with invalid references
#before = len(likes)

#likes = likes[
#    likes["EntryID"].isin(entries["EntryID"]) &
#    likes["UserID"].isin(users["ID"])
#].copy()

#print(f"Removed invalid likes: {before - len(likes):,}")

# Remove duplicate composite keys
#before = len(likes)

#likes = likes.drop_duplicates(
#    subset=["UserID", "EntryID"],
#    keep="first"
#).copy()

#print(f"Removed duplicate likes: {before - len(likes):,}")
#print(f"Remaining likes: {len(likes):,}")

# Save cleaned likes
#likes.to_csv(
#    "likes_cleaned.csv",
#    sep="\t",
#    header=False,
#    index=False,
#    na_rep=r"\N"
#)



# Remove users with duplicate primary keys
#before = len(users)

#users = users.drop_duplicates(
#    subset=["ID"],
#    keep="first"
#).copy()

#print(f"Removed duplicate users: {before - len(users):,}")
#print(f"Remaining users: {len(users):,}")

# Save cleaned users
#users.to_csv(
#    "users_cleaned.csv",
#    sep="|",
#    header=False,
#    index=False,
#    na_rep="null"
#)


# Remove following relationships with invalid user references
before = len(following)

following = following[
    following["FollowedID"].isin(users["ID"]) &
    following["FollowerID"].isin(users["ID"])
].copy()

print(f"Removed following relationships: {before - len(following):,}")
print(f"Remaining relationships: {len(following):,}")

# Save cleaned following dataset
following.to_csv(
    "following_cleaned.csv",
    sep="\t",
    header=False,
    index=False,
    na_rep=r"\N"
)


# Check which entries reference an existing user
#valid_users = entries["PostedBy"].isin(users["ID"])
# Count entries referencing nonexistent users
#print("Invalid users:", (~valid_users).sum())
# Display entries with invalid users
#print(entries[~valid_users])

# Check whether each comment references an existing entry
#valid_entries = comments["EntryID"].isin(entries["EntryID"])
# Count comments referencing nonexistent entries
#print("Invalid entries:", (~valid_entries).sum())
# Display comments referencing nonexistent entries
#print(comments[~valid_entries])


# Check whether each comment was posted by an existing user
#valid_users = comments["PostedBy"].isin(users["ID"])
# Count comments referencing nonexistent users
#print("Invalid users:", (~valid_users).sum())
# Display comments referencing nonexistent users
#print(comments[~valid_users])


# Check whether each like references an existing user
#valid_users = likes["userID"].isin(users["ID"])
# Count likes referencing nonexistent users
#print("Invalid users:", (~valid_users).sum())
# Display likes referencing nonexistent users
#print(likes[~valid_users])


# Check whether each like references an existing entry
#valid_entries = likes["PostID"].isin(entries["EntryID"])
# Count likes referencing nonexistent entries
#print("Invalid entries:", (~valid_entries).sum())
# Display likes referencing nonexistent entries
#print(likes[~valid_entries])


# Check whether FollowedID references an existing user
#valid_followed = following["FollowedID"].isin(users["ID"])
# Check whether FollowerID references an existing user
#valid_followers = following["FollowerID"].isin(users["ID"])
# Count invalid references
#print("Invalid followed users:", (~valid_followed).sum())
#print("Invalid followers:", (~valid_followers).sum())
# Display rows with at least one invalid user
#print(following[~(valid_followed & valid_followers)])


#for name, df in datasets.items():
#    print(f"\n{'=' * 40}")
#    print(f"  {name}")
#    print(f"{'=' * 40}")

#    print(f"\nShape:")
#    print(f"  Rows:    {df.shape[0]:,}")
#    print(f"  Columns: {df.shape[1]}")

#    print("\nMissing values:")
#    print(df.isna().sum().to_string())

#    print(f"\nDuplicate rows:")
#    print(f"  {df.duplicated().sum():,}")

#    if name in keys:
#        print("\nDuplicate keys:")
#        print(f"  {df.duplicated(subset=keys[name]).sum():,}")

#    print("\nData types:")
#    print(df.dtypes.to_string())


#bad_rows = []

#with open("services.csv", "r", encoding="utf-8") as f:
#    for line_number, line in enumerate(f, start=1):
#        fields = line.rstrip("\r\n").split("|")

#        if len(fields) != 6:
#            bad_rows.append((line_number, len(fields), line.strip()))

#print("Number of malformed rows:", len(bad_rows))

#for row in bad_rows:
#    print(row)