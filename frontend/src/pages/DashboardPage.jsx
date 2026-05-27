import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import AlertBanner from "../components/AlertBanner.jsx";
import ATMStatusTable from "../components/ATMStatusTable.jsx";
import LoadingSkeleton from "../components/LoadingSkeleton.jsx";
import RiskBadge from "../components/RiskBadge.jsx";
import SummaryCard from "../components/SummaryCard.jsx";
import { getAtms } from "../services/api.js";
import { formatCash, formatHours, riskOrder } from "../utils/risk.js";

export default function DashboardPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadData() {
    try {
      setError("");
      const response = await getAtms();
      setData(response);
    } catch (err) {
      setError(err.message || "Unable to load dashboard");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
    const interval = window.setInterval(loadData, 60000);
    return () => window.clearInterval(interval);
  }, []);

  const priorityAtms = useMemo(() => {
    if (!data?.atms) return [];
    return [...data.atms]
      .sort((a, b) => {
        const riskDelta = riskOrder[a.risk_level] - riskOrder[b.risk_level];
        if (riskDelta !== 0) return riskDelta;
        return (a.hours_until_low_balance ?? 999) - (b.hours_until_low_balance ?? 999);
      })
      .slice(0, 5);
  }, [data]);

  if (loading) return <LoadingSkeleton rows={6} />;

  if (error && !data) {
    return (
      <div className="rounded-lg border border-red-400/20 bg-red-500/10 p-6 text-red-100 shadow-glow">
        <h2 className="text-xl font-semibold">Backend connection failed</h2>
        <p className="mt-2 text-sm text-red-100/80">
          The dashboard loaded, but it could not reach the FastAPI server. Start the
          backend on port 8000, then refresh this page.
        </p>
        <pre className="mt-4 overflow-auto rounded-lg bg-black/30 p-4 text-sm text-red-50">
{`cd "/Users/aryan/Computer Science/Projects/ATM Cash Demand Predictor/backend"
source .venv/bin/activate
python run.py`}
        </pre>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {error && (
        <div className="rounded-lg border border-red-400/20 bg-red-500/10 p-4 text-red-100">
          {error}
        </div>
      )}

      <AlertBanner criticalCount={data?.critical_atms || 0} highCount={data?.high_risk_atms || 0} />

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <SummaryCard label="Total ATMs" value={data?.total_atms || 0} />
        <SummaryCard label="Critical" value={data?.critical_atms || 0} tone="red" />
        <SummaryCard label="High Risk" value={data?.high_risk_atms || 0} tone="orange" />
        <SummaryCard label="Medium Risk" value={data?.medium_risk_atms || 0} tone="yellow" />
        <SummaryCard label="Safe" value={data?.safe_atms || 0} tone="green" />
      </div>

      <section className="rounded-lg border border-white/10 bg-panel p-5 shadow-glow">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <h2 className="text-lg font-semibold">Priority Ranking</h2>
          <Link to="/atms" className="text-sm font-semibold text-accent">
            View fleet
          </Link>
        </div>
        <div className="mt-5 grid gap-3 lg:grid-cols-5">
          {priorityAtms.map((atm) => (
            <Link
              key={atm.atmId}
              to={`/atms/${atm.atmId}`}
              className="rounded-lg border border-white/10 bg-white/5 p-4 transition hover:border-accent/40"
            >
              <div className="flex items-center justify-between gap-3">
                <p className="truncate font-semibold">{atm.atmId}</p>
                <RiskBadge risk={atm.risk_level} />
              </div>
              <p className="mt-4 text-2xl font-semibold">{formatHours(atm.hours_until_low_balance)}</p>
              <p className="mt-2 text-sm text-muted">Balance {formatCash(atm.current_balance)}</p>
            </Link>
          ))}
        </div>
      </section>

      <section>
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold">Fleet Snapshot</h2>
        </div>
        <ATMStatusTable atms={(data?.atms || []).slice(0, 10)} />
      </section>
    </div>
  );
}
