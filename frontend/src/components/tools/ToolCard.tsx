import React from 'react';
import { Tool } from '../../types';

interface ToolCardProps {
  tool: Tool;
}

const ToolCard: React.FC<ToolCardProps> = ({ tool }) => {
  // Permissions and server URL removed

  const formatParameters = (parameters: Record<string, any>) => {
    if (!parameters || Object.keys(parameters).length === 0) {
      return 'No parameters';
    }
    
    return Object.entries(parameters)
      .map(([key, value]) => `${key}: ${typeof value === 'object' ? JSON.stringify(value) : value}`)
      .join(', ');
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {tool.name}
          </h3>
          <p className="text-sm text-gray-600 mb-2">
            ID: <code className="bg-gray-100 px-2 py-1 rounded text-xs">{tool.id}</code>
          </p>
          {/* No server URL */}
        </div>
        {/* No permission badge */}
      </div>
      
      <div className="mb-4">
        <p className="text-sm text-gray-700 leading-relaxed">
          {tool.description}
        </p>
      </div>
      
      <div className="bg-gray-50 p-3 rounded-lg">
        <h4 className="text-sm font-medium text-gray-900 mb-2">Parameters</h4>
        <p className="text-xs text-gray-600 font-mono">
          {formatParameters(tool.parameters)}
        </p>
      </div>
    </div>
  );
};

export default ToolCard;
