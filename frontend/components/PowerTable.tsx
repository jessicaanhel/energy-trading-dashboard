import { PowerRow } from "../types/power";

interface Props {
  data: PowerRow[];
}

export default function PowerTable({ data }: Props) {
  if (data.length === 0) return <p>No data loaded</p>;

  return (
    <div style={{ overflowX: "auto", width: "100%" }}>
      <table
        style={{
          borderCollapse: "collapse",
          width: "100%",
          minWidth: 400,
        }}
      >
        <thead>
          <tr>
            <th style={{ border: "1px solid #ccc", padding: 5 }}>Hour</th>
            <th style={{ border: "1px solid #ccc", padding: 5 }}>Wind MW</th>
            <th style={{ border: "1px solid #ccc", padding: 5 }}>Solar MW</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.hour}>
              <td style={{ border: "1px solid #ccc", padding: 5 }}>{row.hour}</td>
              <td style={{ border: "1px solid #ccc", padding: 5 }}>{row.wind_mw.toFixed(2)}</td>
              <td style={{ border: "1px solid #ccc", padding: 5 }}>{row.solar_mw.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
