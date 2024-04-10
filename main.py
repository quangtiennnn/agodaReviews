from hotelreviewFunction import *

count = 0 
for hotel_id in df.hotel_id:
    hotelReviews(hotel_id)
    count += 1
    print(count,'/',len(df.hotel_id))