"""
AI Agent for conversation recording with enhanced receive loop stability.
Addresses timing variations and synchronization issues.
"""

import time
import threading
import logging
from typing import Optional, Callable, Dict, Any
from audio_buffer import AudioBuffer


class AIAgent:
    """
    AI Agent with enhanced audio receiving capabilities.
    
    Features:
    - Jitter buffering for variable receive timing
    - Adaptive timeout handling
    - Connection stability monitoring
    - Audio drift correction
    """
    
    def __init__(self, name: str, buffer_size: int = 5):
        self.name = name
        self.audio_buffer = AudioBuffer(initial_size=buffer_size)
        self.is_receiving = False
        self.receive_thread = None
        
        # Timing configuration
        self.expected_interval = 0.064  # 64ms expected interval
        self.adaptive_timeout = 0.080   # 80ms initial timeout
        self.min_timeout = 0.050        # 50ms minimum timeout
        self.max_timeout = 0.150        # 150ms maximum timeout
        
        # Connection monitoring
        self.connection_stable = True
        self.last_successful_receive = time.time()
        self.stability_threshold = 0.200  # 200ms threshold for stability
        
        # Callbacks
        self.on_audio_chunk = None
        self.on_connection_status = None
        
        # Statistics
        self.receive_count = 0
        self.timeout_count = 0
        self.error_count = 0
        
        # Thread safety
        self._lock = threading.Lock()
        
        # Setup logging
        self.logger = logging.getLogger(f"AIAgent_{name}")
        
    def start_receiving(self, audio_source: Callable[[], Optional[bytes]]):
        """
        Start the receive loop in a separate thread.
        
        Args:
            audio_source: Function that returns audio chunks or None
        """
        if self.is_receiving:
            return
        
        self.is_receiving = True
        self.receive_thread = threading.Thread(
            target=self._receive_loop,
            args=(audio_source,),
            daemon=True
        )
        self.receive_thread.start()
        self.logger.info(f"{self.name} started receiving audio")
    
    def stop_receiving(self):
        """Stop the receive loop."""
        self.is_receiving = False
        if self.receive_thread:
            self.receive_thread.join(timeout=1.0)
        self.logger.info(f"{self.name} stopped receiving audio")
    
    def _receive_loop(self, audio_source: Callable[[], Optional[bytes]]):
        """
        Enhanced receive loop with jitter buffering and timing stability.
        
        Args:
            audio_source: Function that returns audio chunks or None
        """
        last_receive_time = time.time()
        consecutive_timeouts = 0
        
        while self.is_receiving:
            loop_start = time.time()
            
            try:
                # Receive audio chunk with adaptive timeout
                chunk = self._receive_with_timeout(audio_source, self.adaptive_timeout)
                
                if chunk is not None:
                    # Successful receive
                    current_time = time.time()
                    
                    # Calculate receive interval
                    interval = current_time - last_receive_time
                    last_receive_time = current_time
                    
                    # Add chunk to buffer
                    self.audio_buffer.add_chunk(chunk, current_time)
                    
                    # Update statistics
                    with self._lock:
                        self.receive_count += 1
                        self.last_successful_receive = current_time
                        consecutive_timeouts = 0
                    
                    # Check connection stability
                    self._update_connection_stability(interval)
                    
                    # Adjust adaptive timeout based on timing
                    self._adjust_adaptive_timeout(interval)
                    
                    # Notify callback if registered
                    if self.on_audio_chunk:
                        self.on_audio_chunk(chunk, current_time)
                    
                    # Log timing information (for debugging)
                    if self.receive_count % 100 == 0:  # Log every 100 chunks
                        self._log_timing_stats()
                        
                else:
                    # Timeout occurred
                    with self._lock:
                        self.timeout_count += 1
                        consecutive_timeouts += 1
                    
                    # Handle consecutive timeouts
                    if consecutive_timeouts > 5:
                        self._handle_connection_loss()
                        consecutive_timeouts = 0
                    
                    # Slightly increase timeout for next attempt
                    self.adaptive_timeout = min(
                        self.adaptive_timeout * 1.1,
                        self.max_timeout
                    )
                
            except Exception as e:
                with self._lock:
                    self.error_count += 1
                self.logger.error(f"{self.name} receive error: {e}")
                time.sleep(0.010)  # Brief pause on error
            
            # Maintain consistent loop timing
            loop_duration = time.time() - loop_start
            if loop_duration < self.expected_interval:
                time.sleep(self.expected_interval - loop_duration)
    
    def _receive_with_timeout(self, audio_source: Callable[[], Optional[bytes]], 
                            timeout: float) -> Optional[bytes]:
        """
        Receive audio chunk with timeout.
        
        Args:
            audio_source: Function that returns audio chunks
            timeout: Timeout in seconds
            
        Returns:
            Audio chunk or None if timeout
        """
        start_time = time.time()
        
        # Simple timeout implementation
        # In a real system, you'd use proper async I/O or threading
        while time.time() - start_time < timeout:
            try:
                chunk = audio_source()
                if chunk is not None:
                    return chunk
                time.sleep(0.001)  # Small delay to prevent busy waiting
            except Exception:
                return None
        
        return None  # Timeout
    
    def _update_connection_stability(self, interval: float):
        """
        Update connection stability based on receive timing.
        
        Args:
            interval: Time interval between receives
        """
        # Check if interval is within acceptable range
        deviation = abs(interval - self.expected_interval)
        was_stable = self.connection_stable
        
        # Update stability status
        self.connection_stable = deviation < (self.expected_interval * 0.2)  # 20% tolerance
        
        # Notify callback if status changed
        if was_stable != self.connection_stable and self.on_connection_status:
            self.on_connection_status(self.connection_stable)
    
    def _adjust_adaptive_timeout(self, interval: float):
        """
        Adjust adaptive timeout based on recent timing.
        
        Args:
            interval: Recent receive interval
        """
        # Get timing statistics from buffer
        stats = self.audio_buffer.get_timing_stats()
        
        if stats['jitter'] > 0.010:  # High jitter
            # Increase timeout
            self.adaptive_timeout = min(
                self.adaptive_timeout * 1.05,
                self.max_timeout
            )
        elif stats['stability'] > 0.95:  # Very stable
            # Decrease timeout
            self.adaptive_timeout = max(
                self.adaptive_timeout * 0.98,
                self.min_timeout
            )
    
    def _handle_connection_loss(self):
        """Handle connection loss scenario."""
        self.logger.warning(f"{self.name} connection appears unstable")
        
        # Reset adaptive timeout
        self.adaptive_timeout = 0.080
        
        # Add silence chunks to buffer to prevent underrun
        current_time = time.time()
        silence_chunk = b'\x00' * 1024  # 1KB of silence
        self.audio_buffer.add_chunk(silence_chunk, current_time)
        
        # Notify callback
        if self.on_connection_status:
            self.on_connection_status(False)
    
    def _log_timing_stats(self):
        """Log timing statistics for debugging."""
        timing_stats = self.audio_buffer.get_timing_stats()
        buffer_stats = self.audio_buffer.get_buffer_stats()
        
        self.logger.info(
            f"{self.name} Stats - "
            f"Chunks: {self.receive_count}, "
            f"Avg Interval: {timing_stats['average_interval']*1000:.1f}ms, "
            f"Jitter: {timing_stats['jitter']*1000:.1f}ms, "
            f"Stability: {timing_stats['stability']*100:.1f}%, "
            f"Buffer: {buffer_stats['current_size']}/{buffer_stats['target_size']}, "
            f"Silence: {buffer_stats['silence_chunks']}, "
            f"Overflows: {buffer_stats['buffer_overflows']}"
        )
    
    def get_audio_chunk(self) -> Optional[dict]:
        """
        Get next audio chunk from buffer.
        
        Returns:
            Chunk data dict or None if buffer is empty
        """
        return self.audio_buffer.get_chunk()
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics.
        
        Returns:
            Dictionary with all statistics
        """
        with self._lock:
            timing_stats = self.audio_buffer.get_timing_stats()
            buffer_stats = self.audio_buffer.get_buffer_stats()
            
            return {
                'name': self.name,
                'receive_count': self.receive_count,
                'timeout_count': self.timeout_count,
                'error_count': self.error_count,
                'connection_stable': self.connection_stable,
                'adaptive_timeout': self.adaptive_timeout,
                'timing': timing_stats,
                'buffer': buffer_stats
            }
    
    def reset_statistics(self):
        """Reset all statistics."""
        with self._lock:
            self.receive_count = 0
            self.timeout_count = 0
            self.error_count = 0
            self.audio_buffer.reset_stats()
    
    def set_callbacks(self, on_audio_chunk: Optional[Callable] = None,
                     on_connection_status: Optional[Callable] = None):
        """
        Set callback functions.
        
        Args:
            on_audio_chunk: Called when audio chunk is received
            on_connection_status: Called when connection status changes
        """
        self.on_audio_chunk = on_audio_chunk
        self.on_connection_status = on_connection_status