#!/usr/bin/env python3
"""
Task CLI - 一个简单实用的任务管理命令行工具
支持添加、查看、完成、删除任务等功能
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
import argparse


class TaskManager:
    """任务管理器"""
    
    def __init__(self, data_file: str = None):
        if data_file is None:
            # 默认存储在用户主目录下
            self.data_file = Path.home() / ".task_cli_data.json"
        else:
            self.data_file = Path(data_file)
        
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> dict:
        """加载任务数据"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"警告: 无法加载任务数据: {e}")
                return {"tasks": [], "next_id": 1}
        return {"tasks": [], "next_id": 1}
    
    def _save_tasks(self):
        """保存任务数据"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"错误: 无法保存任务数据: {e}")
            sys.exit(1)
    
    def add_task(self, title: str, priority: str = "medium", tags: list = None):
        """添加新任务"""
        task = {
            "id": self.tasks["next_id"],
            "title": title,
            "priority": priority,
            "tags": tags or [],
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        self.tasks["tasks"].append(task)
        self.tasks["next_id"] += 1
        self._save_tasks()
        
        print(f"✓ 任务已添加 [ID: {task['id']}]")
        print(f"  标题: {title}")
        print(f"  优先级: {priority}")
        if tags:
            print(f"  标签: {', '.join(tags)}")
    
    def list_tasks(self, status: str = None, priority: str = None, tag: str = None):
        """列出任务"""
        filtered_tasks = self.tasks["tasks"]
        
        # 过滤条件
        if status:
            filtered_tasks = [t for t in filtered_tasks if t["status"] == status]
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t["priority"] == priority]
        if tag:
            filtered_tasks = [t for t in filtered_tasks if tag in t.get("tags", [])]
        
        if not filtered_tasks:
            print("没有找到匹配的任务")
            return
        
        # 按优先级和创建时间排序
        priority_order = {"high": 0, "medium": 1, "low": 2}
        filtered_tasks.sort(key=lambda t: (priority_order.get(t["priority"], 1), t["created_at"]))
        
        print(f"\n{'='*60}")
        print(f"任务列表 (共 {len(filtered_tasks)} 个)")
        print(f"{'='*60}\n")
        
        for task in filtered_tasks:
            status_icon = "✓" if task["status"] == "completed" else "○"
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task["priority"], "⚪")
            
            print(f"{status_icon} [{task['id']}] {task['title']}")
            print(f"   优先级: {priority_icon} {task['priority']}")
            if task.get("tags"):
                print(f"   标签: {', '.join(task['tags'])}")
            print(f"   创建时间: {task['created_at'][:19]}")
            if task["status"] == "completed" and task.get("completed_at"):
                print(f"   完成时间: {task['completed_at'][:19]}")
            print()
    
    def complete_task(self, task_id: int):
        """标记任务为完成"""
        for task in self.tasks["tasks"]:
            if task["id"] == task_id:
                if task["status"] == "completed":
                    print(f"任务 {task_id} 已经完成了")
                    return
                
                task["status"] = "completed"
                task["completed_at"] = datetime.now().isoformat()
                self._save_tasks()
                print(f"✓ 任务 {task_id} 已完成: {task['title']}")
                return
        
        print(f"错误: 找不到任务 ID {task_id}")
    
    def uncomplete_task(self, task_id: int):
        """标记任务为未完成"""
        for task in self.tasks["tasks"]:
            if task["id"] == task_id:
                if task["status"] == "pending":
                    print(f"任务 {task_id} 本来就是未完成状态")
                    return
                
                task["status"] = "pending"
                task["completed_at"] = None
                self._save_tasks()
                print(f"✓ 任务 {task_id} 已标记为未完成: {task['title']}")
                return
        
        print(f"错误: 找不到任务 ID {task_id}")
    
    def delete_task(self, task_id: int):
        """删除任务"""
        for i, task in enumerate(self.tasks["tasks"]):
            if task["id"] == task_id:
                deleted_task = self.tasks["tasks"].pop(i)
                self._save_tasks()
                print(f"✓ 任务 {task_id} 已删除: {deleted_task['title']}")
                return
        
        print(f"错误: 找不到任务 ID {task_id}")
    
    def show_task(self, task_id: int):
        """显示任务详情"""
        for task in self.tasks["tasks"]:
            if task["id"] == task_id:
                status_icon = "✓" if task["status"] == "completed" else "○"
                priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task["priority"], "⚪")
                
                print(f"\n{'='*60}")
                print(f"任务详情")
                print(f"{'='*60}\n")
                print(f"ID: {task['id']}")
                print(f"标题: {task['title']}")
                print(f"状态: {status_icon} {task['status']}")
                print(f"优先级: {priority_icon} {task['priority']}")
                if task.get("tags"):
                    print(f"标签: {', '.join(task['tags'])}")
                print(f"创建时间: {task['created_at'][:19]}")
                if task["status"] == "completed" and task.get("completed_at"):
                    print(f"完成时间: {task['completed_at'][:19]}")
                print()
                return
        
        print(f"错误: 找不到任务 ID {task_id}")
    
    def stats(self):
        """显示统计信息"""
        total = len(self.tasks["tasks"])
        completed = sum(1 for t in self.tasks["tasks"] if t["status"] == "completed")
        pending = total - completed
        
        high_priority = sum(1 for t in self.tasks["tasks"] if t["priority"] == "high" and t["status"] == "pending")
        medium_priority = sum(1 for t in self.tasks["tasks"] if t["priority"] == "medium" and t["status"] == "pending")
        low_priority = sum(1 for t in self.tasks["tasks"] if t["priority"] == "low" and t["status"] == "pending")
        
        print(f"\n{'='*60}")
        print(f"任务统计")
        print(f"{'='*60}\n")
        print(f"总任务数: {total}")
        print(f"已完成: {completed} ({completed/total*100 if total > 0 else 0:.1f}%)")
        print(f"待完成: {pending} ({pending/total*100 if total > 0 else 0:.1f}%)")
        print(f"\n待完成任务优先级分布:")
        print(f"  🔴 高优先级: {high_priority}")
        print(f"  🟡 中优先级: {medium_priority}")
        print(f"  🟢 低优先级: {low_priority}")
        print()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Task CLI - 简单实用的任务管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s add "完成项目报告" -p high -t 工作 -t 紧急
  %(prog)s list -s pending
  %(prog)s complete 1
  %(prog)s show 1
  %(prog)s stats
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # add 命令
    add_parser = subparsers.add_parser("add", help="添加新任务")
    add_parser.add_argument("title", help="任务标题")
    add_parser.add_argument("-p", "--priority", choices=["high", "medium", "low"], 
                          default="medium", help="任务优先级 (默认: medium)")
    add_parser.add_argument("-t", "--tag", action="append", dest="tags",
                          help="任务标签 (可多次使用)")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出任务")
    list_parser.add_argument("-s", "--status", choices=["pending", "completed"],
                           help="按状态过滤")
    list_parser.add_argument("-p", "--priority", choices=["high", "medium", "low"],
                           help="按优先级过滤")
    list_parser.add_argument("-t", "--tag", help="按标签过滤")
    
    # complete 命令
    complete_parser = subparsers.add_parser("complete", help="标记任务为完成")
    complete_parser.add_argument("id", type=int, help="任务ID")
    
    # uncomplete 命令
    uncomplete_parser = subparsers.add_parser("uncomplete", help="标记任务为未完成")
    uncomplete_parser.add_argument("id", type=int, help="任务ID")
    
    # delete 命令
    delete_parser = subparsers.add_parser("delete", help="删除任务")
    delete_parser.add_argument("id", type=int, help="任务ID")
    
    # show 命令
    show_parser = subparsers.add_parser("show", help="显示任务详情")
    show_parser.add_argument("id", type=int, help="任务ID")
    
    # stats 命令
    subparsers.add_parser("stats", help="显示统计信息")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # 创建任务管理器
    manager = TaskManager()
    
    # 执行命令
    if args.command == "add":
        manager.add_task(args.title, args.priority, args.tags)
    elif args.command == "list":
        manager.list_tasks(args.status, args.priority, args.tag)
    elif args.command == "complete":
        manager.complete_task(args.id)
    elif args.command == "uncomplete":
        manager.uncomplete_task(args.id)
    elif args.command == "delete":
        manager.delete_task(args.id)
    elif args.command == "show":
        manager.show_task(args.id)
    elif args.command == "stats":
        manager.stats()


if __name__ == "__main__":
    main()
