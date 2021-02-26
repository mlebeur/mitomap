import os, pandas, csv, re
import numpy as np
from biothings.utils.dataload import dict_convert, dict_sweep
from biothings import config
logging = config.logger
def load_mitomap(data_folder):
    infile = os.path.abspath("/opt/biothings/GRCh37/ExAC/r1/Exac.tsv")
    assert os.path.exists(infile)
    dat = pandas.read_csv(infile,sep="\t",squeeze=True,quoting=csv.QUOTE_NONE).to_dict(orient='records')
    results = {}
    for rec in dat:
        _id = rec["release"] + "_" + str(rec["chromosome"]) + "_" + str(rec["start"]) + "_" + rec["reference"] + "_" + rec["alternative"]       
        process_key = lambda k: k.replace(" ","_").lower()
        rec = dict_convert(rec,keyfn=process_key)
        rec = dict_sweep(rec,vals=[np.nan])
        results.setdefault(_id,[]).append(rec)
    for _id,docs in results.items():
        doc = {"_id": _id, "mitomap" : docs}
        yield doc
