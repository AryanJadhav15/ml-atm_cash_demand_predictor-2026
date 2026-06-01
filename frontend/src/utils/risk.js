export const riskStyles = {
  CRITICAL: "bg-danger/15 text-danger ring-danger/30",
  HIGH: "bg-orange-500/15 text-orange-500 ring-orange-500/30",
  MEDIUM: "bg-warning/15 text-warning ring-warning/30",
  LOW: "bg-success/15 text-success ring-success/30",
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
