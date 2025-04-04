export interface RouteSummary {
  start_point: string;
  end_point: string;
  total_distance: number;
  total_time: number;
}

export interface SearchData {
  fromAddress: string;
  destAddress: string;
}
