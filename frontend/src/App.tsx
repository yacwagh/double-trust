import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import Layout from './components/layout/Layout';
import AgentList from './components/agents/AgentList';
import ToolsList from './components/tools/ToolsList';
import DiscoveryPage from './components/discovery/DiscoveryPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<AgentList />} />
            <Route path="/agents" element={<AgentList />} />
            <Route path="/tools" element={<ToolsList />} />
            <Route path="/discovery" element={<DiscoveryPage />} />
          </Routes>
        </Layout>
      </Router>
    </QueryClientProvider>
  );
};

export default App;
