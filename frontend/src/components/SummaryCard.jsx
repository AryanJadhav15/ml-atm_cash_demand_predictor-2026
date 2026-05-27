export default function SummaryCard({ label, value, tone = "neutral" }) {
  const tones = {
    neutral: "border-white/10 bg-surface",
    green: "border-emerald-400/20 bg-emerald-400/10",
    yellow: "border-yellow-400/20 bg-yellow-400/10",
    red: "border-red-400/25 bg-red-400/10",
    orange: "border-orange-400/20 bg-orange-400/10",
  };

  return (
    <section className={`rounded-lg border p-5 shadow-glow ${tones[tone]}`}>
      <p className="text-sm text-muted">{label}</p>
      <p className="mt-3 text-3xl font-semibold tracking-normal text-ink">{value}</p>
    </section>
  );
}
