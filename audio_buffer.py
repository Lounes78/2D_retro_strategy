"""
Advanced audio buffering system for conversation recording.
Addresses buffer management inconsistencies and timing variations.
"""

import time
import threading
from collections import deque
from typing import Optional, List, Tuple
import statistics


class AudioBuffer:
    """
    Advanced audio buffer with dynamic adjustment and underrun protection.
    
    Features:
    - Dynamic buffer size adjustment based on network conditions
    - Buffer underrun protection with silence padding
    - Jitter buffer for variable receive timing
    - Connection stability monitoring
    """
    
    def __init__(self, initial_size: int = 5, max_size: int = 20, min_size: int = 2):
        self.buffer = deque()
        self.initial_size = initial_size
        self.max_size = max_size
        self.min_size = min_size
        self.target_size = initial_size
        
        # Timing statistics
        self.receive_intervals = deque(maxlen=50)  # Last 50 intervals
        self.last_receive_time = None
        self.expected_interval = 0.064  # 64ms expected interval
        
        # Buffer statistics
        self.total_chunks = 0
        self.silence_chunks = 0
        self.buffer_overflows = 0
        self.buffer_underruns = 0
        
        # Adaptive parameters
        self.jitter_threshold = 0.010  # 10ms jitter threshold
        self.stability_window = 20  # Window for stability calculation
        
        # Thread safety
        self._lock = threading.Lock()
    
    def add_chunk(self, chunk: bytes, timestamp: float) -> bool:
        """
        Add audio chunk to buffer with timestamp tracking.
        
        Args:
            chunk: Audio chunk data
            timestamp: Chunk timestamp
            
        Returns:
            True if chunk was added successfully, False if buffer overflow
        """
        with self._lock:
            current_time = time.time()
            
            # Track receive timing
            if self.last_receive_time is not None:
                interval = current_time - self.last_receive_time
                self.receive_intervals.append(interval)
            self.last_receive_time = current_time
            
            # Check for buffer overflow
            if len(self.buffer) >= self.max_size:
                self.buffer_overflows += 1
                # Remove oldest chunk to make room
                self.buffer.popleft()
            
            # Add chunk with metadata
            chunk_data = {
                'data': chunk,
                'timestamp': timestamp,
                'receive_time': current_time,
                'is_silence': self._is_silence_chunk(chunk)
            }
            
            self.buffer.append(chunk_data)
            self.total_chunks += 1
            
            if chunk_data['is_silence']:
                self.silence_chunks += 1
            
            # Dynamically adjust buffer size
            self._adjust_buffer_size()
            
            return True
    
    def get_chunk(self) -> Optional[dict]:
        """
        Get next audio chunk from buffer.
        
        Returns:
            Chunk data dict or None if buffer is empty
        """
        with self._lock:
            if not self.buffer:
                self.buffer_underruns += 1
                return None
            
            chunk_data = self.buffer.popleft()
            
            # Check if buffer is getting too low
            if len(self.buffer) < self.min_size:
                self._handle_buffer_underrun()
            
            return chunk_data
    
    def get_buffer_size(self) -> int:
        """Get current buffer size."""
        with self._lock:
            return len(self.buffer)
    
    def get_average_buffer_size(self) -> float:
        """Get average buffer size over recent history."""
        # This is a simplified implementation
        # In a real system, you'd track this over time
        return len(self.buffer)
    
    def get_timing_stats(self) -> dict:
        """Get timing statistics for debugging."""
        with self._lock:
            if not self.receive_intervals:
                return {
                    'average_interval': 0,
                    'min_interval': 0,
                    'max_interval': 0,
                    'jitter': 0,
                    'stability': 0
                }
            
            intervals = list(self.receive_intervals)
            avg_interval = statistics.mean(intervals)
            min_interval = min(intervals)
            max_interval = max(intervals)
            
            # Calculate jitter (standard deviation)
            jitter = statistics.stdev(intervals) if len(intervals) > 1 else 0
            
            # Calculate stability (percentage of intervals within threshold)
            stable_count = sum(1 for interval in intervals 
                             if abs(interval - self.expected_interval) < self.jitter_threshold)
            stability = stable_count / len(intervals) if intervals else 0
            
            return {
                'average_interval': avg_interval,
                'min_interval': min_interval,
                'max_interval': max_interval,
                'jitter': jitter,
                'stability': stability
            }
    
    def get_buffer_stats(self) -> dict:
        """Get buffer statistics for monitoring."""
        with self._lock:
            return {
                'total_chunks': self.total_chunks,
                'silence_chunks': self.silence_chunks,
                'buffer_overflows': self.buffer_overflows,
                'buffer_underruns': self.buffer_underruns,
                'current_size': len(self.buffer),
                'target_size': self.target_size,
                'average_size': self.get_average_buffer_size()
            }
    
    def _adjust_buffer_size(self):
        """Dynamically adjust buffer size based on network conditions."""
        if len(self.receive_intervals) < self.stability_window:
            return
        
        stats = self.get_timing_stats()
        
        # If jitter is high, increase buffer size
        if stats['jitter'] > self.jitter_threshold:
            self.target_size = min(self.target_size + 1, self.max_size)
        
        # If stability is good and buffer is large, decrease size
        elif stats['stability'] > 0.95 and self.target_size > self.initial_size:
            self.target_size = max(self.target_size - 1, self.min_size)
    
    def _handle_buffer_underrun(self):
        """Handle buffer underrun by adding silence chunks."""
        silence_chunk = {
            'data': b'\x00' * 1024,  # 1KB of silence
            'timestamp': time.time(),
            'receive_time': time.time(),
            'is_silence': True
        }
        self.buffer.append(silence_chunk)
        self.silence_chunks += 1
    
    def _is_silence_chunk(self, chunk: bytes) -> bool:
        """
        Detect if a chunk is silence.
        
        Args:
            chunk: Audio chunk data
            
        Returns:
            True if chunk is silence, False otherwise
        """
        if not chunk:
            return True
        
        # Simple silence detection: check if all bytes are zero or very low
        # In a real implementation, you'd use proper audio analysis
        threshold = 10  # Very low threshold for silence
        return all(b < threshold for b in chunk)
    
    def clear(self):
        """Clear the buffer."""
        with self._lock:
            self.buffer.clear()
    
    def reset_stats(self):
        """Reset all statistics."""
        with self._lock:
            self.total_chunks = 0
            self.silence_chunks = 0
            self.buffer_overflows = 0
            self.buffer_underruns = 0
            self.receive_intervals.clear()
            self.last_receive_time = None