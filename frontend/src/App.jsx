import { useState } from "react";
import "./App.css";

function App() {

  const [code, setCode] = useState("");

  const analyzeCode = () => {
    console.log(code);
    alert("Backend will analyze this code:\n\n" + code);
  };

  return (
    <div className="container">

      <h1>Intelligent Error Analyzer</h1>

      <div className="card">

        <h3>Paste Python Code</h3>

        <textarea
          rows="12"
          placeholder="Enter your Python code here..."
          value={code}
          onChange={(e) => setCode(e.target.value)}
        />

        <button onClick={analyzeCode}>
          Analyze Code
        </button>

        <div className="result">

          <h3>Analysis Result</h3>

          <p>
            <strong>Error:</strong> Waiting for analysis...
          </p>

          <p>
            <strong>Suggestion:</strong> AI suggestions will appear here.
          </p>

        </div>

      </div>

    </div>
  );
}

export default App;