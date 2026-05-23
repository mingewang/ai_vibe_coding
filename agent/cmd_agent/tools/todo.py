#!/usr/bin/env python3
"""
todo - A CLI todo list application

Usage:
    todo add "Buy groceries" -p high -d 2024-12-25 -c personal
    todo list
    todo list --category work
    todo done 3
    todo delete 5
    todo clear
    todo search "groceries"

Commands:
    add     Add a new task
    list    List all tasks (with optional filters)
    done    Mark a task as completed
    delete  Delete a task
    clear   Clear all tasks
    search  Search tasks by keyword
"""

import argparse
import json
import os
import sys
from datetime import datetime, date
from typing import List, Dict, Optional

# ANSI color codes
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    GRAY = '\033[90m'
    WHITE = '\033[97m'

    @staticmethod
    def colorize(text: str, color: str, bold: bool = False) -> str:
        """Apply color to text."""
        prefix = Colors.BOLD if bold else ''
        return f"{prefix}{color}{text}{Colors.RESET}"


class TodoApp:
    """Main todo application class."""

    DATA_DIR = os.path.expanduser("~/.todo")
    DATA_FILE = os.path.join(DATA_DIR, "tasks.json")

    PRIORITIES = {
        'high': {'symbol': '🔴', 'color': Colors.RED, 'value': 3},
        'medium': {'symbol': '🟡', 'color': Colors.YELLOW, 'value': 2},
        'low': {'symbol': '🟢', 'color': Colors.GREEN, 'value': 1},
        'none': {'symbol': '⚪', 'color': Colors.GRAY, 'value': 0},
    }

    def __init__(self):
        """Initialize the todo app."""
        self.tasks = self._load_tasks()

    def _load_tasks(self) -> List[Dict]:
        """Load tasks from JSON file."""
        if not os.path.exists(self.DATA_DIR):
            os.makedirs(self.DATA_DIR, exist_ok=True)
        if not os.path.exists(self.DATA_FILE):
            return []
        try:
            with open(self.DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_tasks(self):
        """Save tasks to JSON file."""
        with open(self.DATA_FILE, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def _get_next_id(self) -> int:
        """Get the next available task ID."""
        if not self.tasks:
            return 1
        return max(task['id'] for task in self.tasks) + 1

    def _format_date(self, date_str: Optional[str]) -> str:
        """Format a date string for display."""
        if not date_str:
            return "No due date"
        try:
            due_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            today = date.today()
            delta = (due_date - today).days

            if delta < 0:
                return f"{Colors.RED}{due_date.strftime('%b %d')} (OVERDUE){Colors.RESET}"
            elif delta == 0:
                return f"{Colors.YELLOW}Today{Colors.RESET}"
            elif delta == 1:
                return f"{Colors.YELLOW}Tomorrow{Colors.RESET}"
            elif delta <= 7:
                return f"{Colors.YELLOW}{due_date.strftime('%b %d')} ({delta}d){Colors.RESET}"
            else:
                return f"{Colors.GRAY}{due_date.strftime('%b %d')}{Colors.RESET}"
        except ValueError:
            return date_str

    def _format_task(self, task: Dict, show_id: bool = True) -> str:
        """Format a single task for display."""
        status = "✅" if task.get('done') else "⬜"
        priority = self.PRIORITIES.get(task.get('priority', 'none'), self.PRIORITIES['none'])
        priority_str = f"{priority['symbol']} {Colors.colorize(task.get('priority', 'none').upper(), priority['color'])}"

        id_str = f"#{task['id']:3d}"
        task_id = f"{Colors.colorize(id_str, Colors.CYAN, bold=True)}" if show_id else ""
        title = task.get('title', 'Untitled')
        if task.get('done'):
            title = f"{Colors.GRAY}{title}{Colors.RESET}"
        else:
            title = f"{Colors.WHITE}{title}{Colors.RESET}"

        due_date = self._format_date(task.get('due_date'))
        category = task.get('category', '')
        category_str = f" [{Colors.colorize(category, Colors.MAGENTA)}]" if category else ""

        created = task.get('created_at', '')
        created_str = f" {Colors.GRAY}({created[:10]}){Colors.RESET}" if created else ""

        return f"{status} {task_id} {priority_str} {title}{category_str} {due_date}{created_str}"

    def add(self, title: str, priority: str = 'none', due_date: Optional[str] = None,
            category: Optional[str] = None):
        """Add a new task."""
        if not title.strip():
            print(f"{Colors.RED}Error: Task title cannot be empty{Colors.RESET}")
            return

        task = {
            'id': self._get_next_id(),
            'title': title.strip(),
            'done': False,
            'priority': priority,
            'due_date': due_date,
            'category': category or '',
            'created_at': datetime.now().isoformat(),
            'completed_at': None,
        }
        self.tasks.append(task)
        self._save_tasks()
        print(f"{Colors.GREEN}✓ Task added:{Colors.RESET} {title}")
        print(f"  {self._format_task(task)}")

    def list(self, category: Optional[str] = None, priority: Optional[str] = None,
             show_done: bool = True, sort_by: str = 'id'):
        """List all tasks with optional filters."""
        tasks = self.tasks

        # Apply filters
        if category:
            tasks = [t for t in tasks if t.get('category', '').lower() == category.lower()]
        if priority:
            tasks = [t for t in tasks if t.get('priority', 'none') == priority]
        if not show_done:
            tasks = [t for t in tasks if not t.get('done')]

        if not tasks:
            print(f"{Colors.YELLOW}No tasks found.{Colors.RESET}")
            return

        # Sort tasks
        if sort_by == 'priority':
            tasks.sort(key=lambda t: self.PRIORITIES.get(t.get('priority', 'none'), {}).get('value', 0), reverse=True)
        elif sort_by == 'due_date':
            tasks.sort(key=lambda t: t.get('due_date') or '9999-99-99')
        elif sort_by == 'category':
            tasks.sort(key=lambda t: t.get('category', ''))
        else:  # sort by id
            tasks.sort(key=lambda t: t['id'])

        # Count statistics
        total = len(tasks)
        done_count = sum(1 for t in tasks if t.get('done'))
        pending_count = total - done_count

        # Print header
        print(f"\n{Colors.BOLD}📋 Todo List{Colors.RESET}")
        print(f"{Colors.GRAY}{'─' * 60}{Colors.RESET}")

        # Print tasks
        for task in tasks:
            print(f"  {self._format_task(task)}")

        # Print footer with stats
        print(f"{Colors.GRAY}{'─' * 60}{Colors.RESET}")
        print(f"Total: {total} | {Colors.GREEN}Done: {done_count}{Colors.RESET} | "
              f"{Colors.YELLOW}Pending: {pending_count}{Colors.RESET}")

    def done(self, task_id: int):
        """Mark a task as completed."""
        for task in self.tasks:
            if task['id'] == task_id:
                if task.get('done'):
                    print(f"{Colors.YELLOW}Task #{task_id} is already completed.{Colors.RESET}")
                    return
                task['done'] = True
                task['completed_at'] = datetime.now().isoformat()
                self._save_tasks()
                print(f"{Colors.GREEN}✓ Task #{task_id} marked as done!{Colors.RESET}")
                print(f"  {self._format_task(task)}")
                return
        print(f"{Colors.RED}Error: Task #{task_id} not found.{Colors.RESET}")

    def delete(self, task_id: int):
        """Delete a task."""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                deleted = self.tasks.pop(i)
                self._save_tasks()
                print(f"{Colors.RED}✗ Task #{task_id} deleted:{Colors.RESET} {deleted['title']}")
                return
        print(f"{Colors.RED}Error: Task #{task_id} not found.{Colors.RESET}")

    def clear(self, force: bool = False):
        """Clear all tasks."""
        if not self.tasks:
            print(f"{Colors.YELLOW}No tasks to clear.{Colors.RESET}")
            return

        if not force:
            print(f"{Colors.RED}Are you sure you want to delete all {len(self.tasks)} tasks?{Colors.RESET}")
            response = input(f"{Colors.YELLOW}Type 'yes' to confirm: {Colors.RESET}")
            if response.lower() != 'yes':
                print("Cancelled.")
                return

        self.tasks = []
        self._save_tasks()
        print(f"{Colors.GREEN}✓ All tasks cleared.{Colors.RESET}")

    def search(self, keyword: str):
        """Search tasks by keyword."""
        if not keyword.strip():
            print(f"{Colors.RED}Error: Search keyword cannot be empty{Colors.RESET}")
            return

        keyword = keyword.lower()
        results = [t for t in self.tasks if keyword in t.get('title', '').lower()]

        if not results:
            print(f"{Colors.YELLOW}No tasks found matching '{keyword}'.{Colors.RESET}")
            return

        print(f"\n{Colors.BOLD}🔍 Search Results for '{keyword}'{Colors.RESET}")
        print(f"{Colors.GRAY}{'─' * 60}{Colors.RESET}")
        for task in results:
            print(f"  {self._format_task(task)}")
        print(f"{Colors.GRAY}{'─' * 60}{Colors.RESET}")
        print(f"Found {len(results)} task(s)")


def main():
    """Main entry point for the todo CLI."""
    parser = argparse.ArgumentParser(
        description="A CLI todo list application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s add "Buy groceries" -p high -d 2024-12-25 -c personal
  %(prog)s list
  %(prog)s list --category work --pending
  %(prog)s list --sort priority
  %(prog)s done 3
  %(prog)s delete 5
  %(prog)s search "groceries"
  %(prog)s clear --force
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', type=str, help='Task title')
    add_parser.add_argument('-p', '--priority', choices=['high', 'medium', 'low', 'none'],
                           default='none', help='Task priority')
    add_parser.add_argument('-d', '--due-date', type=str, help='Due date (YYYY-MM-DD)')
    add_parser.add_argument('-c', '--category', type=str, help='Task category')

    # List command
    list_parser = subparsers.add_parser('list', help='List all tasks')
    list_parser.add_argument('--category', type=str, help='Filter by category')
    list_parser.add_argument('--priority', choices=['high', 'medium', 'low', 'none'],
                            help='Filter by priority')
    list_parser.add_argument('--pending', action='store_true', help='Show only pending tasks')
    list_parser.add_argument('--sort', choices=['id', 'priority', 'due_date', 'category'],
                            default='id', help='Sort tasks by field')

    # Done command
    done_parser = subparsers.add_parser('done', help='Mark a task as completed')
    done_parser.add_argument('task_id', type=int, help='Task ID to mark as done')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('task_id', type=int, help='Task ID to delete')

    # Clear command
    clear_parser = subparsers.add_parser('clear', help='Clear all tasks')
    clear_parser.add_argument('--force', '-f', action='store_true', help='Skip confirmation')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search tasks by keyword')
    search_parser.add_argument('keyword', type=str, help='Keyword to search for')

    args = parser.parse_args()

    app = TodoApp()

    if args.command == 'add':
        app.add(args.title, args.priority, args.due_date, args.category)
    elif args.command == 'list':
        app.list(args.category, args.priority, not args.pending, args.sort)
    elif args.command == 'done':
        app.done(args.task_id)
    elif args.command == 'delete':
        app.delete(args.task_id)
    elif args.command == 'clear':
        app.clear(args.force)
    elif args.command == 'search':
        app.search(args.keyword)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()