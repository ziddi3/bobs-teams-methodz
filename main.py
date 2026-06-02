#!/usr/bin/env python3
"""
Bob's Teams Methodz - Main Interface
The Only Methodz - Easy-to-use interface for autonomous AI collaboration
"""

import sys
import os

# Add workspace to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bobs_teams_methodz import BobsTeams


def print_banner():
    """Print welcome banner"""
    print(f"\n{'='*70}")
    print(f"{' '*10}🎯 Bob's Teams Methodz - The Only Methodz 🎯")
    print(f"{' '*8}Autonomous AI Agent Collaboration System")
    print(f"{'='*70}\n")


def print_menu():
    """Print main menu"""
    print(f"🎯 Main Menu")
    print(f"{'─'*70}")
    print(f"  1. Submit a new task (stay in loop - ask before proceeding)")
    print(f"  2. Submit a new task (autonomous - execute fully)")
    print(f"  3. View team status")
    print(f"  4. View current progress")
    print(f"  5. View execution results")
    print(f"  6. Reset team")
    print(f"  0. Exit")
    print(f"{'='*70}\n")


def interactive_mode():
    """Run interactive mode"""

    print_banner()

    # Initialize Bob's team
    team = None

    while True:
        print_menu()
        choice = input("Enter your choice (0-6): ").strip()

        if choice == "0":
            print(f"\n👋 Thanks for using Bob's Teams Methodz! 🎯")
            break

        elif choice == "1":
            # Interactive mode - stay in loop
            if team is None:
                team = BobsTeams(keep_in_loop=True)
            
            print(f"\n📝 Submit New Task (Interactive Mode)")
            print(f"{'='*70}")
            
            description = input("Task description: ").strip()
            if not description:
                print(f"❌ Task description cannot be empty")
                continue
            
            task_type = input("Task type (press Enter for 'general'): ").strip() or "general"
            
            # Submit task
            task_id = team.submit_task(description, task_type)
            
            print(f"\n✅ Task '{description}' submitted!")
            print(f"   Task ID: {task_id}")
            print(f"   Mode: Interactive (you'll be asked before execution)\n")
        
        elif choice == "2":
            # Autonomous mode
            if team is None:
                team = WorkforceEngine(keep_in_loop=False)
            
            print(f"\n📝 Submit New Task (Autonomous Mode)")
            print(f"{'='*70}")
            
            description = input("Task description: ").strip()
            if not description:
                print(f"❌ Task description cannot be empty")
                continue
            
            task_type = input("Task type (press Enter for 'general'): ").strip() or "general"
            
            # Submit and execute
            print(f"\n🚀 Starting autonomous execution...")
            team.submit_task(description, task_type)
            team.execute_autonomous()
        
        elif choice == "3":
            # View team status
            if team is None:
                team = WorkforceEngine()
            else:
                team.print_team_status()
        
        elif choice == "4":
            # View progress
            if team is None:
                print(f"\n❌ No active team. Initialize by submitting a task first.\n")
            else:
                team.show_summary(team.get_results())
        
        elif choice == "5":
            # View results
            if team is None:
                print(f"\n❌ No active team. Initialize by submitting a task first.\n")
            else:
                results = team.get_results()
                print(f"\n📊 Execution Results")
                print(f"{'='*70}")
                print(f"\n{json.dumps(results, indent=2)}\n")
        
        elif choice == "6":
            # Reset team
            team = WorkforceEngine()
            print(f"\n✅ Workforce reset successfully!\n")
        
        else:
            print(f"\n❌ Invalid choice. Please enter 0-6.\n")


def quick_demo():
    """Run a quick demonstration"""
    
    print_banner()
    
    print(f"🎬 Quick Demo Mode")
    print(f"{'='*70}")
    print(f"This demo will:")
    print(f"  1. Create an AI team team")
    print(f"  2. Submit a sample task")
    print(f"  3. Execute tasks autonomously")
    print(f"  4. Deliver results")
    print(f"\nPress Enter to continue or Ctrl+C to cancel...")
    input()
    
    # Initialize team
    team = WorkforceEngine(keep_in_loop=False)
    
    # Submit sample task
    sample_task = "Create a research report on renewable energy trends"
    
    print(f"\n📝 Demo Task: {sample_task}")
    print(f"{'─'*70}")
    
    # Execute autonomously
    deliverable = team.execute_autonomous()
    
    print(f"\n✨ Demo Complete!")
    print(f"📦 Deliverable location: {deliverable}")


def main():
    """Main entry point"""
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        quick_demo()
    else:
        interactive_mode()


if __name__ == "__main__":
    main()