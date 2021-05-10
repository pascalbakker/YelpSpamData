import pandas as pd
import pickle
import sys
from rank_bm25 import BM25Okapi

def do_recommendation(texts):
    hotelReview_ds  = pd.read_csv('hotelReview_ds.csv')
    rating_matrix = pd.read_csv('rating_matrix.csv',index_col=0)
    business_info_ds = pd.read_csv('business_info_ds.csv')
    tokenzied_review = pickle.load(open("tokenized_review.bin", "rb"))
    review_dataset = pickle.load(open("review_data.bin", "rb"))

    bm25 = BM25Okapi(tokenzied_review)

    tokenized_query = texts.split(" ")
    doc_scores = bm25.get_scores(tokenized_query)
    bm25.get_top_n(tokenized_query, review_dataset, n=10)
  
    # find simliar user related to that query request
    query_bm25 = hotelReview_ds.loc[doc_scores.argsort()[-10:][::-1]]['reviewer_id']
    # load vectors for similar users
    similar_users = rating_matrix[rating_matrix.index.isin(query_bm25)]
    print(rating_matrix.index)
    # calc avg ratings across the similar users
    similar_users = similar_users.mean(axis=0)
    # convert to dataframe so its easy to sort and filter
    similar_users_df = pd.DataFrame(similar_users, columns=['mean'])
    
    # order the dataframe
    similar_users_df_ordered = similar_users_df.sort_values(by=['mean'], ascending=False)
    # grab the top n hotels   
    top_n_hotels = similar_users_df_ordered.head(10)
    top_n_hotels_indices = top_n_hotels.index.tolist()
    # lookup these hotels in the other dataframe to find informations
    hotel_info = business_info_ds[business_info_ds['id'].isin(top_n_hotels_indices)]
    return hotel_info

if __name__ == '__main__':
# Map command line arguments to function arguments.
    do_recommendation(*sys.argv[1:])