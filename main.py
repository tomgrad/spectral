import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
from PySide6.QtCore import Slot, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
import pyqtgraph as pg
import numpy as np
import soundfile as sf
import tempfile
from pathlib import Path
from ui_mainwindow import Ui_MainWindow

import scipy

# pg.setConfigOption('background', 'w')
# pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self._loadAudio('audio/whiskey.wav')
        self.plotView.plot(x=self.time_axis, y=self.data)
        self.plotView.setLabel('bottom', 'Time', units='s')
        self.plotView.setLabel('left', 'Amplitude')
        self.imageView.show(self.frequencies, self.times, self.Sxx)
        
        # Set histogram checkbox to off by default
        self.histogramCheckBox.setChecked(False)
        self.imageView.ui.histogram.hide()

        # Create playback position lines
        self.playback_line_wave = pg.InfiniteLine(
            pos=0, angle=90, pen=pg.mkPen('r', width=2), movable=False
        )
        self.playback_line_spec = pg.InfiniteLine(
            pos=0, angle=90, pen=pg.mkPen('r', width=2), movable=False
        )
        self.plotView.addItem(self.playback_line_wave)
        self.imageView.view.addItem(self.playback_line_spec)
        self.playback_line_wave.hide()
        self.playback_line_spec.hide()

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.errorOccurred.connect(self.onMediaError)
        self.player.positionChanged.connect(self.updatePlaybackPosition)
        self.player.playbackStateChanged.connect(self.onPlaybackStateChanged)

        self.playButton.clicked.connect(self.playAudio)
        self.openButton.clicked.connect(self.openFile)
        self.exportButton.clicked.connect(self.exportAudio)
        self.reconstructButton.clicked.connect(self.reconstructSignal)
        self.zeroPhaseButton.clicked.connect(self.setPhaseToZero)
        self.randomPhaseButton.clicked.connect(self.setPhaseToRandom)
        self.reconstructPhaseButton.clicked.connect(self.reconstructPhase)
        self.histogramCheckBox.stateChanged.connect(self.toggleHistogram)
        self.imageView.dragCoordinates.connect(self._handle_drag_coordinates)

    def onMediaError(self, error):
        print(f"Media Error: {self.player.errorString()}")

    def toggleHistogram(self, state):
        """Toggle histogram visibility based on checkbox state."""
        if state:  # Checkbox is checked
            self.imageView.ui.histogram.show()
        else:  # Checkbox is unchecked
            self.imageView.ui.histogram.hide()

    def exportAudio(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Audio",
            "",
            "WAV Files (*.wav);;All Files (*)"
        )
        if file_path:
            # Ensure file has .wav extension
            if not file_path.lower().endswith('.wav'):
                file_path += '.wav'
            
            # Normalize audio to int16 range for export
            audio_data = self.data
            if np.max(np.abs(audio_data)) > 0:
                audio_data = audio_data / np.max(np.abs(audio_data))
            audio_int16 = np.int16(audio_data * 32767)
            
            # Write to file
            sf.write(file_path, audio_int16, self.sampling_rate)
            print(f"Audio exported successfully to: {file_path}")

    def openFile(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open WAV File",
            "",
            "WAV Files (*.wav);;All Files (*)"
        )
        if file_path:
            self._loadAudio(file_path)
            self.plotView.clear()
            self.plotView.addItem(self.playback_line_wave)
            self.plotView.plot(x=self.time_axis, y=self.data)
            self.playback_line_wave.hide()
            self.imageView.show(self.frequencies, self.times, self.Sxx)

    def playAudio(self):
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            sf.write(tmp.name, self.data, self.sampling_rate)
            self.player.setSource(QUrl.fromLocalFile(tmp.name))
            self.player.play()
    
    def updatePlaybackPosition(self, position):
        """Update playback line position. Position is in milliseconds."""
        if self.data is None:
            return
        
        # Convert position from milliseconds to seconds
        time_seconds = position / 1000.0
        
        # Update waveform line (position in seconds)
        self.playback_line_wave.setPos(time_seconds)
        
        # Update spectrogram line (position in time)
        self.playback_line_spec.setPos(time_seconds)
    
    def onPlaybackStateChanged(self, state):
        """Handle playback state changes to show/hide playback lines."""
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.playback_line_wave.show()
            self.playback_line_spec.show()
        else:
            # Hide lines when stopped or paused
            self.playback_line_wave.hide()
            self.playback_line_spec.hide()

    def setPhaseToZero(self):
        """Set phase to all zeros."""
        if self.Zxx is None:
            print("No audio loaded")
            return
        
        # Set phase to zero (all imaginary parts = 0)
        self.phase = np.zeros_like(self.Zxx)
        print("Phase set to zero")
        self.reconstructSignal()  # Update signal with new zero phase
    
    def setPhaseToRandom(self):
        """Set phase to random values between -π and π."""
        if self.Zxx is None:
            print("No audio loaded")
            return
        
        # Generate random phase
        self.phase = np.random.uniform(-np.pi, np.pi, self.Zxx.shape)
        print("Phase set to random")
        self.reconstructSignal()  # Update signal with new random phase
    
    def reconstructPhase(self):
        """Reconstruct phase using Griffin-Lim algorithm."""
        if self.Zxx is None or self.Sxx is None:
            print("No audio loaded")
            return
        
        n_iter = self.iterSpinBox.value()
        print(f"Reconstructing phase with {n_iter} iterations...")
        
        # Initialize phase randomly
        phase = np.random.uniform(-np.pi, np.pi, self.Sxx.shape)
        
        # Griffin-Lim iterations
        for iteration in range(n_iter):
            # Create complex STFT from magnitude and current phase estimate
            Zxx_iter = self.Sxx * np.exp(1j * phase)
            
            # Inverse STFT to get time-domain signal
            _, signal = scipy.signal.istft(
                Zxx_iter,
                fs=self.sampling_rate,
                nperseg=1024,
                noverlap=512,
            )
            
            # Forward STFT of reconstructed signal
            _, _, Zxx_reconstructed = scipy.signal.stft(
                signal,
                fs=self.sampling_rate,
                nperseg=1024,
                noverlap=512,
            )
            
            # Extract new phase estimate
            phase = np.angle(Zxx_reconstructed)
            
            if (iteration + 1) % max(1, n_iter // 10) == 0:
                print(f"  Iteration {iteration + 1}/{n_iter}")
        
        # Store reconstructed phase
        self.phase = phase
        print("Phase reconstruction completed")
        self.reconstructSignal()  # Update signal with new reconstructed phase
    
    def reconstructSignal(self):
        if self.Zxx is None or self.Sxx is None:
            print("No audio loaded")
            return
        
        # Use current phase if available, otherwise use original
        if hasattr(self, 'phase'):
            phase = self.phase
        else:
            phase = np.angle(self.Zxx)
        
        # Combine modified magnitude with phase
        Zxx_modified = self.Sxx * np.exp(1j * phase)
        
        # Reconstruct signal from modified STFT
        _, reconstructed_data = scipy.signal.istft(
            Zxx_modified,
            fs=self.sampling_rate,
            nperseg=1024,
            noverlap=512,
        )
        
        # Store reconstructed data
        self.data = reconstructed_data
        
        # Update time axis
        self.time_axis = np.arange(len(self.data)) / self.sampling_rate
        
        # Update plots
        self.plotView.clear()
        self.plotView.addItem(self.playback_line_wave)
        self.plotView.plot(x=self.time_axis, y=self.data)
        self.playback_line_wave.hide()
        
        print("Signal reconstructed successfully")

    def _handle_drag_coordinates(self, freq_idx: int, time_idx: int):
        if self.Sxx is None:
            return

        # Get radius and amplitude from spin boxes
        radius = self.brushSizeSpinBox.value()  # Interpret as radius directly
        amp = self.ampSpinBox.value()  # Range: -1 to 1
        
        # Map amplitude value from [-1, 1] to [0, 1]
        amp_normalized = (amp + 1.0) / 2.0
        
        # Calculate target amplitude in dB space
        epsilon = 1e-10  # Small value to avoid log(0)
        Sxx_dB = 10 * np.log10(self.Sxx + epsilon)
        sxx_min_dB = np.min(Sxx_dB)
        sxx_max_dB = np.max(Sxx_dB)
        
        # Calculate target in dB space
        target_dB = sxx_min_dB + amp_normalized * (sxx_max_dB - sxx_min_dB)
        
        # Convert back to linear space
        target_amplitude = 10 ** (target_dB / 10.0)
        
        # Apply brush with target amplitude
        for df in range(-radius, radius + 1):
            for dt in range(-radius, radius + 1):
                f = freq_idx + df
                t = time_idx + dt
                # Check if within brush radius (circular brush)
                if df*df + dt*dt <= radius*radius:
                    if 0 <= f < self.Sxx.shape[0] and 0 <= t < self.Sxx.shape[1]:
                        self.Sxx[f, t] = target_amplitude
        
        self.imageView.show(self.frequencies, self.times, self.Sxx)

    def _loadAudio(self, file_path):
        original_rate, data = scipy.io.wavfile.read(file_path)
        
        # Normalize audio data to float (-1.0 to 1.0)
        if data.dtype != np.float32 and data.dtype != np.float64:
            data = data.astype(np.float32) / np.iinfo(data.dtype).max
        
        # Convert stereo to mono
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)
        
        # Resample to 22050Hz if needed
        target_rate = 22050
        if original_rate != target_rate:
            num_samples = int(len(data) * target_rate / original_rate)
            data = scipy.signal.resample(data, num_samples)
        
        self.sampling_rate = target_rate
        self.data = data
        
        # Create time axis for waveform plot
        self.time_axis = np.arange(len(self.data)) / self.sampling_rate
        
        # Use complex STFT instead of spectrogram
        self.frequencies, self.times, self.Zxx = scipy.signal.stft(
            self.data,
            fs=self.sampling_rate,
            nperseg=1024,
            noverlap=512,
        )
        
        # Compute magnitude spectrogram from complex STFT
        self.Sxx = np.abs(self.Zxx)
        self.sxx_max = np.max(self.Sxx) if self.Sxx.size else 0.0
        
        # Initialize phase from original STFT
        self.phase = np.angle(self.Zxx).copy()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()