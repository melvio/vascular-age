from pandas import DataFrame


def num_duplicates_ergoid(data: DataFrame) -> int:
    dup_found = abs(data['ergoid'].drop_duplicates().size -
                    data['ergoid'].size)
    print(f'number of duplicate ergoids found: {dup_found}')
    return dup_found


def prettify_calcification_columns(data: DataFrame) -> DataFrame:
    renamings = {'tot_vol_cor': "Calcification Coronaries",
                 'tot_vol_aor': "Calcification Aortic Arch",
                 'tot_vol_ici': "Calcification intracranial carotid arteries",
                 'tot_vol_eci': "Calcification extracranial carotid arteries",
                 'tot_vol_vbac': "Calcification vertebrobasilar arteries"
                 }
    return _prettify_calcification_columns(data, renamings)


def prettify_calcification_columns_short(data: DataFrame) -> DataFrame:
    renamings = {'tot_vol_cor': "CAC",
                 'tot_vol_aor': "AAC",
                 'tot_vol_ici': "ICAC",
                 'tot_vol_eci': "ECAC",
                 'tot_vol_vbac': "VBAC"
                 }
    return _prettify_calcification_columns(data, renamings)


def _prettify_calcification_columns(data: DataFrame,
                                    renamings: dict) -> DataFrame:
    return data.rename(columns=renamings)
