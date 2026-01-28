import { Line } from "react-chartjs-2";
import { PowerRow } from "../types/power";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface Props {
  data: PowerRow[];
  height?: number; // optional, chart will be responsive
}

export default function PowerChart({ data, height = 400 }: Props) {
  if (data.length === 0) return <p>No chart data</p>;

  const chartData = {
    labels: data.map((d) => d.hour),
    datasets: [
      {
        label: "Wind MW",
        data: data.map((d) => d.wind_mw),
        borderColor: "blue",
        backgroundColor: "rgba(0,0,255,0.1)",
        tension: 0.3,
      },
      {
        label: "Solar MW",
        data: data.map((d) => d.solar_mw),
        borderColor: "orange",
        backgroundColor: "rgba(255,165,0,0.1)",
        tension: 0.3,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: "top" as const },
      title: { display: true, text: "Power Production vs Time" },
    },
    scales: {
      x: { title: { display: true, text: "Hour" } },
      y: { title: { display: true, text: "MW" } },
    },
  };

  return <div style={{ height }}>{/* container controls height */}<Line data={chartData} options={options} /></div>;
}
