import React from 'react'

export default function ProgressItem({ item }) {
  const pct = item.status === 'done' ? 100 : item.status === 'in_progress' ? 60 : 10
  return (
    <div className="progress-item">
      <div className="row">
        <div className="task">{item.task}</div>
        <div className={`status ${item.status}`}>{item.status}</div>
      </div>
      <div className="bar"><span style={{ width: pct + '%' }} /></div>
      <div className="agent">{item.agent}</div>
    </div>
  )
}
