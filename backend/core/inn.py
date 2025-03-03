import json
import pandas as pd
import numpy as np
import os
import random

DATA_PATH = r'C:\Users\Sveta\Downloads\zakupki\data'


def avaliability_of_inn(inn):
    inn_not_recomended = np.load(os.path.join(
        DATA_PATH, 'inn_not_recomended.npy'), allow_pickle=True)
    inn_recomended = np.load(os.path.join(
        DATA_PATH, 'inn_recomended.npy'), allow_pickle=True)

    rnp = pd.read_csv(os.path.join(DATA_PATH, 'rnp.csv'), delimiter=';')
    rnp = list(rnp['inn'].values)

    if inn in inn_not_recomended:
        return "Не рекомендуем проводить сделку! \nДанный агент не может принимать участие в торгах из-за отсутствия лицензий или невыполнения критериев 44 ФЗ"

    if inn in rnp:
        return "Не рекомендуем проводить сделку! \nДанный агент внесен в список недобросовестных"

    if inn in inn_recomended:
        return "Рекомендуем рассмотреть контракт с данным агентом. Агент соблюдает все регламенты и имеет необходимые лицензии. "

    if (inn not in inn_recomended) and (inn not in inn_not_recomended):
        return "Осторожно! Недостаточно сведений для оценки возможности агента провести сделку. Рекомендуем запросить дополнительную информацию"


def score_inn_without_history(inn):
    bo_final_dataset = pd.read_csv(os.path.join(
        DATA_PATH, 'bo_final_dataset.csv'))

    if inn not in list(bo_final_dataset['inn'].values):
        return "Не рекомендуем агента. Недостаточно информации", 0
    else:
        if bo_final_dataset.loc[bo_final_dataset['inn'] == inn, 'unappropriated_balance'].values[0] < -1_000:
            return "Не рекомендуем агента. Компания в большом убытке", 0
        elif (bo_final_dataset.loc[bo_final_dataset['inn'] == inn, 'avg_staff_qty'].values[0] <= 5) and \
                (bo_final_dataset.loc[bo_final_dataset['inn'] == inn, 'bo_balance'].values[0] == 0):
            return "Не рекомендуем агента. Компания похожа на фирму-однодневку", 0

        else:
            if bo_final_dataset.loc[bo_final_dataset['inn'] == inn, ['bo_capital_change_3', 'bo_capital_change_2',
                                                                     'bo_financial_results', 'bo_fund_movement',
                                                                     'bo_target_fund_use']].values.mean() == 0:
                return "Данный агент крайне ненадежен на основе бухгалтерской отчетности, истории уплаты налогов и других финансовых показателей", 0
            else:
                aaa = np.round(bo_final_dataset.loc[bo_final_dataset['inn'] == inn, ['bo_capital_change_3', 'bo_capital_change_2',
                                                                                     'bo_financial_results', 'bo_fund_movement',
                                                                                     'bo_target_fund_use']].values.mean() * 100, 0)
                if aaa == 0:
                    return "Данный агент крайне ненадежен на основе бухгалтерской отчетности, истории уплаты налогов и других финансовых показателей", 0
                else:
                    return "Данный агент входит в топ {}% на основе бухгалтерской отчетности, истории уплаты налогов и других финансовых показателей".format(aaa), int(aaa)


def score_inn_with_history(inn, is_supplier):
    if is_supplier:
        contracts_aggr = pd.read_csv(os.path.join(
            DATA_PATH, 'contracts_aggr_supplier.csv'))
    else:
        contracts_aggr = pd.read_csv(os.path.join(
            DATA_PATH, 'contracts_aggr_customer.csv'))

    if inn not in list(contracts_aggr['inn'].values):
        return "Недостаточно информации"

    agent = 'контрагента' if is_supplier else 'агента'

    contracts_aggr_inn = contracts_aggr.loc[contracts_aggr['inn'] == inn]
    return f"У данного {agent} средняя удовлетворенность по {contracts_aggr_inn['id_contract'].values[0]} сделкам равна {contracts_aggr_inn['quality'].values[0]}%"

def assign_supplier_category(rec):
    if 'Рекомендуем' in rec:
        return random.choice(['AAA', 'AA+', 'AA', 'AA–', 'A+', 'A', 'A–', 'BBB+', 'BBB'])
    else:
        return random.choice(['BBB–', 'BB+', 'BB', 'BB–', 'B+', 'B', 'B–', 'CCC'])
    
def main_estimation(inn, is_supplier):
    print(inn, is_supplier)
    if is_supplier:
        contracts_aggr = pd.read_csv(os.path.join(DATA_PATH, 'contracts_aggr_supplier.csv'))
    else:
        contracts_aggr = pd.read_csv(os.path.join(DATA_PATH, 'contracts_aggr_customer.csv'))

    if contracts_aggr.query(f'inn == "{inn}"').shape[0] < 2:
        result_text = (
            '<u>Возможность проводить сделку:</u> <br>' + avaliability_of_inn(inn=inn).replace('\n', '<br>') + '<br>' +
            'У данного агента крайне малая история сделок. <br><br>' +
            '<u>Рекомендации на основе финансовых показателей:</u> <br>' + 
            score_inn_without_history(inn=inn)[0].replace('\n', '<br>')
        )
    else:
        result_text = (
             '<u>Возможность проводить сделку:</u> <br>' + avaliability_of_inn(inn=inn).replace('\n', '<br>') + '<br><br>' +
            score_inn_with_history(inn, is_supplier)[0].replace('\n', '<br>')
        )

    return result_text, int(score_inn_without_history(inn=inn)[1]) if contracts_aggr.query(f'inn == "{inn}"').shape[0] < 2 else int(score_inn_with_history(inn, is_supplier)[1])


def get_inn_reccomends(inn: int, agent: str):
    """Рекомендации по ИНН

    Args:
        inn (int): ИНН компании
        agent (str): Агент или контрагент. Если агент, то True, иначе False

    Returns:
        couple(str, str, int): Рекомендации в виде текста, рейтинг в int
    """
    is_supplier = False if agent == 'агент' else True

    text_1 = avaliability_of_inn(inn)
    rating = score_inn_without_history(inn)
    text_2 = score_inn_with_history(inn, is_supplier)

    answer = []
    answer.extend(rating)
    answer.append(text_1)
    answer.append(text_2)

    return main_estimation(inn, is_supplier)
