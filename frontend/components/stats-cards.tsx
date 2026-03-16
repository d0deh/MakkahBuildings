interface StatsCardsProps {
  stats: {
    total_records: number;
    total_with_buildings: number;
    total_without_buildings: number;
    date_min: string | null;
    date_max: string | null;
    area_name: string;
  };
}

export function StatsCards({ stats }: StatsCardsProps) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
      <div>
        <p className="text-4xl font-bold text-gold">{stats.total_records}</p>
        <p className="text-sm text-muted-foreground mt-1">إجمالي السجلات</p>
      </div>
      <div>
        <p className="text-4xl font-bold text-gold">{stats.total_with_buildings}</p>
        <p className="text-sm text-muted-foreground mt-1">عناوين بها مباني</p>
      </div>
      <div>
        <p className="text-4xl font-bold text-gold">{stats.total_without_buildings}</p>
        <p className="text-sm text-muted-foreground mt-1">أراضي فارغة</p>
      </div>
      <div>
        <p className="text-4xl font-bold text-gold">
          {stats.date_min && stats.date_max
            ? `${stats.date_min.slice(5, 10)}`
            : "—"}
        </p>
        <p className="text-sm text-muted-foreground mt-1">فترة المسح</p>
      </div>
    </div>
  );
}
