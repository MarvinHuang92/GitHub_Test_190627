import pandas as pd

# read data
u_data = pd.read_table('ml-100k/u.data', sep='\t', names=['user_id', 'item_id', 'rating', 'timestamp'])
u_user = pd.read_table('ml-100k/u.user', sep='|', names=['user_id', 'age', 'gender', 'occupation', 'zip_code'])

# print(u_data)
# print(u_user)


# 思路1：先计算每个人自身的标准差，再求分别对男女求两次平均值 （每个人对不同电影的看法差异）
# 思路2：将所有人的平均值再求一次平均值，针对第二个均值求标准差 （所有男性/所有女性内部的标准差）

# get gender info for each user, by merge the 2 input table (on common column 'user_id')
u_data_merged = pd.merge(u_data, u_user, how='inner', on='user_id')
# u_data_merged.drop(columns=['timestamp', 'age', 'occupation', 'zip_code'], inplace=True)
print(u_data_merged)
u_data_merged.to_csv("merged_data.csv", index=False, sep=',')

# get the mean value of 'rating' for each user
pivot = pd.pivot_table(u_data_merged, index='gender', columns='user_id', values='rating', aggfunc='mean')
# pivot = pd.pivot_table(u_data_merged, index='gender', values='rating', aggfunc='mean')
print(pivot)
# pivot = pd.pivot_table(u_data_merged, index='gender', values='rating', aggfunc='std')
# print(pivot)

# split the table into 2 separated tables by 'gender', and then drop all NaN colomns
pivot_male = pivot.drop(index='F').dropna(axis=1)
print(pivot_male)
pivot_male.to_csv("male.csv", sep=',')

pivot_female = pivot.drop(index='M').dropna(axis=1)
print(pivot_female)
pivot_female.to_csv("female.csv", sep=',')


# 然后根据STDEVP（）函数，在excel中直接求出。。。



# print(pd.pivot_table(pivot_male, values='rating', aggfunc='mean'))


# print(pd.pivot_table(u_user, columns=['gender'], values=['age'], aggfunc='mean'))

# pd.merge(left, right, how='inner') 


























# z = input ("Press any key to continue...")