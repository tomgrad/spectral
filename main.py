import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
from PySide6.QtCore import Slot, QUrl, QTimer
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

        # Initialize drawing mask
        self.draw_mask = None
        
        # Display update throttling
        self.display_needs_update = False
        self.display_timer = QTimer()
        self.display_timer.timeout.connect(self._throttled_display_update)
        self.display_timer.setInterval(50)  # Update every 50ms max
        self.display_timer.start()

        self._loadAudio('audio/parowki.wav')
        self.plotView.plot(x=self.time_axis, y=self.data)
        self.plotView.setLabel('bottom', 'Time', units='s')
        self.plotView.setLabel('left', 'Amplitude')
        
        # Set histogram checkbox to off by default
        self.histogramCheckBox.setChecked(False)
        self.imageView.ui.histogram.hide()
        
        # Set Log scale as default (before displaying spectrogram)
        self.scaleComboBox.setCurrentIndex(1)  # Log is at index 1
        
        # Now display with correct scale
        self._display_spectrogram()

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
        self.regenerateButton.clicked.connect(self.regenerateSpectrogram)
        self.zeroPhaseButton.clicked.connect(self.setPhaseToZero)
        self.randomPhaseButton.clicked.connect(self.setPhaseToRandom)
        self.reconstructPhaseButton.clicked.connect(self.reconstructPhase)
        self.histogramCheckBox.stateChanged.connect(self.toggleHistogram)
        self.scaleComboBox.currentIndexChanged.connect(self.onScaleChanged)
        self.imageView.dragCoordinates.connect(self._handle_drag_coordinates)

    def onMediaError(self, error):
        print(f"Media Error: {self.player.errorString()}")

    def toggleHistogram(self, state):
        """Toggle histogram visibility based on checkbox state."""
        if state:  # Checkbox is checked
            self.imageView.ui.histogram.show()
        else:  # Checkbox is unchecked
            self.imageView.ui.histogram.hide()
    
    def onScaleChanged(self, index):
        """Handle spectrogram scale change."""
        self._display_spectrogram()
    
    def _throttled_display_update(self):
        """Update display only if needed (called by timer)."""
        if self.display_needs_update:
            self._display_spectrogram()
            self.display_needs_update = False
    
    def _request_display_update(self):
        """Request a display update (will be throttled)."""
        self.display_needs_update = True
    
    def _display_spectrogram(self):
        """Display spectrogram with currently selected scale."""
        if self.Sxx is None:
            return
        
        # Apply mask to spectrogram if it exists (for display only)
        if self.draw_mask is not None:
            # Efficient masked copy using np.where
            spec_to_display = np.where(np.isnan(self.draw_mask), self.Sxx, self.draw_mask)
        else:
            # No mask - use original spectrogram directly (no copy)
            spec_to_display = self.Sxx
        
        # Apply selected scale for display
        display_spec = self._apply_scale(spec_to_display)
        
        # For Mel scale, create a fake frequency array that matches the Mel bins
        scale_type = self.scaleComboBox.currentText()
        if scale_type == "Mel":
            n_mels = display_spec.shape[0]
            # Create frequencies array for Mel bins (0 to n_mels-1)
            frequencies_for_display = np.arange(n_mels)
        else:
            # Use original frequencies for Linear/Log scales
            frequencies_for_display = self.frequencies
        
        # Display scaled spectrogram
        self.imageView.show(frequencies_for_display, self.times, display_spec)
        
        # Update Y-axis labels based on scale
        if scale_type == "Mel":
            n_mels = display_spec.shape[0]
            self.imageView.set_mel_ticks(n_mels, sr=self.sampling_rate)
        else:
            self.imageView.set_linear_ticks()
    
    def _apply_scale(self, magnitude_spec):
        """Apply selected scale to magnitude spectrogram.
        
        Note: imageView.show() automatically applies log scaling (10*log10).
        We compensate for this based on the selected scale:
        - Linear: Apply inverse log so display shows linear magnitude
        - Log: Use raw magnitude so log application gives us dB
        - Mel: Convert to Mel scale then apply log
        """
        scale_type = self.scaleComboBox.currentText()
        
        if scale_type == "Linear":
            # Apply inverse log to counteract imageView's log application
            # Result: 10*log10(10^(magnitude/10)) = magnitude (linear scale)
            return 10.0 ** (magnitude_spec / 10.0)
        elif scale_type == "Log":
            # Use raw magnitude - imageView will apply log to get dB scale
            return magnitude_spec
        elif scale_type == "Mel":
            return self._to_mel_scale(magnitude_spec)
        else:
            return magnitude_spec
    
    def _to_mel_scale(self, magnitude_spec):
        """Convert linear spectrogram to Mel scale."""
        if not hasattr(self, 'mel_fb'):
            # Create Mel filterbank on first use
            n_fft = (magnitude_spec.shape[0] - 1) * 2
            self.mel_fb = self._create_mel_filterbank(n_fft)
        
        # Apply Mel filterbank
        mel_spec = self.mel_fb @ magnitude_spec
        
        # Ensure no NaN values
        mel_spec = np.nan_to_num(mel_spec, nan=1e-10, posinf=1e-10, neginf=1e-10)
        mel_spec = np.maximum(mel_spec, 1e-10)  # Ensure positive values
        
        return mel_spec
    
    def _create_mel_filterbank(self, n_fft, n_mels=128):
        """Create Mel-scale filterbank matrix."""
        sr = self.sampling_rate
        f_max = sr / 2
        freqs = np.linspace(0, f_max, n_fft // 2 + 1)
        
        # Convert Hz to Mel
        def hz_to_mel(hz):
            return 2595 * np.log10(1 + hz / 700)
        
        def mel_to_hz(mel):
            return 700 * (10 ** (mel / 2595) - 1)
        
        f_min_mel = hz_to_mel(0)
        f_max_mel = hz_to_mel(f_max)
        mel_points = np.linspace(f_min_mel, f_max_mel, n_mels + 2)
        hz_points = mel_to_hz(mel_points)
        
        # Create filterbank
        mel_fb = np.zeros((n_mels, len(freqs)))
        for m in range(n_mels):
            f_left = hz_points[m]
            f_center = hz_points[m + 1]
            f_right = hz_points[m + 2]
            
            left_slope = (freqs - f_left) / (f_center - f_left + 1e-10)
            right_slope = (f_right - freqs) / (f_right - f_center + 1e-10)
            mel_fb[m, :] = np.maximum(0, np.minimum(left_slope, right_slope))
        
        # Pre-compute mapping from Mel bins to frequency bins for faster drawing
        self.mel_to_freq_mapping = {}
        for mel_bin in range(n_mels):
            freq_indices = np.where(mel_fb[mel_bin] > 0)[0]
            self.mel_to_freq_mapping[mel_bin] = freq_indices
        
        return mel_fb

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
            self._display_spectrogram()

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
        
        # Apply mask to spectrogram permanently
        if self.draw_mask is not None:
            mask_valid = ~np.isnan(self.draw_mask)
            self.Sxx[mask_valid] = self.draw_mask[mask_valid]
            # Clear the mask after applying
            self.draw_mask = None
            print("Mask applied to spectrogram")
        
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
    
    def regenerateSpectrogram(self):
        """Recalculate spectrogram from current signal."""
        if not hasattr(self, 'data') or self.data is None:
            print("No audio data available")
            return
        
        # Clear mask
        self.draw_mask = None
        
        # Recalculate STFT from current data
        self.frequencies, self.times, self.Zxx = scipy.signal.stft(
            self.data,
            fs=self.sampling_rate,
            nperseg=1024,
            noverlap=512,
        )
        
        # Compute magnitude spectrogram from complex STFT
        self.Sxx = np.abs(self.Zxx)
        self.sxx_max = np.max(self.Sxx) if self.Sxx.size else 0.0
        
        # Reset phase from new STFT
        self.phase = np.angle(self.Zxx).copy()
        
        # Clear Mel filterbank cache to force regeneration
        if hasattr(self, 'mel_fb'):
            delattr(self, 'mel_fb')
        if hasattr(self, 'mel_to_freq_mapping'):
            delattr(self, 'mel_to_freq_mapping')
        
        # Update display
        self._display_spectrogram()
        print("Spectrogram regenerated from current signal")

    def _handle_drag_coordinates(self, freq_idx: int, time_idx: int):
        if self.Sxx is None:
            return

        # Initialize mask if it doesn't exist
        if self.draw_mask is None:
            self.draw_mask = np.full_like(self.Sxx, np.nan)

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
        
        # Get current scale
        current_scale = self.scaleComboBox.currentText()
        
        # Apply brush to the mask instead of actual spectrogram
        if current_scale == "Mel" and hasattr(self, 'mel_to_freq_mapping'):
            # Optimized path for Mel scale using pre-computed mapping
            for df in range(-radius, radius + 1):
                for dt in range(-radius, radius + 1):
                    # Check if within brush radius (circular brush)
                    if df*df + dt*dt <= radius*radius:
                        mel_bin = freq_idx + df
                        t = time_idx + dt
                        if 0 <= mel_bin < 128 and 0 <= t < self.Sxx.shape[1]:
                            # Use pre-computed frequency indices for this Mel bin
                            freq_indices = self.mel_to_freq_mapping[mel_bin]
                            # Vectorized assignment to mask
                            self.draw_mask[freq_indices, t] = target_amplitude
        else:
            # Linear or Log scale - direct mapping
            for df in range(-radius, radius + 1):
                for dt in range(-radius, radius + 1):
                    # Check if within brush radius (circular brush)
                    if df*df + dt*dt <= radius*radius:
                        f = freq_idx + df
                        t = time_idx + dt
                        if 0 <= f < self.Sxx.shape[0] and 0 <= t < self.Sxx.shape[1]:
                            self.draw_mask[f, t] = target_amplitude
        
        # Request display update (throttled)
        self._request_display_update()

    def _loadAudio(self, file_path):
        # Clear any existing mask when loading new audio
        self.draw_mask = None
        
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