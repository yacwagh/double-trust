import React, { useState, useEffect } from 'react';
import { useQuery } from 'react-query';
import { Agent } from '../../types';
import { agentsApi } from '../../services/api';
import AgentCard from './AgentCard';
import ManageToolsModal from './ManageToolsModal';
import Button from '../common/Button';

const AgentList: React.FC = () => {
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [isManageToolsModalOpen, setIsManageToolsModalOpen] = useState(false);

  const { data, isLoading, error, refetch } = useQuery(
    'agents',
    agentsApi.getAll,
    {
      refetchOnWindowFocus: false,
    }
  );

  const handleManageTools = (agent: Agent) => {
    setSelectedAgent(agent);
    setIsManageToolsModalOpen(true);
  };

  const handleCloseManageTools = () => {
    setIsManageToolsModalOpen(false);
    setSelectedAgent(null);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading agents...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 mb-4">
          <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 19.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">Error loading agents</h3>
        <p className="text-gray-600 mb-4">There was a problem loading the agents list.</p>
        <Button onClick={() => refetch()} variant="primary">
          Try Again
        </Button>
      </div>
    );
  }

  const agents = data?.agents || [];

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Agents</h1>
          <p className="text-gray-600 mt-2">
            {agents.length} agent{agents.length !== 1 ? 's' : ''} found
          </p>
        </div>
        <Button onClick={() => refetch()} variant="secondary">
          Refresh
        </Button>
      </div>

      {agents.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 20a8 8 0 1116 0" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No agents found</h3>
          <p className="text-gray-600">Start by discovering agents from GitHub repositories</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent) => (
            <AgentCard
              key={agent.id}
              agent={agent}
              onManageTools={handleManageTools}
            />
          ))}
        </div>
      )}

      {selectedAgent && (
        <ManageToolsModal
          isOpen={isManageToolsModalOpen}
          onClose={handleCloseManageTools}
          agent={selectedAgent}
        />
      )}
    </div>
  );
};

export default AgentList;
