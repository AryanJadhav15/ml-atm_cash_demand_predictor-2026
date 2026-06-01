export default function SummaryCard({ label, value, tone = "neutral" }) {
  const tones = {
    neutral: "border-border bg-surface",
    green: "border-success/20 bg-success/10",
    yellow: "border-warning/20 bg-warning/10",
    red: "border-danger/25 bg-danger/10",
    orange: "border-orange-400/20 bg-orange-400/10",
  };

  return (
    <section className={`rounded-lg border p-5 shadow-glow ${tones[tone]}`}>
      <p className="text-sm text-muted">{label}</p>
      <p className="mt-3 text-3xl font-semibold tracking-normal text-text">{value}</p>
    </section>
  );
}
