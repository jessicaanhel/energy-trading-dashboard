export type PowerRow = {
  hour: string;
  wind_mw?: number;
  solar_mw?: number;
};

export type VolumeType = "average_per_hour" | "total_per_hour";