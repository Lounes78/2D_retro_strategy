"""
Conversation Manager with audio synchronization and response handling.
Coordinates multiple AI agents and manages conversation flow.
"""

import time
import logging
import threading
from typing import Dict, List, Optional, Callable, Any
from ai_agent import AIAgent
from conversation_recorder import ConversationRecorder


class ConversationManager:
    """
    Manages conversation flow with multiple AI agents.
    
    Features:
    - Multi-agent coordination
    - Audio synchronization checks
    - Response handling with timing validation
    - Conversation flow management
    """
    
    def __init__(self, sync_tolerance_ms: int = 50):
        self.sync_tolerance_ms = sync_tolerance_ms
        self.sync_tolerance_seconds = sync_tolerance_ms / 1000.0
        
        # Agent management
        self.agents: Dict[str, AIAgent] = {}
        self.agent_order: List[str] = []
        
        # Recording
        self.recorder = ConversationRecorder()
        
        # Conversation state
        self.is_active = False
        self.current_speaker = None
        self.conversation_start_time = None
        
        # Synchronization
        self.sync_check_interval = 1.0  # Check sync every second
        self.last_sync_check = 0
        self.sync_warnings = 0
        
        # Audio response handling
        self.response_timeout = 5.0  # 5 second timeout for responses
        self.pending_responses = {}
        
        # Thread safety
        self._lock = threading.Lock()
        
        # Setup logging
        self.logger = logging.getLogger("ConversationManager")
        
        # Statistics
        self.total_responses = 0
        self.sync_violations = 0
        self.timeout_responses = 0
    
    def add_agent(self, agent_name: str, buffer_size: int = 5) -> AIAgent:
        """
        Add an AI agent to the conversation.
        
        Args:
            agent_name: Name of the agent
            buffer_size: Initial buffer size for the agent
            
        Returns:
            Created AIAgent instance
        """
        with self._lock:
            if agent_name in self.agents:
                self.logger.warning(f"Agent {agent_name} already exists")
                return self.agents[agent_name]
            
            agent = AIAgent(agent_name, buffer_size)
            
            # Set up callbacks
            agent.set_callbacks(
                on_audio_chunk=lambda chunk, timestamp, name=agent_name: 
                    self._handle_audio_chunk(name, chunk, timestamp),
                on_connection_status=lambda status, name=agent_name: 
                    self._handle_connection_status(name, status)
            )
            
            self.agents[agent_name] = agent
            self.agent_order.append(agent_name)
            
            self.logger.info(f"Added agent: {agent_name}")
            return agent
    
    def remove_agent(self, agent_name: str):
        """
        Remove an agent from the conversation.
        
        Args:
            agent_name: Name of the agent to remove
        """
        with self._lock:
            if agent_name not in self.agents:
                self.logger.warning(f"Agent {agent_name} not found")
                return
            
            # Stop the agent
            self.agents[agent_name].stop_receiving()
            
            # Remove from tracking
            del self.agents[agent_name]
            if agent_name in self.agent_order:
                self.agent_order.remove(agent_name)
            
            self.logger.info(f"Removed agent: {agent_name}")
    
    def start_conversation(self, session_id: str = None):
        """
        Start a conversation session.
        
        Args:
            session_id: Optional session identifier
        """
        with self._lock:
            if self.is_active:
                self.logger.warning("Conversation already active")
                return
            
            if not self.agents:
                self.logger.error("No agents available for conversation")
                return
            
            self.is_active = True
            self.conversation_start_time = time.time()
            self.current_speaker = self.agent_order[0] if self.agent_order else None
            
            # Start recording
            self.recorder.start_recording(session_id)
            
            # Start all agents
            for agent in self.agents.values():
                # In a real implementation, you'd provide actual audio source
                agent.start_receiving(self._mock_audio_source)
            
            self.logger.info(f"Started conversation with {len(self.agents)} agents")
    
    def stop_conversation(self) -> str:
        """
        Stop the conversation session.
        
        Returns:
            Path to saved recording
        """
        with self._lock:
            if not self.is_active:
                self.logger.warning("No active conversation")
                return None
            
            self.is_active = False
            
            # Stop all agents
            for agent in self.agents.values():
                agent.stop_receiving()
            
            # Stop recording
            recording_path = self.recorder.stop_recording()
            
            # Log final statistics
            self._log_conversation_stats()
            
            self.logger.info("Stopped conversation")
            return recording_path
    
    def _handle_audio_chunk(self, agent_name: str, chunk: bytes, timestamp: float):
        """
        Handle audio chunk from an agent.
        
        Args:
            agent_name: Name of the agent
            chunk: Audio chunk data
            timestamp: Chunk timestamp
        """
        # Add to recorder
        self.recorder.add_audio(agent_name, chunk, timestamp)
        
        # Check synchronization periodically
        current_time = time.time()
        if current_time - self.last_sync_check > self.sync_check_interval:
            self._check_agent_synchronization()
            self.last_sync_check = current_time
    
    def _handle_connection_status(self, agent_name: str, is_stable: bool):
        """
        Handle connection status change from an agent.
        
        Args:
            agent_name: Name of the agent
            is_stable: Whether connection is stable
        """
        if is_stable:
            self.logger.info(f"{agent_name} connection stabilized")
        else:
            self.logger.warning(f"{agent_name} connection unstable")
    
    def _handle_audio_response(self, agent_name: str, response_data: Dict[str, Any]):
        """
        Handle audio response with synchronization checks.
        
        Args:
            agent_name: Name of the responding agent
            response_data: Response data including timing information
        """
        current_time = time.time()
        
        # Validate response timing
        if 'timestamp' in response_data:
            response_timestamp = response_data['timestamp']
            time_since_response = current_time - response_timestamp
            
            # Check if response is too old
            if time_since_response > self.response_timeout:
                self.timeout_responses += 1
                self.logger.warning(
                    f"Response from {agent_name} timed out "
                    f"({time_since_response:.2f}s old)"
                )
                return
        
        # Check synchronization with other agents
        sync_violation = self._check_response_synchronization(agent_name, response_data)
        
        if sync_violation:
            self.sync_violations += 1
            self.logger.warning(f"Sync violation detected for {agent_name}")
        
        # Process the response
        self._process_audio_response(agent_name, response_data)
        
        self.total_responses += 1
    
    def _check_agent_synchronization(self):
        """Check synchronization between agents."""
        if len(self.agents) < 2:
            return
        
        # Get latest statistics from all agents
        agent_stats = {}
        for name, agent in self.agents.items():
            stats = agent.get_statistics()
            agent_stats[name] = stats
        
        # Compare receive counts
        receive_counts = [
            stats['receive_count'] 
            for stats in agent_stats.values()
        ]
        
        if receive_counts:
            max_count = max(receive_counts)
            min_count = min(receive_counts)
            count_variance = max_count - min_count
            
            # Check if variance is too high
            if count_variance > 10:  # More than 10 chunks difference
                self.sync_warnings += 1
                self.logger.warning(
                    f"Agent synchronization issue: "
                    f"chunk count variance = {count_variance}"
                )
                
                # Log per-agent details
                for name, stats in agent_stats.items():
                    self.logger.debug(
                        f"{name}: {stats['receive_count']} chunks, "
                        f"buffer: {stats['buffer']['current_size']}, "
                        f"stability: {stats['timing']['stability']:.2f}"
                    )
    
    def _check_response_synchronization(self, agent_name: str, 
                                      response_data: Dict[str, Any]) -> bool:
        """
        Check if response is synchronized with other agents.
        
        Args:
            agent_name: Name of the responding agent
            response_data: Response data
            
        Returns:
            True if synchronization violation detected
        """
        if 'timestamp' not in response_data:
            return False
        
        response_timestamp = response_data['timestamp']
        
        # Check against other agents' recent activity
        for name, agent in self.agents.items():
            if name == agent_name:
                continue
            
            # Get recent chunk from agent
            recent_chunk = agent.get_audio_chunk()
            if recent_chunk:
                time_diff = abs(response_timestamp - recent_chunk['timestamp'])
                
                # Check if time difference exceeds tolerance
                if time_diff > self.sync_tolerance_seconds:
                    return True
        
        return False
    
    def _process_audio_response(self, agent_name: str, response_data: Dict[str, Any]):
        """
        Process audio response from an agent.
        
        Args:
            agent_name: Name of the agent
            response_data: Response data to process
        """
        # In a real implementation, you would process the audio response
        # For now, we'll just log it
        self.logger.debug(f"Processing response from {agent_name}")
    
    def _mock_audio_source(self) -> Optional[bytes]:
        """
        Mock audio source for testing.
        
        Returns:
            Mock audio chunk or None
        """
        # In a real implementation, this would be actual audio input
        # For testing, we'll generate mock data
        if not self.is_active:
            return None
        
        # Generate mock audio chunk
        import random
        chunk_size = random.randint(512, 1024)
        return bytes([random.randint(0, 255) for _ in range(chunk_size)])
    
    def _log_conversation_stats(self):
        """Log final conversation statistics."""
        if not self.conversation_start_time:
            return
        
        duration = time.time() - self.conversation_start_time
        recording_stats = self.recorder.get_recording_stats()
        
        self.logger.info(
            f"Conversation Statistics:\n"
            f"  Duration: {duration:.2f}s\n"
            f"  Total Responses: {self.total_responses}\n"
            f"  Sync Violations: {self.sync_violations}\n"
            f"  Timeout Responses: {self.timeout_responses}\n"
            f"  Sync Warnings: {self.sync_warnings}\n"
            f"  Recording Quality: {recording_stats.get('quality_score', 0):.2f}"
        )
        
        # Log per-agent statistics
        for name, agent in self.agents.items():
            stats = agent.get_statistics()
            self.logger.info(
                f"  {name}: {stats['receive_count']} chunks, "
                f"stability: {stats['timing']['stability']:.2f}"
            )
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """
        Get current conversation statistics.
        
        Returns:
            Dictionary with conversation statistics
        """
        with self._lock:
            if not self.is_active:
                return {'status': 'inactive'}
            
            duration = time.time() - self.conversation_start_time
            recording_stats = self.recorder.get_recording_stats()
            sync_stats = self.recorder.get_agent_synchronization_stats()
            
            agent_stats = {}
            for name, agent in self.agents.items():
                agent_stats[name] = agent.get_statistics()
            
            return {
                'status': 'active',
                'duration': duration,
                'total_responses': self.total_responses,
                'sync_violations': self.sync_violations,
                'timeout_responses': self.timeout_responses,
                'sync_warnings': self.sync_warnings,
                'recording': recording_stats,
                'synchronization': sync_stats,
                'agents': agent_stats
            }
    
    def get_agent_names(self) -> List[str]:
        """Get list of agent names."""
        return list(self.agents.keys())
    
    def get_agent(self, agent_name: str) -> Optional[AIAgent]:
        """
        Get agent by name.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            AIAgent instance or None if not found
        """
        return self.agents.get(agent_name)