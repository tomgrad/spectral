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
    
    def set_mel_ticks(self, n_mels=128, sr=22050):
        """Set Y-axis ticks and range for Mel scale display with Hz frequency labels.
        
        Parameters:
        -----------
        n_mels : int
            Number of Mel bands
        sr : int
            Sampling rate in Hz
        """
        # Mel to Hz conversion functions
        def mel_to_hz(mel):
            return 700 * (10 ** (mel / 2595) - 1)
        
        # Create tick positions (Mel bin numbers)
        tick_positions = np.linspace(0, n_mels - 1, 11)  # 11 ticks
        
        # Convert Mel bin positions to frequency
        # Map Mel bins 0 to n_mels-1 to Mel scale range
        f_max = sr / 2
        f_min_mel = 2595 * np.log10(1 + 0 / 700)
        f_max_mel = 2595 * np.log10(1 + f_max / 700)
        mel_range = np.linspace(f_min_mel, f_max_mel, n_mels)
        
        # Get Hz values for each tick
        tick_freqs = [mel_to_hz(mel_range[int(pos)]) for pos in tick_positions]
        tick_labels = [f"{int(freq)}" for freq in tick_freqs]
        
        ticks = [(pos, label) for pos, label in zip(tick_positions, tick_labels)]
        self.view.getAxis('left').setTicks([ticks])
        self.view.setLabel('left', 'Frequency', units='Hz')
        
        # Set Y-axis range to match Mel bins (0 to n_mels-1)
        self.view.setYRange(0, n_mels - 1, padding=0)
    
    def set_linear_ticks(self):
        """Set Y-axis ticks for linear frequency display."""
        self.view.getAxis('left').setTicks(None)  # Reset to automatic ticks
        self.view.setLabel('left', 'Frequency', units='Hz')
        
        # Auto-scale Y-axis
        if self.frequencies is not None:
            self.view.setYRange(self.frequencies[0], self.frequencies[-1], padding=0)


