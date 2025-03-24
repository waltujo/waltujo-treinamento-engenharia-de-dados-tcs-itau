#%% Inicialização do JOB
import pandas as pd
from os import listdir
from os.path import isfile
from bibtexparser import load as load_bibtex
import sqlite3
import typing as types
from typing import Literal

OUTPUT_FOLDER = './output'

JCS_INPUT_FILEPATH = "./data/jcs_2020.csv"
SCIMAGO_INPUT_FILEPATH = "./data/scimagojr 2020.csv"

ACM_INPUT_FOLDER = "./data/acm"
IEEE_INPUT_FOLDER = "./data/ieee"
SCIENCE_INPUT_FOLDER = "./data/science_direct"

DB_FILEPATH = ':memory:'
OUTPUT_DB_FILEPATH = './output/db.sqlite3'

class FolderReader:
    @staticmethod
    def get_filepaths_from_folder(folder_path: str) -> list:
        filenames = [path for path in listdir(folder_path) if isfile(f"{folder_path}/{path}")]
        filepaths = [f"{folder_path}/{path}" for path in filenames]
        return filepaths

class BibtexReader:

    @staticmethod
    def read_files_to_dataframe(filepaths: list):
        files = (open(path, encoding="utf-8") for path in filepaths)  # type: ignore
        bibtexts = (load_bibtex(file) for file in files)
        dataframe_list = (pd.DataFrame(bib.entries) for bib in bibtexts)
        return pd.concat(dataframe_list)

class Sqlite3Handler:

    @staticmethod
    def get_connection(db_filepath: str):
        return sqlite3.connect(db_filepath)

    @staticmethod
    def load_dataframe_to_db(df: pd.DataFrame, connection: sqlite3.Connection, table_name: str, if_exists: Literal['fail', 'replace', 'append']):
        df.to_sql(name = table_name, con = connection, if_exists = if_exists)
        return df

    @staticmethod
    def read_df_from_sql(connection: sqlite3.Connection, sql: str):
        return pd.read_sql(sql = sql, con = connection)

    @staticmethod
    def create_index(connection: sqlite3.Connection, index_name: str, table_name: str, cols_name: types.List[str]):
        cols = ",".join(cols_name)
        connection.execute(f"CREATE INDEX {index_name} ON {table_name} ({cols});")

def generate_key_with_journal_name(series: pd.Series):
    return series.str.replace("&", "AND")\
                        .str.replace(r"([^A-Za-z0-9]+)", "")\
                        .str.upper()\
                        .str.strip()\

# %% Ler os arquivos de entrada
DF_ACM = BibtexReader.read_files_to_dataframe(
    FolderReader.get_filepaths_from_folder(ACM_INPUT_FOLDER)
)

DF_IEEE = BibtexReader.read_files_to_dataframe(
    FolderReader.get_filepaths_from_folder(IEEE_INPUT_FOLDER)
)

DF_SD = BibtexReader.read_files_to_dataframe(
    FolderReader.get_filepaths_from_folder(SCIENCE_INPUT_FOLDER)
)

DF_JCS = pd.read_csv(JCS_INPUT_FILEPATH, sep=";")

DF_SCIMAGO = pd.read_csv(SCIMAGO_INPUT_FILEPATH, sep=";", low_memory=False)
# %% Transformacao dos Bibtext
################################ Tratamento dos bibtex ACM ################################
df_acm = DF_ACM.convert_dtypes()
df_acm = df_acm[["author", "title", "keywords", "abstract", "year", "ENTRYTYPE", "doi", "issn", "isbn", "journal", "url"]]
df_acm = df_acm.rename(columns={"ENTRYTYPE": "type_publication"})
df_acm["issn"] = df_acm["issn"].mask(~df_acm["issn"].isnull(), df_acm["issn"].str.replace("-", ""))
df_acm["source"] = "acm"

################################ Tratamento dos bibtex IEEE ################################
df_ieee = DF_IEEE.convert_dtypes()
df_ieee = df_ieee[["author", "title", "keywords", "abstract", "year", "ENTRYTYPE", "doi", "issn", "journal"]]
df_ieee = df_ieee.rename(columns={"ENTRYTYPE": "type_publication"})
df_ieee["url"] = pd.NA
df_ieee["isbn"] = pd.NA
df_ieee["issn"] = df_ieee["issn"].mask(~df_ieee["issn"].isnull(), df_ieee["issn"].str.replace("-", ""))
df_ieee["source"] = "ieee"

################################ Tratamento dos bibtex Science Direct ################################
df_sd = DF_SD.convert_dtypes()
df_sd = df_sd[["author", "title", "keywords", "abstract", "year", "ENTRYTYPE", "doi", "issn", "isbn", "journal", "url"]]
df_sd = df_sd.rename(columns={"ENTRYTYPE": "type_publication"})
df_sd["issn"] = df_sd["issn"].mask(~df_sd["issn"].isnull(), df_sd["issn"].str.replace("-", ""))
df_sd["source"] = "science direct"

# %% Transformação - JCS, SCIMAGO e Bibtex

################################ Tratamento de todos os bibtex ################################
df_bibtex = pd.concat([df_acm, df_ieee, df_sd])
df_bibtex = df_bibtex.convert_dtypes()
df_bibtex = df_bibtex.drop_duplicates()
df_bibtex["journal_title_key"] = df_bibtex["journal"].pipe(generate_key_with_journal_name)  # type: ignore

################################ SCIMAGO ################################
df_scimago = DF_SCIMAGO.convert_dtypes()
df_scimago = df_scimago[['Issn', 'Title', 'SJR']]
df_scimago = df_scimago.rename(columns={'SJR': 'scimago_value', 'Issn': 'issn', 'Title': 'title'})
df_scimago["journal_title_key"] = df_scimago["title"].pipe(generate_key_with_journal_name)  # type: ignore

################################ JCS ################################
df_jcs = DF_JCS.convert_dtypes()
df_jcs = df_jcs[["Full Journal Title", "Journal Impact Factor"]]
df_jcs = df_jcs.rename(columns={"Full Journal Title": "title", "Journal Impact Factor": "jcs_value"})
df_jcs["journal_title_key"] = df_jcs["title"].pipe(generate_key_with_journal_name)  # type: ignore

################################ JOIN ENTRE SCIMAGO E JCS -> df_journal ################################
df_journal = pd.merge(left=df_scimago, right=df_jcs, left_on=["journal_title_key"], right_on=["journal_title_key"], how="outer") 

df_journal["title"] = df_journal["title_x"].mask(pd.isnull(df_journal["title_x"]), df_journal["title_y"])

df_journal = df_journal[['title', "issn", "journal_title_key", "scimago_value", "jcs_value"]]
df_journal = df_journal.rename(columns={"issn": "issn_journal"})

df_journal["issn_journal"] = df_journal["issn_journal"].mask(pd.isnull(df_journal["issn_journal"]), '-')

df_journal["upper_title"] = df_journal["title"].str.upper().str.strip()

df_journal = df_journal.drop_duplicates()

df_regex_groups = df_journal['issn_journal'].str.split(pat=",", n=3, expand=True)
df_journal['issn_1'] = df_regex_groups.loc[:, 0]
df_journal['issn_2'] = df_regex_groups.loc[:, 1]
df_journal['issn_3'] = df_regex_groups.loc[:, 2]

df_journal['issn_1'] = df_journal['issn_1'].mask(df_journal["issn_1"] == '-') #Caso issn seja = '-', coloca nulo no campo
df_journal['issn_2'] = df_journal['issn_2'].mask(df_journal["issn_2"] == '-') #Caso issn seja = '-', coloca nulo no campo
df_journal['issn_3'] = df_journal['issn_3'].mask(df_journal["issn_3"] == '-') #Caso issn seja = '-', coloca nulo no campo

df_journal = df_journal.drop_duplicates()

# %% Transformação - df_bibtex e df_journal
################################ JOIN ENTRE df_journal E df_bibtex no Banco de dados -> df_final ################################
CONNECTION = Sqlite3Handler.get_connection(DB_FILEPATH)
Sqlite3Handler.load_dataframe_to_db(df_bibtex, connection = CONNECTION, table_name = 'df_bibtex', if_exists = 'replace')
Sqlite3Handler.load_dataframe_to_db(df_journal, connection = CONNECTION, table_name = 'df_journal', if_exists = 'replace')
Sqlite3Handler.create_index(CONNECTION, "idx_df_bibtex_1", "df_bibtex", ["issn"])
Sqlite3Handler.create_index(CONNECTION, "idx_df_bibtex_2", "df_bibtex", ["journal_title_key"])
Sqlite3Handler.create_index(CONNECTION, "idx_df_journal_1", "df_journal", ["issn_1"])
Sqlite3Handler.create_index(CONNECTION, "idx_df_journal_2", "df_journal", ["issn_2"])
Sqlite3Handler.create_index(CONNECTION, "idx_df_journal_3", "df_journal", ["issn_3"])
Sqlite3Handler.create_index(CONNECTION, "idx_df_journal_4", "df_journal", ["journal_title_key"])

df_final = Sqlite3Handler.read_df_from_sql(CONNECTION, """--sql
      SELECT DISTINCT
            bib.author
            ,bib.title
            ,bib.keywords
            ,bib.abstract
            ,bib.year
            ,bib.type_publication
            ,bib.doi
            ,bib.issn
            ,COALESCE(bib.journal, jor.title) journal
            ,bib.source
            ,jor.scimago_value
            ,jor.jcs_value
            ,bib.url
      FROM 
            df_bibtex bib
            LEFT JOIN df_journal jor
                  ON (bib.issn = jor.issn_1
                  OR bib.issn = jor.issn_2
                  OR bib.issn = jor.issn_3
                  OR bib.journal_title_key = jor.journal_title_key)
                  AND NOT (bib.issn is null and bib.journal is null);
                  
""")

CONNECTION.close()

# Carga dos dados
OUTPUT_CONNECTION = Sqlite3Handler.get_connection(OUTPUT_DB_FILEPATH)

df_final = df_final.drop_duplicates(subset=["title", "year"])
df_final = df_final.pipe(Sqlite3Handler.load_dataframe_to_db, connection = OUTPUT_CONNECTION, 
                                                                  table_name = 'tb_bibtex_extraidos_manualmente', 
                                                                  if_exists = 'append')

OUTPUT_CONNECTION.close()