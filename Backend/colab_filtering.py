import numpy as np
import pandas as pd
import os
import logging
from scipy.sparse import csr_matrix, save_npz, load_npz
import json
import pdb

class ItemColab: 
    def __init__(self, data_folder_path):
        self.data_path = data_folder_path
        pass

    # Function to open up the batch folder and calculate how many batches we want to process
    def open_batch_folder(self, batch_folder):
        batch_files = os.listdir(batch_folder)
        batch_matrix_files = [os.path.join(batch_folder, file) for file in batch_files if file.endswith('.npz')]
        batch_labels_files = [os.path.join(batch_folder, file) for file in batch_files if file.endswith('.json')]
        file_path_dict = {}
        for file_ in batch_matrix_files:
            for label in batch_labels_files:
                if file_.split('/')[-1].split('_')[1].split('.')[0] == label.split('/')[-1].split('_')[1]:
                    file_path_dict[file_] = label
        print(f"total batches matched = {len(file_path_dict.keys())}")
        num_batches = len(batch_files)
        return file_path_dict
    
    def reconstruct_df(self, matrix_file_path, labels_file_path):
        # Load the sparse matrix
        sparse_matrix = load_npz(matrix_file_path)

        # Load the labels
        with open(labels_file_path, 'r') as f:
            labels = json.load(f)
        row_labels = labels['rows']
        column_labels = labels['columns']
        # Convert the sparse matrix to a DataFrame
        df = pd.DataFrame.sparse.from_spmatrix(sparse_matrix, index=row_labels, columns=column_labels)
        return df

    def cosine_similarity_batch(self, matrix_file_path, labels_file_path):
        df = self.reconstruct_df(matrix_file_path, labels_file_path)
        # Fill NaN values with 0 (or another appropriate value based on your data)
        df_filled = df.fillna(0)
        # calculate dot_product matrix
        dot_product_matrix = np.dot(df_filled.values.T, df_filled.values)
        dot_product_matrix = pd.DataFrame(dot_product_matrix, index = df_filled.columns, columns = df_filled.columns)
        sum_of_squares = pd.DataFrame(np.sum(np.square(df_filled.values.T), axis=1), index = df_filled.columns)
        return dot_product_matrix, sum_of_squares

    def sum_dataframes(self, dfs):
        combined_df = dfs[0].reindex(columns=dfs[0].columns.union(dfs[1].columns), index=dfs[0].index.union(dfs[1].index), fill_value=0)
        for df in dfs[1:]:
            combined_df = combined_df.add(df.reindex(columns=combined_df.columns, index=combined_df.index, fill_value=0), fill_value=0)
        return combined_df

    def compute_cosine_similarity_in_batches(self, file_path_dict):
        numerator = pd.DataFrame()
        denominator = pd.DataFrame()
        batch = 0
        for matrix_file_path, labels_file_path in file_path_dict.items():
            dot_product_matrix, sum_of_squares = self.cosine_similarity_batch(matrix_file_path, labels_file_path)
            # print("computed Numerator")
            numerator = self.sum_dataframes([numerator, dot_product_matrix])
            # print("computed Numerator")
            denominator = self.sum_dataframes([denominator, sum_of_squares])
            # print(f"computed Denominator")
            print(f"batch {batch} processed")
            batch += 1
        # pdb.set_trace()
        denominator_matrix = np.outer(np.sqrt(denominator),np.sqrt(denominator))
        denominator_matrix[denominator_matrix == 0] = 1
        cosine_similarity = numerator/denominator_matrix
        pdb.set_trace()
        cosine_similarity.to_csv("./Temp_data/cosine_sim_mat.csv")
        return cosine_similarity


    # matrix = list(file_path_dict.keys())
    # result = cosine_similarity_batch(matrix[4], file_path_dict[matrix[4]])

    # dot_product_matrix = pd.DataFrame(result[0], index = result[2], columns = result[2])
    # denominator = np.outer(np.sqrt(result[1]), np.sqrt(result[1]))
    # denominator[denominator == 0] = 1
    # cosine_similarity = dot_product_matrix/denominator
    # cosine_similarity

if __name__ == '__main__':
    folder_path = "../Anime_lists"
    item = ItemColab(folder_path)
    file_path_dict = item.open_batch_folder(folder_path)
    file_path_dict
    result =  item.compute_cosine_similarity_in_batches(file_path_dict)
    print(result.shape)