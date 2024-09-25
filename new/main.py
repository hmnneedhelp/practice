import cv2
import pandas as pd
from sqlalchemy import create_engine

def process_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    pixel_values = image.flatten()
    
    return pixel_values

def create_csv(data, csv_file_path):
    data_str = ','.join(map(str, data))
    
    with open(csv_file_path, 'w') as file:
        file.write(data_str)

def csv_to_database(csv_file_path, db_connection_string, table_name):
    engine = create_engine(db_connection_string)
    
    with open(csv_file_path, 'r') as file:
        data_str = file.read()
    
    df = pd.DataFrame([[data_str]], columns=["pixel_data"])
    
    df.to_sql(table_name, con=engine, if_exists='append', index=False)

if __name__ == "__main__":
    image_path = "image1.png"
    
    pixel_data = process_image(image_path)
    
    csv_file_path = "image_data.csv"
    create_csv(pixel_data, csv_file_path)

    db_connection_string = "sqlite:///image_data.db" 
    table_name = "image_data"
    
    csv_to_database(csv_file_path, db_connection_string, table_name)

    print("Данные успешно сохранены в базу данных.")