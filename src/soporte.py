import pandas as pd
import scipy.stats as stats
from scipy.stats import shapiro,  poisson, chisquare, expon, kstest

def read(ruta_archivo):
    return pd.read_csv(ruta_archivo)

def eda (dataframe):
    """
    Realiza un análisis exploratorio básico de un DataFrame, mostrando información sobre duplicados,
    valores nulos, tipos de datos, valores únicos para columnas categóricas y estadísticas descriptivas
    para columnas categóricas y numéricas, agrupadas por la columna de control.

    Parámetros:
    - dataframe (DataFrame): El DataFrame que se va a explorar.

    Returns: 
    No devuelve nada directamente, pero imprime en la consola la información exploratoria.
    """
    
    print(f"El tamaño del dataframe es: {dataframe.shape}")
    print("\n ..................... \n")

    print(f"Los duplicados que tenemos en el conjunto de datos son: {dataframe.duplicated().sum()}")
    print("\n ..................... \n")
    
    
    # generamos un DataFrame para los valores nulos
    print("Los nulos que tenemos en el conjunto de datos son:")
    df_nulos = pd.DataFrame(dataframe.isnull().sum() / dataframe.shape[0] * 100, columns = ["%_nulos"])
    display(df_nulos[df_nulos["%_nulos"] > 0])
    
    print("\n ..................... \n")
    print(f"Los tipos de las columnas son:")
    display(pd.DataFrame(dataframe.dtypes, columns = ["tipo_dato"]))
    
    
    print("\n ..................... \n")
    print("Los valores que tenemos para las columnas categóricas son: ")
    dataframe_categoricas = dataframe.select_dtypes(include = "O")
    
    for col in dataframe_categoricas.columns:
        print(f"La columna {col.upper()} tiene las siguientes valores únicos:")
        display(pd.DataFrame(dataframe[col].value_counts()).head())    
    
    
    print("\n ..................... \n")
    print("Los valores que tenemos para las columnas numéricas son: ")
    dataframe_numericas = dataframe.select_dtypes(include='number')
    
    for col in dataframe_numericas.columns:
        print(f"La columna {col.upper()} tiene las siguientes valores únicos:")
        display(pd.DataFrame(dataframe[col].value_counts()).head())    

    print("\n ..................... \n")
    descripcion = dataframe.describe().T
    print(f"Los principales valores estadísticos son:")
    print(descripcion.to_string())

def modify_columns(dataframe):
    """
    Cambia los nombres de las columnas del DataFrame a minúsculas y reemplaza los espacios por barras bajas.

    Parámetros:
    dataframe: el dataframe al que modificaremos las columnas
    Returns:
    El dataframe con los nombres de las columnas modificados.
    """

    nombres_columnas = dataframe.columns
    nuevos_nombres = [nombre.lower().strip().replace(' ', '_') for nombre in nombres_columnas]
    dataframe.columns = nuevos_nombres
    
    return dataframe

def normalidad(dataframe, columna):
    """
    Evalúa la normalidad de una columna de datos de un DataFrame utilizando la prueba de Shapiro-Wilk.

    Parámetros:
        dataframe (DataFrame): El DataFrame que contiene los datos.
        columna (str): El nombre de la columna en el DataFrame que se va a evaluar para la normalidad.

    Returns:
        None: Imprime un mensaje indicando si los datos siguen o no una distribución normal.
    """
    statistic, p_value = stats.shapiro(dataframe[columna])
    if p_value > 0.05:
        print(f"Para la columna {columna} los datos siguen una distribución normal.")
    else:
        print(f"Para la columna {columna} los datos no siguen una distribución normal.")

def homogeneidad (grupoa,grupob):
    
    """
    Evalúa la homogeneidad de las varianzas entre grupos para una métrica específica en un DataFrame dado mediante la prueba de Levene.

    Parámetros:
    - grupoa: df filtrado para uno de los grupos con la variable
    - grupob: df filtrado para el segundo grupo con la variable

    Returns:
    No devuelve nada directamente, pero imprime en la consola si las varianzas son homogéneas o no entre los grupos.
    """       
    statistic, p_value = stats.levene(grupoa,grupob)
    if p_value > 0.05:
        print(f"Las varianzas son homogéneas entre grupos.")
    else:
        print(f"Las varianzas no son homogéneas entre grupos.")
        
def mann_whitney(grupoa, grupob):
    """
    Realiza la prueba de Mann-Whitney U para comparar las medianas de las métricas entre dos grupos en un DataFrame dado.

    Parámetros:
    - grupoa: df filtrado para uno de los grupos con la variable
    - grupob: df filtrado para el segundo grupo con la variable

    Returns 
    No devuelve nada directamente, pero imprime si hay diferencias significativas entre los dos grupos o no.
    """

    x, p_valor = stats.mannwhitneyu(grupoa, grupob)

    if p_valor < 0.05:
        print("Rechazamos la hipótesis nula.")
        print("Hay una diferencia significativa entre los dos grupos.")
    else:
        print("No podemos rechazar la hipótesis nula.")
        print("No hay evidencia suficiente para afirmar una diferencia significativa entre los dos grupos.")