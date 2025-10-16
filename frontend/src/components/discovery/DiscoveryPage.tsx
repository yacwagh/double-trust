import React from 'react';
import { useQuery } from 'react-query';
import { discoveryApi } from '../../services/api';
import AgentDiscovery from './AgentDiscovery';
import Button from '../common/Button';

const DiscoveryPage: React.FC = () => {
  const { data: status, isLoading, refetch } = useQuery(
    'discovery-status',
    discoveryApi.getStatus,
    {
      refetchOnWindowFocus: false,
    }
  );

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading discovery status...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Discovery</h1>
          <p className="text-gray-600 mt-2">
            Discover AI agents from GitHub repositories
          </p>
        </div>
        <Button onClick={() => refetch()} variant="secondary">
          Refresh Status
        </Button>
      </div>

      {/* Status Overview */}
      {status && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Discovery Status</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{status.total_agents}</div>
              <div className="text-sm text-blue-800">Total Agents</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{status.discovered_agents}</div>
              <div className="text-sm text-green-800">Discovered</div>
            </div>
          </div>
        </div>
      )}

      {/* Discovery Sections */}
      <div className="grid grid-cols-1 gap-8">
        <AgentDiscovery />
      </div>
    </div>
  );
};

export default DiscoveryPage;
