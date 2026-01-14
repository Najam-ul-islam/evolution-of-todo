// components/features/todos/TodoItem.tsx
import { useState } from 'react';
import { Todo } from '@/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import { Trash2, Edit3 } from 'lucide-react';

interface TodoItemProps {
  todo: Todo;
  onUpdate: (id: string, updates: Partial<Todo>) => void;
  onDelete: (id: string) => void;
  onToggleCompletion: (id: string) => void;
}

export default function TodoItem({ todo, onUpdate, onDelete, onToggleCompletion }: TodoItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description);
  const [editPriority, setEditPriority] = useState<'low' | 'medium' | 'high'>(todo.priority);
  const [editDueDate, setEditDueDate] = useState<string>(todo.dueDate ? new Date(todo.dueDate).toISOString().split('T')[0] : '');

  const handleSave = () => {
    onUpdate(todo.id, {
      title: editTitle,
      description: editDescription,
      priority: editPriority,
      dueDate: editDueDate ? new Date(editDueDate) : null
    });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditTitle(todo.title);
    setEditDescription(todo.description);
    setEditPriority(todo.priority);
    setEditDueDate(todo.dueDate ? new Date(todo.dueDate).toISOString().split('T')[0] : '');
    setIsEditing(false);
  };

  const handleDelete = () => {
    onDelete(todo.id);
  };

  const handleToggleCompletion = () => {
    onToggleCompletion(todo.id);
  };

  const formatDate = (date: Date | null) => {
    if (!date) return '';
    return new Date(date).toLocaleDateString();
  };

  return (
    <Card className={`${todo.completed ? 'opacity-70 bg-gray-50' : ''}`}>
      <CardContent className="p-4">
        {isEditing ? (
          // Edit form
          <div className="space-y-3">
            <input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Todo title"
            />
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Description (optional)"
              rows={2}
            />
            <div className="flex space-x-2">
              <select
                value={editPriority}
                onChange={(e) => setEditPriority(e.target.value as 'low' | 'medium' | 'high')}
                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
              <input
                type="date"
                value={editDueDate}
                onChange={(e) => setEditDueDate(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div className="flex justify-end space-x-2">
              <Button type="button" variant="outline" onClick={handleCancel}>
                Cancel
              </Button>
              <Button type="button" onClick={handleSave}>
                Save
              </Button>
            </div>
          </div>
        ) : (
          // Display view
          <div className="flex items-start justify-between">
            <div className="flex items-start space-x-3">
              <Checkbox
                checked={todo.completed}
                onCheckedChange={handleToggleCompletion}
                className="mt-1"
              />
              <div className="flex-1">
                <div className="flex items-center space-x-2">
                  <h3 className={`text-lg font-medium ${todo.completed ? 'line-through' : ''}`}>
                    {todo.title}
                  </h3>
                  <Badge variant={todo.priority === 'high' ? 'destructive' : todo.priority === 'medium' ? 'default' : 'secondary'}>
                    {todo.priority}
                  </Badge>
                </div>
                {todo.description && (
                  <p className={`mt-1 ${todo.completed ? 'line-through text-gray-500' : 'text-gray-600'}`}>
                    {todo.description}
                  </p>
                )}
                {todo.dueDate && (
                  <p className="text-sm text-gray-500 mt-1">
                    Due: {formatDate(todo.dueDate)}
                  </p>
                )}
                <p className="text-xs text-gray-400 mt-1">
                  Created: {new Date(todo.createdAt).toLocaleDateString()}
                </p>
              </div>
            </div>
            <div className="flex space-x-1">
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={() => setIsEditing(true)}
              >
                <Edit3 className="h-4 w-4" />
              </Button>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={handleDelete}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}