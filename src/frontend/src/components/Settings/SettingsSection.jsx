import React from 'react';
import { Card } from '@/components/ui/card';

export default function SettingsSection({ title, icon: Icon, children }) {
  return (
    <Card className="mb-4 overflow-hidden border-border">
      <div className="bg-muted/50 px-6 py-4 border-b border-border">
        <div className="flex items-center">
          <Icon className="w-5 h-5 text-primary mr-3" />
          <h2 className="text-lg font-semibold text-foreground">{title}</h2>
        </div>
      </div>
      <div className="p-6 bg-card">
        {children}
      </div>
    </Card>
  );
}
