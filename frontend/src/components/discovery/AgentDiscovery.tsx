import React, { useState } from 'react';
import { useMutation, useQueryClient } from 'react-query';
import { discoveryApi } from '../../services/api';
import { ApiError } from '../../types';
import Button from '../common/Button';

const AgentDiscovery: React.FC = () => {
  const [githubUrl, setGithubUrl] = useState('');
  const [isValidUrl, setIsValidUrl] = useState(true);
  const queryClient = useQueryClient();

  const discoverMutation = useMutation(
    (url: string) => discoveryApi.discoverAgents(url),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('agents');
        queryClient.invalidateQueries('discovery-status');
        setGithubUrl('');
      },
    }
  );

  const validateGithubUrl = (url: string) => {
    const githubPattern = /^https:\/\/github\.com\/[a-zA-Z0-9_.-]+\/[a-zA-Z0-9_.-]+\/?$/;
    return githubPattern.test(url);
  };

  const handleUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const url = e.target.value;
    setGithubUrl(url);
    setIsValidUrl(url === '' || validateGithubUrl(url));
  };

  const handleDiscover = () => {
    if (githubUrl && isValidUrl) {
      discoverMutation.mutate(githubUrl);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && githubUrl && isValidUrl) {
      handleDiscover();
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Agent Discovery</h3>
        <p className="text-sm text-gray-600">
          Discover AI agents by scanning GitHub repositories !
        </p>
      </div>

      <div className="space-y-4">
        <div>
          <label htmlFor="github-url" className="block text-sm font-medium text-gray-700 mb-2">
            GitHub Repository URL
          </label>
          <input
            type="url"
            id="github-url"
            value={githubUrl}
            onChange={handleUrlChange}
            onKeyPress={handleKeyPress}
            placeholder="https://github.com/username/repository"
            className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 ${
              !isValidUrl && githubUrl ? 'border-red-300' : 'border-gray-300'
            }`}
          />
          {!isValidUrl && githubUrl && (
            <p className="mt-1 text-sm text-red-600">
              Please enter a valid GitHub repository URL
            </p>
          )}
        </div>

        <div className="flex items-center space-x-4">
          <Button
            onClick={handleDiscover}
            disabled={!githubUrl || !isValidUrl || discoverMutation.isLoading}
            variant="primary"
          >
            {discoverMutation.isLoading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Discovering...
              </>
            ) : (
              'Discover Agents'
            )}
          </Button>
        </div>

        {discoverMutation.isError && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Discovery Failed</h3>
                <p className="mt-1 text-sm text-red-700">
                  {(discoverMutation.error as ApiError)?.message || 'An error occurred during discovery'}
                </p>
              </div>
            </div>
          </div>
        )}

        {discoverMutation.isSuccess && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-green-800">Discovery Successful</h3>
                <p className="mt-1 text-sm text-green-700">
                  {discoverMutation.data?.message || 'Agents discovered successfully'}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AgentDiscovery;
