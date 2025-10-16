import React from 'react';
import { useQuery } from 'react-query';
import { Agent, Tool } from '../../types';
import { agentsApi } from '../../services/api';
import Modal from '../common/Modal';
import Button from '../common/Button';

interface ManageToolsModalProps {
  isOpen: boolean;
  onClose: () => void;
  agent: Agent;
}

const ManageToolsModal: React.FC<ManageToolsModalProps> = ({
  isOpen,
  onClose,
  agent,
}) => {
  const { data: toolsData, isLoading } = useQuery<{ agent_id: string; tools: Tool[] }>(
    ['agent-tools', agent.id],
    () => agentsApi.getTools(agent.id),
    {
      enabled: isOpen,
    }
  );

  const tools: Tool[] = toolsData?.tools || [];

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={`Manage Tools for ${agent.role}`}
      size="xl"
    >
      <div className="space-y-6">
        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-medium text-gray-900 mb-2">Agent Details</h4>
          <p className="text-sm text-gray-600">
            <strong>ID:</strong> {agent.id}
          </p>
          <p className="text-sm text-gray-600">
            <strong>Role:</strong> {agent.role}
          </p>
        </div>

        {isLoading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            <span className="ml-2 text-gray-600">Loading tools...</span>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h4 className="font-medium text-gray-900">Tools</h4>
              <span className="text-sm text-gray-600">{tools.length} tool(s)</span>
            </div>
            {tools.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-500">No tools available.</p>
              </div>
            ) : (
              <div className="space-y-3">
                {tools.map((tool: Tool) => (
                  <div key={tool.id} className="p-3 bg-white border border-gray-200 rounded-lg">
                    <h6 className="font-medium text-gray-900">{tool.name}</h6>
                    {tool.description && (
                      <p className="text-sm text-gray-600 mt-1">{tool.description}</p>
                    )}
                    {/* Parameters intentionally hidden for now */}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200">
          <Button onClick={onClose} variant="secondary">
            Close
          </Button>
        </div>
      </div>
    </Modal>
  );
};

export default ManageToolsModal;
