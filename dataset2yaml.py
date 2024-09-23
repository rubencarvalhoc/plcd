"""
name = dataset2yaml
usage:
    dataset2yaml files.csv [options]
options:
    -d      describe the dataset details
    -i      generic info
description: 
    pretty print a comma separated or excel file
"""
import pandas
import yaml
import re

from jjcli import * 

def main():       ## re.* functions also imported
    cl=clfilter(opt="di", man=__doc__)   ## script -d -o arg -t arg1 -t arg2
                                ## options in cl.opt  (...if "-d" in cl.opt:)
                                ## autostrip         (def=True)
                                ## inplace=True      (def=False)
                                ## fs (for csvrow()) (def=",")
                                ## longopts=["opt1", ...] (def=[])
                                ## doc=__doc__   for "--help" (def="FIXME no doc provided")

    for file in cl.args:
        print(f"#------ {file}")
        if file.endswith(".csv"): 
            df = pandas.read_csv(file)
        elif file.endswith(".xlsx"): 
            df = pandas.read_excel(file)

        txt = yaml.dump(
                df.to_dict(orient='records'),
                sort_keys=False,
                width=72, 
                indent=4
            )

        txt = re.sub(r"^-", "\n", txt, flags=re.MULTILINE)
        txt = re.sub(r"^[ \t\r]+", "", txt, flags=re.MULTILINE)

        if "-d" in cl.opt:
            print(df.describe(include="all"))
        elif "-i" in cl.opt:
            print(df.info())
        else:
            print(txt)


#with open('final.yml', 'w') as outfile:
    

# (gdpPercap: \d+.\d+)
# $1\n