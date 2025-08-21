

export default function ChatBubble({ role, text, meta }) {
  const isUser = role === 'user'
  return (
    <div className={`chat-bubble ${isUser ? 'right' : 'left'}`}>
      <div className="chat-header">
        <strong>{isUser ? 'You' : meta?.agent || 'Agent'}</strong>
        {meta?.status && <span className={`tag ${meta.status}`}>{meta.status}</span>}
      </div>
      <div className="chat-text">{text}</div>
      {meta?.logs && meta.logs.length > 0 && (
        <ul className="logs">
          {meta.logs.map((l, i) => (
            <li key={i}>{l}</li>
          ))}
        </ul>
      )}
    </div>
  )
}
