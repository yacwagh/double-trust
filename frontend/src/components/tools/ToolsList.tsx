import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { Tool } from '../../types';
import { toolsApi } from '../../services/api';
import ToolCard from './ToolCard';
import Button from '../common/Button';

const ToolsList: React.FC = () => {
  const [viewMode, setViewMode] = useState<'grid' | 'by-server'>('by-server');

  const { data, isLoading, error, refetch } = useQuery(
    'tools',
    toolsApi.getAll,
    {
      refetchOnWindowFocus: false,
    }
  );

  const { data: toolsByServerData } = useQuery(
    'tools-by-server',
    toolsApi.getByServer,
    {
      refetchOnWindowFocus: false,
    }
  );

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading tools...</p>
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
        <h3 className="text-lg font-medium text-gray-900 mb-2">Error loading tools</h3>
        <p className="text-gray-600 mb-4">There was a problem loading the tools list.</p>
        <Button onClick={() => refetch()} variant="primary">
          Try Again
        </Button>
      </div>
    );
  }

  const tools = data?.tools || [];
  const toolsByServer = toolsByServerData || {};

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Tools</h1>
          <p className="text-gray-600 mt-2">
            {tools.length} tool{tools.length !== 1 ? 's' : ''} from {Object.keys(toolsByServer).length} server{Object.keys(toolsByServer).length !== 1 ? 's' : ''}
          </p>
        </div>
        <div className="flex space-x-2">
          <Button
            onClick={() => setViewMode('by-server')}
            variant={viewMode === 'by-server' ? 'primary' : 'secondary'}
            size="sm"
          >
            By Server
          </Button>
          <Button
            onClick={() => setViewMode('grid')}
            variant={viewMode === 'grid' ? 'primary' : 'secondary'}
            size="sm"
          >
            Grid View
          </Button>
          <Button onClick={() => refetch()} variant="secondary" size="sm">
            Refresh
          </Button>
        </div>
      </div>

      {tools.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No tools found</h3>
          <p className="text-gray-600">No tools available at the moment.</p>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tools.map((tool) => (
            <ToolCard key={tool.id} tool={tool} />
          ))}
        </div>
      ) : (
        <div className="space-y-6">
          {Object.entries(toolsByServer).map(([serverUrl, serverTools]) => (
            <div key={serverUrl} className="border border-gray-200 rounded-lg">
              <div className="bg-gray-100 px-4 py-3 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">{serverUrl}</h3>
                <p className="text-sm text-gray-600">{serverTools.length} tool{serverTools.length !== 1 ? 's' : ''}</p>
              </div>
              <div className="p-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {serverTools.map((tool) => (
                    <ToolCard key={tool.id} tool={tool} />
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ToolsList;
