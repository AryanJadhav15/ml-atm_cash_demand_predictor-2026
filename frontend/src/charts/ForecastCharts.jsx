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

export function BalanceLineChart({ forecast, threshold }) {
  return (
    <section className="rounded-lg border border-white/10 bg-panel p-5 shadow-glow">
      <h2 className="text-lg font-semibold">Future Balance</h2>
      <div className="mt-5 h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={forecast} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
            <CartesianGrid stroke="#2f2d29" strokeDasharray="3 3" />
            <XAxis dataKey="hour" stroke="#a7a29a" />
            <YAxis stroke="#a7a29a" />
            <Tooltip
              contentStyle={{
                background: "#171717",
                border: "1px solid rgba(255,255,255,0.12)",
                borderRadius: "8px",
              }}
            />
            <Legend />
            <ReferenceLine
              y={threshold}
              stroke="#ef4444"
              strokeDasharray="6 6"
              label={{ value: "Threshold", fill: "#fca5a5", position: "insideTopRight" }}
            />
            <Line
              type="monotone"
              dataKey="projected_balance"
              name="Projected balance"
              stroke="#36d399"
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
  return (
    <section className="rounded-lg border border-white/10 bg-panel p-5 shadow-glow">
      <h2 className="text-lg font-semibold">Predicted Withdrawals</h2>
      <div className="mt-5 h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={forecast} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
            <CartesianGrid stroke="#2f2d29" strokeDasharray="3 3" />
            <XAxis dataKey="hour" stroke="#a7a29a" />
            <YAxis stroke="#a7a29a" />
            <Tooltip
              contentStyle={{
                background: "#171717",
                border: "1px solid rgba(255,255,255,0.12)",
                borderRadius: "8px",
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
