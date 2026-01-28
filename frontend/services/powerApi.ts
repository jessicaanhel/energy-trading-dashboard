import { PowerRow, VolumeType } from "../types/power";

const API_URL = "http://localhost:3001/power";
const API_URL_AWS = "https://abcd1234ef.execute-api.eu-west-1.amazonaws.com/Prod/power";


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
