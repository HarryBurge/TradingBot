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

    typepoint = [None]
    yvaluepoint = [None]

    def next(self):
        if self.yvaluepoint[-1] != None and self.typepoint[-1] != None:

            if self.typepoint[-1] == 'peak':
                self.lines.peak[0] = copy.deepcopy(self.yvaluepoint[-1])

            elif self.typepoint[-1] == 'troof':
                self.lines.troof[0] = copy.deepcopy(self.yvaluepoint[-1])

            self.typepoint.append(None)
            self.yvaluepoint.append(None)
        

    def addpoint(self, typepoint, yvalue):
        self.typepoint.append(typepoint)
        self.yvaluepoint.append(yvalue)