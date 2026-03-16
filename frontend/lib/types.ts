export interface ValidationResult {
  total_rows: number;
  rows_with_buildings: number;
  empty_plots: number;
  date_range: { start: string | null; end: string | null };
  area_name: string;
  warnings: string[];
}

export interface UploadResponse {
  session_id: string;
  validation: ValidationResult;
}

export interface ChartData {
  id: string;
  title: string;
  image: string;
}

export interface ChartsResponse {
  charts: ChartData[];
}

export interface AiContent {
  [section: string]: string | null;
}

export interface AiSectionResponse {
  section: string;
  text: string | null;
}

export interface HealthResponse {
  status: string;
  api_key_set: boolean;
}

export interface AreaStats {
  area_name: string;
  total_records: number;
  total_with_buildings: number;
  total_without_buildings: number;
  date_min: string | null;
  date_max: string | null;
  building_types: Record<string, number>;
  building_conditions: Record<string, number>;
  construction_methods: Record<string, number>;
  exterior_finishes: Record<string, number>;
  floor_distribution: Record<string, number>;
  building_usages: Record<string, number>;
  total_residential_occupied: number;
  total_residential_vacant: number;
  total_commercial_occupied: number;
  total_commercial_vacant: number;
  road_types: Record<string, number>;
  road_lighting_yes: number;
  road_lighting_no: number;
  parking_yes: number;
  parking_no: number;
  compliant_count: number;
  non_compliant_count: number;
  na_compliance_count: number;
  non_compliance_reasons: string[];
}

// Chart data types for Recharts
export interface ChartDataPoint {
  name: string;
  value: number;
}

export interface ChartSpec {
  type: "bar" | "pie";
  title: string;
  data: ChartDataPoint[];
  colorMap?: Record<string, string>;
}

export type ChartDataResponse = Record<string, ChartSpec | null>;

// Chat types
export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  chartSpec?: ChartSpec;
}

export interface PinnedItem {
  message_id: string;
  text: string;
  chart_spec?: ChartSpec | null;
}
