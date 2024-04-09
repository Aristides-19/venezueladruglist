from thefuzz.fuzz import partial_token_sort_ratio as partialSortRatio, token_sort_ratio as SortRatio
from unidecode import unidecode
from bs4 import BeautifulSoup
import numpy as np
import json
import re
from rich import print


def delete_accents(array: list) -> list:
    """Elimina Acentos con Unidecode
    """
    return [unidecode(element).lower() for element in array]


def get_locatel_drugs() -> list:
    """Obtiene los datos de Sustancias Activas de Locatel
    """
    try:
        with open('input/Locatel-Active-Substance.txt', 'rb') as html:
            soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

    except FileNotFoundError:
        raise Exception('APP.PY NOT BEING EXECUTED FROM venezueladruglist-main/src\n\tUSE cd venezueladruglist-main/src')

    else:
        drugs = soup.find_all('label', class_="vtex-checkbox__label w-100 c-on-base pointer")

        return [element.get_text().lower() for element in drugs]  # Los retorna en minúscula


def find_similars(drugs: list, umbral: int) -> dict[list]:
    """Busca strings similares, esto ayuda a ver cuáles están duplicados

    Args:
        drugs (list): Lista de Medicamentos Ordenada
        umbral (int): Se comparará con N strings a la derecha y N a la izquierda

    Returns:
        dict[list]: drugName: possibleCopies
    """
    toCorrect = dict()
    alreadyCheckedSet = set()

    for i, drugA in enumerate(drugs):

        # Si ya se comprobaron similitudes, no hay que hacerlo otra vez
        if drugA in alreadyCheckedSet:
            continue

        toCorrect[drugA] = []
        # N elementos a la derecha y N a la izquierda de drugA, determinado por el umbral   
        surroundingDrugs = drugs[max(0, i - umbral): i] + drugs[i + 1: min(i + umbral + 1, len(drugs))]

        for drugB in surroundingDrugs:
            # Promedio entre el Ratio Parcial y Ratio para determinar similitud
            partialR = partialSortRatio(drugA, drugB)
            ratio = SortRatio(drugA, drugB)
            similarity = (partialR + ratio) / 2

            if similarity >= 89:

                toCorrect[drugA].append(drugB)
                alreadyCheckedSet.add(drugB)

        if not toCorrect[drugA]:  # Si no hay similitudes, no aparecerá en el return
            del toCorrect[drugA]

    return toCorrect


def remove_similars(drugs: list) -> list:

    with open('input/to_remove.json', 'r') as toRemove:
        toRemove = json.loads(toRemove.read())  # Lista de medicamentos a remover

        for remove in toRemove:
            drugs.remove(remove.lower())

    drugs.extend(["Factor Ix De La Coagulacion",
                  "Factor Viii De La Coagulacion"])
    
    # toCorrect = find_similars(drugs, 30)
    
    return drugs


def delete_duplicates(array: list) -> list:
    array = np.array(delete_accents(array))
    array = np.unique(array, axis=0)  # Utiliza NumPy para eliminar duplicados

    return array.tolist()


def split_drug(word: str) -> np.ndarray:
    """Busca los medicamentos contenidos en un solo string
    """

    words = re.split(r' y |[/,+()-]+', word)  # Hace split por los caracteres en Regex

    words = np.array(words)
    indexMask = np.array(['mg' not in x and x != 'y' for x in words])

    return words[indexMask]


def clean_drug_strings(array: list) -> list:
    """Limpia y separa los strings de los medicamentos
    """
    drugsExtended = []

    drugs = [split_drug(drug) for drug in array]

    for drug in drugs:
        drugsExtended.extend([string.strip() for string in drug])

    return drugsExtended


def locatel() -> list:

    drugs = sorted(get_locatel_drugs())

    drugsExtended = clean_drug_strings(drugs)

    drugsExtended = delete_duplicates([x for x in drugsExtended if x and len(x) > 3])

    drugsExtended.append('alfalfa')

    return drugsExtended


def sarfe() -> list:

    with open('input/Description-Sarfe.txt', 'r', encoding='utf-8') as med:
        drugs = med.read().split('\n')

    drugs = delete_duplicates(drugs)

    drugsExtended = clean_drug_strings(drugs)

    drugsExtended = delete_duplicates([x for x in drugsExtended if x and len(x) > 3])

    drugsExtended[drugsExtended.index('vita. b')] = 'vitamina B'
    drugsExtended.remove('e. coli')
    drugsExtended.append('5-fluorouracilo')

    return drugsExtended


def main():
    locatelList = locatel()
    sarfeList = sarfe()

    drugs = delete_duplicates(locatelList + sarfeList)

    drugs = remove_similars(sorted(drugs))

    drugs = sorted([x.title().replace('  ', ' ') for x in drugs])

    drugs = {
        'description': 'Lista de Medicamentos Esenciales y Comercializados en Venezuela',
        'sources': ['https://www.locatel.com.ve/', 'https://www.orasconhu.org/documentos/Listado%20de%20Medicamentos%20Esenciales%20Venezuela%20FINAL.pdf'],
        'drug_list': drugs
    }
    jsonData = json.dumps(drugs, indent=4)

    with open('../medicamentos.json', 'w') as data:
        data.write(jsonData)


if __name__ == '__main__':
    main()
