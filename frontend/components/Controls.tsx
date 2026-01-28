import { VolumeType } from "../types/power";

type Props = {
  volume: VolumeType;
  setVolume: (v: VolumeType) => void;
  start: string;
  end: string;
  setStart: (v: string) => void;
  setEnd: (v: string) => void;
  park: string;
  setPark: (v: string) => void;
};

export default function Controls({
  volume,
  setVolume,
  start,
  end,
  setStart,
  setEnd,
  park,
  setPark,
}: Props) {
  return (
    <div style={{ display: "flex", gap: 20, flexWrap: "wrap", marginBottom: 20, alignItems: "center" }}>
      <div>
        <label>Start: </label>
        <input type="date" value={start} onChange={(e) => setStart(e.target.value)} />
      </div>

      <div>
        <label>End: </label>
        <input type="date" value={end} onChange={(e) => setEnd(e.target.value)} />
      </div>

      <div>
        <label>Park: </label>
        <select value={park} onChange={(e) => setPark(e.target.value)}>
          <option value="ALL">All parks</option>
          <option value="WIND_PARK_1">Wind park 1</option>
          <option value="SOLAR_PARK_1">Solar park 1</option>
        </select>
      </div>

      <div>
        <label>Volume: </label>
        <select value={volume} onChange={(e) => setVolume(e.target.value as VolumeType)}>
          <option value="average_per_hour">Average per hour</option>
          <option value="total_per_hour">Total per hour</option>
        </select>
      </div>
    </div>
  );
}
