import mpmath as mp
import pandas as pd

# Load HDF5 Storage
hdf_file = 'fbd_storage.h5'


def hdf_data_load(all_comps=True):
    dfcs = pd.HDFStore(hdf_file)
    cols = list(dfcs['pl'].columns)
    all_df = pd.DataFrame(columns=cols)
    write_path = '/agg/all'
    if all_comps:
        for key in dfcs.keys():
            if len(dfcs.get(key).columns) == 16:
                app_df = pd.DataFrame(dfcs.get(key))
                all_df = all_df.append(app_df)
    if dfcs.__contains__(write_path):
        print("data present at {0}...deleting key".format(write_path))
        dfcs.remove(write_path)
    dfcs.put(key=write_path, value=all_df)
    print("Wrote {0} rows on {1} columns to {2}".format(all_df.shape[0], all_df.shape[1], write_path))
    dfcs.close()
    return