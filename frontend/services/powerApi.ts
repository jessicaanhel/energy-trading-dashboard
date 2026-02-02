import { PowerRow, VolumeType } from "../types/power";

const API_URL = process.env.NEXT_PUBLIC_POWER_API_URL!;

export async function loadPowerData(
  start: string,
  end: string,
  volume: VolumeType,
  park: string = "ALL"
): Promise<PowerRow[]> {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ start, end, volume, park })
  });

  if (!res.ok) throw new Error("Failed to fetch power data");
  return res.json();
}
