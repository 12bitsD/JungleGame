#!/usr/bin/env python3
"""
Jungle Game (斗兽棋) - Main Entry Point
A traditional Chinese board game implementation.

Usage:
    python main.py

Author: Jungle Game Development Team
Version: 1.0
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controller.game_controller import GameController


def main():
    """Main entry point for the game."""
    print("=" * 50)
    print("JUNGLE GAME (斗兽棋)")
    print("=" * 50)
    print("\nWelcome to Jungle Game!")
    print("A strategic board game for two players.")
    print()
    
    try:
        controller = GameController()
        controller.start()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
    except Exception as e:
        print(f"\n\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
