# from pickle import TRUE
from cProfile import label
from tkinter import CENTER
from warnings import catch_warnings
from numpy import arange, bincount, busday_count
import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
user_dict = {}
for line in open('user.txt', 'r'):
	# print(line, end='')
	# line.replace('\n','').replace('\r','')
	temp = line.split(',')
	# temp[1]=int(temp[1])
	user_dict[temp[0]] = int(temp[1])
# print(user_dict)
user_review = {}

business_dict = {}
business_star = {}
business_count = {}
count_sum = 0
with pd.read_json('yelp_academic_dataset_business.json', lines=True, chunksize=1000) as reader:
	# reader
	for chunk in tqdm(reader, desc="Load Business", total=161):
		# print(chunk)
		businesses = pd.Index.to_list(chunk['business_id'])
		tags = pd.Index.to_list(chunk['categories'])
		stars = pd.Index.to_list(chunk['stars'])
		count = pd.Index.to_list(chunk['review_count'])
		count_sum += sum(count)
		for i in range(len(businesses)):
			if businesses[i] not in user_dict:
				business_dict[businesses[i]] = []
			business_dict[businesses[i]].append(tags[i])
			business_star[businesses[i]] = stars[i]
			business_count[businesses[i]] = count[i]
# print(business_dict)


# with pd.read_json('yelp_academic_dataset_review.json', lines=True, chunksize=10000) as reader:
# 	# reader
# 	for chunk in tqdm(reader,desc="Load Review",total=864):
# 		users = pd.Index.to_list(chunk['user_id'])
# 		rating = pd.Index.to_list(chunk['stars'])
# 		business = pd.Index.to_list(chunk['business_id'])
# 		for i in range(len(users)):
# 			if users[i] in user_dict:
# 				if users[i] not in user_review:
# 					user_review[users[i]] = []
# 				user_review[users[i]].append([rating[i], business[i]])


truth_list = []
avg_list = []
top_list = []
for i in tqdm(range(100),desc="Rating Calc"):
	rate_sum = wei_rate_sum =top_rate_sum= count_sum = counting = 0
	rate_data=[]
	for bus_id, tag_list in business_dict.items():
		if tags[i] in tag_list:
			rate_data.append(business_star[bus_id])
			rate_sum += business_star[bus_id]
			wei_rate_sum += business_star[bus_id]*business_count[bus_id]
			count_sum += business_count[bus_id]
			counting += 1
	rate_data =sorted(rate_data,reverse=True)
	if len(rate_data) > 0:
		# print(rate_data)
		for _ in range(int(len(rate_data)*0.15)):
			rate_data.pop()
		# print(rate_data)
		top_rate_sum= sum(rate_data)/len(rate_data)
	if rate_sum > 0 and counting > 50 :
		truth_list.append(wei_rate_sum/count_sum)
		avg_list.append(rate_sum/counting)
		top_list.append(top_rate_sum)
print('Ground Truth:',truth_list)
print('Average:',avg_list)
print('Top 85%:',top_list)
truth = np.array(truth_list)
avg = np.array(avg_list)
top=np.array(top_list)
width=1
# width = total_width / n
x = arange(len(truth_list)) 
params = {'figure.figsize': '12, 6'}
plt.rcParams.update(params)
plt.bar(x, truth, width=0.25,align='center', label='truth')
plt.bar(x+0.25*width, avg, width=0.25,align='center', label='average')
plt.bar(x+0.5*width, top, width=0.25,align='center', label='top 85%')
plt.legend()
plt.savefig('test.jpg')


#--------------original version----------------#


# 	# print(user_review.keys())
# 	# print(rating)
# print('Linking review')
# temp_tup=user_review['Xwnf20FKuikiHcSpcEbpKQ']
# cat_count={}
# cat_data={}
# for tup in temp_tup:
# 	temp_cat_list=business_dict[tup[1]]
# 	for cat in temp_cat_list:
# 		if cat not in cat_count:
# 			cat_count[cat]=0
# 		cat_count[cat]+=1
# 		if cat not in cat_data:
# 			cat_data[cat]=[]
# 		cat_data[cat].append(tup) #add rating and business id
# print("Done")

# print('Filtering review')
# victims=[]
# for cat, num in cat_count.items():
# 	if num <15:
# 		victims.append(cat)
# for cat in victims:
# 	cat_count.pop(cat)
# 	cat_data.pop(cat)
# print('Done')
# 	# print(temp_cat_list)
# mean_={}
# max_={}
# for cat, data in cat_data.items():
# 	temp_sum=0
# 	temp_wei_sum=0
# 	best_num=0
# 	worst_num=0
# 	for i in range(len(data)):
# 		temp_sum+=data[i][0]
# 		temp_wei_sum+=data[i][0]
# 		if data[i][0] == 5:
# 			temp_wei_sum+=5*data[i][0]
# 			best_num+=1
# 		if data[i][0] <2 :
# 			temp_wei_sum-=data[i][0]
# 			worst_num+=1
# 	avg=temp_sum/len(data)
# 	wei=temp_wei_sum/(len(data)+5*best_num-worst_num)
# 	print(cat,'\t',avg,'\t',wei)
# # print(cat_count)
# # print(cat_data)
