import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useTheme } from "../components/ThemeProvider.jsx";

export function BalanceLineChart({ forecast, threshold }) {
  const { resolvedTheme } = useTheme();
  const isDark = resolvedTheme === "dark";
  const gridColor = isDark ? "rgba(255,255,255,0.08)" : "rgba(0,0,0,0.08)";
  const labelColor = isDark ? "#A7A29A" : "#6B7280";
  const tooltipBg = isDark ? "#171717" : "#FFFFFF";
  const tooltipBorder = isDark ? "rgba(255,255,255,0.12)" : "rgba(0,0,0,0.12)";

  return (
    <section className="rounded-lg border border-border bg-panel p-5 shadow-glow">
      <h2 className="text-lg font-semibold text-text">Future Balance</h2>
      <div className="mt-5 h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={forecast} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
            <CartesianGrid stroke={gridColor} strokeDasharray="3 3" />
            <XAxis dataKey="hour" stroke={labelColor} />
            <YAxis stroke={labelColor} />
            <Tooltip
              contentStyle={{
                background: tooltipBg,
                border: `1px solid ${tooltipBorder}`,
                borderRadius: "8px",
                color: isDark ? "#fff" : "#000",
              }}
            />
            <Legend />
            <ReferenceLine
              y={threshold}
              stroke="#ef4444"
              strokeDasharray="6 6"
              label={{ value: "Threshold", fill: "#ef4444", position: "insideTopRight" }}
            />
            <Line
              type="monotone"
              dataKey="projected_balance"
              name="Projected balance"
              stroke="#10b981"
              strokeWidth={3}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}

export function WithdrawalBarChart({ forecast }) {
  const { resolvedTheme } = useTheme();
  const isDark = resolvedTheme === "dark";
  const gridColor = isDark ? "rgba(255,255,255,0.08)" : "rgba(0,0,0,0.08)";
  const labelColor = isDark ? "#A7A29A" : "#6B7280";
  const tooltipBg = isDark ? "#171717" : "#FFFFFF";
  const tooltipBorder = isDark ? "rgba(255,255,255,0.12)" : "rgba(0,0,0,0.12)";

  return (
    <section className="rounded-lg border border-border bg-panel p-5 shadow-glow">
      <h2 className="text-lg font-semibold text-text">Predicted Withdrawals</h2>
      <div className="mt-5 h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={forecast} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
            <CartesianGrid stroke={gridColor} strokeDasharray="3 3" />
            <XAxis dataKey="hour" stroke={labelColor} />
            <YAxis stroke={labelColor} />
            <Tooltip
              contentStyle={{
                background: tooltipBg,
                border: `1px solid ${tooltipBorder}`,
                borderRadius: "8px",
                color: isDark ? "#fff" : "#000",
              }}
            />
            <Bar
              dataKey="predicted_withdrawal"
              name="Predicted withdrawal"
              fill="#f59e0b"
              radius={[6, 6, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
