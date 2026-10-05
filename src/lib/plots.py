import matplotlib.pyplot as plt
import pandas as pd
from src.config import OPENFIG, SAVEFIG

def plot_line(
        scalex:pd.DataFrame, 
        scaley:pd.DataFrame, 
        xlabel:str, 
        ylabel:str, 
        title:str, 
        save_path:str="",
        figsize:tuple[int, int]=(10, 6), 
        xticks_rotation:int=45, 
        marker:str='o'
        ):

    plt.figure(figsize=figsize)
    plt.plot(scalex, scaley, marker=marker)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=xticks_rotation)
    plt.tight_layout()
    if SAVEFIG: plt.savefig(save_path)
    if OPENFIG: plt.show()

def plot_bar(
        y,
        width,
        xlabel:str,
        ylabel:str,
        title:str,
        figsize:tuple[int, int],
        save_path:str="",
        xticks_rotation:int=45
        ):
    plt.figure(figsize=figsize)
    plt.barh(y, width)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=xticks_rotation)
    plt.tight_layout()
    if SAVEFIG: plt.savefig(save_path)
    if OPENFIG: plt.show()

def plot_box_plot(
        data:pd.DataFrame,
        column:str,
        by:str,
        vert:bool,
        figsize:tuple[int, int],
        title:str,
        suptitle:str,
        xlabel:str,
        ylabel:str,
        savepath:str
):
    data.boxplot(column=column, by=by, vert=vert, figsize=figsize)
    plt.title(title)
    plt.suptitle(suptitle)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    if SAVEFIG: plt.savefig(savepath)
    if OPENFIG: plt.show()