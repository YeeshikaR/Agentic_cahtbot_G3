

function App() {
  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>🤖 Chatbot Demo</h1>
      <input
        type="text"
        placeholder="Enter your query..."
        style={{ padding: "8px", width: "250px", marginRight: "10px" }}
      />
      <button style={{ padding: "8px 12px" }}>Run</button>

      <div style={{ marginTop: "20px" }}>
        <p>👉 Logs will appear here...</p>
      </div>
    </div>
  );
}

export default App;
