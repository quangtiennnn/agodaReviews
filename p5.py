from hotelreviewFunction import *

data = pd.read_csv('city2.csv')

count = 0
new_df = split_list(data.hotel_id,4)[1] 
numofhotel  = len(new_df)

for hotel_id in new_df:
    if not fileExisted(hotel_id):
        start = time.time()
        hotelReviews(hotel_id)
        end = time.time()
        print(f"Elapsed time: {round(end-start, 2)} seconds <--> {count}/{numofhotel}")  
        count += 1
    else: 
        print('Skiped!!')