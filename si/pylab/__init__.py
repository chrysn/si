from __future__ import absolute_import, division
from pylab import plot, show, xlabel, ylabel, text, xlim, ylim, sign
from si import MakesNoSense

class Plot(object):
    """Glue-code wrapper between pylab (matplotlib) and si. One plot can only have one SI unit per dimension, so you can plot without having to worry about dimensions.
    
    Does not yet enforce anything about to which window you plot. (You can have two objects simultaneously and show them at the same time.)
    
    >>> from si.common import *
    >>> p = Plot(s, m)
    >>> t = [ms*_x for _x in xrange(200)] # numeric arrays not supported yet.
    >>> g = 10*N/kg
    >>> y = [90*cm - (_t**2 * g / 2) for _t in t]
    >>> p.plot(t, y)
    >>> # p.show()
    """
    def __init__(self, xunit, yunit):
        self.xunit = xunit
        self.yunit = yunit

        self.xlim = None
        self.ylim = None

    def _x2number(self, x):
        if hasattr(self.xunit, "using"):
            return x.using(self.xunit)
        else:
            return x/self.xunit

    def _y2number(self, y):
        if hasattr(self.yunit, "using"):
            return y.using(self.yunit)
        else:
            return y/self.yunit

    def plot(self, x, y, *args, **kwords):
        """Like pylab.plot()."""
        try:
            x = [self._x2number(_x) for _x in x]
            y = [self._y2number(_y) for _y in y]
        except MakesNoSense:
            raise Exception, "units don't match."
        plot(x,y,*args,**kwords)

    def show(self):
        """Like pylab.show()."""
        self.lim()
        show()

    def xlabel(self, label, unit = None):
        """Set x label; use unit to state that label contains an assertion about the unit.
        
        >>> from si.common import *
        >>> p = Plot(s, m)
        >>> p.xlabel("Time (in hours)",h)
        Traceback (most recent call last):
            ...
        AssertionError: Plot unit does not match label unit.
        """
        if unit: assert unit == self.xunit, "Plot unit does not match label unit."
        xlabel(label)

    def ylabel(self, label, unit = None):
        """Set y label; use unit to state that label contains an assertion about the unit.
        
        >>> from si.common import *
        >>> p = Plot(s, m)
        >>> p.ylabel("Length (in metre)",m)
        """
        if unit: assert unit == self.yunit, "Plot unit does not match label unit."
        ylabel(label)

    def text(self, x, y, label):
        """Like pylab.text()."""
        try:
            x = self._x2number(x)
            y = self._y2number(y)
        except MakesNoSense:
            raise Exception, "units don't match."
        text(x,y,label)

    def arrowhead(self, (x,y), (dirx,diry)):
        """Plot an arrowhead with its tip in (x,y) coming from the direction of (dirx,diry) (without units, only direction).""" # FIXME: provide an interface for the non-pylab matplotlib api
        self.lim()

        xsize = (xlim()[1] - xlim()[0]) / 200
        ysize = (ylim()[1] - ylim()[0]) / 200

        if diry:
            raise NotImplementedError, "only left/right supportet until ow"

        x,y = self._x2number(x), self._y2number(y)

        plot([x,x+xsize*sign(dirx)],[y,y+ysize], 'k-')
        plot([x,x+xsize*sign(dirx)],[y,y-ysize], 'k-')

    def lim(self, x=None, y=None):
        """Set the plotting range (like xlim and ylim together).
        
        >>> from si.common import *
        >>> p = Plot(s,m)
        >>> p.lim(x=(1*min,5*min))"""
        if x: self.xlim = (self._x2number(x[0]), self._x2number(x[1]))
        if y: self.ylim = (self._y2number(y[0]), self._y2number(y[1]))

        xlim(self.xlim)
        ylim(self.ylim)

    def xc0(self):
        """Return coordinate of left plot side (for drawing lines without changing the automatic scale)"""
        self.lim()
        return self.xunit * xlim()[0]

    def yc0(self):
        """Return coordinate of bottom plot side (for drawing lines without changing the automatic scale)"""
        self.lim()
        return self.yunit * ylim()[0]
