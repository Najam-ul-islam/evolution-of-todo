// components/features/todos/TodoForm.tsx
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

interface TodoFormProps {
  onSubmit: (title: string, description?: string, priority?: 'low' | 'medium' | 'high', dueDate?: Date | null) => void;
}

export default function TodoForm({ onSubmit }: TodoFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');
  const [dueDate, setDueDate] = useState<string>('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      return;
    }

    onSubmit(
      title.trim(),
      description.trim() || undefined,
      priority,
      dueDate ? new Date(dueDate) : null
    );

    // Reset form
    setTitle('');
    setDescription('');
    setPriority('medium');
    setDueDate('');
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 p-6 bg-gradient-to-br from-card to-secondary rounded-xl border border-border shadow-lg card-elevated">
      <div className="text-center mb-4">
        <h2 className="text-2xl font-bold text-foreground">Create New Task</h2>
        <p className="text-muted-foreground mt-1">Add a new todo to your list</p>
      </div>

      <div className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="title" className="text-foreground font-semibold">Title *</Label>
          <Input
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="What needs to be done?"
            className="bg-background border-2 border-input focus:border-primary focus:ring-0 transition-all duration-200"
            required
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="description" className="text-foreground font-semibold">Description</Label>
          <Textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add details (optional)"
            rows={2}
            className="bg-background border-2 border-input focus:border-primary focus:ring-0 transition-all duration-200"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="priority" className="text-foreground font-semibold">Priority</Label>
            <Select value={priority} onValueChange={(value: 'low' | 'medium' | 'high') => setPriority(value)}>
              <SelectTrigger className="bg-background border-2 border-input focus:border-primary focus:ring-0 transition-all duration-200">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-popover border-border">
                <SelectItem value="low" className="focus:bg-accent">Low</SelectItem>
                <SelectItem value="medium" className="focus:bg-accent">Medium</SelectItem>
                <SelectItem value="high" className="focus:bg-accent">High</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="dueDate" className="text-foreground font-semibold">Due Date</Label>
            <Input
              id="dueDate"
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              className="bg-background border-2 border-input focus:border-primary focus:ring-0 transition-all duration-200"
            />
          </div>
        </div>

        <Button
          type="submit"
          className="w-full bg-gradient-to-r from-primary to-indigo-600 hover:from-primary/90 hover:to-indigo-700 text-primary-foreground font-semibold py-6 text-lg btn-gradient"
        >
          Add Task
        </Button>
      </div>
    </form>
  );
}