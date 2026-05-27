import { Link } from "react-router-dom";
import RiskBadge from "./RiskBadge.jsx";
import { formatCash, formatHours } from "../utils/risk.js";

export default function ATMStatusTable({ atms }) {
  return (
    <div className="overflow-hidden rounded-lg border border-white/10 bg-panel shadow-glow">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-white/10">
          <thead className="bg-white/5">
            <tr>
              <th className="px-5 py-4 text-left text-xs font-semibold uppercase tracking-wide text-muted">
                ATM
              </th>
              <th className="px-5 py-4 text-left text-xs font-semibold uppercase tracking-wide text-muted">
                Balance
              </th>
              <th className="px-5 py-4 text-left text-xs font-semibold uppercase tracking-wide text-muted">
                Risk
              </th>
              <th className="px-5 py-4 text-left text-xs font-semibold uppercase tracking-wide text-muted">
                Hours Left
              </th>
              <th className="px-5 py-4 text-left text-xs font-semibold uppercase tracking-wide text-muted">
                Refill Window
              </th>
              <th className="px-5 py-4 text-left text-xs font-semibold uppercase tracking-wide text-muted">
                Depletion Time
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/8">
            {atms.map((atm) => (
              <tr key={atm.atmId} className="transition hover:bg-white/5">
                <td className="px-5 py-4">
                  <Link to={`/atms/${atm.atmId}`} className="font-semibold text-ink hover:text-accent">
                    {atm.atmId}
                  </Link>
                  <p className="mt-1 max-w-xs truncate text-xs text-muted">{atm.atmName}</p>
                </td>
                <td className="px-5 py-4 text-sm">{formatCash(atm.current_balance)}</td>
                <td className="px-5 py-4">
                  <RiskBadge risk={atm.risk_level} />
                </td>
                <td className="px-5 py-4 text-sm">{formatHours(atm.hours_until_low_balance)}</td>
                <td className="px-5 py-4 text-sm">
                  {formatHours(atm.recommended_refill_within_hours)}
                </td>
                <td className="px-5 py-4 text-sm text-muted">
                  {atm.estimated_depletion_time || "Beyond horizon"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
