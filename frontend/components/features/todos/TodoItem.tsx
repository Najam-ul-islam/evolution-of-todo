// components/features/todos/TodoItem.tsx
import { useState } from 'react';
import { Todo } from '@/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import Pencil from 'lucide-react/dist/esm/icons/pencil';
import Trash2 from 'lucide-react/dist/esm/icons/trash-2';
import Calendar from 'lucide-react/dist/esm/icons/calendar';
import Clock from 'lucide-react/dist/esm/icons/clock';

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

  // Determine priority class based on priority level
  const getPriorityClass = (priority: string) => {
    switch(priority) {
      case 'high':
        return 'bg-gradient-to-r from-red-500 to-red-600 text-white';
      case 'medium':
        return 'bg-gradient-to-r from-amber-500 to-orange-500 text-white';
      case 'low':
        return 'bg-gradient-to-r from-emerald-500 to-green-500 text-white';
      default:
        return 'bg-gradient-to-r from-slate-400 to-slate-500 text-white';
    }
  };

  return (
    <Card className={`p-0 overflow-hidden card-elevated ${todo.completed ? 'opacity-70 bg-gradient-to-r from-emerald-50 to-green-50' : 'bg-gradient-to-r from-card to-secondary'}`}>
      <CardContent className="p-5">
        {isEditing ? (
          // Edit form
          <div className="space-y-4">
            <input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              className="w-full px-4 py-3 bg-background border-2 border-input rounded-lg focus:outline-none focus:border-primary focus:ring-0 transition-all duration-200 text-lg font-medium"
              placeholder="Task title"
            />
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              className="w-full px-4 py-3 bg-background border-2 border-input rounded-lg focus:outline-none focus:border-primary focus:ring-0 transition-all duration-200"
              placeholder="Description (optional)"
              rows={2}
            />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <select
                value={editPriority}
                onChange={(e) => setEditPriority(e.target.value as 'low' | 'medium' | 'high')}
                className="px-4 py-2 bg-background border-2 border-input rounded-lg focus:outline-none focus:border-primary focus:ring-0 transition-all duration-200"
              >
                <option value="low">Low Priority</option>
                <option value="medium">Medium Priority</option>
                <option value="high">High Priority</option>
              </select>
              <input
                type="date"
                value={editDueDate}
                onChange={(e) => setEditDueDate(e.target.value)}
                className="px-4 py-2 bg-background border-2 border-input rounded-lg focus:outline-none focus:border-primary focus:ring-0 transition-all duration-200"
              />
            </div>
            <div className="flex justify-end space-x-2 pt-2">
              <Button
                type="button"
                variant="outline"
                onClick={handleCancel}
                className="border-2"
              >
                Cancel
              </Button>
              <Button
                type="button"
                onClick={handleSave}
                className="bg-gradient-to-r from-primary to-indigo-600 hover:from-primary/90 hover:to-indigo-700 text-primary-foreground"
              >
                Save Changes
              </Button>
            </div>
          </div>
        ) : (
          // Display view
          <div className="flex items-start justify-between">
            <div className="flex items-start space-x-3 flex-1">
              <Checkbox
                checked={todo.completed}
                onCheckedChange={handleToggleCompletion}
                className="mt-1 h-5 w-5 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground"
              />
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <h3 className={`text-lg font-semibold ${todo.completed ? 'line-through text-muted-foreground' : 'text-foreground'}`}>
                    {todo.title}
                  </h3>
                  <span className={`text-xs px-2 py-1 rounded-full font-medium ${getPriorityClass(todo.priority)}`}>
                    {todo.priority.charAt(0).toUpperCase() + todo.priority.slice(1)}
                  </span>
                </div>

                {todo.description && (
                  <p className={`mt-2 text-foreground ${todo.completed ? 'line-through opacity-70' : ''}`}>
                    {todo.description}
                  </p>
                )}

                <div className="flex flex-wrap gap-3 mt-3">
                  {todo.dueDate && (
                    <div className="flex items-center text-sm text-muted-foreground">
                      <Calendar className="h-4 w-4 mr-1" />
                      Due: {formatDate(todo.dueDate)}
                    </div>
                  )}

                  <div className="flex items-center text-sm text-muted-foreground">
                    <Clock className="h-4 w-4 mr-1" />
                    {new Date(todo.createdAt).toLocaleDateString()}
                  </div>
                </div>
              </div>
            </div>

            <div className="flex space-x-1 ml-4">
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => setIsEditing(true)}
                className="h-8 w-8 p-0 border-2 hover:bg-accent"
              >
                <Pencil className="h-4 w-4" />
              </Button>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={handleDelete}
                className="h-8 w-8 p-0 border-2 hover:bg-destructive hover:text-destructive-foreground"
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