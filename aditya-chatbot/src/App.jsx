
import React, { useMemo, useRef, useState } from 'react'
import ChatBubble from './components/ChatBubble'
import ProgressItem from './components/ProgressItem'
import { deriveSubtasks, assignAgentsToSubtasks, simulate } from './agentLogic'
import './styles.css'

export default function App() {
  const [messages, setMessages] = useState([])
  const [subtasks, setSubtasks] = useState([])
  const [query, setQuery] = useState('Organize a robotics workshop')
  const [running, setRunning] = useState(false)
  const [speed, setSpeed] = useState(1)
  const simRef = useRef(null)

  const canSend = useMemo(() => query.trim().length > 0 && !running, [query, running])

  const pushMessage = (m) => setMessages((prev) => [...prev, m])

  const startFlow = (q) => {
    pushMessage({ role: 'user', text: q })
    const sts = assignAgentsToSubtasks(deriveSubtasks(q))
    setSubtasks(sts)

    pushMessage({
      role: 'agent',
      text: `Plan created with ${sts.length} subtasks. Executing...`,
      meta: { agent: 'Planner', status: 'in_progress' }
    })

    setRunning(true)
    simRef.current = simulate(sts, {
      speed,
      onTick: (item, idx) => {
        setSubtasks((prev) => prev.map((p, i) => (i === idx ? { ...item } : p)))
        pushMessage({
          role: 'agent',
          text: `${item.task}`,
          meta: { agent: item.agent, status: item.status, logs: [...item.logs] }
        })
      },
    })

    const interval = setInterval(() => {
      const allDone = sts.every((s) => s.status === 'done')
      if (allDone) {
        clearInterval(interval)
        setRunning(false)
        pushMessage({
          role: 'agent',
          text: 'All subtasks completed. ✅',
          meta: { agent: 'Planner', status: 'done' }
        })
      }
    }, 500)
  }

  const onSubmit = (e) => {
    e.preventDefault()
    const q = query.trim()
    if (!q || running) return

    if (simRef.current) simRef.current.cancel()
    setMessages([])
    setSubtasks([])

    startFlow(q)
  }

  const stopFlow = () => {
    if (simRef.current) simRef.current.cancel()
    setRunning(false)
    pushMessage({ role: 'agent', text: 'Execution cancelled.', meta: { agent: 'System', status: 'pending' } })
  }

  return (
    <div className="app">
      <header>
        <h1>Agentic Chatbot Demo (Mock)</h1>
        <div className="controls">
          <label>
            Speed:
            <select value={speed} onChange={(e) => setSpeed(Number(e.target.value))} disabled={running}>
              <option value={1}>Normal</option>
              <option value={1.5}>Fast</option>
              <option value={2}>Fastest</option>
            </select>
          </label>
          <button className="secondary" onClick={stopFlow} disabled={!running}>Stop</button>
        </div>
      </header>

      <main>
        <section className="left">
          <div className="chat">
            {messages.map((m, i) => (
              <ChatBubble key={i} role={m.role} text={m.text} meta={m.meta} />
            ))}
          </div>
          <form className="input" onSubmit={onSubmit}>
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Type a task… e.g., Organize a robotics workshop"
            />
            <button disabled={!canSend}>Run</button>
          </form>
        </section>

        <section className="right">
          <h3>Subtasks</h3>
          {subtasks.length === 0 && <div className="muted">No subtasks yet. Submit a query to begin.</div>}
          {subtasks.map((item) => (
            <ProgressItem key={item.id} item={item} />
          ))}
        </section>
      </main>

      <footer>
        <span>Mock agentic flow • React + Vite • Deploy on Vercel</span>
      </footer>
    </div>
  )
}

