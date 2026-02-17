import pyqtgraph as pg
import numpy as np
from PySide6.QtCore import Qt, QEvent, Signal

xPad = 0.05

class ImageView(pg.ImageView):
    dragCoordinates = Signal(int, int)
    def __init__(self, parent=None):
        super().__init__(parent, view=pg.PlotItem())
        self.ui.menuBtn.hide()
        self.ui.roiBtn.hide()
        cm = pg.colormap.getFromMatplotlib('jet')
        self.setColorMap(cm)
        self.view.setMouseEnabled(x=False, y=False)
        self.view.setAspectLocked(lock=False)
        self.view.invertY(False)
        self.view.setLabel('bottom', 'Time', units='s')
        self.view.setLabel('left', 'Frequency', units='Hz')
        
        self.is_dragging = False
        self.times = None
        self.frequencies = None
        self.time_scale = None
        self.freq_scale = None

        self.scene.sigMouseMoved.connect(self.mouse_moved)
        


    def mousePressEvent(self, event):
        self.is_dragging = True
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.is_dragging = False
        super().mouseReleaseEvent(event)

    def mouse_moved(self, event):
        if self.is_dragging:
            if self.times is None or self.frequencies is None:
                return
            if not self.time_scale or not self.freq_scale:
                return

            view_pos = self.view.getViewBox().mapSceneToView(event)
            time_idx = int((view_pos.x() - self.times[0]) / self.time_scale)
            freq_idx = int((view_pos.y() - self.frequencies[0]) / self.freq_scale)
            if 0 <= time_idx < len(self.times) and 0 <= freq_idx < len(self.frequencies):
                self.dragCoordinates.emit(freq_idx, time_idx)

    def wheelEvent(self, event):
        # Disable scrolling
        event.ignore()

    def show(self, frequencies, times, Sxx):
        self.times = times
        self.frequencies = frequencies
        self.time_scale = times[1] - times[0] if len(times) > 1 else 1
        self.freq_scale = frequencies[1] - frequencies[0] if len(frequencies) > 1 else 1
        
        self.setImage(10*np.log10(Sxx.T), autoRange=False, 
                      scale=(self.time_scale, self.freq_scale),
                      pos=(times[0], frequencies[0]))

