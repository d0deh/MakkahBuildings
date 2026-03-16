interface EmptyStateProps {
  title: string;
  description?: string;
  action?: {
    label: string;
    href: string;
  };
}

export function EmptyState({ title, description, action }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center">
      <div className="w-16 h-16 rounded-full bg-[hsl(var(--muted))] flex items-center justify-center mb-4">
        <span className="text-2xl text-muted-foreground">!</span>
      </div>
      <h3 className="text-lg font-bold text-foreground mb-2">{title}</h3>
      {description && (
        <p className="text-sm text-muted-foreground max-w-md">{description}</p>
      )}
      {action && (
        <a
          href={action.href}
          className="mt-4 text-gold hover:text-gold-dark hover:underline text-sm font-bold"
        >
          {action.label}
        </a>
      )}
    </div>
  );
}
