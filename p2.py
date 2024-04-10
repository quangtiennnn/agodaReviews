from hotelreviewFunction import *

data = pd.read_csv('city1.csv')

count = 0
new_df = split_list(data.hotel_id,4)[2] 
numofhotel  = len(new_df.hotel_id)

for hotel_id in new_df.hotel_id:
    start = time.time()
    hotelReviews(hotel_id)
    end = time.time()
    new_data = f"Elapsed time: {round(end-start, 2)} seconds <--> {count}/{numofhotel}"
    count += 1
    with open("p2.txt", "a") as file:
        file.write(new_data)
        file.write("\n")