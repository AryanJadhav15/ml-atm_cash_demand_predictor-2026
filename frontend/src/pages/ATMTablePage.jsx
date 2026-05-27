import { useEffect, useMemo, useState } from "react";
import ATMStatusTable from "../components/ATMStatusTable.jsx";
import LoadingSkeleton from "../components/LoadingSkeleton.jsx";
import { getAtms } from "../services/api.js";
import { riskOrder } from "../utils/risk.js";

export default function ATMTablePage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [riskFilter, setRiskFilter] = useState("ALL");
  const [sortKey, setSortKey] = useState("priority");

  useEffect(() => {
    getAtms()
      .then((response) => {
        setData(response);
        setError("");
      })
      .catch((err) => setError(err.message || "Unable to load ATM fleet"))
      .finally(() => setLoading(false));
  }, []);

  const filteredAtms = useMemo(() => {
    let atms = data?.atms || [];
    if (search.trim()) {
      const value = search.trim().toLowerCase();
      atms = atms.filter(
        (atm) =>
          atm.atmId.toLowerCase().includes(value) ||
          (atm.atmName || "").toLowerCase().includes(value),
      );
    }
    if (riskFilter !== "ALL") {
      atms = atms.filter((atm) => atm.risk_level === riskFilter);
    }

    return [...atms].sort((a, b) => {
      if (sortKey === "balance") return a.current_balance - b.current_balance;
      if (sortKey === "hours") {
        return (a.hours_until_low_balance ?? 999) - (b.hours_until_low_balance ?? 999);
      }
      return riskOrder[a.risk_level] - riskOrder[b.risk_level];
    });
  }, [data, search, riskFilter, sortKey]);

  if (loading) return <LoadingSkeleton rows={8} />;

  if (error && !data) {
    return (
      <div className="rounded-lg border border-red-400/20 bg-red-500/10 p-6 text-red-100 shadow-glow">
        <h2 className="text-xl font-semibold">ATM data unavailable</h2>
        <p className="mt-2 text-sm text-red-100/80">
          The frontend is running, but the backend API is not responding on port 8000.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-5">
      <div className="flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
        <div>
          <h2 className="text-2xl font-semibold">ATM Fleet</h2>
          <p className="mt-1 text-sm text-muted">{filteredAtms.length} machines shown</p>
        </div>
        <div className="grid gap-3 sm:grid-cols-3">
          <input
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search ATM"
            className="rounded-lg border border-white/10 bg-panel px-4 py-3 text-sm outline-none ring-accent/30 focus:ring-2"
          />
          <select
            value={riskFilter}
            onChange={(event) => setRiskFilter(event.target.value)}
            className="rounded-lg border border-white/10 bg-panel px-4 py-3 text-sm outline-none ring-accent/30 focus:ring-2"
          >
            <option value="ALL">All risks</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Safe</option>
          </select>
          <select
            value={sortKey}
            onChange={(event) => setSortKey(event.target.value)}
            className="rounded-lg border border-white/10 bg-panel px-4 py-3 text-sm outline-none ring-accent/30 focus:ring-2"
          >
            <option value="priority">Priority</option>
            <option value="hours">Hours remaining</option>
            <option value="balance">Lowest balance</option>
          </select>
        </div>
      </div>
      <ATMStatusTable atms={filteredAtms} />
    </div>
  );
}
