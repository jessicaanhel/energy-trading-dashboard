import { useState, useEffect } from "react";
import { PowerRow, VolumeType } from "../types/power";
import { loadPowerData } from "../services/powerApi";
import PowerTable from "../components/PowerTable";
import PowerChart from "../components/PowerChart";
import Controls from "../components/Controls";

function calculateSummary(data: PowerRow[]) {
  const summary = {
    totalWind: 0,
    totalSolar: 0,
    avgWind: 0,
    avgSolar: 0,
  };

  if (data.length === 0) return summary;

  data.forEach((row) => {
    summary.totalWind += row.wind_mw;
    summary.totalSolar += row.solar_mw;
  });

  summary.avgWind = summary.totalWind / data.length;
  summary.avgSolar = summary.totalSolar / data.length;

  return summary;
}

export default function Home() {
  const [data, setData] = useState<PowerRow[]>([]);
  const [volume, setVolume] = useState<VolumeType>("average_per_hour");
  const [startDate, setStartDate] = useState("2020-01-01");
  const [endDate, setEndDate] = useState("2020-01-12");
  const [park, setPark] = useState("ALL");
  const [loading, setLoading] = useState(false);

  async function fetchData() {
    setLoading(true);
    try {
      const startISO = startDate + "T00:00:00";
      const endISO = endDate + "T23:59:59";
      const result = await loadPowerData(startISO, endISO, volume, park);
      setData(result);
    } finally {
      setLoading(false);
    }
  }

  const summary = calculateSummary(data);

  return (
    <div style={{ padding: 20 }}>
      <h1>Energy Production Dashboard</h1>

      {/* Controls */}
      <Controls
        start={startDate}
        end={endDate}
        setStart={setStartDate}
        setEnd={setEndDate}
        volume={volume}
        setVolume={setVolume}
        park={park}
        setPark={setPark}
      />

      <button onClick={fetchData} disabled={loading} style={{ marginBottom: 20 }}>
        {loading ? "Loading..." : "Load Data"}
      </button>

      {/* Summary Cards */}
      <div style={{ display: "flex", gap: 20, marginBottom: 20, flexWrap: "wrap" }}>
        <div style={{ flex: 1, minWidth: 150, padding: 10, border: "1px solid #ccc", borderRadius: 8 }}>
          <h4>Total Wind MW</h4>
          <p>{summary.totalWind.toFixed(2)}</p>
        </div>
        <div style={{ flex: 1, minWidth: 150, padding: 10, border: "1px solid #ccc", borderRadius: 8 }}>
          <h4>Total Solar MW</h4>
          <p>{summary.totalSolar.toFixed(2)}</p>
        </div>
        <div style={{ flex: 1, minWidth: 150, padding: 10, border: "1px solid #ccc", borderRadius: 8 }}>
          <h4>Avg Wind MW</h4>
          <p>{summary.avgWind.toFixed(2)}</p>
        </div>
        <div style={{ flex: 1, minWidth: 150, padding: 10, border: "1px solid #ccc", borderRadius: 8 }}>
          <h4>Avg Solar MW</h4>
          <p>{summary.avgSolar.toFixed(2)}</p>
        </div>
      </div>

      {/* Chart */}
      <div style={{ height: 400, marginBottom: 20 }}>
        <PowerChart data={data} />
      </div>

      {/* Table */}
      <div style={{ height: 400, overflowY: "auto" }}>
        <PowerTable data={data} />
      </div>
    </div>
  );
}
