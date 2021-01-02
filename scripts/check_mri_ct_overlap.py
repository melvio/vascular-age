#!/usr/bin/env python3

from realage.preprocessing.dataloaders import CtCalcificationsDataLoader, MriDimReducedDataLoader

ct_df = CtCalcificationsDataLoader().load_dataframe()
mri_df = MriDimReducedDataLoader().load_dataframe()

# %%

mri_with_ct = mri_df[mri_df['ergoid'].isin(ct_df['ergoid'])]
ct_with_mri = ct_df[ct_df['ergoid'].isin(mri_df['ergoid'])]

assert len(mri_with_ct) == len(mri_df)
assert mri_with_ct['has_ct'].sum() == len(mri_with_ct)

print(f"total people with CT: {len(ct_df)}\n"
      f"total people with MRI:{len(mri_df)}\n"
      f"total people in MRI dataset who have had CT: {len(mri_with_ct)}")
