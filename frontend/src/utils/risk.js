export const riskStyles = {
  CRITICAL: "bg-red-500/15 text-red-300 ring-red-400/30",
  HIGH: "bg-orange-500/15 text-orange-300 ring-orange-400/30",
  MEDIUM: "bg-yellow-500/15 text-yellow-200 ring-yellow-400/30",
  LOW: "bg-emerald-500/15 text-emerald-300 ring-emerald-400/30",
};

export const riskOrder = {
  CRITICAL: 0,
  HIGH: 1,
  MEDIUM: 2,
  LOW: 3,
};

export function formatHours(hours) {
  if (hours === null || hours === undefined) return "Beyond horizon";
  return `${hours}h`;
}

export function formatCash(value) {
  return Number(value || 0).toLocaleString(undefined, {
    maximumFractionDigits: 0,
  });
}
