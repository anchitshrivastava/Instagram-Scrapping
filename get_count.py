from instaloader import Instaloader, Profile
from instaloader.exceptions import QueryReturnedNotFoundException, LoginRequiredException,ProfileNotExistsException
import pandas as pd
import csv
import os.path

# Name of the input csv
input_csv = "hongkong_combined_2.csv"
# Load the data
data = pd.read_csv(input_csv)

# Name the output csv
output_csv = input_csv.split(".")[0] + "_with_count.csv"
if not os.path.exists(output_csv):
    csvfile=open(output_csv,'w', newline='')
    obj = csv.writer(csvfile)
    obj.writerow(('Insta_Profiles','Insta_Usernames', 'followers', 'following', 'post_count', 'full_name', 'user_bio'))
else:
    csvfile=open(output_csv,'a', newline='')
    obj = csv.writer(csvfile)

# Getting the profile names
users = data['Insta_Usernames']
# Load instaloader
L = Instaloader()
count = 1
for user in users:
    try:
        print("USER", count)
        profile = Profile.from_username(L.context, user)
        profile_url = "https://www.instagram.com/" + user + "/"
        if not profile.is_private and profile.followers > 30:
            print(profile_url)
            followers = profile.followers
            following = profile.followees
            post_count = profile.mediacount
            user_bio = profile.biography
            full_name = profile.full_name
            print(followers, following, post_count)
            print(user_bio,)
            print("==================")
            obj.writerow((profile_url, user, followers, following, post_count, full_name, user_bio))

        else:
            print("PROFILE IS PRIVATE OR HAVE LESS FOLLOWERS")
            print("========================")
    except (QueryReturnedNotFoundException, LoginRequiredException, ProfileNotExistsException):
            print("PROFILE NOT FOUND")
            print("========================")

    count += 1
csvfile.close()
