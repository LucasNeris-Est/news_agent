import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { Route, Switch } from "wouter";
import MonitoramentoTrends from "./pages/MonitoramentoTrends";
import TopTrends from "./pages/TopTrends";

function App() {
  return (
      <Switch>
        <Route path="/" component={MonitoramentoTrends} />
        <Route path="/trends" component={TopTrends} />
      </Switch>
  );
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)