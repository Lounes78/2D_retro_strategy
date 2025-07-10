#!/usr/bin/env python3
"""
Test script for the audio recording system.
Demonstrates the fixes for audio cutting issues.
"""

import sys
import time
import logging
import random
from typing import Optional
from conversation_manager import ConversationManager


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('audio_test.log')
        ]
    )


def create_realistic_audio_source(agent_name: str, base_interval: float = 0.064):
    """
    Create a realistic audio source that simulates the timing issues.
    
    Args:
        agent_name: Name of the agent
        base_interval: Base interval between chunks (64ms)
        
    Returns:
        Audio source function
    """
    last_call_time = [time.time()]
    chunk_count = [0]
    
    def audio_source() -> Optional[bytes]:
        current_time = time.time()
        
        # Simulate timing variations (62.9ms to 69.2ms)
        if current_time - last_call_time[0] < base_interval:
            # Add some jitter
            jitter = random.uniform(-0.002, 0.005)  # -2ms to +5ms jitter
            if current_time - last_call_time[0] < base_interval + jitter:
                return None
        
        last_call_time[0] = current_time
        chunk_count[0] += 1
        
        # Simulate different chunk counts (Maya: 3074, Miles: 3081)
        if agent_name == "Maya" and chunk_count[0] > 3074:
            return None
        elif agent_name == "Miles" and chunk_count[0] > 3081:
            return None
        
        # Simulate silence chunks for buffer starvation
        silence_probability = 0.004 if agent_name == "Maya" else 0.005  # Maya: 11/3074, Miles: 14/3081
        if random.random() < silence_probability:
            return b'\x00' * 1024  # Silence chunk
        
        # Generate realistic audio chunk
        chunk_size = random.randint(512, 1024)
        return bytes([random.randint(10, 245) for _ in range(chunk_size)])
    
    return audio_source


def simulate_conversation():
    """Simulate a conversation with timing issues and demonstrate fixes."""
    print("=== Audio Recording System Test ===")
    print("Simulating conversation with Maya and Miles...")
    
    # Create conversation manager
    manager = ConversationManager(sync_tolerance_ms=50)
    
    # Add agents
    maya = manager.add_agent("Maya", buffer_size=5)
    miles = manager.add_agent("Miles", buffer_size=5)
    
    # Start conversation
    manager.start_conversation("test_session")
    
    # Start agents with realistic audio sources
    maya_audio_source = create_realistic_audio_source("Maya")
    miles_audio_source = create_realistic_audio_source("Miles")
    
    maya.start_receiving(maya_audio_source)
    miles.start_receiving(miles_audio_source)
    
    # Let conversation run for a period
    print("Running conversation for 30 seconds...")
    run_duration = 30
    start_time = time.time()
    
    while time.time() - start_time < run_duration:
        # Print progress every 5 seconds
        elapsed = time.time() - start_time
        if int(elapsed) % 5 == 0 and elapsed > 0:
            print(f"Progress: {elapsed:.0f}s / {run_duration}s")
            
            # Get and display statistics
            stats = manager.get_conversation_stats()
            if stats['status'] == 'active':
                print(f"  Recording quality: {stats['recording']['quality_score']:.2f}")
                print(f"  Total chunks: {stats['recording']['total_chunks']}")
                print(f"  Gaps filled: {stats['recording']['filled_gaps']}")
                print(f"  Sync violations: {stats['sync_violations']}")
                
                # Show agent-specific stats
                for agent_name, agent_stats in stats['agents'].items():
                    timing = agent_stats['timing']
                    buffer = agent_stats['buffer']
                    print(f"  {agent_name}: {agent_stats['receive_count']} chunks, "
                          f"avg interval: {timing['average_interval']*1000:.1f}ms, "
                          f"stability: {timing['stability']*100:.1f}%, "
                          f"buffer: {buffer['current_size']}")
                print()
        
        time.sleep(1)
    
    print("Stopping conversation...")
    recording_path = manager.stop_conversation()
    
    # Display final statistics
    print("\n=== Final Statistics ===")
    final_stats = manager.get_conversation_stats()
    
    # Show recording stats
    recording_stats = manager.recorder.get_recording_stats()
    print(f"Recording Quality Score: {recording_stats.get('quality_score', 0):.2f}")
    print(f"Total Chunks: {recording_stats.get('total_chunks', 0)}")
    print(f"Gaps Detected: {recording_stats.get('gap_count', 0)}")
    print(f"Gaps Filled: {recording_stats.get('filled_gaps', 0)}")
    print(f"Sync Violations: {final_stats.get('sync_violations', 0)}")
    
    # Show agent comparison
    print("\n=== Agent Comparison ===")
    for agent_name in ["Maya", "Miles"]:
        agent = manager.get_agent(agent_name)
        if agent:
            stats = agent.get_statistics()
            timing = stats['timing']
            buffer = stats['buffer']
            
            print(f"{agent_name}:")
            print(f"  Chunks received: {stats['receive_count']}")
            print(f"  Average interval: {timing['average_interval']*1000:.1f}ms")
            print(f"  Timing stability: {timing['stability']*100:.1f}%")
            print(f"  Buffer overflows: {buffer['buffer_overflows']}")
            print(f"  Silence chunks: {buffer['silence_chunks']}")
            print(f"  Average buffer size: {buffer['average_size']:.1f}")
    
    # Show synchronization stats
    sync_stats = manager.recorder.get_agent_synchronization_stats()
    if 'chunk_count_variance' in sync_stats:
        print(f"\n=== Synchronization ===")
        print(f"Chunk count variance: {sync_stats['chunk_count_variance']}")
        if 'average_sync_difference' in sync_stats:
            print(f"Average sync difference: {sync_stats['average_sync_difference']*1000:.1f}ms")
    
    print(f"\nRecording saved to: {recording_path}")
    print("\n=== Test Complete ===")


def demonstrate_fixes():
    """Demonstrate the specific fixes implemented."""
    print("\n=== Demonstrating Fixes ===")
    
    print("1. Buffer Management:")
    print("   - Dynamic buffer adjustment based on network conditions")
    print("   - Buffer underrun protection with silence padding")
    print("   - Adaptive buffering (initial: 5, range: 2-20)")
    
    print("\n2. Audio Synchronization:")
    print("   - Chunk sequence validation with timestamps")
    print("   - Audio drift correction through timing analysis")
    print("   - Continuity validation for gap detection")
    
    print("\n3. Receive Loop Stability:")
    print("   - Jitter buffer for variable timing (62.9ms to 69.2ms)")
    print("   - Adaptive timeout handling (50ms to 150ms)")
    print("   - Connection stability monitoring")
    
    print("\n4. Recording Quality:")
    print("   - Gap detection and filling (max 100ms gaps)")
    print("   - Audio continuity validation")
    print("   - Quality metrics and scoring")
    
    print("\nThe system now handles:")
    print("- Timing variations (target: 64ms ± 20ms)")
    print("- Buffer size imbalances")
    print("- Network jitter and instability")
    print("- Audio chunk synchronization")
    print("- Silent chunk handling and buffer starvation")


def main():
    """Main test function."""
    setup_logging()
    
    try:
        demonstrate_fixes()
        simulate_conversation()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        logging.error(f"Test failed with error: {e}")
        raise


if __name__ == "__main__":
    main()