import { riskStyles } from "../utils/risk.js";

export default function RiskBadge({ risk }) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold ring-1 ${
        riskStyles[risk] || riskStyles.LOW
      }`}
    >
      {risk}
    </span>
  );
}
