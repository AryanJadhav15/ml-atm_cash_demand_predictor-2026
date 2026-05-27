export default function AlertBanner({ criticalCount, highCount }) {
  if (!criticalCount && !highCount) return null;

  return (
    <div className="rounded-lg border border-red-400/20 bg-red-500/10 px-5 py-4 text-red-100 shadow-glow">
      <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
        <p className="font-semibold">Refill attention required</p>
        <p className="text-sm text-red-100/80">
          {criticalCount} critical and {highCount} high-risk ATMs need priority routing.
        </p>
      </div>
    </div>
  );
}
