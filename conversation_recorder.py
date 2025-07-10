"""
Conversation Recorder with audio continuity validation and gap detection.
Addresses recording quality issues and audio cutting problems.
"""

import time
import logging
import threading
from typing import List, Optional, Dict, Any, Tuple
from collections import deque
import os


class ConversationRecorder:
    """
    Enhanced conversation recorder with audio continuity validation.
    
    Features:
    - Audio continuity validation
    - Gap detection and filling
    - Recording quality metrics
    - Synchronized multi-agent recording
    """
    
    def __init__(self, output_dir: str = "recordings", max_gap_ms: int = 100):
        self.output_dir = output_dir
        self.max_gap_ms = max_gap_ms
        self.max_gap_seconds = max_gap_ms / 1000.0
        
        # Recording state
        self.is_recording = False
        self.start_time = None
        self.last_chunk_time = None
        
        # Audio data storage
        self.audio_chunks = deque()
        self.chunk_timestamps = deque()
        self.agent_data = {}  # Per-agent data storage
        
        # Quality metrics
        self.total_chunks = 0
        self.gap_count = 0
        self.filled_gaps = 0
        self.total_silence_added = 0
        self.quality_score = 1.0
        
        # Gap detection
        self.gap_threshold = 0.080  # 80ms gap threshold
        self.silence_chunk_size = 1024  # Size of silence chunks
        
        # Thread safety
        self._lock = threading.Lock()
        
        # Setup logging
        self.logger = logging.getLogger("ConversationRecorder")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
    
    def start_recording(self, session_id: str = None):
        """
        Start recording a conversation session.
        
        Args:
            session_id: Optional session identifier
        """
        with self._lock:
            if self.is_recording:
                self.logger.warning("Recording already in progress")
                return
            
            self.is_recording = True
            self.start_time = time.time()
            self.last_chunk_time = self.start_time
            
            # Clear previous data
            self.audio_chunks.clear()
            self.chunk_timestamps.clear()
            self.agent_data.clear()
            
            # Reset metrics
            self.total_chunks = 0
            self.gap_count = 0
            self.filled_gaps = 0
            self.total_silence_added = 0
            self.quality_score = 1.0
            
            session_id = session_id or f"session_{int(self.start_time)}"
            self.session_id = session_id
            
            self.logger.info(f"Started recording session: {session_id}")
    
    def stop_recording(self) -> str:
        """
        Stop recording and save the session.
        
        Returns:
            Path to the saved recording file
        """
        with self._lock:
            if not self.is_recording:
                self.logger.warning("No recording in progress")
                return None
            
            self.is_recording = False
            end_time = time.time()
            duration = end_time - self.start_time
            
            # Calculate final quality score
            self._calculate_quality_score()
            
            # Save recording
            output_path = self._save_recording()
            
            self.logger.info(
                f"Stopped recording session: {self.session_id}, "
                f"Duration: {duration:.2f}s, "
                f"Quality: {self.quality_score:.2f}, "
                f"Saved to: {output_path}"
            )
            
            return output_path
    
    def add_audio(self, agent_name: str, chunk: bytes, timestamp: float) -> bool:
        """
        Add audio chunk with continuity validation.
        
        Args:
            agent_name: Name of the agent providing the chunk
            chunk: Audio chunk data
            timestamp: Chunk timestamp
            
        Returns:
            True if chunk was added successfully
        """
        if not self.is_recording:
            return False
        
        with self._lock:
            current_time = time.time()
            
            # Initialize agent data if needed
            if agent_name not in self.agent_data:
                self.agent_data[agent_name] = {
                    'chunks': deque(),
                    'timestamps': deque(),
                    'last_timestamp': timestamp,
                    'chunk_count': 0,
                    'gap_count': 0,
                    'continuity_score': 1.0
                }
            
            agent_data = self.agent_data[agent_name]
            
            # Check for gaps in audio continuity
            if agent_data['last_timestamp'] is not None:
                time_gap = timestamp - agent_data['last_timestamp']
                
                if time_gap > self.gap_threshold:
                    self._handle_audio_gap(agent_name, time_gap, timestamp)
            
            # Add chunk to agent's data
            agent_data['chunks'].append(chunk)
            agent_data['timestamps'].append(timestamp)
            agent_data['last_timestamp'] = timestamp
            agent_data['chunk_count'] += 1
            
            # Add to main recording
            self.audio_chunks.append({
                'agent': agent_name,
                'data': chunk,
                'timestamp': timestamp,
                'receive_time': current_time
            })
            self.chunk_timestamps.append(timestamp)
            
            self.total_chunks += 1
            self.last_chunk_time = timestamp
            
            # Validate continuity
            self._validate_continuity(agent_name)
            
            return True
    
    def _handle_audio_gap(self, agent_name: str, gap_duration: float, timestamp: float):
        """
        Handle detected audio gap by adding silence.
        
        Args:
            agent_name: Name of the agent with gap
            gap_duration: Duration of gap in seconds
            timestamp: Current timestamp
        """
        self.gap_count += 1
        self.agent_data[agent_name]['gap_count'] += 1
        
        # Only fill gaps up to maximum threshold
        if gap_duration <= self.max_gap_seconds:
            # Calculate number of silence chunks needed
            expected_interval = 0.064  # 64ms expected interval
            silence_chunks_needed = int(gap_duration / expected_interval)
            
            # Add silence chunks
            for i in range(silence_chunks_needed):
                silence_timestamp = timestamp - gap_duration + (i * expected_interval)
                silence_chunk = b'\x00' * self.silence_chunk_size
                
                self.audio_chunks.append({
                    'agent': agent_name,
                    'data': silence_chunk,
                    'timestamp': silence_timestamp,
                    'receive_time': time.time(),
                    'is_silence_fill': True
                })
                
                self.total_silence_added += len(silence_chunk)
            
            self.filled_gaps += 1
            self.logger.debug(
                f"Filled {gap_duration*1000:.1f}ms gap for {agent_name} "
                f"with {silence_chunks_needed} silence chunks"
            )
        else:
            self.logger.warning(
                f"Gap too large to fill: {gap_duration*1000:.1f}ms for {agent_name}"
            )
    
    def _validate_continuity(self, agent_name: str):
        """
        Validate audio continuity for an agent.
        
        Args:
            agent_name: Name of the agent to validate
        """
        agent_data = self.agent_data[agent_name]
        
        if len(agent_data['timestamps']) < 2:
            return
        
        # Calculate continuity score based on timing consistency
        timestamps = list(agent_data['timestamps'])[-10:]  # Last 10 chunks
        if len(timestamps) < 2:
            return
        
        intervals = []
        for i in range(1, len(timestamps)):
            intervals.append(timestamps[i] - timestamps[i-1])
        
        expected_interval = 0.064  # 64ms
        
        # Calculate how many intervals are within acceptable range
        acceptable_count = 0
        for interval in intervals:
            if abs(interval - expected_interval) < 0.020:  # 20ms tolerance
                acceptable_count += 1
        
        # Update continuity score
        if intervals:
            continuity_score = acceptable_count / len(intervals)
            agent_data['continuity_score'] = continuity_score
    
    def _calculate_quality_score(self):
        """Calculate overall recording quality score."""
        if not self.agent_data:
            self.quality_score = 0.0
            return
        
        # Base score starts at 1.0
        score = 1.0
        
        # Penalize gaps
        if self.total_chunks > 0:
            gap_ratio = self.gap_count / self.total_chunks
            score -= gap_ratio * 0.3  # Max 30% penalty for gaps
        
        # Consider agent continuity scores
        continuity_scores = [
            agent_data['continuity_score'] 
            for agent_data in self.agent_data.values()
        ]
        
        if continuity_scores:
            avg_continuity = sum(continuity_scores) / len(continuity_scores)
            score = (score + avg_continuity) / 2  # Weight continuity heavily
        
        # Penalize excessive silence
        if self.total_chunks > 0:
            silence_ratio = self.total_silence_added / (self.total_chunks * 1024)
            if silence_ratio > 0.1:  # More than 10% silence
                score -= (silence_ratio - 0.1) * 0.2
        
        self.quality_score = max(0.0, min(1.0, score))
    
    def _save_recording(self) -> str:
        """
        Save recording to file.
        
        Returns:
            Path to saved file
        """
        output_path = os.path.join(
            self.output_dir,
            f"{self.session_id}_recording.data"
        )
        
        # In a real implementation, you would save audio data in proper format
        # For now, we'll save metadata and statistics
        recording_data = {
            'session_id': self.session_id,
            'start_time': self.start_time,
            'duration': time.time() - self.start_time,
            'total_chunks': self.total_chunks,
            'gap_count': self.gap_count,
            'filled_gaps': self.filled_gaps,
            'quality_score': self.quality_score,
            'agents': {}
        }
        
        for agent_name, agent_data in self.agent_data.items():
            recording_data['agents'][agent_name] = {
                'chunk_count': agent_data['chunk_count'],
                'gap_count': agent_data['gap_count'],
                'continuity_score': agent_data['continuity_score']
            }
        
        # Save metadata (in a real system, also save audio data)
        with open(output_path, 'w') as f:
            import json
            json.dump(recording_data, f, indent=2)
        
        return output_path
    
    def get_recording_stats(self) -> Dict[str, Any]:
        """
        Get current recording statistics.
        
        Returns:
            Dictionary with recording statistics
        """
        with self._lock:
            if not self.is_recording:
                return {'status': 'not_recording'}
            
            current_time = time.time()
            duration = current_time - self.start_time
            
            agent_stats = {}
            for agent_name, agent_data in self.agent_data.items():
                agent_stats[agent_name] = {
                    'chunk_count': agent_data['chunk_count'],
                    'gap_count': agent_data['gap_count'],
                    'continuity_score': agent_data['continuity_score']
                }
            
            return {
                'status': 'recording',
                'session_id': self.session_id,
                'duration': duration,
                'total_chunks': self.total_chunks,
                'gap_count': self.gap_count,
                'filled_gaps': self.filled_gaps,
                'quality_score': self.quality_score,
                'agents': agent_stats
            }
    
    def get_agent_synchronization_stats(self) -> Dict[str, Any]:
        """
        Get agent synchronization statistics.
        
        Returns:
            Dictionary with synchronization statistics
        """
        with self._lock:
            if len(self.agent_data) < 2:
                return {'status': 'insufficient_agents'}
            
            agent_names = list(self.agent_data.keys())
            sync_stats = {}
            
            # Compare chunk counts between agents
            chunk_counts = [
                self.agent_data[name]['chunk_count'] 
                for name in agent_names
            ]
            
            sync_stats['chunk_count_variance'] = max(chunk_counts) - min(chunk_counts)
            
            # Calculate timing synchronization
            if len(agent_names) >= 2:
                agent1_timestamps = list(self.agent_data[agent_names[0]]['timestamps'])
                agent2_timestamps = list(self.agent_data[agent_names[1]]['timestamps'])
                
                # Find timing differences
                min_len = min(len(agent1_timestamps), len(agent2_timestamps))
                if min_len > 0:
                    time_diffs = [
                        abs(agent1_timestamps[i] - agent2_timestamps[i])
                        for i in range(min_len)
                    ]
                    
                    avg_sync_diff = sum(time_diffs) / len(time_diffs)
                    max_sync_diff = max(time_diffs)
                    
                    sync_stats['average_sync_difference'] = avg_sync_diff
                    sync_stats['max_sync_difference'] = max_sync_diff
            
            return sync_stats