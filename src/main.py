from csv_distribution_loader import CSVDistributionLoader
from random_distribution_loader import RandomDistributionLoader

def loadDistributionFromCSV() -> CSVDistributionLoader:
    file_path: str = input("Introduce la ruta del archivo CSV: ")
    loader: CSVDistributionLoader = CSVDistributionLoader()
    try:
        loader.loadDistribution(file_path)
    except (ValueError, IndexError) as e:
        print(e)
        return None
    return loader.getDistribution()

def loadRandomDistribution() -> CSVDistributionLoader:
    amount_of_variables: int = int(input("Introduce el número de variables de la distribución aleatoria: "))
    loader: RandomDistributionLoader = RandomDistributionLoader()
    try:
        loader.loadDistribution(amount_of_variables)
    except ValueError as e:
        print(e)
        return None
    return loader.getDistribution()

def main():
    load_type: str = input("Introduce la forma de carga de la distribución (1 para CSV y 0 para aleaorio): ")
    distribution = None
    if load_type == "1":
        distribution = loadDistributionFromCSV()
        if distribution is None:
            return
    elif load_type == "0":
        distribution = loadRandomDistribution()
        if distribution is None:
            return
    else:
        print("Opción no válida.")
        return
    
    print("\nDistribución cargada exitosamente: \n")
    distribution.showDistribution()
    
    amount_of_interest_variables: int = int(input("\nIntroduce el número de variables de interés: "))
    for i in range(amount_of_interest_variables):
        variable_index: int = int(input(f"Introduce el índice de la variable de interés {i+1} (1 para X1, etc): "))
        try:
            distribution.setInterestVariable(variable_index - 1)
        except IndexError as e:
            print(e)
            return

    amount_of_conditioned_variables: int = int(input("\nIntroduce el número de variables condicionadas: "))
    for i in range(amount_of_conditioned_variables):
        variable_index: int = int(input(f"Introduce el índice de la variable condicionada {i+1} (1 para X1, etc): "))
        value: int = int(input(f"Introduce el valor de la variable condicionada {i+1} (0 o 1): "))
        try:
            distribution.setConditionedVariable(variable_index - 1, value)
        except (IndexError, ValueError) as e:
            print(e)
            return

    print("\nLas máscaras resultantes son las siguientes: \n")
    distribution.showInterestValuesMask()
    distribution.showConditionedVariablesMask()
    distribution.showConditionedValuesMask()

    
if __name__ == "__main__":
    main()