import seaborn as sns
import matplotlib.pyplot as plt


# https://academic.oup.com/eurjpc/pages/general-instructionshttps://academic.oup.com/eurjpc/pages/general-instructions
# http://www.jesshamrick.com/2016/04/13/reproducible-plots/
def consistent_format():
    sns.set_theme(context='paper', font='Helvetica', font_scale=1)
    plt.rcParams['savefig.pad_inches'] = 0
    plt.rcParams['figure.dpi'] = 1200  # not important for vector graphics
