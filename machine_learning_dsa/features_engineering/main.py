import time

import pandas as pd
import requests
import zipfile
import io
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def get_dataset():
    url = "http://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip"

    response = requests.get(url)
    print(f"{response} | {response.text if response.status_code != 200 else 'Succeded'}")

    try:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            print("Files into ZIP:", z.namelist())

            # Here you put the name of the file
            file_name = 'bank.csv'
            with z.open(file_name) as file:
                df = pd.read_csv(file, sep=';')
                print(f"Selected File: {file_name}", '\n')

        print('########## INFORMAÇÕES GERAIS ##########')
        df.info()
        print('\n########## DESCRIÇÃO ##########\n', df['job'].describe(), '\n')  # df['job'].describe() works
        print('########## CONTAGEM DE VALORES ##########\n', df['job'].value_counts(), '\n')
        print('########## DATAFRAME ##########\n', df.head(), '\n')

        plot_data = df['job'].value_counts()
        plt.figure(figsize=(10, 6))
        plot_data.plot(kind='bar')
        # plt.show()  # Feel free to see the ploted data

        return df

    except Exception as e:
        print(e)

# NOTE: You don't have to apply all steps below. It is just examples of: Map Columns and One-Hot Encoding (Dummies)


df_bank = get_dataset()

# Create a mapped column
de_para = {
    'admin.': 'medio',
    'blue-collar': 'baixo',
    'entrepreneur': 'alto',
    'housemaid': 'baixo',
    'management': 'medio',
    'retired': 'baixo',
    'self-employed': 'baixo',
    'services': 'medio',
    'student': 'alto',
    'technician': 'alto',
    'unemployed': 'baixo',
    'unknown': 'baixo'
}

df_bank['technology_use'] = df_bank['job'].map(de_para)

# Convert categorical variable ('no', 'yes') to numeric (0, 1) in a new column
df_bank['default_n'] = df_bank['default'].map({'no': 0, 'yes': 1})

# One-Hot Encoding
categorical_cols = df_bank.select_dtypes(include=['object', 'category']).columns  # cols needing encoding
df_one_hot = pd.get_dummies(df_bank, columns=categorical_cols, prefix=categorical_cols)  # df with one-hot encoding
df_one_hot = df_one_hot.astype(int)  # Convert bool to int
df_bank = pd.concat([df_bank, df_one_hot], axis=1)  # Concat df_one_hot with df_bank by column

# Concat columns
df_bank['job_marital'] = df_bank['job'] + '_' + df_bank['marital']  # Create a combined column
dummies = pd.get_dummies(df_bank, columns=['job_marital'], prefix='job_marital')  # Apply one-hot encoding
bool_cols = dummies.select_dtypes(include=['bool']).columns  # Get all bool cols
dummies[bool_cols] = dummies[bool_cols].astype(int)  # Convert bool to int
df_bank = pd.concat([df_bank, dummies], axis=1)  # Concatenate the dummy variables with the original DataFrame

print(df_bank.head(50))
time.sleep(1)
print(df_bank.dtypes)
