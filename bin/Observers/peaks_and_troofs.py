import math
import copy

from backtrader.observer import Observer


class PeaksAndTroofs(Observer):
    lines = ('peak', 'troof',)

    plotinfo = dict(plot=True, subplot=False, plotlinelabels=True)
    plotlines = dict(
        peak=dict(marker='v', markersize=8.0, color='purple',
                 fillstyle='full', ls=''),
        troof=dict(marker='^', markersize=8.0, color='blue',
                  fillstyle='full', ls='')
    )

    params = (
        ('barplot', False),  # plot above/below max/min for clarity in bar plot
        ('bardist', 0.015),  # distance to max/min in absolute perc
    )

    typepoint = []
    yvaluepoint = []
    index = []

    def next(self):

        if self.yvaluepoint != [] and self.typepoint != [] and self.index != []:

            for i in range(len(self.index)):

                if self.typepoint[i] == 'peak':
                    self.lines.peak[self.index[i]] = copy.deepcopy(self.yvaluepoint[i])

                elif self.typepoint == 'troof':
                    self.lines.troof[self.index[i]] = copy.deepcopy(self.yvaluepoint[i])

            # self.typepoint = []
            # self.yvaluepoint = []
            # self.index = []
 

    def addpoint(self, index, typepoint, yvalue):
        self.typepoint.append(copy.deepcopy(typepoint))
        self.yvaluepoint.append(copy.deepcopy(yvalue))
        self.index.append(copy.deepcopy(index))