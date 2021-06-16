from instaloader import Instaloader, Profile
from instaloader.exceptions import QueryReturnedNotFoundException, LoginRequiredException,ProfileNotExistsException
import pandas as pd
# L = Instaloader()
# df = pd.read_csv("/Users/anchitshrivastava/Desktop/Tatras Data/Instagram Scrapping/Vietnam csv/Vietnam_combined_2_with_count.csv")
# users = df['Insta_Usernames']
# engagement_data={}
# user_count = 0
# count = 0
# for user in users:
#     # if count == 10:
#     #     break
#     # count += 1
#     try:
#         user = user.strip()
#         user_count= user_count+1
#         print(len(user))
#         print("User:",user_count,':',user)
#         profile = Profile.from_username(L.context, user)
#         profile_url = "https://www.instagram.com/" + user + "/"
#         print(profile_url)
#         if not profile.is_private:
#             ctr=0
#             total_comments=0
#             total_likes=0
#             for post in profile.get_posts():
#                 # L.download_post(post, target=profile.username)
#                 total_likes = total_likes+post.likes
#                 total_comments = total_comments + post.comments
#                 ctr = ctr+1
#                 if ctr == 10:
#                     break
#             engagement = ((total_comments+total_likes)/profile.followers)*10
#             engagement_data[user] = engagement
#         else:
#             print("PROFILE IS PRIVATE OR HAVE LESS FOLLOWERS")
#             print("========================")
#
#     except (QueryReturnedNotFoundException, LoginRequiredException, ProfileNotExistsException):
#         print("PROFILE NOT FOUND")
#         print("========================")
#
# print(engagement_data)


def engagememt_data(user):
    engagement_data = {}
    user_count = 0
    try:
        user = user.strip()
        user_count= user_count+1
        print(len(user))
        print("User:",user_count,':',user)
        profile = Profile.from_username(L.context, user)
        profile_url = "https://www.instagram.com/" + user + "/"
        print(profile_url)
        if not profile.is_private:
            ctr=0
            total_comments=0
            total_likes=0
            for post in profile.get_posts():
                # L.download_post(post, target=profile.username)
                total_likes = total_likes+post.likes
                total_comments = total_comments + post.comments
                ctr = ctr+1
                if ctr == 10:
                    break
            engagement = ((total_comments+total_likes)/profile.followers)*10
            engagement_data[user] = engagement
            print(engagement)
            return engagement
        else:
            print("PROFILE IS PRIVATE OR HAVE LESS FOLLOWERS")
            print("========================")
            pass

    except (QueryReturnedNotFoundException, LoginRequiredException, ProfileNotExistsException):
        print("PROFILE NOT FOUND")
        print("========================")

if __name__ == '__main__':
    L = Instaloader()
    df = pd.read_csv("/Users/anchitshrivastava/Desktop/Tatras Data/Instagram Scrapping/user_data_eng - KSA_1.csv")
    users = df['Insta_Usernames']
    engagement_data = {}
    user_count = 0
    df['Engagement'] = users.apply(engagememt_data)
    df.to_csv("ksa Data with engagement1 1.csv")