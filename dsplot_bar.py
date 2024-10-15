"""
name = dsplot_bar
usage:
    dsplot_bar files.csv [options]
options:
    -x      label
    -y      value
    -w      weight
    -d      describes the dataset
    -i      shows information about dataset
description: 
    make bar charts from a .csv file 
"""

import pandas as pd
import yaml
import re

from jjcli import *


def wmean(df, colx, coly, colw):
    df2 = pd.DataFrame()

    if colw:
        df2["Peso"] = df[colw]
        df2["Produto"] = df[coly] * df[colw]
        df2["x"] = df[colx]
        g = df2.groupby("x")
        return g.Produto.sum() / g.Peso.sum()
    else:
        df2["Produto"] = df[coly]
        df2["x"] = df[colx]
        g = df2.groupby("x")
        return g.Produto.mean()


def main():
    cl = clfilter(opt="dix:y:w:", man=__doc__)

    for file in cl.args:
        print(f"#------ {file}")
        if file.endswith(".csv"):
            df = pd.read_csv(file)
            file_name = re.sub(r".csv", "", file)
        elif file.endswith(".xlsx"):
            df = pd.read_excel(file)
            file_name = re.sub(r".csv", "", file)

        if "-d" in cl.opt:
            print(df.describe(include="all"))
        elif "-i" in cl.opt:
            print(df.info())
        elif "-x" in cl.opt:
            col_x = cl.opt.get("-x")
            col_y = cl.opt.get("-y")
            col_w = cl.opt.get("-w", None)

            df3 = wmean(df, col_x, col_y, col_w)
            # print(df3)

            df3.plot(kind="bar").figure.savefig(f"{file_name}.png")
        else:
            print(txt)


if __name__ == "__main__":
    main()
