export default function MetricCard({
  value,
  label,
  sub,
  status,
}: {
  value: string
  label: string
  sub: string
  status: 'good' | 'warn' | 'bad' | 'none'
}) {
  const color =
    status === 'good' ? 'var(--good)' : status === 'warn' ? 'var(--warn)' : status === 'bad' ? 'var(--bad)' : 'var(--text)'
  return (
    <div className="metric">
      <div className="value" style={{ color }}>
        {value}
      </div>
      <div className="label">{label}</div>
      {sub && <div className="sub">{sub}</div>}
    </div>
  )
}
