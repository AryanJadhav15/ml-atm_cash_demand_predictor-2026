import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { BalanceLineChart, WithdrawalBarChart } from "../charts/ForecastCharts.jsx";
import LoadingSkeleton from "../components/LoadingSkeleton.jsx";
import RiskBadge from "../components/RiskBadge.jsx";
import SummaryCard from "../components/SummaryCard.jsx";
import { getAtmForecast } from "../services/api.js";
import { formatCash, formatHours } from "../utils/risk.js";

export default function ATMDetailsPage() {
  const { atmId } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    getAtmForecast(atmId)
      .then((response) => {
        setData(response);
        setError("");
      })
      .catch((err) => setError(err.message || "Unable to load ATM forecast"))
      .finally(() => setLoading(false));
  }, [atmId]);

  if (loading) return <LoadingSkeleton rows={6} />;

  if (error) {
    return (
      <div className="rounded-lg border border-danger/20 bg-danger/10 p-5 text-danger">
        {error}
      </div>
    );
  }

  const latestBalance = data.forecast?.[0]?.projected_balance + data.forecast?.[0]?.predicted_withdrawal;

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <Link to="/atms" className="text-sm font-semibold text-accent">
            Back to fleet
          </Link>
          <div className="mt-3 flex flex-wrap items-center gap-3">
            <h2 className="text-2xl font-semibold">{data.atmId}</h2>
            <RiskBadge risk={data.risk_level} />
          </div>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <SummaryCard label="Current Balance" value={formatCash(latestBalance)} />
        <SummaryCard label="Hours Left" value={formatHours(data.hours_until_low_balance)} />
        <SummaryCard
          label="Refill Window"
          value={formatHours(data.recommended_refill_within_hours)}
          tone={data.risk_level === "CRITICAL" ? "red" : "orange"}
        />
        <SummaryCard label="Threshold" value={formatCash(data.low_balance_threshold)} tone="yellow" />
      </div>

      <section className="rounded-lg border border-border bg-panel p-5 shadow-glow">
        <div className="grid gap-4 md:grid-cols-3">
          <div>
            <p className="text-sm text-muted">Estimated depletion</p>
            <p className="mt-2 font-semibold">{data.estimated_depletion_time || "Beyond horizon"}</p>
          </div>
          <div>
            <p className="text-sm text-muted">Forecast horizon</p>
            <p className="mt-2 font-semibold">{data.forecast_horizon_hours} hours</p>
          </div>
          <div>
            <p className="text-sm text-muted">Recommendation</p>
            <p className="mt-2 font-semibold">
              Refill within {formatHours(data.recommended_refill_within_hours)}
            </p>
          </div>
        </div>
      </section>

      <div className="grid gap-5 xl:grid-cols-2">
        <BalanceLineChart forecast={data.forecast} threshold={data.low_balance_threshold} />
        <WithdrawalBarChart forecast={data.forecast} />
      </div>

      <section className="rounded-lg border border-border bg-panel p-5 shadow-glow">
        <h2 className="text-lg font-semibold">Depletion Timeline</h2>
        <div className="mt-5 max-h-96 overflow-auto">
          <table className="min-w-full divide-y divide-border">
            <thead className="bg-hover">
              <tr>
                <th className="px-4 py-3 text-left text-xs uppercase text-muted">Hour</th>
                <th className="px-4 py-3 text-left text-xs uppercase text-muted">Time</th>
                <th className="px-4 py-3 text-left text-xs uppercase text-muted">Withdrawal</th>
                <th className="px-4 py-3 text-left text-xs uppercase text-muted">Balance</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {data.forecast.map((point) => (
                <tr key={point.hour}>
                  <td className="px-4 py-3 text-sm">{point.hour}</td>
                  <td className="px-4 py-3 text-sm text-muted">{point.forecast_time}</td>
                  <td className="px-4 py-3 text-sm">{formatCash(point.predicted_withdrawal)}</td>
                  <td className="px-4 py-3 text-sm">{formatCash(point.projected_balance)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
