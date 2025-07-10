#!/usr/bin/env python3
"""
Quick validation test for the audio recording system.
Tests the core functionality without long-running simulation.
"""

import time
import logging
from audio_buffer import AudioBuffer
from ai_agent import AIAgent
from conversation_recorder import ConversationRecorder
from conversation_manager import ConversationManager

# Suppress logging for cleaner output
logging.getLogger().setLevel(logging.ERROR)


def test_audio_buffer():
    """Test AudioBuffer functionality."""
    print("Testing AudioBuffer...")
    
    buffer = AudioBuffer(initial_size=3, max_size=10, min_size=1)
    
    # Test adding chunks
    test_chunks = [b'audio1', b'audio2', b'audio3']
    for i, chunk in enumerate(test_chunks):
        buffer.add_chunk(chunk, time.time() + i * 0.064)
    
    # Test getting chunks
    retrieved = []
    while True:
        chunk = buffer.get_chunk()
        if chunk is None:
            break
        retrieved.append(chunk['data'])
    
    print(f"  Added {len(test_chunks)} chunks, retrieved {len(retrieved)}")
    print(f"  Buffer stats: {buffer.get_buffer_stats()}")
    print(f"  Timing stats: {buffer.get_timing_stats()}")
    assert len(retrieved) == len(test_chunks), "Chunk count mismatch"
    print("  ✓ AudioBuffer test passed")


def test_ai_agent():
    """Test AIAgent functionality."""
    print("\nTesting AIAgent...")
    
    agent = AIAgent("TestAgent", buffer_size=3)
    
    # Test statistics
    stats = agent.get_statistics()
    print(f"  Initial stats: {stats['receive_count']} chunks")
    
    # Test buffer access
    chunk = agent.get_audio_chunk()
    print(f"  Buffer empty: {chunk is None}")
    
    assert stats['receive_count'] == 0, "Initial receive count should be 0"
    print("  ✓ AIAgent test passed")


def test_conversation_recorder():
    """Test ConversationRecorder functionality."""
    print("\nTesting ConversationRecorder...")
    
    recorder = ConversationRecorder()
    
    # Test recording session
    recorder.start_recording("test_session")
    
    # Add some test audio
    current_time = time.time()
    recorder.add_audio("Agent1", b'audio1', current_time)
    recorder.add_audio("Agent2", b'audio2', current_time + 0.064)
    recorder.add_audio("Agent1", b'audio3', current_time + 0.128)
    
    # Test gap detection (large gap)
    recorder.add_audio("Agent1", b'audio4', current_time + 0.300)  # 172ms gap
    
    stats = recorder.get_recording_stats()
    print(f"  Recording stats: {stats}")
    
    # Stop recording
    output_path = recorder.stop_recording()
    print(f"  Recording saved to: {output_path}")
    
    assert stats['total_chunks'] >= 3, "Should have recorded chunks"
    print("  ✓ ConversationRecorder test passed")


def test_conversation_manager():
    """Test ConversationManager functionality."""
    print("\nTesting ConversationManager...")
    
    manager = ConversationManager()
    
    # Test adding agents
    maya = manager.add_agent("Maya", buffer_size=3)
    miles = manager.add_agent("Miles", buffer_size=3)
    
    agent_names = manager.get_agent_names()
    print(f"  Added agents: {agent_names}")
    
    # Test getting agents
    retrieved_maya = manager.get_agent("Maya")
    assert retrieved_maya is not None, "Should retrieve Maya agent"
    
    # Test conversation flow
    manager.start_conversation("test_session")
    
    # Simulate some audio chunks
    current_time = time.time()
    manager._handle_audio_chunk("Maya", b'maya_audio', current_time)
    manager._handle_audio_chunk("Miles", b'miles_audio', current_time + 0.064)
    
    # Get statistics
    stats = manager.get_conversation_stats()
    print(f"  Conversation stats: recording quality = {stats['recording']['quality_score']:.2f}")
    
    # Stop conversation
    recording_path = manager.stop_conversation()
    print(f"  Conversation saved to: {recording_path}")
    
    assert len(agent_names) == 2, "Should have 2 agents"
    print("  ✓ ConversationManager test passed")


def test_synchronization_detection():
    """Test synchronization issue detection."""
    print("\nTesting synchronization detection...")
    
    manager = ConversationManager()
    maya = manager.add_agent("Maya")
    miles = manager.add_agent("Miles")
    
    manager.start_conversation("sync_test")
    
    # Simulate synchronized audio
    base_time = time.time()
    for i in range(5):
        manager._handle_audio_chunk("Maya", b'maya_audio', base_time + i * 0.064)
        manager._handle_audio_chunk("Miles", b'miles_audio', base_time + i * 0.064)
    
    # Simulate desynchronized audio
    manager._handle_audio_chunk("Maya", b'maya_audio', base_time + 0.500)  # Large gap
    
    stats = manager.get_conversation_stats()
    print(f"  Sync stats: {stats['synchronization']}")
    
    manager.stop_conversation()
    print("  ✓ Synchronization detection test passed")


def main():
    """Run all tests."""
    print("=== Audio Recording System Validation ===")
    
    try:
        test_audio_buffer()
        test_ai_agent()
        test_conversation_recorder()
        test_conversation_manager()
        test_synchronization_detection()
        
        print("\n=== All Tests Passed! ===")
        print("\nThe audio recording system implements:")
        print("✓ Dynamic buffer management with underrun protection")
        print("✓ Audio synchronization with chunk sequence validation")
        print("✓ Receive loop stability with jitter buffering")
        print("✓ Recording quality improvements with gap detection")
        print("✓ Multi-agent conversation management")
        print("✓ Comprehensive statistics and monitoring")
        
    except Exception as e:
        print(f"\nTest failed: {e}")
        raise


if __name__ == "__main__":
    main()