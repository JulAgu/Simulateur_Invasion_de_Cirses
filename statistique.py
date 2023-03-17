import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class statsNum:
    '''
    Definition de la classe pour passer à les analyses statistiques dans le cadre d'une modelisation numerique. Mettre en ouvre
    les attributes, que sont des listes qu'on va remplir avec le nombre de repetition, le nombre de jours, nomblre de cirses accumulé,
    de cirses dans l'instant t, nombre de identification accumulé et dans l'instant t (fait avec le drone), et enfin, le nombre de 
    cirses tués par l'herbicide.
    '''
    def __init__(self) -> None:
        self.N_rep = []
        self.J = []
        self.P_acc = []
        self.P_act = []
        self.D_acc = []
        self.D_act = []
        self.E_a = []

    def creerDF(self,droneModalité):
        '''
        Création d'un data frame que contient tous les informations mentionné ci-dessus et son importation 
        par un archive ".csv", plus facile si on veut faire des analyses en utilisent differents softwares, comme R. 
        '''
        self.time = datetime.now()
        self.marktime = (str(self.time.day) + "." + str(self.time.month) + "." + str(self.time.year) + "_" 
                        + str(self.time.hour) + "." + str(self.time.minute) + "." + str(self.time.second))
        nom = 'simulation_' + self.marktime + '.csv'
        self.dictData = {'N.Repetition':self.N_rep, 'Jour' : self.J, 'P. cumulées' : self.P_acc,
                         'P. présentes' : self.P_act, 'D. cumulées': self.D_acc,
                           'D. présentes': self.D_act, 'Eliminations cumulées' : self.E_a}
        
        
        if droneModalité == "non":    
            self.df = pd.DataFrame(self.dictData, columns = ['N.Repetition', 'Jour', 'P. cumulées', 'P. présentes'])
        else:
            self.df = pd.DataFrame(self.dictData, columns = ['N.Repetition', 'Jour', 'P. cumulées', 'P. présentes',
                                                         'D. cumulées', 'D. présentes', 'Eliminations cumulées'])
        
        self.df.to_csv(nom, index = False)

    def statsMaxJours(self, droneModalité):
        '''
        Calcul des statistiques desciptifs (comme moyenne, valeur maximale, valeur minimale, écart type) 
        sur les variables mentioné ci-dessus.
        '''
        self.maxjours_df = self.df.iloc[self.df.groupby('N.Repetition').agg(max_ = ('Jour', lambda data: data.idxmax())).max_]
        self.maxjours_df = self.maxjours_df[self.maxjours_df['Jour'] < 360]

        #self.maxjours_df.to_csv('ejemplo.csv',index = False)
        self.Jmin = self.maxjours_df['Jour'].min()
        self.Jmax = self.maxjours_df['Jour'].max()
        self.Jmean = self.maxjours_df['Jour'].mean()
        self.Jstd = self.maxjours_df['Jour'].std()
        self.Jcount = self.maxjours_df['Jour'].count()

        self.PcumMin = self.maxjours_df['P. cumulées'].min()
        self.PcumMax = self.maxjours_df['P. cumulées'].max()
        self.PcumMean = self.maxjours_df['P. cumulées'].mean()
        self.PcumStd = self.maxjours_df['P. cumulées'].std()

        if droneModalité == "oui":

            self.DcumMin = self.maxjours_df['D. cumulées'].min()
            self.DcumMax = self.maxjours_df['D. cumulées'].max()
            self.DcumMean = self.maxjours_df['D. cumulées'].mean()
            self.DcumStd = self.maxjours_df['D. cumulées'].std()

            self.EcumMin = self.maxjours_df['Eliminations cumulées'].min()
            self.EcumMax = self.maxjours_df['Eliminations cumulées'].max()
            self.EcumMean = self.maxjours_df['Eliminations cumulées'].mean()
            self.EcumStd = self.maxjours_df['Eliminations cumulées'].std()
    
    def histograms(self,droneModalité):
        jourFigure = self.maxjours_df['Jour'].value_counts().plot(kind='bar', title = r"Jour où les cirses ont envahi plus de 95 % de la parcelle")
        jourFigure.set_xlabel("Jour")
        jourFigure.set_ylabel("Frequency")
        jourFigurePDF = jourFigure.get_figure()
        jourFigurePDF.savefig(f'Jours_fréquence{self.marktime}.pdf')
        plt.close(jourFigurePDF)

        pFigure = self.maxjours_df['P. cumulées'].value_counts().plot(kind='bar', title = r"Quantité de plantes accumulées")
        pFigure.set_xlabel("Cirses cumulées ")
        pFigure.set_ylabel("Frequency")
        pFigurePDF = pFigure.get_figure()
        pFigurePDF.savefig(f'Cirses_cumulées{self.marktime}.pdf')
        plt.close(pFigurePDF)

        if droneModalité == "oui":

            dFigure = self.maxjours_df['D. cumulées'].value_counts().plot(kind='bar', title = r"Quantité de plantes detectés")
            dFigure.set_xlabel("Cirses detectés cumulées ")
            dFigure.set_ylabel("Frequency")
            dFigurePDF = dFigure.get_figure()
            dFigurePDF.savefig(f'Cirses_detecteés{self.marktime}.pdf')
            plt.close(dFigurePDF)

            eFigure = self.maxjours_df['D. cumulées'].value_counts().plot(kind='bar', title = r"Quantité de plantes éliminés")
            eFigure.set_xlabel("Cirses éliminés cumulées ")
            eFigure.set_ylabel("Frequency")
            eFigurePDF = eFigure.get_figure()
            eFigurePDF.savefig(f'Cirses_éliminés{self.marktime}.pdf')
            plt.close(eFigurePDF)



