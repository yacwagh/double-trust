import React from 'react';
import { Agent } from '../../types';
import Button from '../common/Button';

interface AgentCardProps {
  agent: Agent;
  onManageTools: (agent: Agent) => void;
}

const AgentCard: React.FC<AgentCardProps> = ({ agent, onManageTools }) => {
  const truncateText = (text: string, maxLength: number) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {agent.role}
          </h3>
          <div className="flex items-center space-x-2">
            {agent.framework && (
              <span
                className={
                  `inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ` +
                  (agent.framework === 'Langchain'
                    ? 'bg-indigo-100 text-indigo-800'
                    : agent.framework === 'Custom'
                    ? 'bg-slate-100 text-slate-800'
                    : 'bg-gray-100 text-gray-800')
                }
              >
                {agent.framework}
              </span>
            )}
            {agent.risk && (
              <span
                className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${agent.risk === 'high' ? 'bg-red-100 text-red-800' : agent.risk === 'medium' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'}`}
                title={agent.risk_reason || ''}
              >
                Risk : {agent.risk}
              </span>
            )}
          </div>
        </div>
      </div>
      
      <div className="mb-4">
        <p className="text-sm text-gray-700 leading-relaxed">
          {truncateText(agent.system_prompt, 150)}
        </p>
      </div>
      
      <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
        <span>Created: {new Date(agent.created_at).toLocaleDateString()}</span>
        {agent.model && (
          <span>Model: {agent.model}</span>
        )}
      </div>
      
      <div className="flex space-x-2">
        <Button
          onClick={() => onManageTools(agent)}
          variant="primary"
          size="sm"
        >
          Manage Tools
        </Button>
      </div>
    </div>
  );
};

export default AgentCard;
