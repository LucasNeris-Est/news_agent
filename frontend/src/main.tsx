import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { Route, Switch } from "wouter";
import MonitoramentoTrends from "./pages/MonitoramentoTrends";
import TopTrends from "./pages/TopTrends";
import TrendDetails from "./pages/TrendDetails";

function App() {
  return (
      <Switch>
        <Route path="/" component={MonitoramentoTrends} />
        <Route path="/trends" component={TopTrends} />
        <Route path="/trends/:keyword" component={TrendDetails} />
      </Switch>
  );
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)